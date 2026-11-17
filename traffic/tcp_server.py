import socket
HOST, PORT = "0.0.0.0", 5000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT)); server.listen(5)
    print(f"TCP server listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024)
            print(f"Received from {addr}: {data.decode(errors='replace')}")
            conn.sendall(b"TCP reply from h2")
