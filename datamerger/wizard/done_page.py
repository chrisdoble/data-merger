from pewlib.io.npz import save
from PySide6 import QtWidgets

from . import wizard_page as wp


class DonePage(wp.WizardPage):
    """The final page of the wizard that confirms the file has been output."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setTitle("Done")
        self.setSubTitle("Your file has been saved.")

        self.setLayout(QtWidgets.QVBoxLayout())

    def initializePage(self) -> None:
        laser = self.get_wizard().elemental_data
        assert laser is not None

        brillouin_data = self.get_wizard().aligned_brillouin_data
        if brillouin_data is not None:
            laser.add("Brillouin", brillouin_data)

        profilometer_data = self.get_wizard().aligned_profilometer_data
        if profilometer_data is not None:
            laser.add("Profilometer", profilometer_data)

        path = self.get_wizard().output_path
        assert path != ""
        save(path, laser)
