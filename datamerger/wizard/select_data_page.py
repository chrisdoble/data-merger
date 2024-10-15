from PySide6 import QtWidgets

from datamerger.widget import PathSelectWidget
from . import wizard_page as wp


class SelectDataPage(wp.WizardPage):
    """The page of the wizard that prompts the user to select the paths to the
    elemental, profilometer, and/or Brillouin data to use.

    Elemental data must be selected and at least one of the profilometer or
    Brillouin data must also be selected (otherwise there's nothing to merge).

    After selecting the data the wizard moves to the load data page. This is
    marked as a commit page so the user can't move back from that page.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self.setCommitPage(True)
        self.setTitle("Select data")
        self.setSubTitle(
            "This program adds profilometer and/or Brillouin data to an"
            ' existing pew² .npz file as additional "elements".\n\nFirst,'
            " select the elemental data and at least one other data source."
        )

        self.__brillouin_path_select_widget = PathSelectWidget(
            "Brillouin files (*.xlsx)",
            lambda: self.completeChanged.emit(),
        )
        self.__elemental_path_select_widget = PathSelectWidget(
            "pew² files (*.npz)",
            lambda: self.completeChanged.emit(),
        )
        self.__profilometer_path_select_widget = PathSelectWidget(
            "Profilometer files (*.txt)",
            lambda: self.completeChanged.emit(),
        )

        layout = QtWidgets.QFormLayout()
        layout.addRow("Elemental data:", self.__elemental_path_select_widget)
        layout.addRow("Profilometer data:", self.__profilometer_path_select_widget)
        layout.addRow("Brillouin data:", self.__brillouin_path_select_widget)
        layout.setFieldGrowthPolicy(
            QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )
        layout.setVerticalSpacing(0)
        self.setLayout(layout)

    def isComplete(self) -> bool:
        return self.elemental_data_path != "" and (
            self.profilometer_data_path != "" or self.brillouin_data_path != ""
        )

    @property
    def brillouin_data_path(self) -> str:
        return self.__brillouin_path_select_widget.path

    @property
    def elemental_data_path(self) -> str:
        return self.__elemental_path_select_widget.path

    @property
    def profilometer_data_path(self) -> str:
        return self.__profilometer_path_select_widget.path
