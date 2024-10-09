from PySide6 import QtCore, QtGui, QtWidgets


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(QtWidgets.QGraphicsScene(-1e5, -1e5, 2e5, 2e5, parent), parent)

        self.setBackgroundBrush(QtCore.Qt.GlobalColor.black)
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        scale = 2 ** (event.angleDelta().y() / 360.0)
        self.scale(scale, scale)
