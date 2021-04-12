SHELL=bash
BUILD_DIR=argon
ICON_RESOLUTIONS=8 16 22 24 32 48 64 128 256

SVG_OBJS_ORIG = $(wildcard ./$(BUILD_DIR)/scalable/*/*.svg)
SVG_OBJS = $(SVG_OBJS_ORIG) $(wildcard ./$(BUILD_DIR)/scalable/*/*/*.svg)
PNG_OBJS = $(subst ./$(BUILD_DIR),./$(BUILD_DIR)/resolution,$(subst .svg,.png,$(SVG_OBJS)))
PNG_LIST = $(wildcard ./$(BUILD_DIR)/*/*/*.png*)

.PHONY: build regen install uninstall clean autoclean index refresh

build: autoclean
	#Generate a list of icons to build, then call make with all the icon svgs
	./make-helper.sh -g "$(ICON_RESOLUTIONS)" "$(BUILD_DIR)" "$(MAKE)"
regen: clean
	#Clean all built file first, then generate each icon and the index
	$(MAKE) $(PNG_OBJS) index
install:
	if [[ -f "$(BUILD_DIR)/index.theme" ]]; then \
	  make uninstall; \
	  mkdir -p "/usr/share/icons/Argon"; \
	  cp -r "./$(BUILD_DIR)/"* /usr/share/icons/Argon/; \
	  make refresh; \
	else \
	  echo "WARNING: $(BUILD_DIR)/index.theme is missing, run 'make index' and try again"; \
	fi
uninstall:
	rm -rf "/usr/share/icons/Argon"
clean:
	#Delete every generated icon and the index
	if [[ "$(PNG_LIST)" != "" ]]; then \
	  rm -r "$(PNG_LIST)"; \
	  find "./$(BUILD_DIR)" -type d -empty -delete; \
	fi
	if [[ -f "$(BUILD_DIR)/index.theme" ]]; then \
	  rm "$(BUILD_DIR)/index.theme"; \
	fi
autoclean:
	#Delete broken symlinks, left over pngs and the index
	find "./$(BUILD_DIR)" -type d -empty -delete
	./make-helper.sh -a "$(BUILD_DIR)"
	if [[ -f "$(BUILD_DIR)/index.theme" ]]; then \
	  rm "$(BUILD_DIR)/index.theme"; \
	fi
$(PNG_OBJS): ./$(BUILD_DIR)/resolution/%.png: ./$(BUILD_DIR)/%.svg
	mkdir -p "$(BUILD_DIR)"
	./make-helper.sh "-i" "$@" "$(ICON_RESOLUTIONS)" "$(BUILD_DIR)"
index:
	./generate-index.py "--index" "$(BUILD_DIR)"
refresh:
	#Refresh icon cache
	if command -v gtk-update-icon-cache > /dev/null; then \
	  echo "Updating gtk-update-icon-cache"; touch /usr/share/icons/Argon > /dev/null; \
	  gtk-update-icon-cache -f /usr/share/icons/Argon/; \
	fi
