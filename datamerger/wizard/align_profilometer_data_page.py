from PySide6 import QtWidgets

from datamerger.widget import DataAlignmentView
from .load_data_page import LASER_FIELD_NAME, PROFILOMETER_DATA_FIELD_NAME


class AlignProfilometerDataPage(QtWidgets.QWizardPage):
    """The page of the wizard that provides controls for the user to align
    profilometer data with elemental data.

    This page isn't shown if the user doesn't select profilometer data.
    """

    __data_alignment_view: DataAlignmentView | None = None
    __layout: QtWidgets.QVBoxLayout

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setTitle("Align profilometer data")
        self.setSubTitle("Align the profilometer data with the elemental data.")

        self.__layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.__layout)

    def initializePage(self) -> None:
        assert self.__data_alignment_view is None
        laser = self.field(LASER_FIELD_NAME)
        profilometer_data = self.field(PROFILOMETER_DATA_FIELD_NAME)
        self.__data_alignment_view = DataAlignmentView(laser, profilometer_data, self)
        self.__layout.addWidget(self.__data_alignment_view)

    def cleanupPage(self) -> None:
        self.__layout.takeAt(0)
        if self.__data_alignment_view is not None:
            self.__data_alignment_view.deleteLater()
            self.__data_alignment_view = None
