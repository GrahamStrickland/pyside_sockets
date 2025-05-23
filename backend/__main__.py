import threading

from .socket_base import SocketBase
from .utils import console_out


def pi_approx(n: int) -> float:
    pi = 1.0
    for i in range(1, n):
        sign = -1 if i % 2 != 0 else 1
        pi += sign * (1 / (2 * i + 1))
    return 4.0 * pi


def req_jobs() -> None:
    req_sock = SocketBase("Request Socket", 37679)
    req_sock.connect()

    try:
        msg = b""
        msgno = 0
        while len(msg := req_sock.recv()) > 0:
            console_out(str(msg))
            msgno += 1
            pi = pi_approx(10*msgno)
            req_sock.send(str(msg) + f": {pi}")
            if msg == "Morning! #2":
                break
                
    except RuntimeError as e:
        console_out(f"ERR: Request Socket, {e}")
    finally:
        req_sock.disconnect()


def upd_jobs() -> None:
    upd_sock = SocketBase("Update Socket", 37680)
    upd_sock.connect()

    msgno = 0
    try:
        while True:
            msgno += 1
            pi = pi_approx(100**msgno)
            upd_sock.send(f"Morning! pi ~= {pi}")
    except RuntimeError as e:
        console_out(f"ERR: Update Socket, {e}")
    finally:
        upd_sock.disconnect()



def main() -> None:
    reqt = threading.Thread(target=req_jobs)
    updt = threading.Thread(target=upd_jobs)

    reqt.start()
    updt.start()

    reqt.join()
    updt.join()


if __name__ == "__main__":
    main()
