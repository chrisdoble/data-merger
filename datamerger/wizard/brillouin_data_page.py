from PySide6 import QtWidgets


class BrillouinDataPage(QtWidgets.QWizardPage):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.__label = QtWidgets.QLabel()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.__label)
        self.setLayout(layout)

    def initializePage(self) -> None:
        self.__label.setText(self.field("npz_path"))
