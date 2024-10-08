import logging

from pewlib.io.npz import load
from PySide6 import QtWidgets

from datamerger import config
from datamerger.util import show_critical_message_box
from datamerger.widget import PathSelectWidget

logger = logging.getLogger(__name__)


class ElementalDataPage(QtWidgets.QWizardPage):
    """The first page of the wizard that collects information about the
    elemental data to use throughout the rest of the wizard.

    This data is in the form of a pew² .npz file.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self.setTitle("Elemental data")
        self.setSubTitle(
            "This program adds Brillouin and/or profilometer data to an"
            ' existing pew² .npz file as additional "elements".\n\nFirst,'
            " select the pew² .npz file you wish to add to."
        )

        self.__path_select_widget = PathSelectWidget("pew² files (*.npz)")
        self.__path_select_widget.path_changed.connect(self.completeChanged)
        self.registerField("npz_path*", self.__path_select_widget, "path")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.__path_select_widget)
        self.setLayout(layout)

    def validatePage(self) -> bool:
        try:
            load(self.__path_select_widget.path)
            return True
        except:
            logger.exception("Unable to load elemental .npz file")
            show_critical_message_box(
                self, "Unable to load pew² .npz file. Check log for more information."
            )
            return False
