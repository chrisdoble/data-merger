from pewlib.io.npz import save
from PySide6 import QtWidgets

from datamerger.util import show_critical_message_box
from . import wizard_page as wp


class DonePage(wp.WizardPage):
    """The final page of the wizard that confirms the file has been output."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.setSubTitle("Your file has been saved.")
        self.setTitle("Done")

    def initializePage(self) -> None:
        try:
            laser = self.get_wizard().elemental_data
            assert laser is not None, "Elemental data is missing"

            brillouin_data = self.get_wizard().aligned_brillouin_data
            if brillouin_data is not None:
                if "Brillouin" in laser.elements:
                    laser.remove("Brillouin")
                laser.add("Brillouin", brillouin_data)

            profilometer_data = self.get_wizard().aligned_profilometer_data
            if profilometer_data is not None:
                if "Profilometer" in laser.elements:
                    laser.remove("Profilometer")
                laser.add("Profilometer", profilometer_data)

            path = self.get_wizard().output_path
            assert path != "", "Output path is missing"
            save(path, laser)
        except BaseException as e:
            self.setTitle("Error")
            self.setSubTitle("An error occurred and your file wasn't saved.")
            raise e
