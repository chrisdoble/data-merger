from PySide6 import QtWidgets

from datamerger import config


def show_critical_message_box(parent: QtWidgets.QWidget, text: str) -> None:
    """Shows a critical error message in a dismissable message box."""
    __show_message_box(QtWidgets.QMessageBox.Icon.Critical, parent, text)


def __show_message_box(
    icon: QtWidgets.QMessageBox.Icon, parent: QtWidgets.QWidget, text: str
) -> None:
    message_box = QtWidgets.QMessageBox(parent)
    message_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
    message_box.setIcon(icon)
    message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    message_box.setText(text)
    message_box.setWindowTitle(config.PROGRAM_NAME)
    message_box.exec()
