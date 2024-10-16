from typing import Callable, cast, Tuple

import numpy as np
from pewlib import Laser
from PySide6 import QtCore, QtGui, QtWidgets
import scipy as sp

from datamerger.io.sized_data import SizedData
from .turbo_color_table import turbo_color_table


class DataAlignmentView(QtWidgets.QWidget):
    __laser: Laser | None = None
    __laser_pixmap_item: QtWidgets.QGraphicsPixmapItem | None = None
    __other_data: SizedData | None = None
    __other_data_manipulated: np.ndarray | None = None
    __other_data_pixmap_item: QtWidgets.QGraphicsPixmapItem | None = None

    def __init__(
        self,
        on_aligned_data_changed: Callable[[], None],
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)

        self.__on_aligned_data_changed = on_aligned_data_changed

        rotate_button = QtWidgets.QPushButton("Rotate", self)
        rotate_button.setAutoDefault(False)

        # Lay out toolbar items horizontally.
        toolbar_layout = QtWidgets.QHBoxLayout()
        toolbar_layout.addWidget(rotate_button)
        toolbar_layout.addStretch()

        # Set up the graphics view.
        graphics_view = QtWidgets.QGraphicsView(QtWidgets.QGraphicsScene(self), self)
        graphics_view.setBackgroundBrush(QtCore.Qt.GlobalColor.black)
        graphics_view.setMinimumSize(640, 480)
        graphics_view.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        graphics_view.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.__graphics_view = graphics_view

        # Place the toolbar above the graphics view.
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.__graphics_view)
        layout.setSpacing(0)
        self.setLayout(layout)

    @property
    def aligned_data(self) -> np.ndarray | None:
        if (
            self.__laser is None
            or self.__other_data_manipulated is None
            or self.__other_data_pixmap_item is None
        ):
            return None

        # Select the portion of data that overlaps the elemental data.
        height, width = self.__laser.data.shape
        x, y = cast(
            Tuple[int, int], self.__other_data_pixmap_item.pos().toPoint().toTuple()
        )
        overlap = self.__other_data_manipulated[
            max(0, -y) : max(0, height - y), max(0, -x) : max(0, width - x)
        ]

        # Determine the dtype. This assumes all elements use the same dtype.
        dtype = self.__laser.get(self.__laser.elements[0]).dtype

        # Create an array that has the same dimensions as the elemental data and
        # insert the overlapping portion at the position it's shown in the UI.
        aligned_data = np.zeros(self.__laser.data.shape, dtype)
        aligned_data[
            max(0, y) : max(0, y) + overlap.shape[0],
            max(0, x) : max(0, x) + overlap.shape[1],
        ] = overlap

        return aligned_data

    def clear_data(self) -> None:
        if self.__laser_pixmap_item:
            self.__scene.removeItem(self.__laser_pixmap_item)

        self.__laser = None
        self.__laser_pixmap_item = None

        if self.__other_data_pixmap_item:
            self.__scene.removeItem(self.__other_data_pixmap_item)

        self.__other_data = None
        self.__other_data_manipulated = None
        self.__other_data_pixmap_item = None

    def set_data(self, laser: Laser, other_data: SizedData) -> None:
        self.clear_data()

        # Render the elemental data in a fixed position.
        self.__laser = laser
        elemental_data = laser.get(laser.elements[0])
        elemental_pixmap = make_pixmap_from_data(elemental_data)
        self.__laser_pixmap_item = self.__scene.addPixmap(elemental_pixmap)

        # Prepare the other data in a background thread.
        self.__other_data = other_data
        data_manipulator = DataManipulator(laser, 0, other_data)
        data_manipulator.signals.success.connect(self.__on_data_manipulator_success)
        QtCore.QThreadPool.globalInstance().start(data_manipulator)

        # If QGraphicsView.sceneRect is unset the view shows the area described
        # by QGraphicsScene.sceneRect. If that is unset the scene's rect is
        # equal to the smallest bounding box that contains all items that have
        # been added to the scene since it was created. In that scenario, as we
        # drag items around the scene the scene's rect grows and the view pans
        # to contain it. This behaviour is strange, so here we set the view's
        # scene rect to its initial value, preventing it from panning on drag.
        self.__graphics_view.setSceneRect(self.__scene.sceneRect())

    def wheelEvent(self, event: QtGui.QWheelEvent):
        self.__graphics_view.setTransformationAnchor(
            QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        scale = 2 ** (event.angleDelta().y() / 360.0)
        self.__graphics_view.scale(scale, scale)

    def __on_data_manipulator_success(self, other_data_manipulated: np.ndarray) -> None:
        self.__other_data_manipulated = other_data_manipulated
        self.__other_data_pixmap_item = self.__scene.addPixmap(
            make_pixmap_from_data(other_data_manipulated)
        )
        self.__other_data_pixmap_item.setFlags(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable
        )
        self.__other_data_pixmap_item.setOpacity(0.5)
        self.__on_aligned_data_changed()

    @property
    def __scene(self) -> QtWidgets.QGraphicsScene:
        return self.__graphics_view.scene()


def make_pixmap_from_data(data: np.ndarray) -> QtGui.QPixmap:
    """Makes a pixmap from a two-dimensional array of data.

    Uses the turbo colour table to colour the data.
    """
    assert data.ndim == 2, "Can't make an image from an array that isn't 2D"

    # Determine the minimum and maximum values (ignoring NaNs).
    minimum = np.nanmin(data)
    maximum = np.nanpercentile(data, 99)

    # Convert values to uint8s to be used as indices into the lookup table.
    # If there are any NaNs NumPy will warn that they're invalid and convert
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


class DataManipulator(QtCore.QRunnable):
    """Manipulates data (rotates, zooms, etc.).

    This can be quite computationally intensive, so we do it in another thread.
    """

    class Signals(QtCore.QObject):
        success = QtCore.Signal(np.ndarray)

    def __init__(self, laser: Laser, rotation: int, sized_data: SizedData) -> None:
        """Initialise the instance.

        :param laser: The laser data to align with.
        :param rotation: The amount to rotate the data. Each unit corresponds to
            a counter-clockwise rotation of 90 degrees, e.g. 1 is 90, -1 is -90.
        :param sized_data: The data to align with the laser data. The rotation
            applies to this data.
        """
        super().__init__()

        self.__laser = laser
        self.__rotation = rotation
        self.signals = self.Signals()
        self.__sized_data = sized_data

    def run(self) -> None:
        # First, remove NaNs otherwise they spread everywhere when we zoom.
        data = np.nan_to_num(self.__sized_data.data, nan=20)

        # Rotate in increments of 90 degrees.
        data = np.rot90(data, k=self.__rotation)

        # Resample the image so it has the same resolution as the laser data.
        data = sp.ndimage.zoom(
            data,
            self.__sized_data.element_size / self.__laser.config.get_pixel_width(),
        )

        self.signals.success.emit(data)
