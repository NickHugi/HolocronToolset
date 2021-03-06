# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(478, 471)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gameCombo = QtWidgets.QComboBox(self.centralwidget)
        self.gameCombo.setObjectName("gameCombo")
        self.verticalLayout_4.addWidget(self.gameCombo)
        self.resourceTabs = QtWidgets.QTabWidget(self.centralwidget)
        self.resourceTabs.setObjectName("resourceTabs")
        self.coreTab = QtWidgets.QWidget()
        self.coreTab.setObjectName("coreTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.coreTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.coreSearchEdit = QtWidgets.QLineEdit(self.coreTab)
        self.coreSearchEdit.setObjectName("coreSearchEdit")
        self.verticalLayout_2.addWidget(self.coreSearchEdit)
        self.coreTree = QtWidgets.QTreeView(self.coreTab)
        self.coreTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.coreTree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.coreTree.setAlternatingRowColors(True)
        self.coreTree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.coreTree.setSortingEnabled(True)
        self.coreTree.setAllColumnsShowFocus(True)
        self.coreTree.setObjectName("coreTree")
        self.coreTree.header().setSortIndicatorShown(True)
        self.coreTree.header().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.coreTree)
        self.resourceTabs.addTab(self.coreTab, "")
        self.modulesTab = QtWidgets.QWidget()
        self.modulesTab.setObjectName("modulesTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.modulesTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.modulesCombo = QtWidgets.QComboBox(self.modulesTab)
        self.modulesCombo.setMaxVisibleItems(18)
        self.modulesCombo.setObjectName("modulesCombo")
        self.horizontalLayout_2.addWidget(self.modulesCombo)
        self.moduleRefreshButton = QtWidgets.QPushButton(self.modulesTab)
        self.moduleRefreshButton.setMinimumSize(QtCore.QSize(70, 0))
        self.moduleRefreshButton.setMaximumSize(QtCore.QSize(16777215, 70))
        self.moduleRefreshButton.setObjectName("moduleRefreshButton")
        self.horizontalLayout_2.addWidget(self.moduleRefreshButton)
        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.modulesTab)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.moduleSearchEdit = QtWidgets.QLineEdit(self.modulesTab)
        self.moduleSearchEdit.setObjectName("moduleSearchEdit")
        self.horizontalLayout_4.addWidget(self.moduleSearchEdit)
        self.moduleReloadButton = QtWidgets.QPushButton(self.modulesTab)
        self.moduleReloadButton.setEnabled(False)
        self.moduleReloadButton.setMinimumSize(QtCore.QSize(70, 0))
        self.moduleReloadButton.setMaximumSize(QtCore.QSize(70, 16777215))
        self.moduleReloadButton.setObjectName("moduleReloadButton")
        self.horizontalLayout_4.addWidget(self.moduleReloadButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.modulesTree = QtWidgets.QTreeView(self.modulesTab)
        self.modulesTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.modulesTree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.modulesTree.setAlternatingRowColors(True)
        self.modulesTree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.modulesTree.setSortingEnabled(True)
        self.modulesTree.setAllColumnsShowFocus(True)
        self.modulesTree.setObjectName("modulesTree")
        self.modulesTree.header().setSortIndicatorShown(False)
        self.verticalLayout.addWidget(self.modulesTree)
        self.resourceTabs.addTab(self.modulesTab, "")
        self.overrideTab = QtWidgets.QWidget()
        self.overrideTab.setObjectName("overrideTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.overrideTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.overrideFolderFrame = QtWidgets.QFrame(self.overrideTab)
        self.overrideFolderFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.overrideFolderFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.overrideFolderFrame.setObjectName("overrideFolderFrame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.overrideFolderFrame)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.overrideFolderCombo = QtWidgets.QComboBox(self.overrideFolderFrame)
        self.overrideFolderCombo.setObjectName("overrideFolderCombo")
        self.horizontalLayout_5.addWidget(self.overrideFolderCombo)
        self.overrideRefreshButton = QtWidgets.QPushButton(self.overrideFolderFrame)
        self.overrideRefreshButton.setMinimumSize(QtCore.QSize(70, 0))
        self.overrideRefreshButton.setMaximumSize(QtCore.QSize(70, 16777215))
        self.overrideRefreshButton.setObjectName("overrideRefreshButton")
        self.horizontalLayout_5.addWidget(self.overrideRefreshButton)
        self.horizontalLayout_5.setStretch(0, 1)
        self.verticalLayout_3.addWidget(self.overrideFolderFrame)
        self.overrideLine = QtWidgets.QFrame(self.overrideTab)
        self.overrideLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.overrideLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.overrideLine.setObjectName("overrideLine")
        self.verticalLayout_3.addWidget(self.overrideLine)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.overrideSearchEdit = QtWidgets.QLineEdit(self.overrideTab)
        self.overrideSearchEdit.setObjectName("overrideSearchEdit")
        self.horizontalLayout_3.addWidget(self.overrideSearchEdit)
        self.overrideReloadButton = QtWidgets.QPushButton(self.overrideTab)
        self.overrideReloadButton.setMinimumSize(QtCore.QSize(70, 0))
        self.overrideReloadButton.setMaximumSize(QtCore.QSize(70, 16777215))
        self.overrideReloadButton.setObjectName("overrideReloadButton")
        self.horizontalLayout_3.addWidget(self.overrideReloadButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.overrideTree = QtWidgets.QTreeView(self.overrideTab)
        self.overrideTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.overrideTree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.overrideTree.setAlternatingRowColors(True)
        self.overrideTree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.overrideTree.setSortingEnabled(True)
        self.overrideTree.setAllColumnsShowFocus(True)
        self.overrideTree.setObjectName("overrideTree")
        self.overrideTree.header().setSortIndicatorShown(False)
        self.verticalLayout_3.addWidget(self.overrideTree)
        self.resourceTabs.addTab(self.overrideTab, "")
        self.texturesTab = QtWidgets.QWidget()
        self.texturesTab.setObjectName("texturesTab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.texturesTab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.texturesCombo = QtWidgets.QComboBox(self.texturesTab)
        self.texturesCombo.setObjectName("texturesCombo")
        self.verticalLayout_6.addWidget(self.texturesCombo)
        self.textureLine = QtWidgets.QFrame(self.texturesTab)
        self.textureLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.textureLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.textureLine.setObjectName("textureLine")
        self.verticalLayout_6.addWidget(self.textureLine)
        self.textureSearchEdit = QtWidgets.QLineEdit(self.texturesTab)
        self.textureSearchEdit.setObjectName("textureSearchEdit")
        self.verticalLayout_6.addWidget(self.textureSearchEdit)
        self.texturesList = TexturesView(self.texturesTab)
        self.texturesList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.texturesList.setProperty("showDropIndicator", False)
        self.texturesList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.texturesList.setIconSize(QtCore.QSize(64, 64))
        self.texturesList.setProperty("isWrapping", True)
        self.texturesList.setResizeMode(QtWidgets.QListView.Adjust)
        self.texturesList.setLayoutMode(QtWidgets.QListView.Batched)
        self.texturesList.setGridSize(QtCore.QSize(92, 92))
        self.texturesList.setViewMode(QtWidgets.QListView.IconMode)
        self.texturesList.setUniformItemSizes(True)
        self.texturesList.setObjectName("texturesList")
        self.verticalLayout_6.addWidget(self.texturesList)
        self.resourceTabs.addTab(self.texturesTab, "")
        self.verticalLayout_4.addWidget(self.resourceTabs)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.vboxlayout.setObjectName("vboxlayout")
        spacerItem = QtWidgets.QSpacerItem(124, 45, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.vboxlayout.addItem(spacerItem)
        self.sidebar = QtWidgets.QFrame(self.centralwidget)
        self.sidebar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sidebar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sidebar.setObjectName("sidebar")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.sidebar)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.openButton = QtWidgets.QPushButton(self.sidebar)
        self.openButton.setObjectName("openButton")
        self.verticalLayout_5.addWidget(self.openButton)
        self.extractButton = QtWidgets.QPushButton(self.sidebar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extractButton.sizePolicy().hasHeightForWidth())
        self.extractButton.setSizePolicy(sizePolicy)
        self.extractButton.setObjectName("extractButton")
        self.verticalLayout_5.addWidget(self.extractButton)
        self.tpcGroup_2 = QtWidgets.QGroupBox(self.sidebar)
        self.tpcGroup_2.setObjectName("tpcGroup_2")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.tpcGroup_2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.tpcDecompileCheckbox = QtWidgets.QCheckBox(self.tpcGroup_2)
        self.tpcDecompileCheckbox.setObjectName("tpcDecompileCheckbox")
        self.verticalLayout_10.addWidget(self.tpcDecompileCheckbox)
        self.tpcTxiCheckbox = QtWidgets.QCheckBox(self.tpcGroup_2)
        self.tpcTxiCheckbox.setObjectName("tpcTxiCheckbox")
        self.verticalLayout_10.addWidget(self.tpcTxiCheckbox)
        self.verticalLayout_5.addWidget(self.tpcGroup_2)
        self.mdlGroup_2 = QtWidgets.QGroupBox(self.sidebar)
        self.mdlGroup_2.setObjectName("mdlGroup_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.mdlGroup_2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.mdlDecompileCheckbox = QtWidgets.QCheckBox(self.mdlGroup_2)
        self.mdlDecompileCheckbox.setObjectName("mdlDecompileCheckbox")
        self.verticalLayout_9.addWidget(self.mdlDecompileCheckbox)
        self.mdlTexturesCheckbox = QtWidgets.QCheckBox(self.mdlGroup_2)
        self.mdlTexturesCheckbox.setObjectName("mdlTexturesCheckbox")
        self.verticalLayout_9.addWidget(self.mdlTexturesCheckbox)
        self.verticalLayout_5.addWidget(self.mdlGroup_2)
        self.vboxlayout.addWidget(self.sidebar)
        spacerItem1 = QtWidgets.QSpacerItem(124, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.vboxlayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 478, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuNew = QtWidgets.QMenu(self.menuFile)
        self.menuNew.setObjectName("menuNew")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuDiscord = QtWidgets.QMenu(self.menuHelp)
        self.menuDiscord.setObjectName("menuDiscord")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.cloneModuleAction = QtWidgets.QAction(MainWindow)
        self.cloneModuleAction.setObjectName("cloneModuleAction")
        self.actionRecent_Files = QtWidgets.QAction(MainWindow)
        self.actionRecent_Files.setObjectName("actionRecent_Files")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionCheck_for_Updates = QtWidgets.QAction(MainWindow)
        self.actionCheck_for_Updates.setObjectName("actionCheck_for_Updates")
        self.actionCreature = QtWidgets.QAction(MainWindow)
        self.actionCreature.setObjectName("actionCreature")
        self.actionItem = QtWidgets.QAction(MainWindow)
        self.actionItem.setObjectName("actionItem")
        self.actionDoor = QtWidgets.QAction(MainWindow)
        self.actionDoor.setObjectName("actionDoor")
        self.actionPlaceable = QtWidgets.QAction(MainWindow)
        self.actionPlaceable.setObjectName("actionPlaceable")
        self.actionMerchant = QtWidgets.QAction(MainWindow)
        self.actionMerchant.setObjectName("actionMerchant")
        self.actionEncounter = QtWidgets.QAction(MainWindow)
        self.actionEncounter.setObjectName("actionEncounter")
        self.actionTrigger = QtWidgets.QAction(MainWindow)
        self.actionTrigger.setObjectName("actionTrigger")
        self.actionWaypoint = QtWidgets.QAction(MainWindow)
        self.actionWaypoint.setObjectName("actionWaypoint")
        self.actionDialog = QtWidgets.QAction(MainWindow)
        self.actionDialog.setEnabled(False)
        self.actionDialog.setObjectName("actionDialog")
        self.openAction = QtWidgets.QAction(MainWindow)
        self.openAction.setObjectName("openAction")
        self.actionNewGFF = QtWidgets.QAction(MainWindow)
        self.actionNewGFF.setObjectName("actionNewGFF")
        self.actionNewERF = QtWidgets.QAction(MainWindow)
        self.actionNewERF.setObjectName("actionNewERF")
        self.actionNewTXT = QtWidgets.QAction(MainWindow)
        self.actionNewTXT.setObjectName("actionNewTXT")
        self.actionEditTLK = QtWidgets.QAction(MainWindow)
        self.actionEditTLK.setEnabled(False)
        self.actionEditTLK.setObjectName("actionEditTLK")
        self.actionHelpUpdates = QtWidgets.QAction(MainWindow)
        self.actionHelpUpdates.setObjectName("actionHelpUpdates")
        self.actionHelpAbout = QtWidgets.QAction(MainWindow)
        self.actionHelpAbout.setObjectName("actionHelpAbout")
        self.actionNewSSF = QtWidgets.QAction(MainWindow)
        self.actionNewSSF.setObjectName("actionNewSSF")
        self.actionNewUTC = QtWidgets.QAction(MainWindow)
        self.actionNewUTC.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icons/kx/creature.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionNewUTC.setIcon(icon)
        self.actionNewUTC.setObjectName("actionNewUTC")
        self.actionCloneModule = QtWidgets.QAction(MainWindow)
        self.actionCloneModule.setEnabled(False)
        self.actionCloneModule.setObjectName("actionCloneModule")
        self.actionNewUTP = QtWidgets.QAction(MainWindow)
        self.actionNewUTP.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/icons/kx/placeable.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewUTP.setIcon(icon1)
        self.actionNewUTP.setObjectName("actionNewUTP")
        self.actionNewUTD = QtWidgets.QAction(MainWindow)
        self.actionNewUTD.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/icons/kx/door.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewUTD.setIcon(icon2)
        self.actionNewUTD.setObjectName("actionNewUTD")
        self.actionNewUTW = QtWidgets.QAction(MainWindow)
        self.actionNewUTW.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/icons/kx/waypoint.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewUTW.setIcon(icon3)
        self.actionNewUTW.setObjectName("actionNewUTW")
        self.actionNewUTT = QtWidgets.QAction(MainWindow)
        self.actionNewUTT.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/icons/kx/trigger.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewUTT.setIcon(icon4)
        self.actionNewUTT.setObjectName("actionNewUTT")
        self.actionNewUTE = QtWidgets.QAction(MainWindow)
        self.actionNewUTE.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/icons/kx/encounter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewUTE.setIcon(icon5)
        self.actionNewUTE.setObjectName("actionNewUTE")
        self.actionNewUTS = QtWidgets.QAction(MainWindow)
        self.actionNewUTS.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/icons/kx/sound.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewUTS.setIcon(icon6)
        self.actionNewUTS.setObjectName("actionNewUTS")
        self.actionNewUTM = QtWidgets.QAction(MainWindow)
        self.actionNewUTM.setEnabled(False)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/images/icons/kx/merchant.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewUTM.setIcon(icon7)
        self.actionNewUTM.setObjectName("actionNewUTM")
        self.actionNewUTI = QtWidgets.QAction(MainWindow)
        self.actionNewUTI.setEnabled(False)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/images/icons/kx/item.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewUTI.setIcon(icon8)
        self.actionNewUTI.setObjectName("actionNewUTI")
        self.actionNewDLG = QtWidgets.QAction(MainWindow)
        self.actionNewDLG.setEnabled(False)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/images/icons/kx/dialog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewDLG.setIcon(icon9)
        self.actionNewDLG.setObjectName("actionNewDLG")
        self.actionNewNSS = QtWidgets.QAction(MainWindow)
        self.actionNewNSS.setEnabled(False)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/images/icons/kx/script.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewNSS.setIcon(icon10)
        self.actionNewNSS.setObjectName("actionNewNSS")
        self.actionEditJRL = QtWidgets.QAction(MainWindow)
        self.actionEditJRL.setEnabled(False)
        self.actionEditJRL.setObjectName("actionEditJRL")
        self.actionFileSearch = QtWidgets.QAction(MainWindow)
        self.actionFileSearch.setEnabled(False)
        self.actionFileSearch.setObjectName("actionFileSearch")
        self.actionGeometryEditor = QtWidgets.QAction(MainWindow)
        self.actionGeometryEditor.setEnabled(False)
        self.actionGeometryEditor.setObjectName("actionGeometryEditor")
        self.actionIndoorMapBuilder = QtWidgets.QAction(MainWindow)
        self.actionIndoorMapBuilder.setEnabled(False)
        self.actionIndoorMapBuilder.setObjectName("actionIndoorMapBuilder")
        self.actionEditModule = QtWidgets.QAction(MainWindow)
        self.actionEditModule.setEnabled(False)
        self.actionEditModule.setObjectName("actionEditModule")
        self.actionInstructions = QtWidgets.QAction(MainWindow)
        self.actionInstructions.setObjectName("actionInstructions")
        self.actionDiscordHolocronToolset = QtWidgets.QAction(MainWindow)
        self.actionDiscordHolocronToolset.setObjectName("actionDiscordHolocronToolset")
        self.actionDiscordKotOR = QtWidgets.QAction(MainWindow)
        self.actionDiscordKotOR.setObjectName("actionDiscordKotOR")
        self.actionDiscordDeadlyStream = QtWidgets.QAction(MainWindow)
        self.actionDiscordDeadlyStream.setObjectName("actionDiscordDeadlyStream")
        self.menuNew.addAction(self.actionNewDLG)
        self.menuNew.addAction(self.actionNewNSS)
        self.menuNew.addAction(self.actionNewUTC)
        self.menuNew.addAction(self.actionNewUTP)
        self.menuNew.addAction(self.actionNewUTD)
        self.menuNew.addAction(self.actionNewUTI)
        self.menuNew.addAction(self.actionNewUTS)
        self.menuNew.addAction(self.actionNewUTT)
        self.menuNew.addAction(self.actionNewUTM)
        self.menuNew.addAction(self.actionNewUTW)
        self.menuNew.addAction(self.actionNewUTE)
        self.menuNew.addSeparator()
        self.menuNew.addAction(self.actionCloneModule)
        self.menuNew.addSeparator()
        self.menuNew.addAction(self.actionNewGFF)
        self.menuNew.addAction(self.actionNewERF)
        self.menuNew.addAction(self.actionNewTXT)
        self.menuNew.addAction(self.actionNewSSF)
        self.menuFile.addAction(self.menuNew.menuAction())
        self.menuFile.addAction(self.openAction)
        self.menuFile.addAction(self.actionEditModule)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuTools.addAction(self.actionEditTLK)
        self.menuTools.addAction(self.actionEditJRL)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionFileSearch)
        self.menuTools.addAction(self.actionIndoorMapBuilder)
        self.menuDiscord.addAction(self.actionDiscordHolocronToolset)
        self.menuDiscord.addAction(self.actionDiscordKotOR)
        self.menuDiscord.addAction(self.actionDiscordDeadlyStream)
        self.menuHelp.addAction(self.actionHelpAbout)
        self.menuHelp.addAction(self.menuDiscord.menuAction())
        self.menuHelp.addAction(self.actionInstructions)
        self.menuHelp.addAction(self.actionHelpUpdates)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.resourceTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Holocron Toolset"))
        self.coreSearchEdit.setPlaceholderText(_translate("MainWindow", "search..."))
        self.resourceTabs.setTabText(self.resourceTabs.indexOf(self.coreTab), _translate("MainWindow", "Core"))
        self.moduleRefreshButton.setToolTip(_translate("MainWindow", "Refresh the list of modules."))
        self.moduleRefreshButton.setText(_translate("MainWindow", "Refresh"))
        self.moduleSearchEdit.setPlaceholderText(_translate("MainWindow", "search..."))
        self.moduleReloadButton.setToolTip(_translate("MainWindow", "Reload the active module."))
        self.moduleReloadButton.setText(_translate("MainWindow", "Reload"))
        self.resourceTabs.setTabText(self.resourceTabs.indexOf(self.modulesTab), _translate("MainWindow", "Modules"))
        self.overrideRefreshButton.setToolTip(_translate("MainWindow", "Refresh the list of modules."))
        self.overrideRefreshButton.setText(_translate("MainWindow", "Refresh"))
        self.overrideSearchEdit.setPlaceholderText(_translate("MainWindow", "search..."))
        self.overrideReloadButton.setToolTip(_translate("MainWindow", "Refresh the list of files in the override folder."))
        self.overrideReloadButton.setText(_translate("MainWindow", "Reload"))
        self.resourceTabs.setTabText(self.resourceTabs.indexOf(self.overrideTab), _translate("MainWindow", "Override"))
        self.textureSearchEdit.setPlaceholderText(_translate("MainWindow", "search..."))
        self.resourceTabs.setTabText(self.resourceTabs.indexOf(self.texturesTab), _translate("MainWindow", "Textures"))
        self.openButton.setText(_translate("MainWindow", "Open Selected"))
        self.extractButton.setText(_translate("MainWindow", "Extract Selected"))
        self.tpcGroup_2.setTitle(_translate("MainWindow", "TPC"))
        self.tpcDecompileCheckbox.setText(_translate("MainWindow", "Decompile"))
        self.tpcTxiCheckbox.setText(_translate("MainWindow", "Extract TXI"))
        self.mdlGroup_2.setTitle(_translate("MainWindow", "MDL"))
        self.mdlDecompileCheckbox.setText(_translate("MainWindow", "Decompile"))
        self.mdlTexturesCheckbox.setText(_translate("MainWindow", "Extract Textures"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuNew.setTitle(_translate("MainWindow", "New"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuDiscord.setTitle(_translate("MainWindow", "Discord"))
        self.cloneModuleAction.setText(_translate("MainWindow", "Clone Module"))
        self.actionRecent_Files.setText(_translate("MainWindow", "Recent Files"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionCheck_for_Updates.setText(_translate("MainWindow", "Check for Updates"))
        self.actionCreature.setText(_translate("MainWindow", "Creature"))
        self.actionItem.setText(_translate("MainWindow", "Item"))
        self.actionDoor.setText(_translate("MainWindow", "Door"))
        self.actionPlaceable.setText(_translate("MainWindow", "Placeable"))
        self.actionMerchant.setText(_translate("MainWindow", "Merchant"))
        self.actionEncounter.setText(_translate("MainWindow", "Encounter"))
        self.actionTrigger.setText(_translate("MainWindow", "Trigger"))
        self.actionWaypoint.setText(_translate("MainWindow", "Waypoint"))
        self.actionDialog.setText(_translate("MainWindow", "Dialog"))
        self.openAction.setText(_translate("MainWindow", "Open"))
        self.actionNewGFF.setText(_translate("MainWindow", "GFF"))
        self.actionNewERF.setText(_translate("MainWindow", "ERF"))
        self.actionNewTXT.setText(_translate("MainWindow", "TXT"))
        self.actionEditTLK.setText(_translate("MainWindow", "Edit Talk Table"))
        self.actionHelpUpdates.setText(_translate("MainWindow", "Check For Updates"))
        self.actionHelpAbout.setText(_translate("MainWindow", "About"))
        self.actionNewSSF.setText(_translate("MainWindow", "SSF"))
        self.actionNewUTC.setText(_translate("MainWindow", "Creature"))
        self.actionCloneModule.setText(_translate("MainWindow", "Clone Module"))
        self.actionNewUTP.setText(_translate("MainWindow", "Placeable"))
        self.actionNewUTD.setText(_translate("MainWindow", "Door"))
        self.actionNewUTW.setText(_translate("MainWindow", "Waypoint"))
        self.actionNewUTT.setText(_translate("MainWindow", "Trigger"))
        self.actionNewUTE.setText(_translate("MainWindow", "Encounter"))
        self.actionNewUTS.setText(_translate("MainWindow", "Sound"))
        self.actionNewUTM.setText(_translate("MainWindow", "Merchant"))
        self.actionNewUTI.setText(_translate("MainWindow", "Item"))
        self.actionNewDLG.setText(_translate("MainWindow", "Dialog"))
        self.actionNewNSS.setText(_translate("MainWindow", "Script"))
        self.actionEditJRL.setText(_translate("MainWindow", "Edit Journal"))
        self.actionFileSearch.setText(_translate("MainWindow", "File Search"))
        self.actionGeometryEditor.setText(_translate("MainWindow", "Geometry Editor"))
        self.actionIndoorMapBuilder.setText(_translate("MainWindow", "Indoor Map Builder"))
        self.actionEditModule.setText(_translate("MainWindow", "Edit Module"))
        self.actionInstructions.setText(_translate("MainWindow", "Instructions"))
        self.actionDiscordHolocronToolset.setText(_translate("MainWindow", "Holocron Toolset"))
        self.actionDiscordKotOR.setText(_translate("MainWindow", "r/KotOR"))
        self.actionDiscordDeadlyStream.setText(_translate("MainWindow", "Deadly Stream"))
from toolset.mainwindow import TexturesView
import resources_rc
