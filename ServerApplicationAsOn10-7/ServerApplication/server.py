# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.server = QtWidgets.QLabel(self.centralwidget)
        self.server.setGeometry(QtCore.QRect(320, 20, 161, 17))
        self.server.setObjectName("server")
        self.saGroup = QtWidgets.QScrollArea(self.centralwidget)
        self.saGroup.setGeometry(QtCore.QRect(620, 80, 120, 191))
        self.saGroup.setWidgetResizable(True)
        self.saGroup.setObjectName("saGroup")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 118, 189))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.pbDisconnect = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pbDisconnect.setGeometry(QtCore.QRect(10, 40, 89, 25))
        self.pbDisconnect.setObjectName("pbDisconnect")
        self.pbConnect = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pbConnect.setGeometry(QtCore.QRect(10, 0, 89, 25))
        self.pbConnect.setObjectName("pbConnect")
        self.pbSettings = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pbSettings.setGeometry(QtCore.QRect(10, 80, 89, 25))
        self.pbSettings.setObjectName("pbSettings")
        self.pbSend = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pbSend.setGeometry(QtCore.QRect(10, 120, 89, 25))
        self.pbSend.setObjectName("pbSend")
        self.pbExit = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pbExit.setGeometry(QtCore.QRect(10, 160, 89, 25))
        self.pbExit.setObjectName("pbExit")
        self.saGroup.setWidget(self.scrollAreaWidgetContents)
        self.message = QtWidgets.QTextEdit(self.centralwidget)
        self.message.setGeometry(QtCore.QRect(180, 70, 421, 231))
        self.message.setObjectName("message")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.server.setText(_translate("MainWindow", "Server Application"))
        self.pbDisconnect.setText(_translate("MainWindow", "Disconnect"))
        self.pbConnect.setText(_translate("MainWindow", "Connect"))
        self.pbSettings.setText(_translate("MainWindow", "Settings"))
        self.pbSend.setText(_translate("MainWindow", "Send"))
        self.pbExit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
