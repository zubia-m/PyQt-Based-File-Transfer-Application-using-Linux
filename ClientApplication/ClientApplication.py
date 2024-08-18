# from PyQt5 import QtCore, QtGui, uic
# from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QTextEdit,QVBoxLayout, QWidget, QPushButton, QLineEdit
# import sys, time

# from PyQt5.QtCore import QDataStream, QIODevice, QByteArray
# from PyQt5.QtWidgets import QApplication, QDialog
# from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from PyQt5 import uic
import sys

            
class Ui(QMainWindow):
        def __init__(self):
            super(Ui, self).__init__()
            # Setup UI
            uic.loadUi('mainwindow.ui', self)

            self.serverIPAddress = self.findChild(QLineEdit,"leServerIPAddress")
            self.serverPortNumber = self.findChild(QLineEdit,"leServerPort")
            
            self.pbClose = self.findChild(QPushButton,"pbClose")
            self.pbClose.clicked.connect(self.close) 
            
            self.pbClearMessages = self.findChild(QPushButton,"pbClearMessages")
            self.pbClearMessages.clicked.connect(self.slotOnClearText) 

            self.teMessageHistory = self.findChild(QTextEdit, "teMessageHistory")
            self.leTextMessage = self.findChild(QLineEdit, "leTextMessage")
            
            self.pbSendMessage = self.findChild(QPushButton,"pbSendMessage")
            self.pbSendMessage.clicked.connect(self.slotSendMessageToServer)
            
            self.pbBrowseFiles = self.findChild(QPushButton,"pbSelectFile")
            self.pbBrowseFiles.clicked.connect(self.slotOnSelectFile)
         
            self.leSelectedFileName = self.findChild(QLineEdit,"leSelectedFileName")
            self.pbSendFile = self.findChild(QPushButton,"pbSendFile")
            self.pbSendFile.clicked.connect(self.slotOnSendFile)
            # self.pbSendMessage.clicked.connect(self.slotSendMessageToServer)
         

            self.pbConnectToServer = self.findChild(QPushButton,"pbConnectToServer")
            self.pbConnectToServer.clicked.connect(self.slotConnectToServer) 
            
            self.pbDisconnectFromServer = self.findChild(QPushButton,"pbDisconnectFromServer")
            self.pbDisconnectFromServer.clicked.connect(self.slotOnDisconnectedFromServer) 

            self.show()
            


        def slotConnectToServer(self):
            # self.blockSize = 0

            # Open Server Socket
            self.tcpSocket = QTcpSocket(self)
            # self.serverConnection = QTcpSocket(self)

            self.blockSize = 0

            self.tcpSocket.connected.connect(self.slotOnConnectedToServer)
            self.tcpSocket.disconnected.connect(self.slotOnDisconnectedFromServer)
            
            self.tcpSocket.readyRead.connect(self.slotOnDataAvailable)
            self.tcpSocket.error.connect(self.slotSocketError) 

            serverIPAddress = self.serverIPAddress.text() 
            serverPortNumber = int(self.serverPortNumber.text() )
            
            self.tcpSocket.connectToHost(serverIPAddress, serverPortNumber, QIODevice.ReadWrite)

            self.tcpSocket.waitForConnected(2000)
            
        def slotDisconnectFromServer(self):
            self.tcpSocket.disconnectFromHost
            # self.teMessageHistory.append("Disconnected from Server")
            # self.pbSendMessage.setEnabled(0)

        
        def slotOnConnectedToServer(self):
            self.teMessageHistory.append("Connected to Server")
            self.pbSendMessage.setEnabled(1)

        def slotOnDisconnectedFromServer(self):
            self.tcpSocket.close
            self.tcpSocket.deleteLater
            self.teMessageHistory.append("Disconnected from Server")
            self.pbSendMessage.setEnabled(0)

        def slotSendMessageToServer(self):
            ##################################################################
            # block = QByteArray()
            # # QDataStream class provides serialization of binary data to a QIODevice
            # out = QDataStream(block, QIODevice.ReadWrite)
            # # We are using PyQt5 so set the QDataStream version accordingly.
            # out.setVersion(QDataStream.Qt_5_0)
            # out.writeUInt16(0)
            # # this is the message we will send it could come from a widget.
            # message = self.leTextMessage.text()
            # # get a byte array of the message encoded appropriately.
            # message = bytes(message, encoding='ascii')
            # # now use the QDataStream and write the byte array to it.
            # out.writeString(message)
            # out.device().seek(0)
            # out.writeUInt16(block.size() - 2)

            # self.tcpSocket.disconnected.connect(self.tcpSocket.deleteLater)
            # # now send the QByteArray.
            # self.tcpSocket.write(block)
            # self.teMessageHistory.append("Sent: " + self.leTextMessage.text()) 
            # # now disconnect connection.
            ########################################################################
            message = self.leTextMessage.text()
            
            # stream = QDataStream(self.tcpSocket)
            # stream.setVersion(QDataStream.Qt_5_6)

            # block = QByteArray
            # out = QDataStream(block)
            # out.setDevice(self.tcpSocket)
            # out.setVersion(QDataStream.Qt_5_0)
            # out << message << "!\x0d\x0a"
            # self.tcpSocket.write(block)

            # baData = QByteArray()
            block = QByteArray()
            out = QDataStream(block, QIODevice.ReadWrite)
            out.setVersion(QDataStream.Qt_5_0)
            out.writeUInt16(0)

            message = bytes(message, encoding='ascii')
            out.writeString(message)
            out.device().seek(0)
            out.writeUInt16(block.size() - 2)
            self.tcpSocket.write(block)
            
            # self.tcpSocket.write(dsReader.write)

        def slotOnDataAvailable(self):
                instr = QDataStream(self.tcpSocket)
                instr.setVersion(QDataStream.Qt_5_0)
                if self.blockSize == 0:
                    if self.tcpSocket.bytesAvailable() < 2:
                        return
                    self.blockSize = instr.readUInt16()
                if self.tcpSocket.bytesAvailable() < self.blockSize:
                    return
                # Print response to terminal, we could use it anywhere else we wanted.
                messsage = str(instr.readString()) 
                self.teMessageHistory.append(messsage)

                

        def slotSocketError(self, socketError):
            self.teMessageHistory.append("Failed to Connect to Server: " + self.tcpSocket.errorString())
            self.pbSendMessage.setEnabled(0)


        def slotOnClearText(self):
            self.teMessageHistory.setPlainText("")


        def slotOnDataReceiving(self):
            #Message from client sent to server
            if self.tcpSocket.bytesAvailable() > 0:
                    instr = self.tcpSocket.readAll()
                    self.tcpSocket.nextBlockSize = 0
                    message = str(instr.data(), encoding='utf-8')
                    self.teMessageHistory.append(message)

        def slotOnSelectFile(self):
            fileDialog = QFileDialog(self)
            if (fileDialog.exec()):
                fileNames = fileDialog.selectedFiles()
                selectedFileName = fileNames[0]
                self.leSelectedFileName.setText(selectedFileName)
                self.pbSendFile.setEnabled(1)
            else:
                 self.pbSendFile.setEnabled(0)


        def slotOnSendFile(self):

            selectedFileName = self.leSelectedFileName.text()
            # Send file name first
            self.tcpSocket.write(selectedFileName)
            # Read file contents and send to server
            
            file = QFile(selectedFileName, QIODevice.Read)
            # file.open(QIODevice::ReadOnly)
            dsFile = QDataStream(file)    
            
            self.tcpSocket.write(dsFile.data)
            
            self.teMessageHistory.append("File is sent")             


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Ui()
    window.show()
    sys.exit(app.exec_())
       