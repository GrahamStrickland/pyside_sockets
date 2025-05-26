from PySide6.QtCore import QByteArray, QIODeviceBase, QObject, Signal
from PySide6.QtNetwork import QAbstractSocket, QHostAddress, QTcpSocket


class ClientBase(QObject):
    _address: QHostAddress
    _port: int
    _socket: QTcpSocket

    errsig = Signal(str)
    msgsig = Signal(str)

    def __init__(
        self, address: QHostAddress, port: int, parent: QObject | None = None
    ) -> None:
        super().__init__(parent)
        self._address = address
        self._port = port

        self._socket = QTcpSocket()
        self._connect(self._address, self._port)

    def send(self, message: str, timeout: int = 50) -> None:
        if self._socket.state() != QAbstractSocket.SocketState.ConnectedState:
            self.errsig.emit("Socket not connected")
            self._connect(self._address, self._port)

        self.msgsig.emit(f"Sending message {message}")
        msg_bytes = bytes(message, "utf-8")
        sz_bytes = (len(msg_bytes) + 4).to_bytes(4, byteorder="little", signed=True)
        barr = bytearray(sz_bytes)
        barr.extend(msg_bytes)
        self._socket.write(barr)
        if not self._socket.waitForBytesWritten(timeout):
            self.errsig.emit(self._socket.errorString())
            return

    def recv(self, timeout: int | None = 2000) -> str | list:
        if self._socket.state() != QAbstractSocket.SocketState.ConnectedState:
            self.errsig.emit("Socket not connected")
            self._connect(self._address, self._port)

        msg_sz = -1
        bbuff = QByteArray()
        messages = []

        while True:
            msg_sz_bytes = self._socket.read(4)
            if msg_sz_bytes.length() == 0:
                return messages

            msg_sz = int.from_bytes(msg_sz_bytes, byteorder="little", signed=True)

            msg_recvd = False
            while not msg_recvd:
                bytes = self._socket.read(msg_sz - bbuff.length())
                bbuff.append(bytes)

                if bbuff.length() == msg_sz:
                    message = str(bbuff, encoding="utf-8")
                    messages.append(message)
                    bbuff.clear()
                    msg_recvd = True
                else:
                    if not self._socket.waitForReadyRead():
                        self.errsig.emit("Missing packet")
                        return

    def _connect(self, address: QHostAddress, port: int) -> None:
        self._socket.connectToHost(
            address.toString(),
            port,
            QIODeviceBase.OpenModeFlag.ReadWrite,
            QAbstractSocket.NetworkLayerProtocol.IPv4Protocol,
        )
        if not self._socket.waitForConnected(1000):
            self.errsig.emit(self._socket.errorString())
            raise ConnectionError(self._socket.errorString())
