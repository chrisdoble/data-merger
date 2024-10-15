This file exists to explain architectural decisions that may be non-obvious.

# Wizard fields and signals

During development I found that using the field and signal systems of PySide6's `QWizardPage` resulted in unpredictable segfaults. For this reason, they're not used (although some use of signals is unavoidable). The alternative is for each wizard page to access data it requires via the wizard itself. The `Wizard` class defines properties for all the relevant data and the `WizardPage` base class provides a type-safe `get_wizard()` method that pages can use to access these properties. Also, where possible, callbacks are favoured over signals.
