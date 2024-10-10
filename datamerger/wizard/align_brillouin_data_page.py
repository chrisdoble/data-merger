from PySide6 import QtWidgets


class AlignBrillouinDataPage(QtWidgets.QWizardPage):
    """The page of the wizard that provides controls for the user to align
    Brillouin data with elemental data.

    This page isn't shown if the user doesn't select Brillouin data.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setTitle("Align Brillouin data")
        self.setSubTitle("Align the Brillouin data with the elemental data.")

        self.setLayout(QtWidgets.QVBoxLayout())
