from .socket_base import SocketBase


def main() -> None:
    req_sock = SocketBase(37679)
    req_sock.connect()

    upd_sock = SocketBase(37680)
    upd_sock.connect()

    try:
        while True:
            print(req_sock.recv())
    except RuntimeError as errmsg:
        print(errmsg)
    finally:
        upd_sock.disconnect()
        req_sock.disconnect()


if __name__ == "__main__":
    main()
