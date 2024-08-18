from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from PyQt5 import uic
import sys       

class Ui(QMainWindow):
        def __init__(self):
            super(Ui, self).__init__()
            uic.loadUi('mainwindow.ui', self)
            # Setup UI

            self.hostIPAddress = self.findChild(QLineEdit,"leHostIPAddress")
            self.hostPortNumber = self.findChild(QLineEdit,"leHostPort")


            self.pbClose = self.findChild(QPushButton,"pbClose")
            self.pbClose.clicked.connect(self.close) 

            self.pbClear = self.findChild(QPushButton,"pbClearText")
            self.pbClear.clicked.connect(self.slotOnClearText) 

            self.teMessageHistory = self.findChild(QTextEdit, "teMessageHistory")

            self.pbDisconnect = self.findChild(QPushButton,"pbDisconnect")
            self.pbDisconnect.clicked.connect(self.slotOnDisconnectClicked) 

            self.pbSendMessage = self.findChild(QPushButton,"pbSendMessage")
            self.pbSendMessage.clicked.connect(self.slotOnSendMessageToClient)

            self.leTextMessage = self.findChild(QLineEdit, "leTextMessage")

            self.lbShow = self.findChild(QLabel, "lbShow")

            self.show()


            # Create Server Socket
            self.tcpServer = QTcpServer(self)
            self.clientConnection = QTcpSocket(self)
            
            hostIPAddress = self.hostIPAddress.text() 
            hostPortNumber = int(self.hostPortNumber.text())



            if self.tcpServer.listen(QHostAddress(hostIPAddress), hostPortNumber):
                pass
            else:
                self.teMessageHistory.append("Failed to Listen") 
                self.close()
                return  
            self.tcpServer.newConnection.connect(self.slotOnNewConnection)


        def slotOnNewConnection(self):
             # Get a QTcpSocket from the QTcpServer
            self.clientConnection = self.tcpServer.nextPendingConnection()
            self.clientConnection.readyRead.connect(self.slotOnDataAvailable)
            self.teMessageHistory.append("New Connection Request") 

            
        def slotOnDataAvailable(self):
            #Message from client sent to server
            if self.clientConnection.bytesAvailable() > 0:
                    instr = self.clientConnection.readAll()
                    self.clientConnection.nextBlockSize = 0
                    message = str(instr.data(), encoding='utf-8')
                    # self.teMessageHistory.append(str(instr, encoding='ascii'))
                    self.teMessageHistory.append("File Received: " + message)



        def slotOnDisconnectClicked(self):
            self.tcpServer.close
            self.tcpServer.deleteLater
            self.teMessageHistory.append("Disconnected from Client")
            # self.pbSend.setEnabled(0)


        def slotOnClearText(self):
            self.teMessageHistory.setPlainText("")
            self.lbShow.setText(f'Enter your message: {self.teMessageHistory.toPlainText()}')

        def slotOnSendMessageToClient(self):
                 # this is the message comes from the widget.
                message = self.leTextMessage.text()

                block = QByteArray()
                # QDataStream class provides serialization of binary data to a QIODevice
                out = QDataStream(block, QIODevice.ReadWrite)
                # We are using PyQt5 so set the QDataStream version accordingly.
                out.setVersion(QDataStream.Qt_5_0)
                out.writeUInt16(0)
               
                # get a byte array of the message encoded appropriately.
                message = bytes(message, encoding='ascii')
                # now use the QDataStream and write the byte array to it.
                out.writeString(message)
                out.device().seek(0)
                out.writeUInt16(block.size() - 2)

                # self.tcpServer.disconnected.connect(self.tcpServer.deleteLater)
                # now send the QByteArray.
                # self.tcpServer.write(block)
                self.clientConnection.write(block)
                self.teMessageHistory.append("Sent to Client: " + self.leTextMessage.text()) 
                # now disconnect connection.

                
        def slotOnReceivingData(self, clientConnection):
             fileName = clientConnection.readLine().trimmed().decode()
             self.teMessageHistory(f"Receiving file: {filename}")

             # Receive file data
             receivedFile = QFile(fileName)
             if receivedFile.open(QFile.WriteOnly):
                while clientConnection.bytesAvailable() > 0:
                    receivedFile.write(clientConnection.readAll())
                receivedFile.close()

             self.teMessageHistory("File transfer complete.")

            # Perform operations on the received file
             self.slotOnReceivingFile(fileName)

            # Close the connection
             clientConnection.close()
        

        def slotOnUpdateStatus(self, text):
            self.teMessageHistory.setText(text)
            QApplication.processEvents()

        def slotOnReceivingFile(self, filename):
            # Perform any desired operations on the received file
            with open(filename, 'rb') as file:
                filename = file.read()
                # Process the file data or save it to a specific location

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())