from pewlib import Laser
from PySide6 import QtCore, QtGui, QtWidgets

from datamerger.io.sized_data import SizedData


class DataAlignmentView(QtWidgets.QGraphicsView):
    def __init__(
        self,
        laser: Laser,
        sized_data: SizedData,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(QtWidgets.QGraphicsScene(-1e5, -1e5, 2e5, 2e5, parent), parent)

        self.setBackgroundBrush(QtCore.Qt.GlobalColor.black)
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.setMinimumSize(640, 480)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        scale = 2 ** (event.angleDelta().y() / 360.0)
        self.scale(scale, scale)
