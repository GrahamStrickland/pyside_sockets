from datetime import datetime


def console_out(msg: str) -> None:
    curr_time = datetime.now().strftime("%H:%M:%S.%f")
    print(f"{curr_time}: {msg}")


def l2bin(msg: str) -> bytes:
    bmsg = bytes(msg, encoding="utf-8")
    msglen = len(bmsg)
    return msglen.to_bytes(4, byteorder="little", signed=True)
