SHELL = bash
BUILD_DIR = argon
PREFIX_DIR ?= /usr
THEME_DIR := $(PREFIX_DIR)/share/icons/Argon

.PHONY: check install uninstall index refresh

#Check all symlinks are valid
check:
	./scripts/symlink-tool.py "--check-symlinks" "$(BUILD_DIR)"
install: check
	  $(MAKE) uninstall
	  mkdir -p "$(THEME_DIR)"
	  cp -r "./$(BUILD_DIR)/scalable" "./$(BUILD_DIR)/symbolic" "$(THEME_DIR)"
	  ./scripts/symlink-tool.py "--install-symlinks" "$(BUILD_DIR)" "$(THEME_DIR)"
	  $(MAKE) index
	  $(MAKE) refresh
uninstall:
	rm -rf "$(THEME_DIR)"
index:
	./scripts/generate-index.py "$(THEME_DIR)"
#Refresh / generate icon cache
refresh:
	@if command -v gtk-update-icon-cache > /dev/null; then \
	  touch "$(THEME_DIR)" > /dev/null && \
	  gtk-update-icon-cache -f "$(THEME_DIR)"; \
	fi
	@if command -v gtk4-update-icon-cache > /dev/null; then \
	  touch "$(THEME_DIR)" > /dev/null && \
	  gtk4-update-icon-cache -f "$(THEME_DIR)"; \
	fi
