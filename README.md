# argon-icon-theme
  - A minimalistic, material icon theme, designed to run on GNOME with Yaru
  - This project contains some assets from [Papirus Icon Theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme)

## Installing:
  - `make index`, or if modifications have been made: `make build`
  - `sudo make install`
  - Set the icon theme using gnome-tweaks, or `gsettings set org.gnome.desktop.interface icon-theme Argon`

## Building:
  - It's not necessary to rebuild the theme to install, only if modifications have been made
  - `make build` will only generate changed icons (automatically uses multiple cores) - faster alternative to `make clean && make regen -jX`
  - `make regen -jX` will regenerate all icons, whether they have been changed or not
  - `make clean` will delete all generated icons and index.theme
  - `make autoclean` will delete icons missing a corresponding svg, broken symlinks, index.theme and empty directories
  - `make index` will generate index.theme, done automatically by `build` and `regen`

## Contributing:
  - Create / modify / delete the appropriate .svg file(s)
  - Run `make autoclean; make build` to clean up left over files and generate new icons
  - Submit a pull request with the changes

## Build Dependencies:
  - coreutils
  - findutils
  - git
  - inkscape
  - make
  - optipng
  - sed

## Themed Icons:
  - Audacity
  - Chromium
  - Discord
  - GNU Image Manipulation Program (GIMP)
  - GNOME Boxes
  - GNOME Calculator
  - GNOME Tweaks
  - Google Chrome + Beta + Unstable
  - GParted
  - Kernel Notify (Upstreamed, kept for older versions)
  - Minecraft Launcher
  - Nvidia Settings
  - OBS Studio
  - Psensor (Upstreamed, kept for older versions)
  - Remmina
  - Retroarch
  - Spotify
  - Steam

## Papirus icons:
  - Htop
  - Inkscape
  - Vim
  - Vlc
  - Winetricks
