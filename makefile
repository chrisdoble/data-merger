SHELL := bash -eu

.PHONY: package
package: type_check
	pyinstaller --noconfirm main.spec

.PHONY: type_check
type_check:
	mypy main.py datamerger

.PHONY: clean
clean:
	rm -fr build dist
