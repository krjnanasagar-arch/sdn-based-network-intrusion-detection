import socket, sys, time
target = sys.argv[1] if len(sys.argv) > 1 else "10.0.0.2"
for port in range(4000, 4012):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.settimeout(.08); s.connect((target,port))
    except Exception:
        pass
    finally:
        try: s.close()
        except Exception: pass
    time.sleep(.03)
print("Bounded Mininet port-scan simulation completed.")
