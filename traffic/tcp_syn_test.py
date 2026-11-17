import socket, sys, time
target = sys.argv[1] if len(sys.argv) > 1 else "10.0.0.2"
for _ in range(35):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.settimeout(.03); s.connect((target,4999))
    except Exception:
        pass
    finally:
        try: s.close()
        except Exception: pass
    time.sleep(.01)
print("Bounded Mininet TCP connection-attempt simulation completed.")
