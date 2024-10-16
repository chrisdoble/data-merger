import numpy as np
from PySide6 import QtWidgets

from datamerger.widget import DataAlignmentView
from . import wizard_page as wp


class AlignProfilometerDataPage(wp.WizardPage):
    """The page of the wizard that provides controls for the user to align
    profilometer data with elemental data.

    This page isn't shown if the user doesn't select profilometer data.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.__data_alignment_view = DataAlignmentView(
            lambda: self.completeChanged.emit(), self
        )

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.__data_alignment_view)

        self.setLayout(layout)
        self.setSubTitle("Align the profilometer data with the elemental data.")
        self.setTitle("Align profilometer data")

    def initializePage(self) -> None:
        elemental_data = self.get_wizard().elemental_data
        profilometer_data = self.get_wizard().profilometer_data
        assert elemental_data is not None and profilometer_data is not None
        self.__data_alignment_view.set_data(elemental_data, profilometer_data)

    def cleanupPage(self) -> None:
        self.__data_alignment_view.clear_data()

    def isComplete(self) -> bool:
        return self.__data_alignment_view.aligned_data is not None

    @property
    def aligned_data(self) -> np.ndarray | None:
        return self.__data_alignment_view.aligned_data
