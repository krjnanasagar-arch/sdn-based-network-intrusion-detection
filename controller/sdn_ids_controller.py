import time
from collections import defaultdict, deque

from os_ken.base import app_manager
from os_ken.controller import ofp_event
from os_ken.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from os_ken.ofproto import ofproto_v1_3
from os_ken.lib.packet import packet, ethernet, ipv4, tcp, udp


class SDNIDSController(app_manager.OSKenApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    WINDOW = 5.0
    PORT_SCAN_THRESHOLD = 8
    SYN_THRESHOLD = 25
    UDP_THRESHOLD = 60
    BLOCK_SECONDS = 30

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.port_history = defaultdict(lambda: deque())
        self.syn_history = defaultdict(lambda: deque())
        self.udp_history = defaultdict(lambda: deque())
        self.blocked_until = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        dp = ev.msg.datapath
        ofp = dp.ofproto
        parser = dp.ofproto_parser

        match = parser.OFPMatch()

        actions = [
            parser.OFPActionOutput(
                ofp.OFPP_CONTROLLER,
                ofp.OFPCML_NO_BUFFER
            )
        ]

        self.add_flow(dp, 0, match, actions)

        self.logger.info("[IDS] Switch connected: %s", dp.id)

    def add_flow(
        self,
        dp,
        priority,
        match,
        actions,
        idle_timeout=0,
        hard_timeout=0
    ):
        ofp = dp.ofproto
        parser = dp.ofproto_parser

        # Explicitly clear the action set for a DROP flow.
        if not actions:
            instructions = [
                parser.OFPInstructionActions(
                    ofp.OFPIT_CLEAR_ACTIONS,
                    []
                )
            ]
        else:
            instructions = [
                parser.OFPInstructionActions(
                    ofp.OFPIT_APPLY_ACTIONS,
                    actions
                )
            ]

        mod = parser.OFPFlowMod(
            datapath=dp,
            priority=priority,
            match=match,
            instructions=instructions,
            idle_timeout=idle_timeout,
            hard_timeout=hard_timeout
        )

        dp.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPErrorMsg, [CONFIG_DISPATCHER, MAIN_DISPATCHER])
    def openflow_error_handler(self, ev):
        self.logger.error(
            "[IDS] OpenFlow ERROR: type=%s code=%s",
            ev.msg.type,
            ev.msg.code
        )

    def block_source(self, dp, src_ip, reason):
        now = time.time()

        if self.blocked_until.get(src_ip, 0) > now:
            return

        parser = dp.ofproto_parser

        match = parser.OFPMatch(
            eth_type=0x0800,
            ipv4_src=src_ip
        )

        # Empty actions now creates a real DROP flow.
        self.add_flow(
            dp,
            100,
            match,
            [],
            hard_timeout=self.BLOCK_SECONDS
        )

        self.blocked_until[src_ip] = now + self.BLOCK_SECONDS

        self.logger.warning(
            "[IDS] BLOCKED %s for %ss - %s",
            src_ip,
            self.BLOCK_SECONDS,
            reason
        )

    @staticmethod
    def trim(q, now, window):
        cutoff = now - window

        while q and q[0][0] < cutoff:
            q.popleft()

    def forward_packet(self, msg):
        dp = msg.datapath
        ofp = dp.ofproto
        parser = dp.ofproto_parser

        in_port = msg.match.get("in_port")

        action = parser.OFPActionOutput(
            ofp.OFPP_FLOOD,
            0
        )

        out = parser.OFPPacketOut(
            datapath=dp,
            buffer_id=ofp.OFP_NO_BUFFER,
            in_port=in_port,
            actions=[action],
            data=msg.data
        )

        dp.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath

        pkt = packet.Packet(msg.data)

        eth = pkt.get_protocol(ethernet.ethernet)
        ip = pkt.get_protocol(ipv4.ipv4)

        if eth is None or ip is None:
            self.forward_packet(msg)
            return

        src = ip.src
        now = time.time()

        # Enforce temporary controller-level blocking.
        # Packets from a blocked source are not forwarded.
        if self.blocked_until.get(src, 0) > now:
            return

        # Remove expired block entry.
        if src in self.blocked_until:
            del self.blocked_until[src]

        # TCP detection
        t = pkt.get_protocol(tcp.tcp)

        if t:

            # TCP SYN burst detection
            if t.bits & tcp.TCP_SYN and not (t.bits & tcp.TCP_ACK):
                q = self.syn_history[src]

                q.append((now, t.dst_port))
                self.trim(q, now, self.WINDOW)

                if len(q) >= self.SYN_THRESHOLD:
                    self.logger.warning(
                        "[IDS] TCP SYN burst suspected from %s: %d SYNs/%ss",
                        src,
                        len(q),
                        self.WINDOW
                    )

                    self.block_source(
                        dp,
                        src,
                        "TCP SYN burst"
                    )

                    q.clear()
                    return

            # TCP port scan detection
            q = self.port_history[src]

            q.append((now, t.dst_port))
            self.trim(q, now, self.WINDOW)

            ports = {p for _, p in q}

            if len(ports) >= self.PORT_SCAN_THRESHOLD:
                self.logger.warning(
                    "[IDS] PORT SCAN suspected from %s: %d destination ports/%ss",
                    src,
                    len(ports),
                    self.WINDOW
                )

                self.block_source(
                    dp,
                    src,
                    "TCP port scan"
                )

                q.clear()
                return

        # UDP detection
        u = pkt.get_protocol(udp.udp)

        if u:
            q = self.udp_history[src]

            q.append((now, u.dst_port))
            self.trim(q, now, self.WINDOW)

            if len(q) >= self.UDP_THRESHOLD:
                self.logger.warning(
                    "[IDS] UDP burst suspected from %s: %d packets/%ss",
                    src,
                    len(q),
                    self.WINDOW
                )

                self.block_source(
                    dp,
                    src,
                    "UDP burst"
                )

                q.clear()
                return

        # Normal traffic
        self.forward_packet(msg)


