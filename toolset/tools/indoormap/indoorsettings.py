from PyQt5.QtWidgets import QDialog, QWidget

from data.installation import HTInstallation
from editors.editor import Editor
from tools.indoormap import indoorsettings_ui
from tools.indoormap.indoormap import IndoorMap


class IndoorMapSettings(QDialog):
    def __init__(self, parent: QWidget, installation: HTInstallation, indoorMap: IndoorMap):
        super().__init__(parent)

        self.ui = indoorsettings_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.nameEdit.setInstallation(installation)

        self._indoorMap: IndoorMap = indoorMap

        self.ui.nameEdit.setLocstring(indoorMap.name)
        self.ui.colorEdit.setColor(indoorMap.lighting)
        self.ui.warpCodeEdit.setText(indoorMap.module_id)

    def _setupSignals(self) -> None:
        ...

    def accept(self) -> None:
        super().accept()

        self._indoorMap.name = self.ui.nameEdit.locstring()
        self._indoorMap.lighting = self.ui.colorEdit.color()
        self._indoorMap.module_id = self.ui.warpCodeEdit.text()
