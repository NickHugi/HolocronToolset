import math
from typing import Optional, Dict, NamedTuple, Set

from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QFileDialog, QMessageBox, QDialog
from pykotor.common.geometry import Vector3, SurfaceMaterial, Vector2, Polygon2
from pykotor.common.misc import ResRef, Game
from pykotor.common.stream import BinaryReader
from pykotor.extract.installation import SearchLocation
from pykotor.resource.formats.bwm import read_bwm, BWM
from pykotor.resource.formats.gff import read_gff, write_gff
from pykotor.resource.formats.lyt import read_lyt, LYT
from pykotor.resource.generics.git import GIT, construct_git, GITTrigger, dismantle_git
from pykotor.resource.type import ResourceType

from data.installation import HTInstallation
from editors.editor import Editor
from misc import ui_edit_trigger
from misc.triggers import ui_geometry_editor

_TRANS_FACE_ROLE = QtCore.Qt.UserRole + 1
_TRANS_EDGE_ROLE = QtCore.Qt.UserRole + 2


class VertexSelection(NamedTuple):
    trigger: GITTrigger
    index: int


class GeometryEditor(Editor):
    def __init__(self, parent: QWidget, installation: Optional[HTInstallation] = None):
        supported = [ResourceType.GIT]
        super().__init__(parent, "Geometry Editor", "trigger", supported, supported, installation)

        self.ui = ui_geometry_editor.Ui_MainWindow()
        self.ui.setupUi(self)
        self._setupMenus()
        self._setupSignals()

        self._bwm: Optional[BWM] = None
        self._git: Optional[GIT] = None
        self._selectedTrigger: Optional[GITTrigger] = None
        self._selectedVertex: Optional[int] = None
        self._selectedOrigin: Vector2 = Vector2.from_null()
        self._extendTrigger: bool = False

        self.materialColors: Dict[SurfaceMaterial, QColor] = {
            SurfaceMaterial.UNDEFINED:      QColor(255, 0, 0, 40),
            SurfaceMaterial.OBSCURING:      QColor(255, 0, 0, 40),
            SurfaceMaterial.DIRT:           QColor(0x444444),
            SurfaceMaterial.GRASS:          QColor(0x444444),
            SurfaceMaterial.STONE:          QColor(0x444444),
            SurfaceMaterial.WOOD:           QColor(0x444444),
            SurfaceMaterial.WATER:          QColor(0x444444),
            SurfaceMaterial.NON_WALK:       QColor(255, 0, 0, 40),
            SurfaceMaterial.TRANSPARENT:    QColor(255, 0, 0, 40),
            SurfaceMaterial.CARPET:         QColor(0x444444),
            SurfaceMaterial.METAL:          QColor(0x444444),
            SurfaceMaterial.PUDDLES:        QColor(0x444444),
            SurfaceMaterial.SWAMP:          QColor(0x444444),
            SurfaceMaterial.MUD:            QColor(0x444444),
            SurfaceMaterial.LEAVES:         QColor(0x444444),
            SurfaceMaterial.LAVA:           QColor(255, 0, 0, 40),
            SurfaceMaterial.BOTTOMLESS_PIT: QColor(255, 0, 0, 40),
            SurfaceMaterial.DEEP_WATER:     QColor(255, 0, 0, 40),
            SurfaceMaterial.DOOR:           QColor(0x444444),
            SurfaceMaterial.NON_WALK_GRASS: QColor(255, 0, 0, 40),
            SurfaceMaterial.TRIGGER:        QColor(0x999900)
        }
        self.ui.drawArea.materialColors = self.materialColors
        self.ui.drawArea.hideWalkmeshEdges = True

        self.new()

    def _setupSignals(self) -> None:
        self.ui.actionSelectLayout.triggered.connect(self.openLayout)

        #self.ui.drawArea.mousePressed.connect(self.onWalkmeshMousePressed)
        self.ui.drawArea.mouseMoved.connect(self.onWorldMouseMoved)
        self.ui.drawArea.mouseScrolled.connect(self.onMouseScrolled)
        #self.ui.drawArea.instanceHovered.connect(self.onInstanceHovered)
        #self.ui.drawArea.mouseReleased.connect(self.onWalkmeshMouseReleased)

        '''self.ui.triggerList.itemSelectionChanged.connect(self.reloadGeomList)
        self.ui.addTriggerButton.clicked.connect(self.onAddTrigger)
        self.ui.removeTriggerButton.clicked.connect(self.onRemoveTrigger)
        self.ui.editTriggerButton.clicked.connect(self.onEditTrigger)

        self.ui.addGeomButton.clicked.connect(self.onAddGeom)
        self.ui.removeGeomButton.clicked.connect(self.onRemoveGeom)
        self.ui.editGeomButton.clicked.connect(self.onEditGeom)

        self.ui.actionZoomIn.triggered.connect(lambda: self.ui.drawArea.cameraZoom(2))
        self.ui.actionZoomOut.triggered.connect(lambda: self.ui.drawArea.cameraZoom(-2))

        QShortcut("Esc", self).activated.connect(self.onStopAddGeom)'''

    def load(self, filepath: str, resref: str, restype: ResourceType, data: bytes) -> None:
        super().load(filepath, resref, restype, data)

        order = [SearchLocation.OVERRIDE, SearchLocation.CHITIN]
        result = self._installation.resource(resref, ResourceType.LYT, order)
        if result:
            m = QMessageBox(QMessageBox.Information, "Found the corresponding LYT file.",
                            "Would you like to load it?\n" + result.filepath,
                            QMessageBox.Yes | QMessageBox.No, self)
            if m.exec():
                self.loadLayout(read_lyt(result.data))

        self._git = construct_git(read_gff(data))
        self.ui.drawArea.setGit(self._git)
        self.reloadTriggerList()

    def reloadTriggerList(self) -> None:
        self.ui.triggerList.clear()
        for i, trigger in enumerate(self._git.triggers):
            text = "[{}] {}".format(i, trigger.resref)
            item = QListWidgetItem(text)
            item.setData(QtCore.Qt.UserRole, trigger)
            self.ui.triggerList.addItem(item)

    def reloadGeomList(self) -> None:
        hasItem = len(self.ui.triggerList.selectedItems()) != 0
        self.ui.addGeomButton.setEnabled(hasItem)
        self.ui.removeGeomButton.setEnabled(hasItem)
        self.ui.geometryList.clear()

        if not hasItem:
            return

        item = self.ui.triggerList.selectedItems()[0]
        trigger = item.data(QtCore.Qt.UserRole)
        self._selectedTrigger = trigger
        self.ui.drawArea.setHighlightedTrigger(trigger)
        for i, point in enumerate(trigger.geometry):
            text = "Point {}".format(i)
            item = QListWidgetItem(text)
            item.setData(QtCore.Qt.UserRole, point)
            self.ui.geometryList.addItem(item)

    def loadLayout(self, layout: LYT) -> None:
        walkmeshes = []
        for room in layout.rooms:
            order = [SearchLocation.OVERRIDE, SearchLocation.CHITIN]
            bwmData = self._installation.resource(room.model, ResourceType.WOK, order).data
            walkmeshes.append(read_bwm(bwmData))

        self.ui.drawArea.setWalkmeshes(walkmeshes)

    def openLayout(self) -> None:
        filepath, _ = QFileDialog.getOpenFileName(self, "Select a layout file", "", "Walkmesh (*.lyt)")
        if filepath:
            layoutData = BinaryReader.load_file(filepath)
            layout = read_lyt(layoutData)
            self.loadLayout(layout)

    def build(self) -> bytes:
        data = bytearray()
        write_gff(dismantle_git(self._git, Game.K2 if self._installation.tsl else Game.K1), data)
        return data

    def new(self) -> None:
        super().new()

    def onWalkmeshMousePressed(self, x: float, y: float) -> None:
        mouse = self.ui.drawArea.toRenderCoords(x, y)

        if self._extendTrigger:
            trigger = self._selectedTrigger
            if len(trigger.geometry) == 0:
                trigger.position = Vector3(x, y, 0)
                trigger.geometry.append(Vector3(0, 0, 0))
            else:
                trigger.geometry.append(Vector3(x-trigger.position.x, y-trigger.position.y, 0))
            self.reloadGeomList()
        else:
            self.selectTrigger(None)
            for trigger in self._git.triggers:
                if self._selectedTrigger is not None:
                    break

                poly = Polygon2.from_polygon3(trigger.geometry)
                for i, point in enumerate(trigger.geometry):
                    local = self.ui.drawArea.toRenderCoords(point.x+trigger.position.x, point.y+trigger.position.y)
                    distance = math.sqrt((local.x - mouse.x) ** 2 + (local.y - mouse.y) ** 2)
                    if distance <= 6:
                        self.selectTrigger(trigger)
                        self.selectVertex(point)
                        break
                else:
                    if poly.inside(Vector2(x-trigger.position.x, y-trigger.position.y)):
                        self.selectTrigger(trigger)
                        self._selectedOrigin = Vector2(trigger.position.x - x, trigger.position.y - y)
                        break

    def onWorldMouseMoved(self, screen: Vector2, delta: Vector2, buttons: Set[int], keys: Set[int]) -> None:
        world = self.ui.drawArea.toWorldCoords(screen.x, screen.y)

        if QtCore.Qt.LeftButton in buttons and QtCore.Qt.Key_Control in keys:
            self.ui.drawArea.panCamera(-delta.x, -delta.y)
        elif QtCore.Qt.MiddleButton in buttons and QtCore.Qt.Key_Control in keys:
            self.ui.drawArea.rotateCamera(delta.x / 50)

        if self.ui.drawArea._hoveredInstance and self.ui.drawArea._hoveredInstance[0].resref:
            xy = " || ResRef: {} ".format(self.ui.drawArea._hoveredInstance[0].resref)
        else:
            xy = " || "

        self.statusBar().showMessage("x: {:.2f}, y: {:.2f}, z: {:.2f}".format(world.x, world.y, world.z) + xy)

        return
        if self._extendTrigger:
            return

        trigger = self._selectedTrigger
        if self._selectedVertex is not None:
            point = trigger.geometry[self._selectedVertex]
            point.x, point.y = x-trigger.position.x, y-trigger.position.y
        elif self._selectedTrigger is not None:
            trigger.position.x = x + self._selectedOrigin.x
            trigger.position.y = y + self._selectedOrigin.y

    def onMouseScrolled(self, delta: Vector2, buttons: Set[int], keys: Set[int]) -> None:
        if QtCore.Qt.Key_Control in keys:
            self.ui.drawArea.zoomInCamera(delta.y / 50)

    def onWalkmeshMouseReleased(self):
        self.selectVertex(None)

    def onAddTrigger(self) -> None:
        trigger = GITTrigger()
        trigger.resref = ResRef("newTrigger")
        self._git.triggers.append(trigger)
        self.reloadTriggerList()

    def onRemoveTrigger(self) -> None:
        if self.ui.triggerList.selectedItems():
            item = self.ui.triggerList.selectedItems()[0]
            trigger = item.data(QtCore.Qt.UserRole)
            self._git.triggers.remove(trigger)
            self.reloadTriggerList()

    def onEditTrigger(self) -> None:
        if self.ui.triggerList.selectedItems():
            item = self.ui.triggerList.selectedItems()[0]
            trigger = item.data(QtCore.Qt.UserRole)
            EditTriggerDialog(self, trigger).exec_()
            self.reloadTriggerList()

    def onAddGeom(self) -> None:
        if self._selectedTrigger:
            self._extendTrigger = True
            self.refreshStatusBar()

    def onStopAddGeom(self) -> None:
        self._extendTrigger = False
        self.refreshStatusBar()

    def onRemoveGeom(self) -> None:
        if self.ui.geometryList.selectedItems():
            item = self.ui.geometryList.selectedItems()[0]
            point = item.data(QtCore.Qt.UserRole)
            self._selectedTrigger.geometry.remove(point)
            self.reloadGeomList()

    def onEditGeom(self) -> None:
        if self.ui.geometryList.selectedItems():
            item = self.ui.geometryList.selectedItems()[0]
            point = item.data(QtCore.Qt.UserRole)
            EditVector3Dialog(self, point).exec_()
            self.reloadGeomList()

    def selectTrigger(self, trigger: Optional[GITTrigger]) -> None:
        self.ui.drawArea.setHighlightedTrigger(trigger)
        self._selectedTrigger = trigger

        if trigger is None:
            self.ui.triggerList.setCurrentItem(None)
            self.selectVertex(None)
            return

        for i in range(self.ui.triggerList.count()):
            item = self.ui.triggerList.item(i)
            if item.data(QtCore.Qt.UserRole) is trigger:
                self.ui.triggerList.setCurrentItem(item)

    def selectVertex(self, point: Optional[Vector3]) -> None:
        if self._selectedTrigger is None or point is None:
            self._selectedVertex = None
            self.ui.geometryList.setCurrentItem(None)
            return

        self._selectedVertex = self._selectedTrigger.geometry.index(point)
        for i in range(self.ui.geometryList.count()):
            item = self.ui.geometryList.item(i)
            if item.data(QtCore.Qt.UserRole) is point:
                self.ui.geometryList.setCurrentItem(item)

    def refreshStatusBar(self) -> None:
        message = ""
        if self._extendTrigger:
            index = self._git.triggers.index(self._selectedTrigger)
            resref = self._selectedTrigger.resref.get()
            message = "Adding geometry to [{}] {}. Press ESC to stop.".format(index, resref)
        self.statusBar().showMessage(message)


