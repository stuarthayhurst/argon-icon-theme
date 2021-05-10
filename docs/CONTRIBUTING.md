# Contributing to argon-icon-theme
## Overview:
 - Your contributions and pull requests are welcome, this project can always use extra help!
 - In short, to contribute:
   - Make an issue describing what you're working on
   - Thoroughly test the contribution
   - Create a merge request, and make any requested changes

## Suggestions for contributing:
 - New icons
 - Improved versions of existing icons
 - Bug fixes and performance improvements to the build system
 - Documentation fixes and clarity improvements

## Working with issues:
 - If someone else is already working on a reported, feel free help them out. Please don't try and commandeer the issue, if you want to work on something on your own, find another issue
 - Please report issues before submitting a pull request to fix them
 - If you are working on your own issue, use that report as a space to track information and progress relating to the issue
 - If any help is required, please make it known, instead of silently dropping the issue

## Adding an icon:
 - Icons are created via svg files in `argon/scalable/[context]/icon.svg`
 - Icon templates can be found in `guides/`, and should be followed to match the style of the theme
 - The icons need to be regenerated, as stated below

## Building and installing the icon theme:
  > Generating new icons:
   - If new icons have been added, or existing icons changed, the build system can handle updating only changed icons:
   - `make build -j$(nproc)`
   - Alternatively, `make regen -j$(nproc)` will completely clear the project and regenerate all assets
   - If a new icon category / context was added, or values were changed for an existing one, run `make index`
  > Adding new symlinks:
   - If a new symlink is required, do the following:
     - Change into the directory where the new symlink should go
     - Symlink between the new icon and the target icon
     - Example: `cd argon/scalable/apps; ln -s blender.svg new-blender.svg`
     - If the symlink needs to link to an icon in a different directory, use a relative path
  > Installing:
   - Install with `sudo make install`
   - Uninstall with `sudo make uninstall`
   - Set the theme using gnome-tweaks, or `gsettings set org.gnome.desktop.interface icon-theme Argon`
  > Cleaning assets:
   - `make clean` will delete all generated icons and `index.theme`
   - `make autoclean` will remove clutter (icons missing a corresponding svg, broken symlinks and empty directories)

## Submitting a pull request:
 - When you believe your contribution to be complete, submit a pull request
   - Explain why the change was necessary, and what was changed
   - If the code isn't ready to be merged yet, please make this known
 - Your changes will be reviewed and either given suggestions for changes, or it'll be approved and merged
 - If possible, please write a summary of changes you made. This makes it easier to make a new release and document the changes

## Other informaton:
 - ALL changes must be allowed under the license (See `LICENSE.md`)
 - ALL changes and discussions must abide by the Code of Conduct (`docs/CODE_OF_CONDUCT.md`)
