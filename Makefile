SHELL = bash
BUILD_DIR = argon
INSTALL_DIR ?= /usr/share/icons/Argon

.PHONY: check install uninstall index refresh

#Check all symlinks are valid
check:
	./scripts/symlink-tool.py "--check-symlinks" "$(BUILD_DIR)"
install: check
	  $(MAKE) uninstall
	  mkdir -p "$(INSTALL_DIR)"
	  cp -r "./$(BUILD_DIR)/"* "$(INSTALL_DIR)"
	  ./scripts/symlink-tool.py "--install-symlinks" "$(BUILD_DIR)" "$(INSTALL_DIR)"
	  rm -rf "$(INSTALL_DIR)/symlinks"
	  $(MAKE) index refresh
uninstall:
	rm -rf "$(INSTALL_DIR)"
index:
	./scripts/generate-index.py "$(INSTALL_DIR)"
#Refresh / generate icon cache
refresh:
	@if command -v gtk-update-icon-cache > /dev/null; then \
	  touch "$(INSTALL_DIR)" > /dev/null && \
	  gtk-update-icon-cache -f "$(INSTALL_DIR)"; \
	fi
	@if command -v gtk4-update-icon-cache > /dev/null; then \
	  touch "$(INSTALL_DIR)" > /dev/null && \
	  gtk4-update-icon-cache -f "$(INSTALL_DIR)"; \
	fi
