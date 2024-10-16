import numpy as np
from PySide6 import QtWidgets

from datamerger.widget.data_alignment_view import DataAlignmentView
from . import wizard_page as wp


class AlignBrillouinDataPage(wp.WizardPage):
    """The page of the wizard that provides controls for the user to align
    Brillouin data with elemental data.

    This page isn't shown if the user doesn't select Brillouin data.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.__data_alignment_view = DataAlignmentView(
            lambda: self.completeChanged.emit(), self
        )

        self.__layout = QtWidgets.QVBoxLayout()
        self.__layout.addWidget(self.__data_alignment_view)
        self.setLayout(self.__layout)

        self.setTitle("Align Brillouin data")
        self.setSubTitle("Align the Brillouin data with the elemental data.")

    def initializePage(self) -> None:
        elemental_data = self.get_wizard().elemental_data
        brillouin_data = self.get_wizard().brillouin_data
        assert elemental_data is not None and brillouin_data is not None
        self.__data_alignment_view.set_data(elemental_data, brillouin_data)

    def cleanupPage(self) -> None:
        self.__data_alignment_view.clear_data()

    def isComplete(self) -> bool:
        return self.__data_alignment_view.aligned_data is not None

    @property
    def aligned_data(self) -> np.ndarray | None:
        return self.__data_alignment_view.aligned_data
