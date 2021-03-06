import os
from contextlib import suppress
from typing import Set, Dict, Optional

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap, QIcon, QKeyEvent, QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QTreeWidgetItem, QMenu, QAction, QListWidgetItem, \
    QMessageBox, QDialog, QDialogButtonBox, QCheckBox
from pykotor.common.geometry import Vector2
from pykotor.common.misc import ResRef
from pykotor.common.module import Module, ModuleResource
from pykotor.common.stream import BinaryWriter
from pykotor.extract.file import ResourceIdentifier
from pykotor.resource.formats.erf import read_erf, write_erf
from pykotor.resource.formats.rim import read_rim, write_rim
from pykotor.resource.generics.git import GITCreature, GITPlaceable, GITDoor, GITTrigger, GITEncounter, GITWaypoint, \
    GITSound, GITStore, GITCamera, GITInstance
from pykotor.resource.generics.utc import bytes_utc, UTC
from pykotor.resource.generics.utd import bytes_utd, UTD
from pykotor.resource.generics.ute import bytes_ute, UTE
from pykotor.resource.generics.utm import UTM, bytes_utm
from pykotor.resource.generics.utp import bytes_utp, UTP
from pykotor.resource.generics.uts import bytes_uts, UTS
from pykotor.resource.generics.utt import bytes_utt, UTT
from pykotor.resource.generics.utw import bytes_utw, UTW
from pykotor.resource.type import ResourceType

from data.installation import HTInstallation
from misc.help.help import HelpWindow
from pykotor.gl.scene import RenderObject, FocusedCamera

from tools.module.me_controls import ModuleEditorControls, DynamicModuleEditorControls, HolocronModuleEditorControls
from utils.window import openResourceEditor


