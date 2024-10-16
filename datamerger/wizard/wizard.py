import logging
from typing import Type
from types import TracebackType

import numpy as np
from pewlib import Laser
from PySide6 import QtCore, QtWidgets

from datamerger import config
from datamerger.io.sized_data import SizedData
from datamerger.util import show_critical_message_box
from . import (
    align_brillouin_data_page as abdp,
    align_profilometer_data_page as apdp,
    done_page as dp,
    load_data_page as ldp,
    output_page as op,
    select_data_page as sdp,
)

logger = logging.getLogger(__name__)


class Wizard(QtWidgets.QWizard):
    # Page IDs
    __select_data_page_id = 0
    __load_data_page_id = 1
    __align_brillouin_data_page_id = 2
    __align_profilometer_data_page_id = 3
    __output_page_id = 4
    __done_page_id = 5

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        # See __on_current_id_changed for more information.
        self.__previous_page_id = self.__select_data_page_id
        self.currentIdChanged.connect(self.__on_current_id_changed)

        # Add pages.
        self.setPage(self.__select_data_page_id, sdp.SelectDataPage())
        self.setPage(self.__load_data_page_id, ldp.LoadDataPage())
        self.setPage(self.__align_brillouin_data_page_id, abdp.AlignBrillouinDataPage())
        self.setPage(
            self.__align_profilometer_data_page_id, apdp.AlignProfilometerDataPage()
        )
        self.setPage(self.__output_page_id, op.OutputPage())
        self.setPage(self.__done_page_id, dp.DonePage())

        #  Configure the wizard.
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
                    self.__align_brillouin_data_page_id
                    if self.brillouin_data_path != ""
                    else None
                ),
                (
                    self.__align_profilometer_data_page_id
                    if self.profilometer_data_path != ""
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

    def excepthook(
        self,
        type: Type[BaseException],
        value: BaseException,
        traceback: TracebackType | None,
    ) -> None:
        """Handles exceptions that would otherwise be unhandled."""

        logger.exception("Unhandled exception", exc_info=(type, value, traceback))
        show_critical_message_box(
            self, f"An unexpected error occurred:\n\n{type.__name__}: {value}"
        )

    # If the user clicks back from the first align data page we want to go to
    # the select data page, not the load data page. This method detects the case
    # where we've moved backwards to the load data page and calls back again to
    # implement the desired behaviour.
    def __on_current_id_changed(self, new_id: int) -> None:
        # __previous_page_id must be set before calling back, otherwise it
        # becomes invalid and the user is stuck on the select data page.
        previous_page_id = self.__previous_page_id
        self.__previous_page_id = new_id

        if (
            new_id == self.__load_data_page_id
            and previous_page_id != self.__select_data_page_id
        ):
            self.back()

    # SelectDataPage properties
    def __get_select_data_page(self) -> sdp.SelectDataPage:
        page = self.page(self.__select_data_page_id)
        assert isinstance(page, sdp.SelectDataPage)
        return page

    @property
    def brillouin_data_path(self) -> str:
        return self.__get_select_data_page().brillouin_data_path

    @property
    def elemental_data_path(self) -> str:
        return self.__get_select_data_page().elemental_data_path

    @property
    def profilometer_data_path(self) -> str:
        return self.__get_select_data_page().profilometer_data_path

    # LoadDataPage properties
    def __get_load_data_path(self) -> ldp.LoadDataPage:
        page = self.page(self.__load_data_page_id)
        assert isinstance(page, ldp.LoadDataPage)
        return page

    @property
    def brillouin_data(self) -> SizedData | None:
        return self.__get_load_data_path().brillouin_data

    @property
    def elemental_data(self) -> Laser | None:
        return self.__get_load_data_path().elemental_data

    @property
    def profilometer_data(self) -> SizedData | None:
        return self.__get_load_data_path().profilometer_data

    # AlignProfilometerDataPage properties
    def __get_align_profilometer_data_page(self) -> apdp.AlignProfilometerDataPage:
        page = self.page(self.__align_profilometer_data_page_id)
        assert isinstance(page, apdp.AlignProfilometerDataPage)
        return page

    @property
    def aligned_profilometer_data(self) -> np.ndarray | None:
        return self.__get_align_profilometer_data_page().aligned_data

    # AlignBrillouinDataPage properties
    def __get_align_brillouin_data_page(self) -> abdp.AlignBrillouinDataPage:
        page = self.page(self.__align_brillouin_data_page_id)
        assert isinstance(page, abdp.AlignBrillouinDataPage)
        return page

    @property
    def aligned_brillouin_data(self) -> np.ndarray | None:
        return self.__get_align_brillouin_data_page().aligned_data

    # OutputPage properties
    def __get_output_page(self) -> op.OutputPage:
        page = self.page(self.__output_page_id)
        assert isinstance(page, op.OutputPage)
        return page

    @property
    def output_path(self) -> str:
        return self.__get_output_page().path
