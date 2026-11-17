# SDN-Based Network Intrusion Detection System

Educational CN project using Mininet, Open vSwitch, OS-Ken and OpenFlow 1.3.

Architecture:
h1, h2, h3 -> s1 (Open vSwitch) -> OS-Ken controller

Detection prototype:
- TCP destination-port scan
- TCP SYN burst
- UDP burst

When a threshold is crossed, the controller installs a temporary high-priority source-IP drop rule.

This project is intended only for an isolated Mininet lab.

## Ubuntu commands

1. Unzip and enter:
   cd ~/CN-Network-Intrusion-Detection-SDN

2. Create/activate controller environment:
   python3 -m venv controller/venv
   source controller/venv/bin/activate

3. Install:
   python -m pip install --upgrade pip
   python -m pip install os-ken==4.2.2

4. Verify:
   python -c "import os_ken; print('OS-Ken working:', os_ken.__file__)"
   which osken-manager
   osken-manager --help

## Run

Terminal 1:
cd ~/CN-Network-Intrusion-Detection-SDN
source controller/venv/bin/activate
osken-manager controller/sdn_ids_controller.py --ofp-tcp-listen-port 6653

Terminal 2:
cd ~/CN-Network-Intrusion-Detection-SDN
sudo mn -c
sudo python3 topology/topology.py

Inside Mininet:
pingall

Normal TCP test:
h2 python3 traffic/tcp_server.py &
h1 python3 traffic/normal_client.py h2 5000

Port scan test:
h3 python3 traffic/port_scan_test.py 10.0.0.2

UDP burst test:
h3 python3 traffic/udp_flood_test.py 10.0.0.2 5001

TCP connection-attempt test:
h3 python3 traffic/tcp_syn_test.py 10.0.0.2

Exit Mininet:
exit
sudo mn -c

If the controller is not found, activate controller/venv first. If port 6653 is occupied:
sudo ss -ltnp | grep 6653

Do not claim an attack is fully detected/blocked until it has been demonstrated successfully.
