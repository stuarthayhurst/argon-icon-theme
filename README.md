## argon-icon-theme
  - A minimalistic app icon theme for Linux, designed for GNOME, but should work elsewhere
  - Any donations are greatly appreciated :)

<p align='center'>
  <img src='https://raw.githubusercontent.com/stuarthayhurst/argon-icon-theme/master/docs/Preview.png' alt="Icon Preview"/>
</p>

## Themed icons:
  - This icon theme targets the following areas:
    - App icons
    - MIME types
    - Weather, device and miscellaneous status icons

## Installing:
  - `sudo make install`
  - Set the icon theme using gnome-tweaks, or `gsettings set org.gnome.desktop.interface icon-theme Argon`
  - Installation path can be configured using the environment variable `INSTALL_DIR`
    - For example, `INSTALL_DIR=/usr/share/icons/Argon sudo make install`

## Building:
  - `make index` will generate `index.theme`
  - `make check` will check all defined symlinks are valid
  - `make install` will copy the theme to the install location, check and generate symlinks, generate `index.theme`, then run `make refresh`
  - `make refresh` will generate an icon cache for the theme

## Contributing:
  - Contribution guidelines can be found in `docs/CONTRIBUTING.md`, but in summary:
    - Create / modify / delete the appropriate .svg file(s)
    - Submit a pull request with the changes
  - Guides to make icons can be found in `guides/`

## Install Dependencies:
  - make
  - python3 (3.9+)
