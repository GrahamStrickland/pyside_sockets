import socket

from .utils import console_out, l2bin


class SocketBase:
    BUFFSZ = 4096

    _socket: socket.socket
    _client: socket.socket
    _name: str
    _port: int
    _addr: int

    def __init__(self, name: str, port: int) -> None:
        self._name = name
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        self._socket.bind(("127.0.0.1", self._port))
        self._socket.listen(1)
        self._client, self._addr = self._socket.accept()

    def send(self, msg: str) -> None:
        totalsent = 0
        bmsg = b"".join((l2bin(msg), bytes(msg, encoding="utf-8")))
        console_out(f"{self._name} sending {bmsg} on address {self._addr}")
        while totalsent < len(bmsg):
            sent = self._client.send(bmsg)
            if sent == 0:
                raise RuntimeError("Socket connection broken while sending")
            totalsent = totalsent + sent

    def recv(self) -> bytes:
        console_out(f"{self._name} receiving on address {self._addr}")

        chunks = []
        bytes_recvd = 4
        bytes = self._client.recv(bytes_recvd)
        msg_sz = int.from_bytes(bytes, byteorder="little", signed=True)

        while bytes_recvd < msg_sz:
            chunk = self._client.recv(min(msg_sz - bytes_recvd, self.BUFFSZ))
            if chunk == b"":
                raise RuntimeError("Socket connection broken while receiving")
            chunks.append(chunk)
            bytes_recvd = bytes_recvd + len(chunk)

        bmsg = b"".join(chunks)

        return bmsg

    def disconnect(self) -> None:
        self._socket.close()
        return
