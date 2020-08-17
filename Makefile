SHELL=bash
BUILD_DIR=build
ICON_RESOLUTIONS=8 14 16 22 24 32 36 42 48 64 72 96 128 192 256 512

SVG_OBJS = $(wildcard ./argon/*/*.svg)
PNG_LIST = $(subst .svg,.png,$(SVG_OBJS))
PNG_OBJS = $(subst ./argon,./build/resolution,$(PNG_LIST))

.PHONY: build install uninstall clean index refresh test

test:
	#$(SVG_OBJS)
	#$(PNG_OBJS)
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
