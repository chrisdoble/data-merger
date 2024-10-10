from PySide6 import QtWidgets

from .brillouin_data_page import BrillouinDataPage
from datamerger import config
from .done_page import DonePage
from .load_data_page import LoadDataPage
from .output_page import OutputPage
from .profilometer_data_page import ProfilometerDataPage
from .select_data_page import SelectDataPage


class Wizard(QtWidgets.QWizard):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.addPage(SelectDataPage())
        self.addPage(LoadDataPage())
        self.addPage(ProfilometerDataPage())
        self.addPage(BrillouinDataPage())
        self.addPage(OutputPage())
        self.addPage(DonePage())

        self.setButtonText(QtWidgets.QWizard.WizardButton.BackButton, "Back")
        self.setButtonText(QtWidgets.QWizard.WizardButton.CommitButton, "Next")
        self.setButtonText(QtWidgets.QWizard.WizardButton.NextButton, "Next")
        self.setOptions(
            QtWidgets.QWizard.WizardOption.NoBackButtonOnLastPage
            | QtWidgets.QWizard.WizardOption.NoCancelButton
        )
        self.setWindowTitle(config.PROGRAM_NAME)
