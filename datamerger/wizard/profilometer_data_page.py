import logging

import numpy as np
from pewlib.io.npz import load as load_npz
from PySide6 import QtCore, QtGui, QtWidgets

from datamerger import config
from datamerger.io.profilometer import load as load_profilometer
from datamerger.util import show_critical_message_box, show_information_message_box
from datamerger.widget import GraphicsView, PathSelectWidget, turbo_color_table

logger = logging.getLogger(__name__)


class ProfilometerDataPage(QtWidgets.QWizardPage):
    """The second page of the wizard that collects information about the
    profilometer data to use throughout the rest of the wizard (if any).

    This data is in the form of a .txt file.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setTitle("Profilometer data")
        self.setSubTitle("Select a profilometer .txt file or click next to skip.")

        self.__path_select_widget = PathSelectWidget("Profilometer files (*.txt)")

        self.__graphics_view = GraphicsView(self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.__path_select_widget)
        layout.addWidget(self.__graphics_view)
        self.setLayout(layout)

    def initializePage(self) -> None:
        laser = load_npz(self.field("elemental_path"))
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
        pixmap_item = self.__graphics_view.scene().addPixmap(pixmap)
        self.__graphics_view.centerOn(pixmap_item)

    def cleanupPage(self) -> None:
        self.__path_select_widget.set_path("")

    def validatePage(self) -> bool:
        # Ensure at least one type of data has been selected.
        path = self.field("profilometer_path")
        if self.field("brillouin_path") == "" and path == "":
            show_information_message_box(
                self, "You haven't selected any Brillouin or profilometer data."
            )
            return False

        # Ensure the data is valid.
        if path != "":
            try:
                load_profilometer(path, 0)
            except:
                logger.exception("Unable to load profilometer .txt file")
                show_critical_message_box(
                    self,
                    "Unable to load profilometer .txt file. Check log for more information.",
                )
                return False

        return True
