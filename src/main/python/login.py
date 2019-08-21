from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from awsutil import *
import six
if six.PY2:
    import ConfigParser as configparser
else:
    import configparser

import syslog
syslog.openlog("SDKTOOL")

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self, ctx):
        super(Ui_MainWindow,self).__init__()
        self.ctx = ctx
        self.setupUi(self)
        self.retranslateUi(self)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(586, 325)
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)

        MainWindow.setWindowIcon(self.ctx.icon_logo)
        MainWindow.setStyleSheet("background-image:url(background.jpg)")

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        # aws s3 name
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(250, 40, 200, 25))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")


        # aws s3 region
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(250, 80, 200, 25))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")

        # aws accesskeyId
        self.accessId = QtWidgets.QLineEdit(self.centralWidget)
        self.accessId.setGeometry(QtCore.QRect(250, 120, 200, 25))
        self.accessId.setText("")
        self.accessId.setObjectName("accessId")

        # aws accesskeyId
        self.lineEdit_accesskey = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_accesskey.setGeometry(QtCore.QRect(250, 160, 200, 25))
        self.lineEdit_accesskey.setText("")
        self.lineEdit_accesskey.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_accesskey.setObjectName("lineEdit_accesskey")


        # aws s3 name label
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(150, 40, 70, 30))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")

        # aws s3 region label
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(150, 80, 70, 30))
        self.label_2.setObjectName("label_2")


        # aws accessid label
        self.accessId_label = QtWidgets.QLabel(self.centralWidget)
        self.accessId_label.setGeometry(QtCore.QRect(150, 120, 70, 30))
        self.accessId_label.setObjectName("accessId_label")


        # aws accesskey label
        self.label_accesskey = QtWidgets.QLabel(self.centralWidget)
        self.label_accesskey.setGeometry(QtCore.QRect(150, 160, 70, 30))
        self.label_accesskey.setObjectName("label_accesskey")

        # login button
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 220, 75, 33))
        self.pushButton.setObjectName("pushButton")

        # cancel button
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 220, 75, 33))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralWidget)

        # connect the click function to the button
        self.pushButton.clicked.connect(self.word_get)
        self.pushButton_2.clicked.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Demo"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "S3 Name"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Region"))
        self.accessId.setPlaceholderText(_translate("MainWindow", "Access ID"))
        self.lineEdit_accesskey.setPlaceholderText(_translate("MainWindow", "Access Key"))
        self.label.setText(_translate("MainWindow", "S3 Name"))
        self.label_2.setText(_translate("MainWindow", "Region"))
        self.accessId_label.setText(_translate("MainWindow", "Access ID"))
        self.label_accesskey.setText(_translate("MainWindow", "Access Key"))
        self.pushButton.setText(_translate("MainWindow", "Login"))
        self.pushButton_2.setText(_translate("MainWindow", "Cancel"))


        # just test
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.accessId.setText('')
        self.lineEdit_accesskey.setText('')

    def word_get(self):
        try:
            res, values = self.check_valid()
            if res:
                aws = AwsCaller(values)
                ret, msg = aws.validate_permission()
                # if ret = True, validate successfully
                if ret:
                    self.close()
                    self.ctx.ui_hello.set_default_s3(aws)
                    self.ctx.ui_hello.show()
                else:
                    QMessageBox.warning(self, "Warning", msg,
                                        QMessageBox.Yes)
        except Exception as e:
            syslog.syslog(syslog.LOG_ALERT, "sdktools: %s" % e)

    def check_valid(self):
        valid = True
        values = None
        s3_name = self.lineEdit.text().strip()
        if s3_name is None:
            valid = False
            QMessageBox.warning(self, "Warning", "S3 Name Empty",
                    QMessageBox.Yes)
            self.lineEdit.setFocus()

        s3_region = self.lineEdit_2.text().strip()
        if s3_region is None:
            valid = False
            QMessageBox.warning(self, "Warning", "S3 Region Empty",
                    QMessageBox.Yes)
            self.lineEdit_2.setFocus()
        access_id = self.accessId.text().strip()
        if access_id is None:
            valid = False
            QMessageBox.warning(self, "Warning", "Access ID Empty",
                    QMessageBox.Yes)
            self.accessId.setFocus()

        access_key = self.lineEdit_accesskey.text().strip()
        if access_key is None:
            valid = False
            QMessageBox.warning(self, "Warning", "Access Key Empty",
                    QMessageBox.Yes)
            self.lineEdit_accesskey.setFocus()
        if valid:
            values = {'name': s3_name, 'region': s3_region,
                      'accessId': access_id,'access_key': access_key
                      }
        return valid, values