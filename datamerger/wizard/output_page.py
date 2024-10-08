from PySide6 import QtWidgets

from datamerger.widget import PathSelectWidget


class OutputPage(QtWidgets.QWizardPage):
    """The fourth page of the wizard that collects information about where to
    output the final .npz file."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setTitle("Output")
        self.setSubTitle(
            "Select the output path where you would like the final pew² .npz "
            "file to be emitted.\n\nNote that if you select the original file "
            "it will be overridden."
        )

        self.__path_select_widget = PathSelectWidget(
            "pew² files (*.npz)",
            accept_mode=QtWidgets.QFileDialog.AcceptMode.AcceptSave,
            file_mode=QtWidgets.QFileDialog.FileMode.AnyFile,
        )
        self.__path_select_widget.path_changed.connect(self.completeChanged)
        self.registerField("output_path*", self.__path_select_widget, "path")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.__path_select_widget)
        self.setLayout(layout)
