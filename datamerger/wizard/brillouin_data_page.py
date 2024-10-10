import logging

from PySide6 import QtWidgets

from datamerger.io.brillouin import load
from datamerger.util import show_critical_message_box
from datamerger.widget import PathSelectWidget

logger = logging.getLogger(__name__)


class BrillouinDataPage(QtWidgets.QWizardPage):
    """The third page of the wizard that collects information about the
    Brillouin data to use throughout the rest of the wizard (if any).

    This data is in the form of an .xlsx file.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setTitle("Brillouin data")
        self.setSubTitle("Select a Brillouin .xlsx file or click next to skip.")

        self.__path_select_widget = PathSelectWidget("Brillouin files (*.xlsx)")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.__path_select_widget)
        self.setLayout(layout)

    def cleanupPage(self) -> None:
        self.__path_select_widget.set_path("")

    def validatePage(self) -> bool:
        # Ensure the data is valid.
        path = self.__path_select_widget.get_path()
        if path != "":
            try:
                load(path)
            except:
                logger.exception("Unable to load Brillouin .xlsx file")
                show_critical_message_box(
                    self,
                    "Unable to load Brillouin .xlsx file. Check log for more information.",
                )
                return False

        return True
