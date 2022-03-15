import json
import math
import os
from copy import copy
from typing import Optional, List, Set, Tuple

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QPointF, QRectF
from PyQt5.QtGui import QImage, QPixmap, QPaintEvent, QTransform, QPainter, QColor, QWheelEvent, QMouseEvent, QKeyEvent, \
    QPen
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QMainWindow
from pykotor.common.geometry import Vector3, Vector2
from pykotor.common.stream import BinaryReader
from pykotor.extract.installation import Installation
from pykotor.resource.formats.bwm import read_bwm, BWM
from pykotor.resource.type import ResourceType

from data.installation import HTInstallation
from tools.indoormap import indoorbuilder_ui
from tools.indoormap.indoorkit import KitComponent, KitComponentHook, Kit, KitDoor
from tools.indoormap.indoormap import IndoorMap, IndoorMapRoom


class IndoorMapBuilder(QMainWindow):
    def __init__(self, parent: QWidget, installation: Optional[HTInstallation] = None):
        super().__init__(parent)

        self._installation: HTInstallation = installation
        self._kits: List[Kit] = []
        self._map: IndoorMap = IndoorMap()

        self.ui = indoorbuilder_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self._setupSignals()
        self._setupKits()

        self.ui.mapRenderer.setMap(self._map)

    def _setupSignals(self) -> None:
        self.ui.kitSelect.currentIndexChanged.connect(self.onKitSelected)
        self.ui.componentList.currentItemChanged.connect(self.onComponentSelected)

        self.ui.mapRenderer.mouseMoved.connect(self.onMouseMoved)
        self.ui.mapRenderer.mousePressed.connect(self.onMousePressed)
        self.ui.mapRenderer.mouseScrolled.connect(self.onMouseScrolled)

    def _setupKits(self) -> None:
        kits_path: str = "C:/Users/hugin/Documents/Apps/HolocronToolset/kits"
        for filename in [filename for filename in os.listdir(kits_path) if filename.endswith(".json")]:
            kit_json = json.loads(BinaryReader.load_file("{}/{}".format(kits_path, filename)))
            kit = Kit(kit_json["name"])
            kit_identifier = kit_json["id"]
            for component_json in kit_json["components"]:
                name = component_json["name"]
                component_identifier = component_json["id"]

                image = QImage("{}/{}/{}.png".format(kits_path, kit_identifier, component_identifier)).mirrored()

                bwm = read_bwm("{}/{}/{}.wok".format(kits_path, kit_identifier, component_identifier))
                mdl = BinaryReader.load_file("{}/{}/{}.mdl".format(kits_path, kit_identifier, component_identifier))
                mdx = BinaryReader.load_file("{}/{}/{}.mdx".format(kits_path, kit_identifier, component_identifier))
                component = KitComponent(name, image, bwm, mdl, mdx)

                for hook_json in component_json["doorhooks"]:
                    position = Vector3(hook_json["x"], hook_json["y"], hook_json["z"])
                    rotation = hook_json["rotation"]
                    door = hook_json["door"]
                    edge = hook_json["edge"]
                    hook = KitComponentHook(position, rotation, edge, door)
                    component.hooks.append(hook)

                kit.components.append(component)
            for door_json in kit_json["doors"]:
                name = door_json["name"]
                width = door_json["width"]
                priority = door_json["priority"]
                door = KitDoor(name, width, priority)
                kit.doors.append(door)
            self._kits.append(kit)

        for kit in self._kits:
            self.ui.kitSelect.addItem(kit.name, kit)

    def selectedComponent(self) -> KitComponent:
        return self.ui.componentList.currentItem().data(QtCore.Qt.UserRole)

    def onKitSelected(self) -> None:
        kit: Kit = self.ui.kitSelect.currentData()

        self.ui.componentList.clear()
        for component in kit.components:
            item = QListWidgetItem(component.name)
            item.setData(QtCore.Qt.UserRole, component)
            self.ui.componentList.addItem(item)

    def onComponentSelected(self, item: QListWidgetItem) -> None:
        component: KitComponent = item.data(QtCore.Qt.UserRole)
        self.ui.componentImage.setPixmap(QPixmap.fromImage(component.image))
        self.ui.mapRenderer.setCursorComponent(component)

    def onMouseMoved(self, screen: Vector2, delta: Vector2, buttons: Set[int], keys: Set[int]) -> None:
        worldDelta = self.ui.mapRenderer.toWorldDelta(delta.x, delta.y)

        if QtCore.Qt.LeftButton in buttons and QtCore.Qt.Key_Control in keys:
            self.ui.mapRenderer.panCamera(-worldDelta.x, -worldDelta.y)
        elif QtCore.Qt.MiddleButton in buttons and QtCore.Qt.Key_Control in keys:
            self.ui.mapRenderer.rotateCamera(delta.x / 50)

    def onMousePressed(self, screen: Vector2, buttons: Set[int], keys: Set[int]) -> None:
        if QtCore.Qt.RightButton in buttons:
            component = self.selectedComponent()
            room = IndoorMapRoom(component, self.ui.mapRenderer._cursorPoint, self.ui.mapRenderer._cursorRotation)
            self._map.rooms.append(room)
            self._map.rebuildRoomConnections()

        if (self.ui.mapRenderer.roomUnderMouse() not in self.ui.mapRenderer.selectedRooms()
                and QtCore.Qt.LeftButton in buttons
                and not QtCore.Qt.Key_Control in keys
                and self.ui.mapRenderer.roomUnderMouse()):
            clearExisting = QtCore.Qt.Key_Shift not in keys
            self.ui.mapRenderer.selectRoom(self.ui.mapRenderer.roomUnderMouse(), clearExisting)

    def onMouseScrolled(self, delta: Vector2, buttons: Set[int], keys: Set[int]) -> None:
        if QtCore.Qt.Key_Control in keys:
            self.ui.mapRenderer.zoomInCamera(delta.y / 50)
        else:
            self.ui.mapRenderer._cursorRotation += math.copysign(15, delta.y)