class EditTriggerDialog(QDialog):
    def __init__(self, parent: QWidget, trigger: GITTrigger):
        super().__init__(parent)
        self.ui = ui_edit_trigger.Ui_Dialog()
        self.ui.setupUi(self)

        self.trigger: GITTrigger = trigger
        self.ui.resrefEdit.setText(trigger.resref.get())
        self.ui.xPosSpin.setValue(trigger.position.x)
        self.ui.yPosSpin.setValue(trigger.position.y)
        self.ui.zPosSpin.setValue(trigger.position.z)

    def accept(self) -> None:
        self.trigger.resref.set(self.ui.resrefEdit.text())
        self.trigger.position.x = self.ui.xPosSpin.value()
        self.trigger.position.y = self.ui.yPosSpin.value()
        self.trigger.position.z = self.ui.zPosSpin.value()
        super().accept()


class EditVector3Dialog(QDialog):
    def __init__(self, parent: QWidget, vector: Vector3):
        super().__init__(parent)
        self.ui = ui_edit_trigger.Ui_Dialog()
        self.ui.setupUi(self)

        self.vector: Vector3 = vector
        self.ui.xPosSpin.setValue(vector.x)
        self.ui.yPosSpin.setValue(vector.y)
        self.ui.zPosSpin.setValue(vector.z)

    def accept(self) -> None:
        self.vector.x = self.ui.xPosSpin.value()
        self.vector.y = self.ui.yPosSpin.value()
        self.vector.z = self.ui.zPosSpin.value()
        super().accept()
