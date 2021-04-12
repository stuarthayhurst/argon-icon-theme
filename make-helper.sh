#!/bin/bash
#Create an array containing all the resolutions to build icon for
#Need iconType and a list of resolutions
getMaxResolution() {
  iconType="$1"
  iconResolutions=()
  #Loop through context.csv contents
  for line in "${contextData[@]}"; do
    #If the icon type and context type match, continue
    if [[ "$iconType" == "${line%%,*}" ]]; then
      match="true"
      maxResolution="${line##*,}"
      #Loop through all resolutions, and create an array of resolutions equal to or below $maxResolution
      for resolution in $2; do
        if [[ "$resolution" -le "$maxResolution" ]]; then
          iconResolutions+=("$resolution")
        fi
      done
      break
    fi
  done
  if [[ "$match" != "true" ]]; then
    echo "No entry in context.csv for '$iconType', please report this"
    exit 1
  else
    match="false"
  fi
}

generateImage() {
  outputFile="$1"
  buildDir="$3"

  #Generate $inputFile
  inputFile="${outputFile//png/svg}"
  inputFile="${inputFile/resolution\/}"

  iconType="${inputFile##*argon/scalable/}"
  iconType="${iconType%%/*}"

  #Create array with resolutions to generate images for
  getMaxResolution "$iconType" "$2"

  origOutputFile="$outputFile"
  for resolution in "${iconResolutions[@]}"; do
    outputFile="${origOutputFile//resolution\/scalable/$resolution\x$resolution}"
    if [[ -L "./$inputFile" ]]; then
      iconTarget="$(readlink "$inputFile")"
      iconTarget="${iconTarget/svg/png}"
      mkdir -p "${outputFile%/*}"
      if [[ -f "$outputFile" ]]; then
        rm "./$outputFile"
      fi
      echo "Symlink: $outputFile -> $iconTarget"
      ln -s "$iconTarget" "$outputFile"
    else
      outputDir="${outputFile%/*}"
      tempFile="$outputDir/$$.png"
      echo "Processing $inputFile -> $outputFile ($tempFile)"
      mkdir -p "$outputDir"
      inkscape "--export-filename=$tempFile" -w "$resolution" -h "$resolution" "$inputFile" > /dev/null 2>&1
      echo "Compressing $outputFile..."
      optipng -quiet -strip all "$tempFile"
      mv "$tempFile" "$outputFile"
    fi
  done
}

autoclean() {
  buildDir="$1"
  for resolution in "./$buildDir/"*"x"*; do
    if [[ -d "$resolution" ]]; then
      for iconType in "$resolution"/*; do
        for pngIcon in "$iconType"/*; do
          resolution="${resolution/"./$buildDir/"}"
          svgIcon="${pngIcon/$resolution/scalable}"
          svgIcon="${svgIcon/png/svg}"
          if [[ ! -e "$pngIcon" ]]; then
            rm -rv "$pngIcon"
          fi
          if [[ ! -f "$svgIcon" ]]; then
            if [[ -f "$pngIcon" ]]; then
              rm -rv "$pngIcon"
            fi
          fi
        done
      done
    fi
  done
}

i="0"
while read -r line; do
  i=$(( i + 1 ))
  contextData[i]="$line"
done < index/context.csv

case $1 in
  -a|--autoclean) autoclean "$2"; exit;;
  -i|--images) generateImage "$2" "$3" "$4"; exit;;
esac
