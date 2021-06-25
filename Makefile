SHELL=bash
BUILD_DIR=argon
INSTALL_DIR=/usr/share/icons/Argon
ICON_RESOLUTIONS=8 16 22 24 32 48 64 128 256

SVG_OBJS_ORIG = $(wildcard ./$(BUILD_DIR)/scalable/*/*.svg)
SVG_OBJS = $(SVG_OBJS_ORIG) $(wildcard ./$(BUILD_DIR)/scalable/*/*/*.svg)
PNG_OBJS = $(subst ./$(BUILD_DIR),./$(BUILD_DIR)/resolution,$(subst .svg,.png,$(SVG_OBJS)))
PNG_LIST = $(wildcard ./$(BUILD_DIR)/*/*/*.png*)

.PHONY: build regen install uninstall clean autoclean index refresh

build: autoclean
	#Generate a list of icons to build, then call make with all the icon svgs
	./icon_builder.py "--list" "$(BUILD_DIR)" "$(ICON_RESOLUTIONS)" "$(MAKE)"
regen: clean
	#Clean all built files first, then generate each icon and the index
	$(MAKE) $(PNG_OBJS) index
install:
	if [[ -f "$(BUILD_DIR)/index.theme" ]]; then \
	  make uninstall; \
	  mkdir -p "$(INSTALL_DIR)"; \
	  cp -r "./$(BUILD_DIR)/"* "$(INSTALL_DIR)"; \
	  #Install symlinks; \
	  ./icon_builder.py "--install-symlinks" "$(BUILD_DIR)" "$(ICON_RESOLUTIONS)" "$(INSTALL_DIR)"; \
	  rm -rf "$(INSTALL_DIR)/symlinks"; \
	  make refresh; \
	else \
	  echo "WARNING: $(BUILD_DIR)/index.theme is missing, run 'make index' and try again"; \
	fi
uninstall:
	rm -rf "$(INSTALL_DIR)"
clean:
	#Delete every generated icon and the index
	PNG_LIST="$(PNG_LIST)"
	if [[ -z "$$PNG_LIST" ]]; then \
	  rm -r $(PNG_LIST); \
	  $(MAKE) autoclean; \
	fi
	if [[ -f "$(BUILD_DIR)/index.theme" ]]; then \
	  rm "$(BUILD_DIR)/index.theme"; \
	fi
autoclean:
	#Delete broken symlinks, left over pngs and empty directories
	./autoclean.py "$(BUILD_DIR)"
$(PNG_OBJS): ./$(BUILD_DIR)/resolution/%.png: ./$(BUILD_DIR)/%.svg
	mkdir -p "$(BUILD_DIR)"
	./icon_builder.py "--generate" "$(BUILD_DIR)" "$(ICON_RESOLUTIONS)" "$@"
index:
	./generate-index.py "--index" "$(BUILD_DIR)" "$(ICON_RESOLUTIONS)"
refresh:
	#Refresh icon cache
	if command -v gtk-update-icon-cache > /dev/null; then \
	  echo "Updating gtk-update-icon-cache"; touch "$(INSTALL_DIR)" > /dev/null; \
	  gtk-update-icon-cache -f "$(INSTALL_DIR)"; \
	fi
