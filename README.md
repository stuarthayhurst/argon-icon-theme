# argon-icon-theme
  - A minimalistic icon theme to run on top of Yaru, to provide new icons and some tweaks
  - This project contains some assets from [Papirus Icon Theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme)

## Installing:
  - `make index`
  - `sudo make install`
  - Set the icon theme using gnome-tweaks, or `gsettings set org.gnome.desktop.interface icon-theme Argon`

## Building:
  - It's not necessary to rebuild the theme to install, only if modifications have been made
  - `make build` will only generate changed icons (automatically uses multiple cores) - this means it will act like `make regen -jX`, if `make clean` was run immediately before `make build`
  - `make regen -j4` will regenerate all icons, whether they have been changed or not
  - `make clean` will delete all generated icons and index.theme
  - `make autoclean` will delete icons missing a corresponding svg, broken symlinks, index.theme and empty directories
  - `make index` will generate index.theme, done automatically by `build` and `regen`

## Contributing:
  - Create / modify / delete the appropriate .svg file(s)
  - Run `make build` if no icons were deleted
  - If icons were deleted, run `make clean; make regen -j8`
  - Submit a pull request with the changes

## Build Dependencies:
  - coreutils
  - git
  - inkscape
  - make
  - optipng
  - sed

## Themed Icons:
  - Audacity
  - Chromium
  - GNU Image Manipulation Program (GIMP)
  - Gnome Calculator
  - Gnome Tweaks
  - Google Chrome
  - GParted
  - Kernel Notify (Upstreamed, kept for older versions)
  - Minecraft Launcher
  - Nvidia Settings
  - OBS Studio
  - Psensor (Upstreamed, kept for older versions)
  - Remmina
  - Retroarch
  - Steam

## Papirus icons:
  - Htop
  - Inkscape
  - Vim
  - Vlc
  - Winetricks
