import time
import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *

class hello_mainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(hello_mainWindow,self).__init__()
        self.qTimer = QtCore.QTimer()
        # set interval to 1 s
        self.qTimer.setInterval(3000)  # 1000 ms = 1 s
        self.s3 = None
        self.setupUi(self)
        self.retranslateUi(self)
        self.add_action()

    def set_default_s3(self, s3):
        self.s3 = s3

    def setupUi(self, mainWindow):
        try:
            mainWindow.setObjectName("mainWindow")
            mainWindow.setWindowModality(QtCore.Qt.WindowModal)
            mainWindow.setFixedSize(700, 511)

            self.centralWidget = QtWidgets.QWidget(mainWindow)
            self.centralWidget.setObjectName("centralWidget")

            # label for selected files
            self.label_fileinput = QtWidgets.QLabel(self.centralWidget)
            self.label_fileinput.setGeometry(QtCore.QRect(20, 54, 150, 35))
            self.label_fileinput.setTextFormat(QtCore.Qt.AutoText)
            self.label_fileinput.setObjectName("label")


            # label for selected folders
            self.label_folders = QtWidgets.QLabel(self.centralWidget)
            self.label_folders.setGeometry(QtCore.QRect(15, 54, 160, 35))
            self.label_folders.setTextFormat(QtCore.Qt.AutoText)
            self.label_folders.setObjectName("label")

            # label for upload
            self.label_upload = QtWidgets.QLabel(self.centralWidget)
            self.label_upload.setGeometry(QtCore.QRect(20, 260, 150, 35))
            self.label_upload.setTextFormat(QtCore.Qt.AutoText)
            self.label_upload.setObjectName("label")

            # this display for selected files
            self.textedit = QtWidgets.QTextEdit(self.centralWidget)
            self.textedit.setGeometry(QtCore.QRect(120, 60, 520, 170))
            self.textedit.setObjectName("textedit")

            # this display for selected files
            self.textedit_folder = QtWidgets.QTextEdit(self.centralWidget)
            self.textedit_folder.setGeometry(QtCore.QRect(120, 60, 520, 170))
            self.textedit_folder.setObjectName("textedit")

            # this for uploaded files
            self.textedit_upload = QtWidgets.QTextEdit(self.centralWidget)
            self.textedit_upload.setGeometry(QtCore.QRect(120, 260, 520, 170))
            self.textedit_upload.setObjectName("textedit")

            self.pushButton = QtWidgets.QPushButton(self.centralWidget)
            self.pushButton.setGeometry(QtCore.QRect(120, 20, 120, 30))
            self.pushButton.setObjectName("pushButton")

            self.directory_pushButton = QtWidgets.QPushButton(self.centralWidget)
            self.directory_pushButton.setGeometry(QtCore.QRect(280, 20, 120, 30))
            self.directory_pushButton.setObjectName("pushButton")

            self.upload_pushButton = QtWidgets.QPushButton(self.centralWidget)
            self.upload_pushButton.setGeometry(QtCore.QRect(440, 20, 80, 30))
            self.upload_pushButton.setObjectName("pushButton")

            self.reset_pushButton = QtWidgets.QPushButton(self.centralWidget)
            self.reset_pushButton.setGeometry(QtCore.QRect(560, 20, 80, 30))
            self.reset_pushButton.setObjectName("pushButton")

            # label for upload
            self.label_version = QtWidgets.QLabel(self.centralWidget)
            self.label_version.setGeometry(QtCore.QRect(20, 470, 630, 35))
            self.label_version.setTextFormat(QtCore.Qt.AutoText)
            self.label_version.setObjectName("label")

            mainWindow.setCentralWidget(self.centralWidget)
            self.retranslateUi(mainWindow)
            QtCore.QMetaObject.connectSlotsByName(mainWindow)
        except:
            pass
    def choose_files(self):
        try:
            self.textedit.setLineWrapColumnOrWidth(800)
            self.textedit.setLineWrapMode(QtWidgets.QTextEdit.FixedPixelWidth)
            self.textedit_folder.hide()
            self.label_folders.hide()

            self.textedit_folder.setText('')
            self.textedit_upload.setText('')
            self.textedit.show()
            self.label_fileinput.show()

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileNames(self, "Open file", "~/Documents",
                                                    "All Files (*);;", options=options)

            select_files = []
            old_files = self.textedit.toPlainText()

            if old_files:
                files_list = old_files.strip().split('\n')
                select_files.extend(files_list[1:])

            select_files.extend(files)
            select_files = list(set(select_files))
            select_files.insert(0, 'Total %s Selected' % len(select_files) )
            self.textedit.setText('\n'.join(select_files))
        except:
            pass

    def choose_folders(self):
        try:
            self.textedit_folder.show()
            self.label_folders.show()
            self.textedit.hide()
            self.textedit.setText('')
            self.textedit_upload.setText('')
            self.label_fileinput.hide()
            folder_path = QFileDialog.getExistingDirectory(self, "Select Folders", "~/Documents")
            select_folders = []
            old_folders = self.textedit_folder.toPlainText().strip()

            if old_folders:
                files_list = old_folders.strip().split('\n')
                select_folders.extend(files_list[1:])

            select_folders.append(str(folder_path))
            select_folders = list(set(select_folders))
            select_folders.insert(0, 'Total %s Selected' % len(select_folders) )
            self.textedit_folder.setText('\n'.join(select_folders))
        except:
            pass

    def clear_files(self):
        try:
            self.textedit.setText('')
            self.textedit_upload.setText('')
            self.textedit_folder.setText('')
            self.upload_pushButton.setEnabled(True)
            self.pushButton.setEnabled(True)
            self.directory_pushButton.setEnabled(True)
            if self.qTimer.isActive():
                self.qTimer.stop()
        except:
            pass

    def retranslateUi(self, mainWindow):

        _translate = QtCore.QCoreApplication.translate
        #self.lineEdit_fileinput.setPlaceholderText(_translate("MainWindow", "choose files"))
        self.label_fileinput.setText(_translate("MainWindow", "Selected Files"))
        self.label_folders.setText(_translate("MainWindow", "Selected Folders"))
        self.pushButton.setText(_translate("MainWindow", "Choose Files"))
        self.directory_pushButton.setText(_translate("MainWindow", "Choose Folders"))
        self.upload_pushButton.setText(_translate("MainWindow", "Upload"))
        self.reset_pushButton.setText(_translate("MainWindow", "Clean"))
        self.label_upload.setText(_translate("MainWindow", "Uploaded Files"))
        self.label_version.setText(_translate("MainWindow", "Version 1.0"))
        self.textedit_upload.setText(_translate("MainWindow", ""))

        mainWindow.setWindowTitle(_translate("mainWindow", "Demo"))

    def add_action(self):
        try:
            self.upload_pushButton.setEnabled(True)
            self.pushButton.setEnabled(True)
            self.pushButton.clicked.connect(self.choose_files)
            self.upload_pushButton.clicked.connect(self.upload_files)
            self.directory_pushButton.clicked.connect(self.choose_folders)
            self.reset_pushButton.clicked.connect(self.clear_files)
            self.qTimer.timeout.connect(self.check_result)

            self.textedit_upload.hide()
            self.label_upload.hide()
            self.textedit_upload.setText('')
            self.textedit.setReadOnly(True)
            self.textedit_folder.hide()
            self.label_folders.hide()
            self.textedit_folder.setReadOnly(True)
        except:
            pass


    def upload_files(self):
        """
        upload files to the S3
        :return:
        """
        # refresh status of some widgets
        try:
            if not self.textedit.toPlainText().strip() and not self.textedit_folder.toPlainText():
                QMessageBox.warning(self, "Warning", "No Files OR Folders",
                        QMessageBox.Yes)
                return
            self.textedit_upload.show()
            self.textedit_upload.setText('')
            self.label_upload.show()
            self.upload_pushButton.setEnabled(False)
            self.pushButton.setEnabled(False)
            self.directory_pushButton.setEnabled(False)

            # to keep every record in one line
            self.textedit_upload.setLineWrapColumnOrWidth(1000)
            self.textedit_upload.setLineWrapMode(QtWidgets.QTextEdit.FixedPixelWidth)

            self.textedit_upload.setText('start to upload... ')
            # get the values and push to s3
            self.__start_upload_time = time.time()
            if self.textedit.isVisible():
                files_list = self.textedit.toPlainText().strip().split('\n')[1:]
                self.s3.batch_upload_files(files_list)

            if self.textedit_folder.isVisible():
                folder_list = self.textedit_folder.toPlainText().strip().split('\n')[1:]
                self.s3.batch_upload_directory(folder_list)
                self.s3.list_objects()

            #start the qtimer
            self.qTimer.start()
        except:
            pass

    def __get_selected_num(self):
        total_num = 0
        try:
            if self.textedit.isVisible():
                files_str = self.textedit.toPlainText()
                files_list = files_str.split('\n')[1:]
                total_num = len(files_list)
            else:
                # if the dectory seleced, calculate all the files.
                files_str = self.textedit_folder.toPlainText()
                files_list = files_str.split('\n')[1:]
                total_num = len(files_list)
        except:
            pass

        return total_num

    def __get_files_num(self):
        files_nums = 0
        try:
            files_str = self.textedit_folder.toPlainText()
            files_list = files_str.split('\n')[1:]
            for directory in files_list:
                for subdir, dirs, files in os.walk(directory):
                    files_nums += len(files)
        except:
            pass

        return files_nums

    def check_result(self):
        try:
            total_num = self.__get_selected_num()
            uploaded_list = self.s3.get_uploaded_files()
            display_list = []
            uploaded_num = len(uploaded_list)
            if self.textedit.isVisible():
                if uploaded_num >= total_num :
                    final_list = self.s3.get_uploaded_files()
                    final_list.insert(0, 'Total %s, %s Uploaded, %s Remaining, Status: Completed, %s Seconds Cost' % (
                        total_num, uploaded_num, (total_num-uploaded_num), int(time.time()- self.__start_upload_time)
                        ))
                    self.textedit_upload.setText('\n'.join(final_list))
                    self.qTimer.stop()
                    self.upload_pushButton.setEnabled(True)
                    self.pushButton.setEnabled(True)
                    self.directory_pushButton.setEnabled(True)

                else:
                    display_list.append('Total %s, %s Uploaded, %s Remaining, Status: Uploading' % (
                    total_num, uploaded_num, total_num - uploaded_num))
                    display_list.extend(uploaded_list)
                    self.textedit_upload.setText('\n'.join(display_list))
            else:
                # need check the files number
                display_list = []
                files_num = self.__get_files_num()
                if uploaded_num >= files_num:
                    final_list = self.s3.get_uploaded_files()
                    final_list.insert(0, 'Total %s folders, %s files, %s Uploaded, %s Remaining,'
                                         ' Status: Completed, %s Seconds Cost' % (
                        total_num, files_num, uploaded_num, (files_num-uploaded_num),
                        int(time.time()- self.__start_upload_time)
                        ))
                    self.textedit_upload.setText('\n'.join(final_list))
                    self.qTimer.stop()
                    self.upload_pushButton.setEnabled(True)
                    self.pushButton.setEnabled(True)
                    self.directory_pushButton.setEnabled(True)
                else:
                    display_list.append('Total %s folders, %s files, %s Uploaded, %s Remaining, Status: Uploading' % (
                    total_num, files_num, uploaded_num, files_num - uploaded_num))
                    display_list.extend(uploaded_list)
                    self.textedit_upload.setText('\n'.join(display_list))

            self.s3.list_objects()
        except:
            pass