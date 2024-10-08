import sys

from PySide6 import QtWidgets

from datamerger import config
from datamerger.wizard import *


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    wizard = QtWidgets.QWizard()
    wizard.addPage(ElementalDataPage())
    wizard.addPage(BrillouinDataPage())
    wizard.addPage(ProfilometerDataPage())
    wizard.setWindowTitle(config.PROGRAM_NAME)
    wizard.show()

    sys.exit(app.exec())
