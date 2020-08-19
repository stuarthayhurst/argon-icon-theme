# argon-icon-theme
  - A minimalistic icon theme to run on top of Yaru, to provide new icons and some tweaks
  - This project contains some assets from [Papirus Icon Theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme)

## Installing:
  - `make index`
  - `sudo make install`
  - Set the icon theme using gnome-tweaks, or `gsettings set org.gnome.desktop.interface icon-theme Argon`

## Building:
  - It's not necessary to rebuild the theme to install, only if modifications have been made
  - `make build` will only generate changed icons (automatically uses multiple cores)
  - `make regen -j4` will regenerate all icons, whether they have been changed or not
  - `make clean` will delete all generated icons and index.theme
  - `make autoclean` will only delete icons missing a corresponding svg
  - `make index` will generate index.theme, done automatically by `build` and `regen`

## Contributing:
  - Create / modify the appropriate .svg file
  - Run `make build` if the change is minor
  - If many icons were changed, run `make clean; make regen -j8`
  - Submit a pull request with the changes

## Build Dependencies:
  - coreutils
  - git
  - inkscape
  - optipng
  - sed

## Themed Icons:
  - GNU Image Manipulation Program (GIMP)
  - Gnome-tweaks
  - Gparted
  - Minecraft-launcher
  - Psensor (Upstreamed, kept for older versions)
  - Retroarch
  - Steam

## Papirus icons:
  - Htop
  - Inkscape
  - Vim
  - Vlc
  - Winetricks
