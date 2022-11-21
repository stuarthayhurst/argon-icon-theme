## argon-icon-theme
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/stuartahayhurst)
  - A minimalistic icon theme for Linux, designed for GNOME, but should work elsewhere
  - Any donations are greatly appreciated :)

<p align='center'>
  <img src='https://raw.githubusercontent.com/stuarthayhurst/argon-icon-theme/master/docs/Preview.png' alt="Icon Preview"/>
</p>

## Installing:
  - `sudo make install`
  - Set the icon theme using gnome-tweaks, or `gsettings set org.gnome.desktop.interface icon-theme Argon`

## Building:
  - It's not necessary to rebuild the theme to install, only if modifications have been made
  - `make build -jX` will autoclean, then generate changed icons and `index.theme`
  - `make regen -jX` will regenerate all icons, whether they have been changed or not, and `index.theme`
  - `make clean` will delete all generated icons and `index.theme`
  - `make autoclean` will delete icons missing a corresponding svg, broken symlinks and empty directories, then prune
  - `make prune` will delete rubbish elements and attributes from the svgs
  - `make index` will generate `index.theme` (Done automatically by `build` and `regen`)
  - `make check` will check all defined symlinks are valid
  - `make install` will copy the theme in its current state to the install location, check and generate any symlinks, then run `make refresh`
  - `make refresh` will generate an icon cache for the theme

## Contributing:
  - Contribution guidelines can be found in `docs/CONTRIBUTING.md`, but summarised:
    - Create / modify / delete the appropriate .svg file(s)
    - Run `make build` to clean up left over files, generate new icons and index
    - Submit a pull request with the changes
  - Guides to make icons can be found in `guides/`

## Install Dependencies: (Required to install with no modifications)
  - make
  - python3

## Build Dependencies: (Required when icon .svgs have been modified)
  - `Install dependencies`
  - git
  - inkscape
  - optipng
