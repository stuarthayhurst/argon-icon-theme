SHELL = bash
BUILD_DIR = argon
INSTALL_DIR ?= /usr/share/icons/Argon

.PHONY: build regen check install uninstall reset clean prune index refresh

#Generate a list of icons to build, then call make with all the icon svgs
build: clean
	./scripts/generate-icons.py "$(BUILD_DIR)"
	$(MAKE) check index
#Clean all built files first, then generate each icon and the index
regen: reset
	$(MAKE) build
#Check all symlinks are valid
check:
	./scripts/symlink-tool.py "--check-symlinks" "$(BUILD_DIR)"
install: check
	@if [[ -f "$(BUILD_DIR)/index.theme" ]]; then \
	  $(MAKE) uninstall && \
	  mkdir -p "$(INSTALL_DIR)" && \
	  cp -r "./$(BUILD_DIR)/"* "$(INSTALL_DIR)" && \
	  ./scripts/symlink-tool.py "--install-symlinks" "$(BUILD_DIR)" "$(INSTALL_DIR)" && \
	  rm -rf "$(INSTALL_DIR)/symlinks" && \
	  $(MAKE) refresh; \
	else \
	  echo "WARNING: $(BUILD_DIR)/index.theme is missing, run 'make index' and try again"; \
	fi
uninstall:
	rm -rf "$(INSTALL_DIR)"
#Delete every generated icon and the index
reset:
	cd "$(BUILD_DIR)" && \
	find -type f -iname '*.png' -delete -print
	$(MAKE) clean
	@if [[ -f "$(BUILD_DIR)/index.theme" ]]; then \
	  rm "$(BUILD_DIR)/index.theme"; \
	fi
#Delete broken symlinks, left over pngs and empty directories
clean: prune
	@./scripts/clean-dirs.py "$(BUILD_DIR)"
#Clean up svgs
prune:
	@./scripts/clean-svgs.py
index:
	./scripts/generate-index.py "$(BUILD_DIR)"
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
