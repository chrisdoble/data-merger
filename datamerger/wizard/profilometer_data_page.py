import logging

from PySide6 import QtWidgets

from datamerger import config
from datamerger.io.profilometer import load
from datamerger.util import show_critical_message_box, show_information_message_box
from datamerger.widget import PathSelectWidget

logger = logging.getLogger(__name__)


class ProfilometerDataPage(QtWidgets.QWizardPage):
    """The third page of the wizard that collects information about the
    profilometer data to use throughout the rest of the wizard (if any).

    This data is in the form of a .txt file.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setTitle("Profilometer data")
        self.setSubTitle("Select a profilometer .txt file or click next to skip.")

        self.__path_select_widget = PathSelectWidget("Profilometer files (*.txt)")
        self.registerField("profilometer_path", self.__path_select_widget, "path")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.__path_select_widget)
        self.setLayout(layout)

    def cleanupPage(self) -> None:
        self.__path_select_widget.set_path("")

    def validatePage(self) -> bool:
        # Ensure at least one type of data has been selected.
        path = self.field("profilometer_path")
        if self.field("brillouin_path") == "" and path == "":
            show_information_message_box(
                self, "You haven't selected any Brillouin or profilometer data."
            )
            return False

        # Ensure the data is valid.
        if path != "":
            try:
                load(path, 0)
            except:
                logger.exception("Unable to load profilometer .txt file")
                show_critical_message_box(
                    self,
                    "Unable to load profilometer .txt file. Check log for more information.",
                )
                return False

        return True
