SHELL=bash
BUILD_DIR=build
ICON_RESOLUTIONS=8 14 16 22 24 32 36 42 48 64 72 96 128 192 256 512

SVG_OBJS_ORIG = $(wildcard ./$(BUILD_DIR)/scalable/*/*.svg)
SVG_OBJS = $(SVG_OBJS_ORIG) $(wildcard ./$(BUILD_DIR)/scalable/*/*/*.svg)
PNG_OBJS = $(subst ./$(BUILD_DIR),./$(BUILD_DIR)/resolution,$(subst .svg,.png,$(SVG_OBJS)))
PNG_LIST = $(wildcard ./$(BUILD_DIR)/*/*/*.png)

.PHONY: build install uninstall clean index refresh

build: $(PNG_OBJS) index
install:
	mkdir -p "/usr/share/icons/Argon"
	cp -r ./build/* /usr/share/icons/Argon/
	make refresh
uninstall:
	rm -rf "/usr/share/icons/Argon"
clean:
	rm -rf $(BUILD_DIR)
$(PNG_OBJS): ./build/resolution/%.png: ./argon/%.svg
	mkdir -p $(BUILD_DIR)
	./make-helper.sh "-i" "$@" "$(ICON_RESOLUTIONS)"
index:
	./make-helper.sh "-t" "$(BUILD_DIR)" "$(ICON_RESOLUTIONS)"
refresh:
	if command -v gtk-update-icon-cache > /dev/null; then \
	  echo "Updating gtk-update-icon-cache"; touch /usr/share/icons/Argon > /dev/null; \
	  gtk-update-icon-cache -f /usr/share/icons/Argon/; \
	fi \
