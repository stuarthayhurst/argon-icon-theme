#!/bin/bash
generateChangedImages() {
  buildDir="$2"
  makeCommand="$3"

  #Check that git is present and .git is also present
  if ! git status > /dev/null 2>&1; then
    echo "Either git isn't installed, or .git missing"
    echo "This feature isn't available on releases"
    exit 1
  fi

  #Add any new svgs, svgs with missing pngs, or svgs with modifications to list
  for iconType in "$buildDir/scalable/"*; do
    for svgIcon in "$iconType/"*.svg; do
      rebuildIcon="false"
      if ! git diff --exit-code -s "$svgIcon" > /dev/null 2>&1; then
        rebuildIcon="true"
      fi
      if ! git ls-files --error-unmatch "$svgIcon" > /dev/null 2>&1; then
        rebuildIcon="true"
      fi

      #Generate list of icon resolutions to check for
      getMaxResolution "${iconType##*/}" "$1"

      for resolution in "${iconResolutions[@]}"; do
        pngIcon="${svgIcon/"$buildDir/scalable"/"$buildDir/${resolution}x${resolution}"}"
        pngIcon="${pngIcon/svg/png}"
        if [[ ! -f "$pngIcon" ]]; then
          rebuildIcon="true"
        fi
      done
      #If the icon is a symlink, check it's not broken
      if [[ -L "$svgIcon" ]]; then
        #Get the path to the target, and append the target
        linkTarget="${svgIcon%/*}/$(readlink "$svgIcon")"
        if [[ ! -f "$linkTarget" ]]; then
          echo "$svgIcon: broken symlink, ignoring"
          rebuildIcon="false"
        fi
      fi
      if [[ "$rebuildIcon" == "true" ]]; then
        pngIcon="${svgIcon/svg/png}"
        pngIcon="./${pngIcon/"$buildDir/scalable"/"$buildDir/resolution/scalable"}"
        rebuildList+=("$pngIcon")
      fi
    done
  done

  #Generate any new icons and index.theme
  rebuildList+=("index")
  $makeCommand "${rebuildList[@]}"
}

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
  -g|--generate) generateChangedImages "$2" "$3" "$4"; exit;;
  -i|--images) generateImage "$2" "$3" "$4"; exit;;
esac
