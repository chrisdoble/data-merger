from PySide6 import QtWidgets

from datamerger.widget import PathSelectWidget


class OutputPage(QtWidgets.QWizardPage):
    """The page of the wizard that prompts the user to choose an output path for
    the merged .npz file."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setTitle("Select output")
        self.setSubTitle(
            "Select where you would like the final pew² .npz file to be saved."
            "\n\nNote that if you select the original file it will be overridden."
        )

        self.__path_select_widget = PathSelectWidget(
            "pew² files (*.npz)",
            lambda: self.completeChanged.emit(),
            accept_mode=QtWidgets.QFileDialog.AcceptMode.AcceptSave,
            file_mode=QtWidgets.QFileDialog.FileMode.AnyFile,
        )

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.__path_select_widget)
        self.setLayout(layout)

    def isComplete(self) -> bool:
        return self.__path_select_widget.path != ""
