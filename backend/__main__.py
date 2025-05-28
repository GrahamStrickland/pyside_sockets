import threading
from random import random
from queue import Queue

from .socket_base import SocketBase
from .utils import console_out, pi_approx


def socket_loop(name: str, port: int, queue: Queue, queue_lock: threading.Lock) -> None:
    sock = SocketBase(name, port)
    sock.connect()

    try:
        msg = b""
        while True:
            with queue_lock:
                if len(msg := sock.recv()) > 0:
                    if msg == b"quit":
                        console_out(f"Qutting {name}...")
                        sock.disconnect()
                        return
                    else:
                        console_out(f"{name} received '{msg}'")
                        queue.put(str(msg))
                elif not queue.empty():
                    msg = queue.get()
                    console_out(f"{name} sent '{msg}'")
                    sock.send(msg)

            for b in msg:
                pi_approx(int(random() * 2**b))

    except RuntimeError as e:
        console_out(f"ERROR: On {name}, {e}")
    finally:
        sock.disconnect()


def main() -> None:
    req_queue = Queue()
    req_queue_lock = threading.Lock()
    reqt = threading.Thread(
        target=socket_loop, args=["Request Socket", 37679, req_queue, req_queue_lock]
    )
    reqt.daemon = True

    upd_queue = Queue()
    upd_queue_lock = threading.Lock()
    updt = threading.Thread(
        target=socket_loop, args=["Update Socket", 37680, upd_queue, upd_queue_lock]
    )
    updt.daemon = True

    console_out("Starting request thread...")
    reqt.start()

    console_out("Starting update thread...")
    updt.start()

    msg_recvd = False
    msg = ""
    while True:
        for ch in msg:
            pi_approx(int(random() * 2 ** ord(ch)))

        with req_queue_lock:
            if not req_queue.empty():
                msg_recvd = True
                msg = req_queue.get()
                console_out(msg)
                msg = f"Hello! Thanks for your msg '{msg}'. How are you?"
                console_out(f"Writing message '{msg}'...")
                req_queue.put(msg)

        with upd_queue_lock:
            if not upd_queue.empty():
                msg = upd_queue.get()
                console_out(msg)
            elif msg_recvd:
                msg = "Please read my messages!"
                console_out(f"Writing message '{msg}'...")
                upd_queue.put(msg)
                msg_recvd = False

    try:
        reqt.join()
        updt.join()
    except KeyboardInterrupt as _:
        console_out("Keyboard interrupt, quitting...")


if __name__ == "__main__":
    main()
