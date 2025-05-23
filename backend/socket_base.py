import socket


class SocketBase:
    MSGLEN = 4096

    _socket: socket.socket
    _client: socket.socket
    _port: int
    _addr: int

    def __init__(self, port: int) -> None:
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        self._socket.bind(("127.0.0.1", self._port))
        self._socket.listen(1)
        self._client, self._addr = self._socket.accept()

    def send(self, msg: str) -> None:
        print(f"sending on address {self._addr}")

        totalsent = 0
        while totalsent < self.MSGLEN:
            sent = self._client.send(msg)
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def recv(self) -> bytes:
        print(f"receiving on address {self._addr}")

        chunks = []
        bytes_recvd = 4
        bytes = self._client.recv(bytes_recvd)
        msg_sz = int.from_bytes(bytes, byteorder="little", signed=True)

        while bytes_recvd < msg_sz:
            chunk = self._client.recv(min(msg_sz - bytes_recvd, self.MSGLEN))
            if chunk == b"":
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recvd = bytes_recvd + len(chunk)

        return b"".join(chunks)

    def disconnect(self) -> None:
        self._socket.close()
        return
