from PySide6 import QtCore, QtWidgets


class PathSelectWidget(QtWidgets.QWidget):
    """A widget that allows selection of a filesystem path."""

    # The path that has been selected (if any).
    __path: str | None = None

    # Emitted when the path changes, i.e. a file is selected or cleared.
    path_changed = QtCore.Signal(str)

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        # The text box that shows that path.
        self.__line_edit = QtWidgets.QLineEdit()
        self.__line_edit.setPlaceholderText("Path to file...")
        self.__line_edit.textChanged.connect(self.__on_line_edit_text_changed)

        # The button that opens the file dialog.
        self.__button = QtWidgets.QPushButton("Select file")
        self.__button.clicked.connect(self.__on_button_clicked)

        # Place the widgets side by side with the text box expanding.
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.__line_edit, 1)
        layout.addWidget(self.__button)
        self.setLayout(layout)

    @QtCore.Property(str)
    def path(self) -> str | None:
        return self.__path

    @path.setter
    def path(self, new_path: str | None) -> None:
        self.__path = new_path

    @QtCore.Slot()
    def __on_line_edit_text_changed(self, text: str) -> None:
        self.__path = text
        self.path_changed.emit(text)

    @QtCore.Slot()
    def __on_button_clicked(self) -> None:
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("pew² files (*.npz)")
        dialog.exec()

        selected_files = dialog.selectedFiles()
        if len(selected_files) == 1:
            [path] = selected_files
            self.__line_edit.setText(path)
            self.__path = path
            self.path_changed.emit(path)
