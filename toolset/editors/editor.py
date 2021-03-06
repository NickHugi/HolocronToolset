import os
import traceback
from abc import abstractmethod
from copy import deepcopy
from typing import List, Union, Optional

from PyQt5 import QtCore
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog, QMessageBox, QListWidgetItem, \
    QShortcut, QLineEdit, QWidget, QPlainTextEdit

from editors import ui_savetomodule, ui_loadfrommodule, ui_locstring
from pykotor.common.language import LocalizedString, Language, Gender
from pykotor.extract.capsule import Capsule
from pykotor.resource.formats.erf import write_erf, read_erf, ERFType
from pykotor.resource.formats.rim import read_rim, write_rim
from pykotor.resource.formats.tlk import read_tlk, write_tlk
from pykotor.resource.type import ResourceType

from data.configuration import Configuration
from data.installation import HTInstallation


class Editor(QMainWindow):
    """
    Editor is a base class for all file-specific editors. It provides methods for saving and loading files that are
    stored directly in folders and for files that are encapsulated in a MOD or RIM.
    """

    newFile = QtCore.pyqtSignal()
    savedFile = QtCore.pyqtSignal(object, object, object, object)
    loadedFile = QtCore.pyqtSignal(object, object, object, object)

    def __init__(
            self,
            parent: Optional[QWidget],
            title: str, iconName: str,
            readSupported: List[ResourceType],
            writeSupported: List[ResourceType],
            installation: Optional[HTInstallation] = None,
            mainwindow: Optional[QMainWindow] = None
    ):
        super().__init__(parent)

        self._filepath: Optional[str] = None
        self._resref: Optional[str] = None
        self._restype: Optional[ResourceType] = None
        self._revert: Optional[bytes] = None
        self._readSupported: List[ResourceType] = readSupported
        self._writeSupported: List[ResourceType] = writeSupported
        self._config: Configuration = Configuration()
        self._installation: Optional[HTInstallation] = installation
        self._mainwindow = mainwindow

        self._editorTitle = title
        self.setWindowTitle(title)
        self._setupIcon(iconName)

        self._saveFilter: str = "All valid files ("
        for resource in writeSupported:
            self._saveFilter += "*.{}{}".format(resource.extension, "" if writeSupported[-1] == resource else " ")
        self._saveFilter += " *.erf *.mod *.rim);;"
        for resource in writeSupported:
            self._saveFilter += "{} File (*.{});;".format(resource.category, resource.extension)
        self._saveFilter += "Save into module (*.erf *.mod *.rim)"

        self._openFilter: str = "All valid files ("
        for resource in readSupported:
            self._openFilter += "*.{}{}".format(resource.extension, "" if readSupported[-1] == resource else " ")
        self._openFilter += " *.erf *.mod *.rim);;"
        for resource in readSupported:
            self._openFilter += "{} File (*.{});;".format(resource.category, resource.extension)
        self._openFilter += "Load from module (*.erf *.mod *.rim)"

    def _setupMenus(self) -> None:
        for action in self.menuBar().actions()[0].menu().actions():
            if action.text() == "New": action.triggered.connect(self.new)
            if action.text() == "Open": action.triggered.connect(self.open)
            if action.text() == "Save": action.triggered.connect(self.save)
            if action.text() == "Save As": action.triggered.connect(self.saveAs)
            if action.text() == "Revert": action.triggered.connect(self.revert)
            if action.text() == "Revert": action.setEnabled(False)
            if action.text() == "Exit": action.triggered.connect(self.close)
        QShortcut("Ctrl+N", self).activated.connect(self.new)
        QShortcut("Ctrl+O", self).activated.connect(self.open)
        QShortcut("Ctrl+S", self).activated.connect(self.save)
        QShortcut("Ctrl+Shift+S", self).activated.connect(self.saveAs)
        QShortcut("Ctrl+R", self).activated.connect(self.revert)
        QShortcut("Ctrl+Q", self).activated.connect(self.exit)

    def _setupIcon(self, iconName: str) -> None:
        iconVersion = "x" if self._installation is None else "2" if self._installation.tsl else "1"
        iconPath = ":/images/icons/k{}/{}.png".format(iconVersion, iconName)
        self.setWindowIcon(QIcon(QPixmap(iconPath)))

    def encapsulated(self) -> bool:
        return self._filepath.endswith(".rim") or self._filepath.endswith(".erf") or self._filepath.endswith(".mod") or self._filepath.endswith(".bif")

    def refreshWindowTitle(self) -> None:
        installationName = "No Installation" if self._installation is None else self._installation.name

        if self._filepath is None:
            self.setWindowTitle(self._editorTitle)
        elif self.encapsulated():
            self.setWindowTitle("{}/{}.{} - {} - {}".format(os.path.basename(self._filepath), self._resref, self._restype.extension, installationName, self._editorTitle))
        else:
            folders = os.path.normpath(self._filepath).split(os.sep)
            folder = folders[-2] if len(folders) >= 2 else ""
            self.setWindowTitle("{}/{}.{} - {} - {}".format(folder, self._resref, self._restype.extension, installationName, self._editorTitle))

    def saveAs(self) -> None:
        filepath, filter = QFileDialog.getSaveFileName(self, "Save As", "", self._saveFilter, "")
        if filepath != "":
            encapsulated = filepath.endswith(".erf") or filepath.endswith(".mod") or filepath.endswith(".rim")
            encapsulated = encapsulated and "Save into module (*.erf *.mod *.rim)" in self._saveFilter
            if encapsulated:
                if self._resref is None:
                    self._resref = "new"
                    self._restype = self._writeSupported[0]

                dialog2 = SaveToModuleDialog(self._resref, self._restype, self._writeSupported)
                if dialog2.exec_():
                    self._resref = dialog2.resref()
                    self._restype = dialog2.restype()
                    self._filepath = filepath
            else:
                self._filepath = filepath
                self._resref, restype_ext = os.path.basename(self._filepath).split('.', 1)
                self._restype = ResourceType.from_extension(restype_ext)
            self.save()

            self.refreshWindowTitle()
            for action in self.menuBar().actions()[0].menu().actions():
                if action.text() == "Revert": action.setEnabled(True)

    def save(self) -> None:
        if self._filepath is None:
            self.saveAs()
            return

        try:
            data = self.build()
            self._revert = data

            if self._filepath.endswith(".bif"):
                QMessageBox(QMessageBox.Critical, "Could not save file",
                            "Cannot save resource into a .BIF file, select another destination instead.",
                            QMessageBox.Ok, self).show()
            elif self._filepath.endswith(".rim"):
                rim = read_rim(self._filepath)
                rim.set(self._resref, self._restype, data)
                write_rim(rim, self._filepath)
                self.savedFile.emit(self._filepath, self._resref, self._restype, data)
            elif self._filepath.endswith(".erf") or self._filepath.endswith(".mod"):
                erf = read_erf(self._filepath)
                erf.erf_type = ERFType.ERF if self._filepath.endswith(".erf") else ERFType.MOD
                erf.set(self._resref, self._restype, data)
                write_erf(erf, self._filepath)
                self.savedFile.emit(self._filepath, self._resref, self._restype, data)
            else:
                with open(self._filepath, 'wb') as file:
                    file.write(data)
                self.savedFile.emit(self._filepath, self._resref, self._restype, data)

        except Exception as e:
            with open("errorlog.txt", 'a') as file:
                lines = traceback.format_exception(type(e), e, e.__traceback__)
                file.writelines(lines)
                file.write("\n----------------------\n")
            print(''.join(lines))
            QMessageBox(QMessageBox.Critical, "Failed to write to file", str(e)).exec_()

    def open(self):
        filepath, filter = QFileDialog.getOpenFileName(self, "Open file", "", self._openFilter)
        if filepath != "":
            encapsulated = filepath.endswith(".erf") or filepath.endswith(".mod") or filepath.endswith(".rim")
            encapsulated = encapsulated and "Load from module (*.erf *.mod *.rim)" in self._openFilter
            if encapsulated:
                dialog = LoadFromModuleDialog(Capsule(filepath), self._readSupported)
                if dialog.exec_():
                    self.load(filepath, dialog.resref(), dialog.restype(), dialog.data())
            else:
                resref, restype_ext = os.path.basename(filepath).split('.', 1)
                restype = ResourceType.from_extension(restype_ext)
                with open(filepath, 'rb') as file:
                    data = file.read()

                self.load(filepath, resref, restype, data)

    @abstractmethod
    def build(self) -> bytes:
        ...

    def load(self, filepath: str, resref: str, restype: ResourceType, data: bytes) -> None:
        self._filepath = filepath
        self._resref = resref
        self._restype = restype
        self._revert = data
        for action in self.menuBar().actions()[0].menu().actions():
            if action.text() == "Revert": action.setEnabled(True)
        self.refreshWindowTitle()
        self.loadedFile.emit(self._filepath, self._resref, self._restype, data)

    def exit(self) -> None:
        self.close()

    def new(self) -> None:
        self._revert = None
        self._filepath = None
        for action in self.menuBar().actions()[0].menu().actions():
            if action.text() == "Revert": action.setEnabled(False)
        self.refreshWindowTitle()
        self.newFile.emit()

    def revert(self) -> None:
        if self._revert is not None:
            self.load(self._filepath, self._resref, self._restype, self._revert)

    def _loadLocstring(self, textbox: Union[QLineEdit, QPlainTextEdit], locstring: LocalizedString) -> None:
        setText = textbox.setPlainText if isinstance(textbox, QPlainTextEdit) else textbox.setText
        className = "QLineEdit" if isinstance(textbox, QLineEdit) else "QPlainTextEdit"

        textbox.locstring = locstring
        if locstring.stringref == -1:
            text = str(locstring)
            setText(text if text != "-1" else "")
            textbox.setStyleSheet(className + " {background-color: white;}")
        else:
            setText(self._installation.talktable().string(locstring.stringref))
            textbox.setStyleSheet(className + " {background-color: #fffded;}")

    def filepath(self) -> None:
        return self._filepath


