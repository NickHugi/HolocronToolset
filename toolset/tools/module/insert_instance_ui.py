# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tools\module\insert_instance.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(390, 425)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.resrefEdit = QtWidgets.QLineEdit(Dialog)
        self.resrefEdit.setMaxLength(16)
        self.resrefEdit.setObjectName("resrefEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.resrefEdit)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.locationSelect = QtWidgets.QComboBox(Dialog)
        self.locationSelect.setObjectName("locationSelect")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.locationSelect)
        self.verticalLayout.addLayout(self.formLayout)
        self.templateCheck = QtWidgets.QCheckBox(Dialog)
        self.templateCheck.setChecked(True)
        self.templateCheck.setObjectName("templateCheck")
        self.verticalLayout.addWidget(self.templateCheck)
        self.templateList = QtWidgets.QListWidget(Dialog)
        self.templateList.setObjectName("templateList")
        self.verticalLayout.addWidget(self.templateList)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Insert Instance"))
        self.label.setText(_translate("Dialog", "ResRef:"))
        self.label_2.setText(_translate("Dialog", "Location:"))
        self.templateCheck.setText(_translate("Dialog", "Use existing template"))
