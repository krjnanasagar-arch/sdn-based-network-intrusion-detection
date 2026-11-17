import socket, sys, time
target = sys.argv[1] if len(sys.argv) > 1 else "10.0.0.2"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 5001
with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
    for _ in range(100):
        s.sendto(b"MININET_UDP_TEST",(target,port)); time.sleep(.005)
print(f"Sent 100 bounded UDP test packets to {target}:{port}")
