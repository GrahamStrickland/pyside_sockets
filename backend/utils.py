from datetime import datetime


def console_out(msg: str) -> None:
    curr_time = datetime.now().strftime("%H:%M:%S.%f")
    print(f"{curr_time}: {msg}")


def l2bin(msg: str) -> bytes:
    bmsg = bytes(msg, encoding="utf-8")
    msglen = len(bmsg)
    return msglen.to_bytes(4, byteorder="little", signed=True)


def pi_approx(n: int) -> float:
    pi = 1.0
    for i in range(1, n):
        sign = -1 if i % 2 != 0 else 1
        pi += sign * (1 / (2 * i + 1))
    return 4.0 * pi
