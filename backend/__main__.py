import threading
from queue import Queue

from .socket_base import SocketBase
from .utils import console_out


def socket_loop(name: str, port: int, queue: Queue, queue_lock: threading.Lock) -> None:
    sock = SocketBase(name, port)
    sock.connect()

    try:
        msg = b""
        while True:
            if len(msg := sock.recv()) > 0:
                if msg == b"quit":
                    console_out(f"Qutting {name}...")
                    sock.disconnect()
                    return
                else:
                    with queue_lock:
                        queue.put(str(msg))

            if len(msg) > 0 or name == "Update Socket":
                with queue_lock:
                    if queue.empty():
                        continue
                    else:
                        msg = queue.get()
                        sock.send(msg)

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

    msg_recvd = 0
    upd_messages = ["Hello", "ERROR!"]

    while True:
        with req_queue_lock:
            if not req_queue.empty():
                msg = req_queue.get()
                console_out(msg)
                req_queue.put(f"Response to {msg} from Request Socket")
                msg_recvd += 1

        with upd_queue_lock:
            if msg_recvd > 2:
                if not upd_queue.empty():
                    msg = upd_queue.get()
                    console_out(msg)
                if len(upd_messages) > 0:
                    msg = upd_messages.pop()
                    upd_queue.put(f"Message {msg} from Update Socket")

    try:
        reqt.join()
        updt.join()
    except KeyboardInterrupt as _:
        console_out("Keyboard interrupt, quitting...")


if __name__ == "__main__":
    main()
