# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editors\nss\nss_editor.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
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
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.codeEdit = CodeEditor(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.codeEdit.setFont(font)
        self.codeEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.codeEdit.setObjectName("codeEdit")
        self.verticalLayout.addWidget(self.codeEdit)
        self.descriptionEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.descriptionEdit.setFont(font)
        self.descriptionEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.descriptionEdit.setReadOnly(True)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.verticalLayout.addWidget(self.descriptionEdit)
        self.verticalLayout.setStretch(0, 5)
        self.verticalLayout.setStretch(1, 3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.functionSearchEdit = QtWidgets.QLineEdit(self.tab)
        self.functionSearchEdit.setObjectName("functionSearchEdit")
        self.verticalLayout_2.addWidget(self.functionSearchEdit)
        self.functionList = QtWidgets.QListWidget(self.tab)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(8)
        self.functionList.setFont(font)
        self.functionList.setObjectName("functionList")
        self.verticalLayout_2.addWidget(self.functionList)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.constantSearchEdit = QtWidgets.QLineEdit(self.tab_2)
        self.constantSearchEdit.setObjectName("constantSearchEdit")
        self.verticalLayout_3.addWidget(self.constantSearchEdit)
        self.constantList = QtWidgets.QListWidget(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(8)
        self.constantList.setFont(font)
        self.constantList.setObjectName("constantList")
        self.verticalLayout_3.addWidget(self.constantList)
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionRevert = QtWidgets.QAction(MainWindow)
        self.actionRevert.setObjectName("actionRevert")
        self.actionCompile = QtWidgets.QAction(MainWindow)
        self.actionCompile.setObjectName("actionCompile")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionRevert)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionCompile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.functionSearchEdit.setPlaceholderText(_translate("MainWindow", "search..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Functions"))
        self.constantSearchEdit.setPlaceholderText(_translate("MainWindow", "search..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Constants"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionRevert.setText(_translate("MainWindow", "Revert"))
        self.actionCompile.setText(_translate("MainWindow", "Compile"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
from toolset.editors.nss.nss_editor import CodeEditor
