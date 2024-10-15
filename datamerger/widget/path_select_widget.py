from typing import Callable

from PySide6 import QtCore, QtGui, QtWidgets


class PathSelectWidget(QtWidgets.QWidget):
    """A widget that allows selection of a filesystem path."""

    def __init__(
        self,
        name_filter: str,
        on_path_changed: Callable[[], None],
        accept_mode: QtWidgets.QFileDialog.AcceptMode = QtWidgets.QFileDialog.AcceptMode.AcceptOpen,
        file_mode: QtWidgets.QFileDialog.FileMode = QtWidgets.QFileDialog.FileMode.AnyFile,
        initial_path: str = "",
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        """Initialises the widget.

        :param name_filter: The filter to apply to files, e.g.
            "CPP files (*.cpp *.h)".
        :param accept_mode: The accept mode for the `QFileDialog`. Used to
            control if it's an "open" or "save" dialog.
        :param file_mode: The file mode for the `QFileDialog`. Used to control
            the kinds of paths that may be selected (existing, new, etc.).
        :param parent: The parent of this widget.
        """
        super().__init__(parent)

        self.__accept_mode = accept_mode
        self.__file_mode = file_mode
        self.__name_filter = name_filter
        self.__on_path_changed = on_path_changed
        self.__path = initial_path

        # The text box that shows that path.
        self.__line_edit = ClickableReadOnlyLineEdit(self.__show_file_dialog, self)
        self.__line_edit.setPlaceholderText("Path to file...")
        self.__line_edit.setText(self.__path)

        # The button that opens the file dialog.
        self.__button = QtWidgets.QPushButton("Select file")
        self.__button.clicked.connect(self.__show_file_dialog)

        # Place the widgets side by side with the text box expanding.
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.__line_edit, 1)
        layout.addWidget(self.__button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    @property
    def path(self) -> str:
        return self.__path

    @QtCore.Slot()
    def __on_line_edit_text_changed(self, text: str) -> None:
        self.__path = text
        self.__on_path_changed()

    @QtCore.Slot()
    def __show_file_dialog(self) -> None:
        dialog = QtWidgets.QFileDialog(self)
        dialog.setAcceptMode(self.__accept_mode)
        dialog.setFileMode(self.__file_mode)
        dialog.setNameFilter(self.__name_filter)

        if dialog.exec() == QtWidgets.QFileDialog.DialogCode.Accepted:
            selected_files = dialog.selectedFiles()
            if len(selected_files) == 1:
                [path] = selected_files
                self.__line_edit.setText(path)
                self.__path = path
                self.__on_path_changed()


class ClickableReadOnlyLineEdit(QtWidgets.QLineEdit):
    def __init__(
        self,
        on_clicked: Callable[[], None],
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.__on_clicked = on_clicked
        self.setReadOnly(True)

    def mousePressEvent(self, _event: QtGui.QMouseEvent) -> None:
        self.__on_clicked()
