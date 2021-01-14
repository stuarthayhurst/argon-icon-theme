# argon-icon-theme
  - A minimalistic, material icon theme, designed for GNOME with Yaru
  - Currently, this theme looks best if Yaru is installed before it
  - This project contains some assets from [Papirus Icon Theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme) and [Yaru](https://github.com/ubuntu/yaru)

<p align='center'>
  <img src='https://raw.githubusercontent.com/Dragon8oy/argon-icon-theme/master/Preview.png' alt="Icon Preview"/>
</p>

## Installing:
  - `make build -j$(nproc); sudo make install`
    - `$(nproc)` can be replaced with a specific number, if necessary
  - Set the icon theme using gnome-tweaks, or `gsettings set org.gnome.desktop.interface icon-theme Argon`

## Building:
  - It's not necessary to rebuild the theme to install, only if modifications have been made
  - `make build -jX` will generate changed icons and `index.theme`
  - `make regen -jX` will regenerate all icons, whether they have been changed or not
  - `make clean` will delete all generated icons and `index.theme`
  - `make autoclean` will delete icons missing a corresponding svg, broken symlinks, `index.theme` and empty directories
  - `make index` will generate `index.theme` (Done automatically by `build` and `regen`)

## Contributing:
  - Create / modify / delete the appropriate .svg file(s)
  - Run `make build` to clean up left over files and generate new icons
  - Submit a pull request with the changes
  - Guides to make icons can be found in `guides/`

## Install Dependencies: (Required to install with no modifications)
  - make
  - sed

## Build Dependencies: (Required when icon .svgs have been modified)
  - findutils
  - git
  - inkscape
  - make
  - optipng
  - sed
