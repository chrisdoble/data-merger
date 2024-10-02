SHELL := bash -eu

.PHONY: package
package: dist/main.app

.PONY: clean
clean:
	rm -fr build dist

dist/main.app: main.py main.spec
	pyinstaller --noconfirm main.spec