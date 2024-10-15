from PySide6 import QtWidgets

from datamerger.widget import DataAlignmentView
from .load_data_page import LASER_FIELD_NAME, PROFILOMETER_DATA_FIELD_NAME


class AlignProfilometerDataPage(QtWidgets.QWizardPage):
    """The page of the wizard that provides controls for the user to align
    profilometer data with elemental data.

    This page isn't shown if the user doesn't select profilometer data.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.__data_alignment_view = DataAlignmentView(self)

        self.__layout = QtWidgets.QVBoxLayout()
        self.__layout.addWidget(self.__data_alignment_view)
        self.setLayout(self.__layout)

        self.setTitle("Align profilometer data")
        self.setSubTitle("Align the profilometer data with the elemental data.")

    def initializePage(self) -> None:
        laser = self.field(LASER_FIELD_NAME)
        profilometer_data = self.field(PROFILOMETER_DATA_FIELD_NAME)
        self.__data_alignment_view.set_data(laser, profilometer_data)

    def cleanupPage(self) -> None:
        self.__data_alignment_view.clear_data()