class SaveToModuleDialog(QDialog):
    """
    SaveToModuleDialog lets the user specify a ResRef and a resource type when saving to a module.
    """
    def __init__(self, resref, restype, supported):
        super().__init__()

        self.ui = ui_savetomodule.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.resrefEdit.setText(resref)
        self.ui.typeCombo.addItems([restype.extension.upper() for restype in supported])
        self.ui.typeCombo.setCurrentIndex(supported.index(restype))

    def resref(self) -> str:
        return self.ui.resrefEdit.text()

    def restype(self) -> ResourceType:
        return ResourceType.from_extension(self.ui.typeCombo.currentText().lower())


class LoadFromModuleDialog(QDialog):
    """
    LoadFromModuleDialog lets the user select a resource from a ERF or RIM.
    """
    def __init__(self, capsule: Capsule, supported):
        super().__init__()

        self.ui = ui_loadfrommodule.Ui_Dialog()
        self.ui.setupUi(self)

        for resource in capsule:
            if resource.restype() not in supported:
                continue
            filename = resource.resname() + "." + resource.restype().extension
            item = QListWidgetItem(filename)
            item.resource = resource
            self.ui.resourceList.addItem(item)

    def resref(self) -> str:
        return self.ui.resourceList.currentItem().resource.resname()

    def restype(self) -> ResourceType:
        return self.ui.resourceList.currentItem().resource.restype()

    def data(self) -> bytes:
        return self.ui.resourceList.currentItem().resource.data()


