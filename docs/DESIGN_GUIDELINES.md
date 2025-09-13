# Designing icons for argon-icon-theme
## Overview:
 - Where possible, icons should follow the templates in `guides/`
 - Basic colours are defined here, which should be used when appropriate
 - Shadow usage is also defined here, when to use it and the strength of the shadow
 - Any text used should be converted from text to a path
   - Cantarell should be used, except in specific edge cases

## Fonts:
 - Cantarell should be used for letters and symbols
 - DejaVu Sans should be used for numbers
 - Individual exceptions can be made, but all fonts must be converted to paths and definitions removed

## Templates:
 - Templates for icons can be found in `guides/`
 - These template have the correct sizing, layers and opacities for icons that may be designed
 - Templates for mimetypes are also provided, again with everything you may need for the icon
 - `DevelLayer.svg` would be applied to icons with the suffix `-devel` or `-dev`
 - Exceptions to the templates can be discussed in an issue / PR for a new icon

## Symbolic icons:
 - Aside from some exceptions, symbolic icons should be suffixed with `-symbolic.symbolic`
 - They should also be 16x16, and use only black as a colour
 - Different opacities can be used, but the colour code must still be `#000000XX`, where `XX` is the opacity
 - Symbolic icons shouldn't be too detailed, and try to avoid crossing pixel boundaries
 - Most new app icons in `argon/scalable/apps/` should have a corresponding symbolic icon created

## Colours:
 - Shades of grey should generally have the red, green and blue values match
 - Highlights should be white (`#FFFFFF`), with an opacity of 10
   - This generally doesn't matter, as the `Highlight` layer should take care of the opacity
 - Accent colours should be a shade of light blue / turquoise, or lime green
 - Warning colour: `#FF9200`
 - Error colour: `#DA2214`
 - Success colour: `#00A80E`

## Shadows:
 - Shadows should be solid black, with an opacity of 40, applied 2 steps downwards, with the down arrow
 - Items on icons should have shadows applied to them, if they are supposed to 'float' off of the icon
 - Icon base layers and their extensions should also have shadows applied
 - Mimetype icons have slightly different rules:
   - Objects, like a database icon, should have a shadow applied
   - Application icons should have shadows if added to a mimetype icon
   - Objects 'branded' into the file, like a settings cog, or a chainlink shouldn't have a shadow
 - If you're unsure about when to apply a shadow, ask in an issue / PR
