# Contributing to argon-icon-theme
## Overview:
 - Your contributions and pull requests are welcome, this project can always use extra help!
 - In short, to contribute:
   - Make an issue describing what you're working on
   - Thoroughly test the contribution
   - Create a merge request, and make any requested changes

## Suggestions for contributing:
 - New icons or symlinks
 - Improved versions of existing icons
 - Bug fixes and performance improvements to the build system
 - Documentation fixes and clarity improvements

## Adding an icon:
 - **Icons should follow the guidelines in `docs/DESIGN_GUIDELINES.md`**
 - Icons are all SVG files, such as `argon/scalable/[context]/icon.svg`
 - Icon templates can be found in `guides/`, and should be followed to match the style of the theme

## Adding symlinks:
 - If a new symlink is required, do the following:
   - Look in `argon/symlinks/` for the `.list` file corresponding to the icon's category
   - Add a new line to the file, ensuring the alphabetical order is preserved
   - Fill in the line with `newIcon.svg -> targetIcon.svg`
   - `targetIcon.svg` should already exist, and `newIcon.svg` will be created at install time
   - Run `make check`, to validate the symlinks
   - Example: `blender.svg -> new-blender.svg`
   - Please use a relative path, as the symlinks are generated exactly with the given data in the install directory

## Installing the icon theme:
 - Install with `sudo make install`
 - Uninstall with `sudo make uninstall`
 - Set the theme using GNOME Tweaks, or `gsettings set org.gnome.desktop.interface icon-theme Argon`

## Submitting a pull request:
 - When you believe your contribution to be complete, submit a pull request
   - Explain why the change was necessary, and what was changed
   - If the code isn't ready to be merged yet, please make this known
 - Your changes will be reviewed and either given suggestions for changes, or it'll be approved and merged
 - If possible, please write a summary of changes you made. This makes it easier to make a new release and document the changes

## Other informaton:
 - ALL changes must be allowed under the license (See `LICENSE.md`)
 - ALL changes and discussions must abide by the Code of Conduct (`docs/CODE_OF_CONDUCT.md`)