class ModuleEditor(QMainWindow):
    def __init__(self, parent: Optional[QWidget], installation: HTInstallation, module: Module):
        super().__init__(parent)

        self._installation: HTInstallation = installation
        self._module: Module = module
        self.hideCreatures: bool = False
        self.hidePlaceables: bool = False
        self.hideDoors: bool = False
        self.hideTriggers: bool = False
        self.hideEncounters: bool = False
        self.hideWaypoints: bool = False
        self.hideSounds: bool = False
        self.hideStores: bool = False
        self.hideCameras: bool = False

        from tools.module import ui_moduleeditor
        self.ui = ui_moduleeditor.Ui_MainWindow()
        self.ui.setupUi(self)
        self._setupSignals()

        self.customControls: Dict[str, DynamicModuleEditorControls] = {}
        self.activeControls: ModuleEditorControls = HolocronModuleEditorControls(self.ui.mainRenderer)

        self.ui.mainRenderer.init(installation, module)
        self._setupControlsMenu()
        if "aurora.jsonc" in self.customControls:
            self.activateCustomControls(self.customControls["aurora.jsonc"])

        self._refreshWindowTitle()
        self.rebuildResourceTree()
        self.rebuildInstanceList()

    def _setupSignals(self) -> None:
        self.ui.actionSave.triggered.connect(self.saveGit)
        self.ui.actionInstructions.triggered.connect(self.showHelpWindow)

        self.ui.resourceTree.customContextMenuRequested.connect(self.onResourceTreeContextMenu)

        self.ui.viewCreatureCheck.toggled.connect(self.updateInstanceVisibility)
        self.ui.viewPlaceableCheck.toggled.connect(self.updateInstanceVisibility)
        self.ui.viewDoorCheck.toggled.connect(self.updateInstanceVisibility)
        self.ui.viewSoundCheck.toggled.connect(self.updateInstanceVisibility)
        self.ui.viewTriggerCheck.toggled.connect(self.updateInstanceVisibility)
        self.ui.viewEncounterCheck.toggled.connect(self.updateInstanceVisibility)
        self.ui.viewWaypointCheck.toggled.connect(self.updateInstanceVisibility)
        self.ui.viewCameraCheck.toggled.connect(self.updateInstanceVisibility)
        self.ui.viewStoreCheck.toggled.connect(self.updateInstanceVisibility)

        self.ui.viewCreatureCheck.mouseDoubleClickEvent = lambda _: self.onInstanceVisiblityDoubleClick(self.ui.viewCreatureCheck)
        self.ui.viewPlaceableCheck.mouseDoubleClickEvent = lambda _: self.onInstanceVisiblityDoubleClick(self.ui.viewPlaceableCheck)
        self.ui.viewDoorCheck.mouseDoubleClickEvent = lambda _: self.onInstanceVisiblityDoubleClick(self.ui.viewDoorCheck)
        self.ui.viewSoundCheck.mouseDoubleClickEvent = lambda _: self.onInstanceVisiblityDoubleClick(self.ui.viewSoundCheck)
        self.ui.viewTriggerCheck.mouseDoubleClickEvent = lambda _: self.onInstanceVisiblityDoubleClick(self.ui.viewTriggerCheck)
        self.ui.viewEncounterCheck.mouseDoubleClickEvent = lambda _: self.onInstanceVisiblityDoubleClick(self.ui.viewEncounterCheck)
        self.ui.viewWaypointCheck.mouseDoubleClickEvent = lambda _: self.onInstanceVisiblityDoubleClick(self.ui.viewWaypointCheck)
        self.ui.viewCameraCheck.mouseDoubleClickEvent = lambda _: self.onInstanceVisiblityDoubleClick(self.ui.viewCameraCheck)
        self.ui.viewStoreCheck.mouseDoubleClickEvent = lambda _: self.onInstanceVisiblityDoubleClick(self.ui.viewStoreCheck)

        self.ui.instanceList.doubleClicked.connect(self.onInstanceListDoubleClicked)

        self.ui.mainRenderer.sceneInitalized.connect(self.onRendererSceneInitialized)
        self.ui.mainRenderer.mousePressed.connect(self.onRendererMousePressed)
        self.ui.mainRenderer.mouseMoved.connect(self.onRendererMouseMoved)
        self.ui.mainRenderer.mouseScrolled.connect(self.onRendererMouseScrolled)
        self.ui.mainRenderer.objectSelected.connect(self.onRendererObjectSelected)
        self.ui.mainRenderer.customContextMenuRequested.connect(self.onRendererContextMenu)

    def _setupControlsMenu(self) -> None:
        self.ui.menuControls.clear()
        folder = "./controls/3d/"
        if os.path.exists(folder):
            for path in [path for path in os.listdir(folder) if path.endswith(".json") or path.endswith(".jsonc")]:
                with suppress(Exception):
                    controls = DynamicModuleEditorControls(self.ui.mainRenderer)
                    controls.load(folder + path)
                    self.customControls[path] = controls

                    action = QAction(controls.name, self)
                    action.triggered.connect(lambda _, c=controls: self.activateCustomControls(c))
                    self.ui.menuControls.addAction(action)

            self.ui.menuControls.addSeparator()
            action = QAction("Reload", self)
            action.triggered.connect(self._setupControlsMenu)
            self.ui.menuControls.addAction(action)

    def _refreshWindowTitle(self) -> None:
        title = "{} - {} - Module Editor".format(self._module._id, self._installation.name)
        self.setWindowTitle(title)

    def showHelpWindow(self) -> None:
        window = HelpWindow(self, "./help/tools/1-moduleEditor.md")
        window.show()

    def saveGit(self) -> None:
        self._module.git().save()

    def activateCustomControls(self, controls: DynamicModuleEditorControls) -> None:
        self.activeControls = controls

    def rebuildResourceTree(self) -> None:
        self.ui.resourceTree.clear()
        categories = {
            ResourceType.UTC: QTreeWidgetItem(["Creatures"]),
            ResourceType.UTP: QTreeWidgetItem(["Placeables"]),
            ResourceType.UTD: QTreeWidgetItem(["Doors"]),
            ResourceType.UTI: QTreeWidgetItem(["Items"]),
            ResourceType.UTE: QTreeWidgetItem(["Encounters"]),
            ResourceType.UTT: QTreeWidgetItem(["Triggers"]),
            ResourceType.UTW: QTreeWidgetItem(["Waypoints"]),
            ResourceType.UTS: QTreeWidgetItem(["Sounds"]),
            ResourceType.UTM: QTreeWidgetItem(["Merchants"]),
            ResourceType.DLG: QTreeWidgetItem(["Dialogs"]),
            ResourceType.FAC: QTreeWidgetItem(["Factions"]),
            ResourceType.MDL: QTreeWidgetItem(["Models"]),
            ResourceType.TGA: QTreeWidgetItem(["Textures"]),
            ResourceType.NCS: QTreeWidgetItem(["Scripts"]),
            ResourceType.IFO: QTreeWidgetItem(["Module Data"]),
            ResourceType.INVALID: QTreeWidgetItem(["Other"])
        }
        categories[ResourceType.MDX] = categories[ResourceType.MDL]
        categories[ResourceType.WOK] = categories[ResourceType.MDL]
        categories[ResourceType.TPC] = categories[ResourceType.TGA]
        categories[ResourceType.IFO] = categories[ResourceType.IFO]
        categories[ResourceType.ARE] = categories[ResourceType.IFO]
        categories[ResourceType.GIT] = categories[ResourceType.IFO]
        categories[ResourceType.LYT] = categories[ResourceType.IFO]
        categories[ResourceType.VIS] = categories[ResourceType.IFO]
        categories[ResourceType.PTH] = categories[ResourceType.IFO]
        categories[ResourceType.NSS] = categories[ResourceType.NCS]

        for category in categories:
            self.ui.resourceTree.addTopLevelItem(categories[category])

        for resource in self._module.resources.values():
            item = QTreeWidgetItem([resource.resname() + "." + resource.restype().extension])
            item.setData(0, QtCore.Qt.UserRole, resource)
            category = categories[resource.restype()] if resource.restype() in categories else categories[ResourceType.INVALID]
            category.addChild(item)

        self.ui.resourceTree.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.ui.resourceTree.setSortingEnabled(True)

    def openModuleResource(self, resource: ModuleResource) -> None:
        editor = openResourceEditor(resource.active(), resource.resname(), resource.restype(), resource.data(),
                                    self._installation, self)[1]

        if editor is None:
            QMessageBox(QMessageBox.Critical,
                        "Failed to open editor",
                        "Failed to open editor for file: {}.{}".format(resource.resname(), resource.restype().extension))
        else:
            editor.savedFile.connect(lambda: self._onSavedResource(resource))

    def _onSavedResource(self, resource: ModuleResource) -> None:
        resource.reload()
        self.ui.mainRenderer.scene.clearCacheBuffer.append(ResourceIdentifier(resource.resname(), resource.restype()))

    def copyResourceToOverride(self, resource: ModuleResource) -> None:
        location = "{}/{}.{}".format(self._installation.override_path(), resource.resname(), resource.restype().extension)
        BinaryWriter.dump(location, resource.data())
        resource.add_locations([location])
        resource.activate(location)
        self.ui.mainRenderer.scene.clearCacheBuffer.append(ResourceIdentifier(resource.resname(), resource.restype()))

    def activateResourceFile(self, resource: ModuleResource, location: str) -> None:
        resource.activate(location)
        self.ui.mainRenderer.scene.clearCacheBuffer.append(ResourceIdentifier(resource.resname(), resource.restype()))

    def selectResouceItem(self, instance: GITInstance, clearExisting: bool = True) -> None:
        if clearExisting:
            self.ui.resourceTree.clearSelection()

        for i in range(self.ui.resourceTree.topLevelItemCount()):
            parent = self.ui.resourceTree.topLevelItem(i)
            for j in range(parent.childCount()):
                item = parent.child(j)
                res: ModuleResource = item.data(0, QtCore.Qt.UserRole)
                if res.resname() == instance.reference() and res.restype() == instance.extension():
                    parent.setExpanded(True)
                    item.setSelected(True)
                    self.ui.resourceTree.scrollToItem(item)

    def onResourceTreeContextMenu(self, point: QPoint) -> None:
        menu = QMenu(self)

        data = self.ui.resourceTree.currentItem().data(0, QtCore.Qt.UserRole)
        if isinstance(data, ModuleResource):
            copyToOverrideAction = QAction("Copy To Override", self)
            copyToOverrideAction.triggered.connect(lambda _, r=data: self.copyResourceToOverride(r))

            menu.addAction("Edit Active File").triggered.connect(lambda _, r=data: self.openModuleResource(r))
            menu.addAction("Reload Active File").triggered.connect(lambda _: data.reload())
            menu.addAction(copyToOverrideAction)
            menu.addSeparator()
            for location in data.locations():
                locationAciton = QAction(location, self)
                locationAciton.triggered.connect(lambda _, l=location: self.activateResourceFile(data, l))
                if location == data.active():
                    locationAciton.setEnabled(False)
                if "override" in location.lower():
                    copyToOverrideAction.setEnabled(False)
                menu.addAction(locationAciton)

        menu.exec_(self.ui.resourceTree.mapToGlobal(point))

    def rebuildInstanceList(self) -> None:
        visibleMapping = {
            GITCreature: self.hideCreatures,
            GITPlaceable: self.hidePlaceables,
            GITDoor: self.hideDoors,
            GITTrigger: self.hideTriggers,
            GITEncounter: self.hideEncounters,
            GITWaypoint: self.hideWaypoints,
            GITSound: self.hideSounds,
            GITStore: self.hideStores,
            GITCamera: self.hideCameras,
            GITInstance: False
        }

        iconMapping = {
            GITCreature: QPixmap(":/images/icons/k1/creature.png"),
            GITPlaceable: QPixmap(":/images/icons/k1/placeable.png"),
            GITDoor: QPixmap(":/images/icons/k1/door.png"),
            GITSound: QPixmap(":/images/icons/k1/sound.png"),
            GITTrigger: QPixmap(":/images/icons/k1/trigger.png"),
            GITEncounter: QPixmap(":/images/icons/k1/encounter.png"),
            GITWaypoint: QPixmap(":/images/icons/k1/waypoint.png"),
            GITCamera: QPixmap(":/images/icons/k1/camera.png"),
            GITStore: QPixmap(":/images/icons/k1/merchant.png"),
            GITInstance: QPixmap(32, 32)
        }

        self.ui.instanceList.clear()
        for instance in self._module.git().resource().instances():
            if visibleMapping[type(instance)]:
                continue

            if instance.reference():
                resource = self._module.resource(instance.reference().get(), instance.extension())
                text = resource.localized_name()
                if text is None or text.isspace():
                    text = "[{}]".format(resource.resname())
            else:
                text = "Camera #{}".format(self._module.git().resource().index(instance))

            icon = QIcon(iconMapping[type(instance)])
            item = QListWidgetItem(icon, text)
            item.setToolTip("" if instance.reference() is None else instance.reference().get())
            item.setData(QtCore.Qt.UserRole, instance)
            self.ui.instanceList.addItem(item)

    def selectInstanceItemOnList(self, instance: GITInstance) -> None:
        self.ui.instanceList.clearSelection()
        for i in range(self.ui.instanceList.count()):
            item = self.ui.instanceList.item(i)
            data: GITInstance = item.data(QtCore.Qt.UserRole)
            if data is instance:
                item.setSelected(True)
                self.ui.instanceList.scrollToItem(item)

    def onInstanceVisiblityDoubleClick(self, checkbox: QCheckBox) -> None:
        """
        This method should be called whenever one of the instance visibility checkboxes have been double clicked. The
        resulting affect should be that all checkboxes become unchecked except for the one that was pressed.
        """
        self.ui.viewCreatureCheck.setChecked(False)
        self.ui.viewPlaceableCheck.setChecked(False)
        self.ui.viewDoorCheck.setChecked(False)
        self.ui.viewSoundCheck.setChecked(False)
        self.ui.viewTriggerCheck.setChecked(False)
        self.ui.viewEncounterCheck.setChecked(False)
        self.ui.viewWaypointCheck.setChecked(False)
        self.ui.viewCameraCheck.setChecked(False)
        self.ui.viewStoreCheck.setChecked(False)

        checkbox.setChecked(True)

    def updateInstanceVisibility(self) -> None:
        self.hideCreatures = self.ui.mainRenderer.scene.hide_creatures = not self.ui.viewCreatureCheck.isChecked()
        self.hidePlaceables = self.ui.mainRenderer.scene.hide_placeables = not self.ui.viewPlaceableCheck.isChecked()
        self.hideDoors = self.ui.mainRenderer.scene.hide_doors = not self.ui.viewDoorCheck.isChecked()
        self.hideTriggers = self.ui.mainRenderer.scene.hide_triggers = not self.ui.viewTriggerCheck.isChecked()
        self.hideEncounters = self.ui.mainRenderer.scene.hide_encounters = not self.ui.viewEncounterCheck.isChecked()
        self.hideWaypoints = self.ui.mainRenderer.scene.hide_waypoints = not self.ui.viewWaypointCheck.isChecked()
        self.hideSounds = self.ui.mainRenderer.scene.hide_sounds = not self.ui.viewSoundCheck.isChecked()
        self.hideStores = self.ui.mainRenderer.scene.hide_stores = not self.ui.viewStoreCheck.isChecked()
        self.hideCameras = self.ui.mainRenderer.scene.hide_cameras = not self.ui.viewCameraCheck.isChecked()
        self.rebuildInstanceList()

    def onInstanceListDoubleClicked(self) -> None:
        if self.ui.instanceList.selectedItems():
            item = self.ui.instanceList.selectedItems()[0]
            instance: GITInstance = item.data(QtCore.Qt.UserRole)
            self.ui.mainRenderer.scene.select(instance)

            self.selectResouceItem(item.data(QtCore.Qt.UserRole))
            self.ui.mainRenderer.snapCameraToPoint(instance.position)

    def addInstance(self, instance: GITInstance) -> None:
        instance.position.z = self.ui.mainRenderer.walkmeshPoint(instance.position.x, instance.position.y,
                                                                 self.ui.mainRenderer.scene.camera.z).z

        if not isinstance(instance, GITCamera):
            dialog = InsertInstanceDialog(self, self._installation, self._module, instance.extension())

            if dialog.exec_():
                self.rebuildResourceTree()
                instance.resref = ResRef(dialog.resname)
                self._module.git().resource().add(instance)
        else:
            self._module.git().resource().add(instance)
        self.rebuildInstanceList()

    def removeSelectedInstances(self) -> None:
        for selected in self.ui.mainRenderer.scene.selection:
            if isinstance(selected.data, GITInstance):
                self._module.git().resource().remove(selected.data)
        self.ui.mainRenderer.scene.selection.clear()

    def onRendererMouseMoved(self, screen: Vector2, delta: Vector2, buttons: Set[int], keys: Set[int]) -> None:
        self.activeControls.onMouseMoved(screen, delta, buttons, keys)

    def onRendererMouseScrolled(self, delta: Vector2, buttons: Set[int], keys: Set[int]) -> None:
        self.activeControls.onMouseScrolled(delta, buttons, keys)

    def onRendererMousePressed(self, screen: Vector2, buttons: Set[int], keys: Set[int]) -> None:
        self.activeControls.onMousePressed(screen, buttons, keys)

    def onRendererObjectSelected(self, obj: RenderObject) -> None:
        if obj is not None:
            data = obj.data
            self.selectInstanceItemOnList(data)
            self.selectResouceItem(data)

    def onRendererContextMenu(self, point: QPoint) -> None:
        menu = QMenu(self)
        world = self.ui.mainRenderer.walkmeshPoint(self.ui.mainRenderer.scene.camera.x, self.ui.mainRenderer.scene.camera.y)

        if len(self.ui.mainRenderer.scene.selection) == 0:
            menu.addAction("Insert Creature").triggered.connect(lambda: self.addInstance(GITCreature(world.x, world.y)))
            menu.addAction("Insert Door").triggered.connect(lambda: self.addInstance(GITDoor(world.x, world.y)))
            menu.addAction("Insert Placeable").triggered.connect(lambda: self.addInstance(GITPlaceable(world.x, world.y)))
            menu.addAction("Insert Store").triggered.connect(lambda: self.addInstance(GITStore(world.x, world.y)))
            menu.addAction("Insert Sound").triggered.connect(lambda: self.addInstance(GITSound(world.x, world.y)))
            menu.addAction("Insert Waypoint").triggered.connect(lambda: self.addInstance(GITWaypoint(world.x, world.y)))
            menu.addAction("Insert Camera").triggered.connect(lambda: self.addInstance(GITCamera(world.x, world.y)))
            menu.addAction("Insert Encounter").triggered.connect(lambda: self.addInstance(GITEncounter(world.x, world.y)))
            menu.addAction("Insert Trigger").triggered.connect(lambda: self.addInstance(GITTrigger(world.x, world.y)))
        else:
            menu.addAction("Remove").triggered.connect(self.removeSelectedInstances)

        menu.popup(self.ui.mainRenderer.mapToGlobal(point))
        menu.aboutToHide.connect(self.ui.mainRenderer.resetMouseButtons)

    def onRendererSceneInitialized(self) -> None:
        if self.activeControls.cameraStyle == "FOCUSED":
            self.ui.mainRenderer.scene.camera = FocusedCamera.from_unfocused(self.ui.mainRenderer.scene.camera)

    def keyPressEvent(self, e: QKeyEvent, bubble: bool = True) -> None:
        super().keyPressEvent(e)
        if bubble:
            self.ui.mainRenderer.keyPressEvent(e, False)
        self.activeControls.onKeyPressed(self.ui.mainRenderer.mouseDown(), self.ui.mainRenderer.keysDown())

    def keyReleaseEvent(self, e: QKeyEvent, bubble: bool = True) -> None:
        super().keyReleaseEvent(e)
        if bubble:
            self.ui.mainRenderer.keyReleaseEvent(e, False)
        self.activeControls.onKeyReleased(self.ui.mainRenderer.mouseDown(), self.ui.mainRenderer.keysDown())


