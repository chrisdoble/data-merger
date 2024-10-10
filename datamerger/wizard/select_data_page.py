from PySide6 import QtWidgets

from datamerger.widget import PathSelectWidget

ELEMENTAL_PATH_FIELD_NAME = "elemental_path"
PROFILOMETER_PATH_FIELD_NAME = "profilometer_path"
BRILLOUIN_PATH_FIELD_NAME = "brillouin_path"


class SelectDataPage(QtWidgets.QWizardPage):
    """The first page of the wizard that prompts the user to select the
    elemental, profilometer, and/or Brillouin data to use."""

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self.setCommitPage(True)
        self.setTitle("Select data")
        self.setSubTitle(
            "This program adds profilometer and/or Brillouin data to an"
            ' existing pew² .npz file as additional "elements".\n\nFirst,'
            " select the elemental data and at least one other data source."
        )

        # Elemental data
        self.__elemental_path_select_widget = PathSelectWidget("pew² files (*.npz)")
        self.__elemental_path_select_widget.path_changed.connect(self.completeChanged)
        self.registerField(
            f"{ELEMENTAL_PATH_FIELD_NAME}*", self.__elemental_path_select_widget, "path"
        )

        # Profilometer data
        self.__profilometer_path_select_widget = PathSelectWidget(
            "Profilometer files (*.txt)"
        )
        self.__profilometer_path_select_widget.path_changed.connect(
            self.completeChanged
        )
        self.registerField(
            PROFILOMETER_PATH_FIELD_NAME, self.__profilometer_path_select_widget, "path"
        )

        # Brillouin data
        self.__brillouin_path_select_widget = PathSelectWidget(
            "Brillouin files (*.xlsx)"
        )
        self.__brillouin_path_select_widget.path_changed.connect(self.completeChanged)
        self.registerField(
            BRILLOUIN_PATH_FIELD_NAME, self.__brillouin_path_select_widget, "path"
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
        return self.__elemental_path_select_widget.get_path() != "" and (
            self.__profilometer_path_select_widget.get_path() != ""
            or self.__brillouin_path_select_widget.get_path() != ""
        )
