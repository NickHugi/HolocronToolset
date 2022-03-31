import json
from typing import Dict, Optional

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QTreeWidgetItem, QMessageBox
from pykotor.common.stream import BinaryReader

from misc.help import helpwindow_ui


class HelpWindow(QMainWindow):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.ui = helpwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self._setupSignals()
        self._setupContents()

        self.ui.textDisplay.setSearchPaths(["./help/images"])

    def _setupSignals(self) -> None:
        self.ui.contentsTree.itemDoubleClicked.connect(self.onContentsDoubleClicked)

    def _setupContents(self) -> None:
        text = BinaryReader.load_file("./help/contents.json")
        data = json.loads(text)
        self._setupContentsRec(None, data)

    def _setupContentsRec(self, parent: Optional[QTreeWidgetItem], data: Dict) -> None:
        add = self.ui.contentsTree.addTopLevelItem if parent is None else parent.addChild

        if "structure" in data:
            for title in data["structure"]:
                item = QTreeWidgetItem([title])
                item.setData(0, QtCore.Qt.UserRole, data["structure"][title]["filename"])
                add(item)
                self._setupContentsRec(item, data["structure"][title])

    def displayFile(self, filepath: str) -> None:
        try:
            text = BinaryReader.load_file(filepath).decode()
            self.ui.textDisplay.setHtml(text)
        except (IOError, FileNotFoundError):
            QMessageBox(QMessageBox.Critical, "Failed to open help file", "Could not access '{}'.".format(filepath)).exec_()

    def onContentsDoubleClicked(self, item: QTreeWidgetItem) -> None:
        filename = item.data(0, QtCore.Qt.UserRole)
        if filename != "":
            self.displayFile("./help/{}".format(filename))
