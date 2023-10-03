.PHONY: clean build install

clean:
	sudo rm -rf $(CURDIR)/build
	sudo rm -rf $(CURDIR)/dist
	sudo rm -rf $(CURDIR)/lattejuice.spec

remove:
	sudo rm -rf /usr/bin/lattejuice

build:
	pyinstaller --onefile lattejuice.py

	upx --best --lzma $(CURDIR)/dist/lattejuice

install: clean build
	sudo cp -r $(CURDIR)/dist/lattejuice /usr/bin

	sudo chmod +x /usr/bin/lattejuice