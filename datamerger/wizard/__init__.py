from PySide6 import QtWidgets

from .align_brillouin_data_page import AlignBrillouinDataPage
from .align_profilometer_data_page import AlignProfilometerDataPage
from datamerger import config
from .done_page import DonePage
from .load_data_page import LoadDataPage
from .output_page import OutputPage
from .select_data_page import (
    BRILLOUIN_PATH_FIELD_NAME,
    PROFILOMETER_PATH_FIELD_NAME,
    SelectDataPage,
)


class Wizard(QtWidgets.QWizard):
    # Page IDs
    __select_data_page_id = 0
    __load_data_page_id = 1
    __align_profilometer_data_page_id = 2
    __align_brillouin_data_page_id = 3
    __output_page_id = 4
    __done_page_id = 5

    # The previous page ID. Used to detect if we're moving back to the load data
    # page, in which case we should continue back to the select data page.
    __previous_page_id = __select_data_page_id

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.currentIdChanged.connect(self.__on_current_id_changed)

        self.setPage(self.__select_data_page_id, SelectDataPage())
        self.setPage(self.__load_data_page_id, LoadDataPage())
        self.setPage(
            self.__align_profilometer_data_page_id, AlignProfilometerDataPage()
        )
        self.setPage(self.__align_brillouin_data_page_id, AlignBrillouinDataPage())
        self.setPage(self.__output_page_id, OutputPage())
        self.setPage(self.__done_page_id, DonePage())

        self.setButtonText(QtWidgets.QWizard.WizardButton.BackButton, "Back")
        self.setButtonText(QtWidgets.QWizard.WizardButton.CommitButton, "Next")
        self.setButtonText(QtWidgets.QWizard.WizardButton.NextButton, "Next")
        self.setOptions(
            QtWidgets.QWizard.WizardOption.NoBackButtonOnLastPage
            | QtWidgets.QWizard.WizardOption.NoCancelButton
        )
        self.setWindowTitle(config.PROGRAM_NAME)

    def nextId(self) -> int:
        page_ids = [
            i
            for i in [
                self.__select_data_page_id,
                self.__load_data_page_id,
                (
                    self.__align_profilometer_data_page_id
                    if self.field(PROFILOMETER_PATH_FIELD_NAME) != ""
                    else None
                ),
                (
                    self.__align_brillouin_data_page_id
                    if self.field(BRILLOUIN_PATH_FIELD_NAME) != ""
                    else None
                ),
                self.__output_page_id,
                self.__done_page_id,
                -1,
            ]
            if i is not None
        ]

        current_page_index = page_ids.index(self.currentId())
        return page_ids[current_page_index + 1]

    # If the user clicks back from the first align data page we want to go to
    # the select data page, not the load data page. This method detects the case
    # where we've moved backwards to the load data page and calls back again to
    # implement the desired behaviour.
    def __on_current_id_changed(self, new_id: int) -> None:
        # `__previous_page_id` must be set before calling `back`, otherwise it
        # becomes invalid and the user is stuck on the select data page.
        previous_page_id = self.__previous_page_id
        self.__previous_page_id = new_id

        if (
            new_id == self.__load_data_page_id
            and previous_page_id != self.__select_data_page_id
        ):
            self.back()
