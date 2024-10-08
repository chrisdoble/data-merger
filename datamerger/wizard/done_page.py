from PySide6 import QtWidgets


class DonePage(QtWidgets.QWizardPage):
    """The final page of the wizard that confirms the file has been output."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setTitle("Done")
        self.setSubTitle("Your file has been saved.")

        self.setLayout(QtWidgets.QVBoxLayout())