class InsertInstanceDialog(QDialog):
    def __init__(self, parent: QWidget, installation: HTInstallation, module: Module, restype: ResourceType):
        super().__init__(parent)

        self._installation: HTInstallation = installation
        self._module: Module = module
        self._restype: ResourceType = restype

        self.resname: str = ""
        self.data: bytes = b''
        self.filepath: str = ""

        from tools.module import ui_insert_instance
        self.ui = ui_insert_instance.Ui_Dialog()
        self.ui.setupUi(self)
        self._setupSignals()
        self._setupLocationSelect()
        self._setupResourceList()

    def _setupSignals(self) -> None:
        self.ui.createResourceRadio.toggled.connect(self.onResourceRadioToggled)
        self.ui.reuseResourceRadio.toggled.connect(self.onResourceRadioToggled)
        self.ui.copyResourceRadio.toggled.connect(self.onResourceRadioToggled)
        self.ui.resrefEdit.textEdited.connect(self.onResRefEdited)
        self.ui.resourceFilter.textChanged.connect(self.onResourceFilterChanged)

    def _setupLocationSelect(self) -> None:
        self.ui.locationSelect.addItem(self._installation.override_path())
        for capsule in self._module.capsules():
            self.ui.locationSelect.addItem(capsule.path())

    def _setupResourceList(self) -> None:
        for resource in self._installation.chitin_resources():
            if resource.restype() == self._restype:
                item = QListWidgetItem(resource.resname())
                item.setToolTip(resource.filepath())
                item.setData(QtCore.Qt.UserRole, resource)
                self.ui.resourceList.addItem(item)

        for capsule in self._module.capsules():
            for resource in [resource for resource in capsule if resource.restype() == self._restype]:
                if resource.restype() == self._restype:
                    item = QListWidgetItem(resource.resname())
                    item.setToolTip(resource.filepath())
                    item.setForeground(QColor(30, 30, 30))
                    item.setData(QtCore.Qt.UserRole, resource)
                    self.ui.resourceList.addItem(item)

        if self.ui.resourceList.count() > 0:
            self.ui.resourceList.item(0).setSelected(True)

    def accept(self) -> None:
        super().accept()

        new = True
        resource = self.ui.resourceList.selectedItems()[0].data(QtCore.Qt.UserRole)

        if self.ui.reuseResourceRadio.isChecked():
            new = False
            self.resname = resource.resname()
            self.filepath = resource.filepath()
            self.data = resource.data()
        elif self.ui.copyResourceRadio.isChecked():
            self.resname = self.ui.resrefEdit.text()
            self.data = resource.data()
        elif self.ui.createResourceRadio.isChecked():
            self.resname = self.ui.resrefEdit.text()
            if self._restype == ResourceType.UTC:
                self.data = bytes_utc(UTC())
            elif self._restype == ResourceType.UTP:
                self.data = bytes_utp(UTP())
            elif self._restype == ResourceType.UTD:
                self.data = bytes_utd(UTD())
            elif self._restype == ResourceType.UTE:
                self.data = bytes_ute(UTE())
            elif self._restype == ResourceType.UTT:
                self.data = bytes_utt(UTT())
            elif self._restype == ResourceType.UTS:
                self.data = bytes_uts(UTS())
            elif self._restype == ResourceType.UTM:
                self.data = bytes_utm(UTM())
            elif self._restype == ResourceType.UTW:
                self.data = bytes_utw(UTW())
            else:
                self.data = b''

        if new:
            if self.filepath.endswith(".erf") or self.filepath.endswith(".mod"):
                erf = read_erf(self.filepath)
                erf.set(self.resname, self._restype, self.data)
                write_erf(erf, self.filepath)
            elif self.filepath.endswith(".rim"):
                rim = read_rim(self.filepath)
                rim.set(self.resname, self._restype, self.data)
                write_rim(rim, self.filepath)
            else:
                self.filepath = "{}/{}.{}".format(self.filepath, self.resname, self._restype.extension)
                BinaryWriter.dump(self.filepath, self.data)

        self._module.add_locations(self.resname, self._restype, [self.filepath])

    def onResourceRadioToggled(self) -> None:
        self.ui.resourceList.setEnabled(not self.ui.createResourceRadio.isChecked())
        self.ui.resourceFilter.setEnabled(not self.ui.createResourceRadio.isChecked())
        self.ui.resrefEdit.setEnabled(not self.ui.reuseResourceRadio.isChecked())

        if self.ui.reuseResourceRadio.isChecked():
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

        if self.ui.copyResourceRadio.isChecked():
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.isValidResref(self.ui.resrefEdit.text()))

        if self.ui.createResourceRadio.isChecked():
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.isValidResref(self.ui.resrefEdit.text()))

    def onResRefEdited(self, text: str) -> None:
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.isValidResref(text))

    def onResourceFilterChanged(self) -> None:
        text = self.ui.resourceFilter.text()
        for row in range(self.ui.resourceList.count()):
            item = self.ui.resourceList.item(row)
            item.setHidden(text not in item.text())

    def isValidResref(self, text: str) -> bool:
        return self._module.resource(text, self._restype) is None and text != ""
