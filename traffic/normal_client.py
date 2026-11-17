import socket, sys
host = sys.argv[1] if len(sys.argv) > 1 else "10.0.0.2"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
with socket.create_connection((host, port), timeout=3) as s:
    s.sendall(b"Hello from normal client")
    print("Server replied:", s.recv(1024).decode(errors="replace"))
