# import socket

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socServer:
#     socServer.bind((HOST, PORT))
#     socServer.listen()
#     addrChild, sockChild = socServer.accept()
#     with sockChild:
#         print(f"Connected by {addrChild}")
#         while True:
#             data = sockChild.recv(1024)
#             if not data:
#                 break
#             sockChild.sendall(data)

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton
from PyQt5.QtNetwork import QTcpServer, QHostAddress
from PyQt5.QtCore import QByteArray, QDataStream


# class Server(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.tcp_server = QTcpServer(self)
#         self.tcp_server.newConnection.connect(self.on_new_connection)
#         self.tcp_clients = []

#         self.init_ui()
#         self.start_server()

#     def init_ui(self):
#         self.setWindowTitle("Server")
#         self.text_edit = QTextEdit(self)
#         self.setCentralWidget(self.text_edit)

#     def start_server(self):
#         if not self.tcp_server.listen(QHostAddress.Any, 1234):
#             print("Failed to start the server.")
#             sys.exit(1)

#         self.text_edit.append("Server started. Waiting for connections...")

#     def on_new_connection(self):
#         client_connection = self.tcp_server.nextPendingConnection()
#         client_connection.readyRead.connect(
#             lambda: self.receive_data(client_connection)
#         )
#         self.tcp_clients.append(client_connection)

#         self.text_edit.append(
#             f"New client connected: {client_connection.peerAddress().toString()}"
#         )

#     def receive_data(self, client_connection):
#         data = client_connection.readAll().data().decode()
#         self.text_edit.append(f"Received data: {data}")

#         # Echo the received data back to the client
#         response = QByteArray(data.encode())
#         client_connection.write(response)
#         client_connection.flush()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     server = Server()
#     server.show()
#     sys.exit(app.exec_())


PORT = 9999
SIZEOF_UINT32 = 4

class ServerDlg(QPushButton):

    def __init__(self, parent=None):
        super(ServerDlg, self).__init__(
                "&Close Server", parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.tcpServer = QTcpServer(self)
        self.tcpServer.listen(QHostAddress("0.0.0.0"), PORT)
        self.connect(self.tcpServer, SIGNAL("newConnection()"),
                    self.addConnection)
        self.connections = []
        self.messageRecord = []

        self.connect(self, SIGNAL("clicked()"), self.close)
        font = self.font()
        font.setPointSize(24)
        self.setFont(font)
        self.setWindowTitle("Server")

    def addConnection(self):
        clientConnection = self.tcpServer.nextPendingConnection()
        clientConnection.nextBlockSize = 0
        self.connections.append(clientConnection)

        self.connect(clientConnection, SIGNAL("readyRead()"),
                self.receiveMessage)
        self.connect(clientConnection, SIGNAL("disconnected()"),
                self.removeConnection)
        self.connect(clientConnection, SIGNAL("error()"),
                self.socketError)

        def receiveMessage(self, connections):
                for s in self.connections:
                    if s.bytesAvailable() > 0:
                        stream = QDataStream(s)
                        stream.setVersion(QDataStream.Qt_4_2)

                        if s.nextBlockSize == 0:
                            if s.bytesAvailable() < SIZEOF_UINT32:
                                return
                            s.nextBlockSize = stream.readUInt32()
                        if s.bytesAvailable() < s.nextBlockSize:
                            return

                        textFromClient = stream.readQString()
                        s.nextBlockSize = 0
                        self.sendMessage(textFromClient,
                                        s.socketDescriptor())
                        s.nextBlockSize = 0

        def sendMessage(self, text, socketId):
                now = datetime.datetime.now()
                for s in self.connections:
                    if s.socketDescriptor() == socketId:
                        message = "<p>"+str(now.strftime("%Y-%m-%d %H:%M:%S")) + "</p>" +  "<font color=red>You</font> > {}".format(text)
                    else:
                        message = "<p>"+str(now.strftime("%Y-%m-%d %H:%M:%S")) + "</p>" + "<font color=green>{}</font> > {}".format(socketId, text)
                    msRecorded = "<p>"+str(now.strftime("%Y-%m-%d %H:%M:%S")) + "</p>" + "<font color=green>{}</font> > {}".format(socketId, text)
                    self.messageRecord.append(msRecorded)
                    reply = QByteArray()
                    stream = QDataStream(reply, QIODevice.WriteOnly)
                    stream.setVersion(QDataStream.Qt_4_2)
                    stream.writeUInt32(0)
                    stream.writeQString(message)
                    stream.device().seek(0)
                    stream.writeUInt32(reply.size() - SIZEOF_UINT32)
                    s.write(reply)

        def removeConnection(self):
                pass

        def socketError(self):
                pass


app = QApplication(sys.argv)
form = ServerDlg()
form.show()
form.move(0, 0)
app.exec_()
