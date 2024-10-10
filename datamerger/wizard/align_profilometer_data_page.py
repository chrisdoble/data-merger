import numpy as np
from pewlib.io.npz import load
from PySide6 import QtGui, QtWidgets

from datamerger.widget import DataAlignmentView, turbo_color_table
from .load_data_page import LASER_FIELD_NAME


class AlignProfilometerDataPage(QtWidgets.QWizardPage):
    """The page of the wizard that provides controls for the user to align
    profilometer data with elemental data.

    This page isn't shown if the user doesn't select profilometer data.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setTitle("Align profilometer data")
        self.setSubTitle("Align the profilometer data with the elemental data.")

        self.__data_alignment_view = DataAlignmentView(self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.__data_alignment_view)
        self.setLayout(layout)

    def initializePage(self) -> None:
        laser = self.field(LASER_FIELD_NAME)
        data = laser.get(laser.elements[0])

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

        pixmap = QtGui.QPixmap.fromImage(image)
        pixmap_item = self.__data_alignment_view.scene().addPixmap(pixmap)
        self.__data_alignment_view.centerOn(pixmap_item)
