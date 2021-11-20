SHELL=bash
BUILD_DIR=argon
INSTALL_DIR=/usr/share/icons/Argon
ICON_RESOLUTIONS=8 16 22 24 32 48 64 128 256

SVG_OBJS = $(wildcard ./$(BUILD_DIR)/scalable/*/*.svg) $(wildcard ./$(BUILD_DIR)/scalable/*/*/*.svg)
PNG_OBJS = $(subst ./$(BUILD_DIR),./$(BUILD_DIR)/resolution,$(subst .svg,.png,$(SVG_OBJS)))
PNG_LIST = $(wildcard ./$(BUILD_DIR)/*/*/*.png*)

.PHONY: build regen check install uninstall clean autoclean prune index refresh

#Generate a list of icons to build, then call make with all the icon svgs
build: autoclean
	./icon_builder.py "--list" "$(BUILD_DIR)" "$(ICON_RESOLUTIONS)" "$(MAKE)"
	$(MAKE) check
#Clean all built files first, then generate each icon and the index
regen: clean
	$(MAKE) $(PNG_OBJS) index
#Check all symlinks are valid
check:
	./icon_builder.py "--check-symlinks" "$(BUILD_DIR)" "$(ICON_RESOLUTIONS)"
install: check
	@if [[ -f "$(BUILD_DIR)/index.theme" ]]; then \
	  $(MAKE) uninstall; \
	  mkdir -p "$(INSTALL_DIR)"; \
	  cp -r "./$(BUILD_DIR)/"* "$(INSTALL_DIR)"; \
	  #Install symlinks; \
	  ./icon_builder.py "--install-symlinks" "$(BUILD_DIR)" "$(ICON_RESOLUTIONS)" "$(INSTALL_DIR)"; \
	  rm -rf "$(INSTALL_DIR)/symlinks"; \
	  $(MAKE) refresh; \
	else \
	  echo "WARNING: $(BUILD_DIR)/index.theme is missing, run 'make index' and try again"; \
	fi
uninstall:
	rm -rf "$(INSTALL_DIR)"
#Delete every generated icon and the index
clean:
	rm -rfv $(PNG_LIST)
	$(MAKE) autoclean
	@if [[ -f "$(BUILD_DIR)/index.theme" ]]; then \
	  rm "$(BUILD_DIR)/index.theme"; \
	fi
#Delete broken symlinks, left over pngs and empty directories
autoclean:
	$(MAKE) prune apply-autoclean
apply-autoclean:
	./autoclean.py "$(BUILD_DIR)"
#Clean up svgs
prune:
	./clean-svgs.py
$(PNG_OBJS): ./$(BUILD_DIR)/resolution/%.png: ./$(BUILD_DIR)/%.svg
	mkdir -p "$(BUILD_DIR)"
	./icon_builder.py "--generate" "$(BUILD_DIR)" "$(ICON_RESOLUTIONS)" "$@"
index:
	./generate-index.py "--index" "$(BUILD_DIR)" "$(ICON_RESOLUTIONS)"
#Refresh / generate icon cache
refresh:
	@if command -v gtk-update-icon-cache > /dev/null; then \
	  echo "Updating gtk-update-icon-cache..."; touch "$(INSTALL_DIR)" > /dev/null; \
	  gtk-update-icon-cache -f "$(INSTALL_DIR)"; \
	fi
