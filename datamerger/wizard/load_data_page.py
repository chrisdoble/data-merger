import logging
from typing import Callable

import numpy as np
from pewlib import Laser
from pewlib.io.npz import load as load_npz
from PySide6 import QtCore, QtWidgets

from datamerger.io.brillouin import load as load_brillouin
from datamerger.io.profilometer import load as load_profilometer
from datamerger.io.sized_data import SizedData
from datamerger.util import show_critical_message_box
from .select_data_page import (
    BRILLOUIN_PATH_FIELD_NAME,
    ELEMENTAL_PATH_FIELD_NAME,
    PROFILOMETER_PATH_FIELD_NAME,
)

logger = logging.getLogger(__name__)

LASER_FIELD_NAME = "laser"
PROFILOMETER_DATA_FIELD_NAME = "profilometer_data"
BRILLOUIN_DATA_FIELD_NAME = "brillouin_data"


class LoadDataPage(QtWidgets.QWizardPage):
    """The second page of the wizard that loads the data into memory.

    If the data loads successfully the wizard moves to the next page. If it
    fails to load the wizard shows an error and moves to the previous page.
    """

    # Elemental data loaded from a pew² .npz file.
    __laser: Laser | None = None

    # Profilometer data loaded from a .txt file.
    __profilometer_data: SizedData | None = None

    # Brillouin data loaded from an .xlsx file.
    __brillouin_data: SizedData | None = None

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setTitle("Load data")
        self.setSubTitle("Loading the selected data. This might take a few seconds.")

        # Show an indeterminate progress bar to indicate that something is happening.
        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setMaximum(0)
        progress_bar.setMinimum(0)

        layout = QtWidgets.QVBoxLayout()
        layout.addStretch()
        layout.addWidget(progress_bar)
        layout.addStretch()
        self.setLayout(layout)

        self.registerField(LASER_FIELD_NAME, self, "laser")
        self.registerField(PROFILOMETER_DATA_FIELD_NAME, self, "profilometer_data")
        self.registerField(BRILLOUIN_DATA_FIELD_NAME, self, "brillouin_data")

    def initializePage(self) -> None:
        # Load all the data in serial to make it easier to handle the case where
        # loading one fails. Otherwise we need to cancel parallel jobs, etc.
        self.__load_elemental_data()

    def cleanupPage(self) -> None:
        self.__brillouin_data = None
        self.__laser = None
        self.__profilometer_data = None

    def isComplete(self) -> bool:
        # Disable the next button so the user can't move to the next page.
        return False

    def get_laser(self) -> Laser | None:
        return self.__laser

    laser = QtCore.Property(Laser, get_laser)

    def get_profilometer_data(self) -> SizedData | None:
        return self.__profilometer_data

    profilometer_data = QtCore.Property(SizedData, get_profilometer_data)

    def get_brillouin_data(self) -> SizedData | None:
        return self.__brillouin_data

    brillouin_data = QtCore.Property(SizedData, get_brillouin_data)

    def __load_elemental_data(self) -> None:
        def on_success(laser: Laser):
            self.__laser = laser
            self.__load_profilometer_data()

        load_elemental_data = LoadElementalData(self.field(ELEMENTAL_PATH_FIELD_NAME))
        load_elemental_data.signals.error.connect(
            self.__make_error_handler("elemental")
        )
        load_elemental_data.signals.success.connect(on_success)
        QtCore.QThreadPool.globalInstance().start(load_elemental_data)

    def __load_profilometer_data(self) -> None:
        def on_success(profilometer_data: SizedData | None):
            self.__profilometer_data = profilometer_data
            self.__load_brillouin_data()

        path = self.field(PROFILOMETER_PATH_FIELD_NAME)
        if path == "":
            on_success(None)
            return

        load_profilometer_data = LoadProfilometerData(path)
        load_profilometer_data.signals.error.connect(
            self.__make_error_handler("profilometer")
        )
        load_profilometer_data.signals.success.connect(on_success)
        QtCore.QThreadPool.globalInstance().start(load_profilometer_data)

    def __load_brillouin_data(self) -> None:
        def on_success(brillouin_data: SizedData | None):
            self.__brillouin_data = brillouin_data
            self.wizard().next()

        path = self.field(BRILLOUIN_PATH_FIELD_NAME)
        if path == "":
            on_success(None)
            return

        load_brillouin_data = LoadBrillouinData(path)
        load_brillouin_data.signals.error.connect(
            self.__make_error_handler("Brillouin")
        )
        load_brillouin_data.signals.success.connect(on_success)
        QtCore.QThreadPool.globalInstance().start(load_brillouin_data)

    def __make_error_handler(self, data_type: str) -> Callable[[], None]:
        def on_error():
            self.wizard().back()
            show_critical_message_box(
                self, f"Failed to load {data_type} data. See logs for more details."
            )

        return on_error


class LoadElementalData(QtCore.QRunnable):
    class Signals(QtCore.QObject):
        error = QtCore.Signal()
        success = QtCore.Signal(Laser)

    def __init__(self, path: str) -> None:
        super().__init__()

        self.signals = self.Signals()
        self.__path = path

    def run(self) -> None:
        try:
            self.signals.success.emit(load_npz(self.__path))
        except:
            logging.exception(f"Failed to load elemental data at {self.__path}")
            self.signals.error.emit()


class LoadProfilometerData(QtCore.QRunnable):
    class Signals(QtCore.QObject):
        error = QtCore.Signal()
        success = QtCore.Signal(np.ndarray)

    def __init__(self, path: str) -> None:
        super().__init__()

        self.signals = self.Signals()
        self.__path = path

    def run(self) -> None:
        try:
            self.signals.success.emit(load_profilometer(self.__path))
        except:
            logging.exception(f"Failed to load profilometer data at {self.__path}")
            self.signals.error.emit()


class LoadBrillouinData(QtCore.QRunnable):
    class Signals(QtCore.QObject):
        error = QtCore.Signal()
        success = QtCore.Signal(np.ndarray)

    def __init__(self, path: str) -> None:
        super().__init__()

        self.signals = self.Signals()
        self.__path = path

    def run(self) -> None:
        try:
            self.signals.success.emit(load_brillouin(self.__path))
        except:
            logging.exception(f"Failed to load Brillouin data at {self.__path}")
            self.signals.error.emit()
