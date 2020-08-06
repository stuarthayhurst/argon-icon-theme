SHELL=bash
BUILD_DIR=build
ICON_RESOLUTIONS=8 14 16 22 24 32 36 42 48 64 72 96 128 192 256 512

SVG_OBJS = $(wildcard ./argon/icons/*.svg)
PNG_LIST = $(subst .svg,.png,$(SVG_OBJS))
PNG_OBJS = $(subst ./argon/icons,./build/resolution/apps,$(PNG_LIST))

.PHONY: build install uninstall clean index refresh

build: $(PNG_OBJS) index
install:
	mkdir -p "/usr/share/icons/Argon"
	cp -r ./build/* /usr/share/icons/Argon/
uninstall:
	rm -rf "/usr/share/icons/Argon"
clean:
	rm -rf $(BUILD_DIR)
$(PNG_OBJS): ./build/resolution/apps/%.png: ./argon/icons/%.svg
	mkdir -p $(BUILD_DIR)
	mkdir -p "./build/scalable/apps"
	for resolution in $(ICON_RESOLUTIONS); do \
	  filename=$@; \
	  inputFile="argon/icons$${filename/build\/resolution\/apps}"; \
	  inputFile="$${inputFile//.png/.svg}"; \
	  outputFile="$${filename//resolution/$$resolution\x$$resolution}"; \
	  echo "$$inputFile -> $$outputFile"; \
	  mkdir -p "./build/"$$resolution"x"$$resolution"/apps"; \
	  inkscape --export-filename=$$outputFile -w $$resolution -h $$resolution $$inputFile > /dev/null 2>&1; \
	  optipng -strip all $$outputFile; \
	done; \
	cp "$$inputFile" "./build/scalable/apps/"
index:
	mkdir -p $(BUILD_DIR)
	cp "./argon/index.theme" $(BUILD_DIR)
	for resolution in $(ICON_RESOLUTIONS) scalable; do \
	    if [[ "$$resolution" != "scalable" ]]; then \
	      resolution="$${resolution}x$${resolution}"; \
	    fi; \
	    sed "s|^Directories=.*|&$$resolution/apps,|" ./build/index.theme > ./build/index.theme.temp; \
	    resolution="$${resolution%%x*}"; \
	    echo "" >> ./build/index.theme.temp; \
	    fileContent="$$(cat ./argon/directory.template)"; \
	    fileContent="$${fileContent//resolution/$$resolution}"; \
	    fileContent="$${fileContent//Size=/Size=$$resolution}"; \
	    if [[ "$$resolution" != "scalable" ]]; then \
	      fileContent="$${fileContent//Type=/Type=Threshold}"; \
	    else
	      fileContent="$${fileContent//Type=/Type=Scalable}"; \
	    fi; \
	    echo "$$fileContent" >> ./build/index.theme.temp; \
	    mv ./build/index.theme.temp ./build/index.theme; \
	done
	sed 's/,$$//' ./build/index.theme > ./build/index.theme.temp
	mv ./build/index.theme.temp ./build/index.theme
refresh:
	if command -v gtk-update-icon-cache > /dev/null; then \
	  echo "Updating gtk-update-icon-cache"; touch /usr/share/icons/Argon > /dev/null; \
	  gtk-update-icon-cache -f /usr/share/icons/Argon/; \
	fi \
