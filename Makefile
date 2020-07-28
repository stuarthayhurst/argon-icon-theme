SHELL=bash
BUILD_DIR=build
ICON_RESOLUTIONS=8 14 16 22 24 32 36 42 48 64 72 96 128 192 256 512

.PHONY: build install uninstall clean icons index refresh

build:
	make icons
	make index
install:
	mkdir -p "/usr/share/icons/argon"
	cp -r ./build/* /usr/share/icons/argon/
uninstall:
	rm -rf "/usr/share/icons/argon"
clean:
	rm -rf $(BUILD_DIR)
icons:
	mkdir -p $(BUILD_DIR)
	for resolution in $(ICON_RESOLUTIONS); do \
	  mkdir -p "./build/"$$resolution"x"$$resolution; \
	  mkdir -p "./build/"$$resolution"x"$$resolution"/apps"; \
	  for filename in ./argon/icons/*.svg; do \
	    inkscape --export-filename=$${filename//.svg/.png} -w $$resolution -h $$resolution $$filename > /dev/null 2>&1; \
	    mv $${filename//.svg/.png} "./build/"$$resolution"x"$$resolution"/apps"; \
	  done; \
	done
	mkdir -p "./build/scalable"
	mkdir -p "./build/scalable/apps"
	cp "./argon/icons/"* "./build/scalable/apps"
	for resolution in $(ICON_RESOLUTIONS); do \
	  for filename in "./build/"$$resolution"x"$$resolution"/apps/*.png"; do \
	    optipng -o7 -strip all $$filename; \
	  done; \
	done
index:
	mkdir -p $(BUILD_DIR)
	cp "./argon/index.theme" $(BUILD_DIR)
	for dirname in $$(ls build| sort -n); do \
	  if [[ ! "$$dirname" =~ "index" ]]; then \
	    resolution="$${dirname//'build/'}"; \
	    sed "s|^Directories=.*|&$$resolution/apps,|" ./build/index.theme > ./build/index.theme.temp; \
	    echo "" >> ./build/index.theme.temp; \
	    fileContent="$$(cat ./argon/directory.template)"; \
	    fileContent="$${fileContent//resolution/$$resolution}"; \
	    fileContent="$${fileContent//Size=/Size=$$resolution}"; \
	    fileContent="$${fileContent//Type=/Type=Threshold}"; \
	    echo "$$fileContent" >> ./build/index.theme.temp; \
	    mv ./build/index.theme.temp ./build/index.theme; \
	  fi; \
	done
	sed 's/,$$//' ./build/index.theme > ./build/index.theme.temp
	mv ./build/index.theme.temp ./build/index.theme
refresh:
	if command -v gtk-update-icon-cache > /dev/null; then \
	  echo "Updating gtk-update-icon-cache"; touch /usr/share/icons/argon > /dev/null; \
	  gtk-update-icon-cache -f /usr/share/icons/argon/; \
	fi \
