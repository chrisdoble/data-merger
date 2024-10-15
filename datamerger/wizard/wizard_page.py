from __future__ import annotations

from PySide6 import QtWidgets

from . import wizard as w


class WizardPage(QtWidgets.QWizardPage):
    """The common wizard page base class.

    This class exists to give all wizard pages a get_wizard method that returns
    the wizard instance with the correct type. See ARCHITECTURE.md for an
    explanation as to why this is necessary.
    """

    def get_wizard(self) -> w.Wizard:
        wizard = self.wizard()
        assert isinstance(wizard, w.Wizard)
        return wizard
