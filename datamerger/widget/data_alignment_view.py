import numpy as np
from pewlib import Laser
from PySide6 import QtCore, QtGui, QtWidgets
import scipy as sp

from datamerger.io.sized_data import SizedData
from .turbo_color_table import turbo_color_table


class DataAlignmentView(QtWidgets.QGraphicsView):
    def __init__(
        self,
        laser: Laser,
        sized_data: SizedData,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(QtWidgets.QGraphicsScene(parent), parent)

        self.setBackgroundBrush(QtCore.Qt.GlobalColor.black)
        self.setMinimumSize(640, 480)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Render the elemental data such that it is in a fixed position.
        elemental_data = laser.get(laser.elements[0])
        elemental_pixmap = make_pixmap_from_data(elemental_data)
        self.scene().addPixmap(elemental_pixmap)

        # Render the other data such that it is moveable and semi-transparent.
        other_data = sp.ndimage.zoom(
            np.rot90(np.nan_to_num(sized_data.data, nan=20), k=-1),
            sized_data.element_size / laser.config.get_pixel_width(),
        )
        other_data_pixmap = make_pixmap_from_data(other_data)
        other_data_pixmap_item = self.scene().addPixmap(other_data_pixmap)
        other_data_pixmap_item.setFlags(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable
        )
        other_data_pixmap_item.setOpacity(0.5)

        # If QGraphicsView.sceneRect is unset the view shows the area described
        # by QGraphicsScene.sceneRect. If that is unset the scene's rect is
        # equal to the smallest bounding box that contains all items that have
        # been added to the scene since it was created. In that scenario, as we
        # drag items around the scene the scene's rect grows and the view pans
        # to contain it. This behaviour is strange, so here we set the view's
        # scene rect to its initial value, preventing it from panning on drag.
        self.setSceneRect(self.scene().sceneRect())

    def wheelEvent(self, event: QtGui.QWheelEvent):
        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        scale = 2 ** (event.angleDelta().y() / 360.0)
        self.scale(scale, scale)


def make_pixmap_from_data(data: np.ndarray) -> QtGui.QPixmap:
    """Makes a pixmap from a two-dimensional array of data.

    Uses the turbo colour table to colour the data.
    """
    assert data.ndim == 2, "Can't make an image from an array that isn't 2D"

    # Determine the minimum and maximum values (ignoring NaNs).
    minimum = np.nanmin(data)
    maximum = np.nanpercentile(data, 99)

    # Convert values to uint8s to be used as indices into the lookup table.
    # If there are any NaNs numpy will warn that they're invalid and convert
    # them to 0s. The context manager suppresses those warnings.
    with np.errstate(invalid="ignore"):
        data = (255 * (data - minimum) / (maximum - minimum)).astype(np.uint8)

    # Create an image from the data.
    image = QtGui.QImage(
        data.data,
        data.shape[1],
        data.shape[0],
        data.strides[0],
        QtGui.QImage.Format.Format_Indexed8,
    )
    image.setColorTable(turbo_color_table)
    image.setColorCount(len(turbo_color_table))

    return QtGui.QPixmap.fromImage(image)