class IndoorMapRenderer(QWidget):
    mouseMoved = QtCore.pyqtSignal(object, object, object, object)  # screen coords, screen delta, mouse, keys
    """Signal emitted when mouse is moved over the widget."""

    mouseScrolled = QtCore.pyqtSignal(object, object, object)  # screen delta, mouse, keys
    """Signal emitted when mouse is scrolled over the widget."""

    mouseReleased = QtCore.pyqtSignal(object, object, object)  # screen coords, mouse, keys
    """Signal emitted when a mouse button is released after being pressed on the widget."""

    mousePressed = QtCore.pyqtSignal(object, object, object)  # screen coords, mouse, keys
    """Signal emitted when a mouse button is pressed on the widget."""

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self._map: IndoorMap = IndoorMap()
        self._underMouseRoom: Optional[IndoorMapRoom] = None
        self._selectedRooms: List[IndoorMapRoom] = []

        self._camPosition: Vector2 = Vector2.from_null()
        self._camRotation: float = 0.0
        self._camScale = 1.0
        self._cursorComponent: Optional[KitComponent] = None
        self._cursorPoint: Vector3 = Vector3.from_null()
        self._cursorRotation: float = 0.0

        self._keysDown: Set[int] = set()
        self._mouseDown: Set[int] = set()
        self._mousePrev: Vector2 = Vector2.from_null()

        self.hideMagnets: bool = False
        self.highlightRoomsHover: bool = False

        self._loop()

    def _loop(self) -> None:
        """
        The render loop.
        """
        self.repaint()
        QTimer.singleShot(33, self._loop)

    def setMap(self, indoorMap: IndoorMap) -> None:
        self._map = indoorMap

    def setCursorComponent(self, component: KitComponent) -> None:
        self._cursorComponent = component

    def selectRoom(self, room: IndoorMapRoom, clearExisting: bool) -> None:
        if clearExisting:
            self._selectedRooms.clear()
        self._selectedRooms.append(room)

    def roomUnderMouse(self) -> None:
        return self._underMouseRoom

    def selectedRooms(self) -> List[IndoorMapRoom]:
        return self._selectedRooms

    def toRenderCoords(self, x, y) -> Vector2:
        """
        Returns a screen-space coordinates coverted from the specified world-space coordinates. The origin of the
        screen-space coordinates is the top-left of the WalkmeshRenderer widget.

        Args:
            x: The world-space X value.
            y: The world-space Y value.

        Returns:
            A vector representing a point on the widget.
        """
        cos = math.cos(self._camRotation)
        sin = math.sin(self._camRotation)
        x -= self._camPosition.x
        y -= self._camPosition.y
        x2 = (x*cos - y*sin) * self._camScale + self.width() / 2
        y2 = (x*sin + y*cos) * self._camScale + self.height() / 2
        return Vector2(x2, y2)

    def toWorldCoords(self, x, y) -> Vector3:
        """
        Returns the world-space coordinates converted from the specified screen-space coordinates. The Z component
        is calculated using the X/Y components and the walkmesh face the mouse is over. If there is no face underneath
        the mouse, the Z component is set to zero.

        Args:
            x: The screen-space X value.
            y: The screen-space Y value.

        Returns:
            A vector representing a point in the world.
        """
        cos = math.cos(-self._camRotation)
        sin = math.sin(-self._camRotation)
        x = (x - self.width() / 2) / self._camScale
        y = (y - self.height() / 2) / self._camScale
        x2 = x*cos - y*sin + self._camPosition.x
        y2 = x*sin + y*cos + self._camPosition.y
        return Vector3(x2, y2, 0)

    def toWorldDelta(self, x, y) -> Vector2:
        """
        Returns the coordinates representing a change in world-space. This is convereted from coordinates representing
        a change in screen-space, such as the delta paramater given in a mouseMove event.

        Args:
            x: The screen-space X value.
            y: The screen-space Y value.

        Returns:
            A vector representing a change in position in the world.
        """
        cos = math.cos(-self._camRotation)
        sin = math.sin(-self._camRotation)
        x = x / self._camScale
        y = y / self._camScale
        x2 = x*cos - y*sin
        y2 = x*sin + y*cos
        return Vector2(x2, y2)

    def getConnectedHooks(self, room1: IndoorMapRoom, room2: IndoorMapRoom) -> Tuple:
        hook1 = None
        hook2 = None

        for hook in room1.component.hooks:
            hookPos = room1.hookPosition(hook)
            for otherHook in room2.component.hooks:
                otherHookPos = room2.hookPosition(otherHook)
                if hookPos.distance(otherHookPos) < 1:
                    hook1 = hook
                    hook2 = otherHook

        return hook1, hook2

    # region Camera Transformations
    def cameraZoom(self) -> float:
        """
        Returns the current zoom value of the camera.

        Returns:
            The camera zoom value.
        """
        return self._camScale

    def setCameraZoom(self, zoom: float) -> None:
        """
        Sets the camera zoom to the specified value. Values smaller than 1.0 are clamped.

        Args:
            zoom: Zoom-in value.
        """
        self._camScale = max(zoom, 1.0)

    def zoomInCamera(self, zoom: float) -> None:
        """
        Changes the camera zoom value by the specified amount.

        This method is a wrapper for setCameraZoom().

        Args:
            zoom: The value to increase by.
        """
        self.setCameraZoom(self._camScale + zoom)

    def cameraPosition(self) -> Vector2:
        """
        Returns the position of the camera.

        Returns:
            The camera position vector.
        """
        return copy(self._camPosition)

    def setCameraPosition(self, x: float, y: float) -> None:
        """
        Sets the camera position to the specified values.

        Args:
            x: The new X value.
            y: The new Y value.
        """
        self._camPosition.x = x
        self._camPosition.y = y

    def panCamera(self, x: float, y: float) -> None:
        """
        Moves the camera by the specified amount. The movement takes into account both the rotation and zoom of the
        camera.

        Args:
            x: Units to move the x coordinate.
            y: Units to move the y coordinate.
        """
        self._camPosition.x += x
        self._camPosition.y += y

    def cameraRotation(self) -> float:
        """
        Returns the current angle of the camera in radians.

        Returns:
            The camera angle in radians.
        """
        return self._camRotation

    def setCameraRotation(self, radians: float) -> None:
        """
        Sets the camera rotation to the specified angle.

        Args:
            radians: The new camera angle.
        """
        self._camRotation = radians

    def rotateCamera(self, radians: float) -> None:
        """
        Rotates the camera by the angle specified.

        Args:
            radians: The angle of rotation to apply to the camera.
        """
        self._camRotation += radians
    # endregion

    def _drawImage(self, painter: QPainter, image: QImage, coords: Vector2, rotation: float) -> None:
        original = painter.transform()

        trueWidth, trueHeight = image.width(), image.height()
        width, height = image.width() / 10, image.height() / 10

        transform = QTransform()
        transform.translate(self.width() / 2, self.height() / 2)
        transform.rotate(math.degrees(self._camRotation))
        transform.scale(self._camScale, self._camScale)
        transform.translate(-self._camPosition.x, -self._camPosition.y)

        transform.translate(coords.x, coords.y)
        transform.rotate(rotation)
        transform.translate(-width / 2, -height / 2)

        painter.setTransform(transform)

        source = QRectF(0, 0, trueWidth, trueHeight)
        rect = QRectF(0, 0, width, height)
        painter.drawImage(rect, image, source)

        painter.setTransform(original)

    def _drawRoomHighlight(self, painter: QPainter, room: IndoorMapRoom, alpha: int) -> None:
        width, height = room.component.image.width() / 10, room.component.image.height() / 10
        painter.setBrush(QColor(255, 255, 255, alpha))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(room.position.x - width / 2, room.position.y - height / 2, width, height)

    def _drawCircle(self, painter: QPainter, coords: Vector2):
        ...

    # region Events
    def paintEvent(self, e: QPaintEvent) -> None:
        screen = self.mapFromGlobal(self.cursor().pos())
        world = self.toWorldCoords(screen.x(), screen.y())

        transform = QTransform()
        transform.translate(self.width() / 2, self.height() / 2)
        transform.rotate(math.degrees(self._camRotation))
        transform.scale(self._camScale, self._camScale)
        transform.translate(-self._camPosition.x, -self._camPosition.y)

        painter = QPainter(self)
        painter.setBrush(QColor(0))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.setTransform(transform)

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QPainter.LosslessImageRendering, True)

        for room in self._map.rooms:
            self._drawImage(painter, room.component.image, Vector2.from_vector3(room.position), room.rotation)

            for hook in room.component.hooks if not self.hideMagnets else []:
                hookIndex = room.component.hooks.index(hook)
                if room.hooks[hookIndex] is not None:
                    continue

                hookPos = room.hookPosition(hook)
                painter.setBrush(QColor("red"))
                painter.setPen(QtCore.Qt.NoPen)
                painter.drawEllipse(QPointF(hookPos.x, hookPos.y), 0.5, 0.5)

        for room in self._map.rooms:
            for hookIndex, hook in enumerate(room.component.hooks):
                if room.hooks[hookIndex] is not None:
                    hookPos = room.hookPosition(hook)
                    painter.setBrush(QColor("green"))
                    painter.setPen(QtCore.Qt.NoPen)
                    painter.drawEllipse(QPointF(hookPos.x, hookPos.y), 0.5, 0.5)

        if self._cursorComponent:
            painter.setOpacity(0.5)
            self._drawImage(painter, self._cursorComponent.image, Vector2.from_vector3(self._cursorPoint), self._cursorRotation)

        if self._underMouseRoom:
            self._drawRoomHighlight(painter, self._underMouseRoom, 50)

        for room in self._selectedRooms:
            self._drawRoomHighlight(painter, room, 100)

    def wheelEvent(self, e: QWheelEvent) -> None:
        self.mouseScrolled.emit(Vector2(e.angleDelta().x(), e.angleDelta().y()), e.buttons(), self._keysDown)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        coords = Vector2(e.x(), e.y())
        coordsDelta = Vector2(coords.x - self._mousePrev.x, coords.y - self._mousePrev.y)
        self._mousePrev = coords
        self.mouseMoved.emit(coords, coordsDelta, self._mouseDown, self._keysDown)

        world = self.toWorldCoords(coords.x, coords.y)
        self._cursorPoint = world

        if self._cursorComponent:
            fakeCursorRoom = IndoorMapRoom(self._cursorComponent, self._cursorPoint, self._cursorRotation)
            for room in self._map.rooms:
                hook1, hook2 = self.getConnectedHooks(fakeCursorRoom, room)
                if hook1 is not None:
                    self._cursorPoint = room.position - fakeCursorRoom.hookPosition(hook1, False) + room.hookPosition(hook2, False)

        self._underMouseRoom = None
        for room in self._map.rooms:
            walkmesh = room.walkmesh()
            if walkmesh.faceAt(world.x, world.y):
                self._underMouseRoom = room
                break

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self._mouseDown.add(e.button())
        coords = Vector2(e.x(), e.y())
        self.mousePressed.emit(coords, self._mouseDown, self._keysDown)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self._mouseDown.discard(e.button())

        coords = Vector2(e.x(), e.y())
        self.mouseReleased.emit(coords, e.buttons(), self._keysDown)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        self._keysDown.add(e.key())

    def keyReleaseEvent(self, e: QKeyEvent) -> None:
        self._keysDown.discard(e.key())
    # endregion