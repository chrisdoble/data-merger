import sys

from PySide6 import QtWidgets

from datamerger.wizard import Wizard


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    wizard = Wizard()
    sys.excepthook = wizard.excepthook
    wizard.show()
    sys.exit(app.exec())