class LocalizedStringDialog(QDialog):
    def __init__(self, parent: QWidget, installation: HTInstallation, locstring: LocalizedString):
        super().__init__(parent)

        self.ui = ui_locstring.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("{} - {} - Localized String Editor".format(installation.talktable().language().name.title(), installation.name))

        self.ui.stringrefSpin.valueChanged.connect(self.stringrefChanged)
        self.ui.stringrefNewButton.clicked.connect(self.newTlkString)
        self.ui.stringrefNoneButton.clicked.connect(self.noTlkString)
        self.ui.maleRadio.clicked.connect(self.substringChanged)
        self.ui.femaleRadio.clicked.connect(self.substringChanged)
        self.ui.languageSelect.currentIndexChanged.connect(self.substringChanged)
        self.ui.stringEdit.textChanged.connect(self.stringEdited)

        self._installation = installation
        self.locstring = deepcopy(locstring)
        self.ui.stringrefSpin.setValue(locstring.stringref)

    def accept(self) -> None:
        if self.locstring.stringref != -1:
            tlk = read_tlk(self._installation.path() + "dialog.tlk")
            if len(tlk) <= self.locstring.stringref:
                tlk.resize(self.locstring.stringref + 1)
            tlk.get(self.locstring.stringref).text = self.ui.stringEdit.toPlainText()
            write_tlk(tlk, self._installation.path() + "dialog.tlk")
        super().accept()

    def reject(self) -> None:
        super().reject()

    def stringrefChanged(self, stringref: int) -> None:
        self.ui.substringFrame.setVisible(stringref == -1)
        self.locstring.stringref = stringref

        if stringref == -1:
            language = Language(self.ui.languageSelect.currentIndex())
            gender = Gender(int(self.ui.femaleRadio.isChecked()))
            text = self.locstring.get(language, gender) if self.locstring.get(language, gender) is not None else ""
            self.ui.stringEdit.setPlainText(text)
        else:
            self.ui.stringEdit.setPlainText(self._installation.talktable().string(stringref))

    def newTlkString(self):
        self.ui.stringrefSpin.setValue(self._installation.talktable().size())

    def noTlkString(self) -> None:
        self.ui.stringrefSpin.setValue(-1)

    def substringChanged(self) -> None:
        language = Language(self.ui.languageSelect.currentIndex())
        gender = Gender(int(self.ui.femaleRadio.isChecked()))
        text = self.locstring.get(language, gender) if self.locstring.get(language, gender) is not None else ""
        self.ui.stringEdit.setPlainText(text)

    def stringEdited(self) -> None:
        if self.locstring.stringref == -1:
            language = Language(self.ui.languageSelect.currentIndex())
            gender = Gender(int(self.ui.femaleRadio.isChecked()))
            self.locstring.set(language, gender, self.ui.stringEdit.toPlainText())


class HTPlainTextEdit(QPlainTextEdit):
    keyReleased = QtCore.pyqtSignal()
    doubleClicked = QtCore.pyqtSignal()

    def keyReleaseEvent(self, e: QKeyEvent) -> None:
        super().keyReleaseEvent(e)
        self.keyReleased.emit()

    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        super().mouseDoubleClickEvent(e)
        self.doubleClicked.emit()
