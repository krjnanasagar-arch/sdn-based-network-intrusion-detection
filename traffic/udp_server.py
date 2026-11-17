import socket
HOST, PORT = "0.0.0.0", 5001
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")
    while True:
        data, addr = server.recvfrom(2048)
        print(f"Received UDP from {addr}: {data[:80]!r}")
