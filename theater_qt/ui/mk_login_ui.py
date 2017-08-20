# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mk_login.ui'
#
# Created: Tue Aug  8 14:07:19 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MK_Login(object):
    def setupUi(self, MK_Login):
        MK_Login.setObjectName("MK_Login")
        MK_Login.resize(248, 101)
        self.verticalLayout = QtWidgets.QVBoxLayout(MK_Login)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.login_lineinput_username = QtWidgets.QLineEdit(MK_Login)
        self.login_lineinput_username.setObjectName("login_lineinput_username")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.login_lineinput_username)
        self.login_lineinput_password = QtWidgets.QLineEdit(MK_Login)
        self.login_lineinput_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_lineinput_password.setObjectName("login_lineinput_password")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.login_lineinput_password)
        self.label = QtWidgets.QLabel(MK_Login)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(MK_Login)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.login_dialog_button = QtWidgets.QDialogButtonBox(MK_Login)
        self.login_dialog_button.setOrientation(QtCore.Qt.Horizontal)
        self.login_dialog_button.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.login_dialog_button.setObjectName("login_dialog_button")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.login_dialog_button)
        self.verticalLayout.addLayout(self.formLayout_2)

        self.retranslateUi(MK_Login)
        self.login_dialog_button.accepted.connect(MK_Login.accept)
        self.login_dialog_button.rejected.connect(MK_Login.reject)
        QtCore.QMetaObject.connectSlotsByName(MK_Login)

    def retranslateUi(self, MK_Login):
        _translate = QtCore.QCoreApplication.translate
        MK_Login.setWindowTitle(_translate("MK_Login", "MediaKraken Login"))
        self.label.setText(_translate("MK_Login", "Username:"))
        self.label_2.setText(_translate("MK_Login", "Password:"))

