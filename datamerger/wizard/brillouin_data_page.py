from PySide6 import QtWidgets

from datamerger.widget import PathSelectWidget


class BrillouinDataPage(QtWidgets.QWizardPage):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setTitle("Brillouin data")
        self.setSubTitle("Select a Brillouin .xlsx file or click continue to skip.")

        self.__path_select_widget = PathSelectWidget("Brillouin files (*.xlsx)")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.__path_select_widget)
        self.setLayout(layout)

    def cleanupPage(self) -> None:
        self.__path_select_widget.set_path("")
