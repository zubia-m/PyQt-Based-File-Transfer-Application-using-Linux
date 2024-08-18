# import socket

# HOST = "127.0.0.1"  # The server's hostname or IP address
# PORT = 65432  # The port used by the server

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b"Hello, world")
#     data = s.recv(1024)

# print(f"Received {data!r}")


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PyQt5.QtNetwork import QTcpSocket


class Client(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tcpServer = None
        self.tcp_socket = QTcpSocket(self)
        self.tcp_socket.readyRead.connect(self.receive_data)

        self.init_ui()
        self.connect_to_server()

    def init_ui(self):
        self.setWindowTitle("Client")

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        self.setCentralWidget(central_widget)

    def connect_to_server(self):
        self.tcp_socket.connectToHost("localhost", 1234)

        if not self.tcp_socket.waitForConnected(5000):
            print("Failed to connect to the server.")
            # sys.exit(1)

        self.text_edit.append("Connected to the server.")

    def send_message(self):
        message = self.text_edit.toPlainText() 
        self.tcp_socket.write(message.encode())
        self.tcp_socket.flush()

    def receive_data(self):
        data = self.tcp_socket.readAll().data().decode()
        self.text_edit.append(f"Received data: {data}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())
