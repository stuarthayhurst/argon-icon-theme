#!/bin/bash
generateNewImages() {
  read -ra iconResolutions <<< "$1"
  buildDir="$2"

  #Check that git is present and .git is also present
  if ! git status > /dev/null 2>&1; then
    echo "Either git isn't installed, or .git missing"
    echo "This feature isn't available on releases"
    exit 1
  fi

  #Add any new svgs, svgs with missing pngs, or svgs with modifications to list
  for iconType in "$buildDir/scalable/"*; do
    for svgIcon in "$iconType/"*; do
      rebuildIcon="false"
      if ! git diff --exit-code -s "$svgIcon" > /dev/null 2>&1; then
        rebuildIcon="true"
      fi
      if ! git ls-files --error-unmatch "$svgIcon" > /dev/null 2>&1; then
        rebuildIcon="true"
      fi
      for resolution in "${iconResolutions[@]}"; do
        pngIcon="${svgIcon/"$buildDir/scalable"/"$buildDir/${resolution}x${resolution}"}"
        pngIcon="${pngIcon/svg/png}"
        if [[ ! -f "$pngIcon" ]]; then
          rebuildIcon="true"
        fi
      done
      if [[ "$rebuildIcon" == "true" ]]; then
        pngIcon="${svgIcon/svg/png}"
        pngIcon="./${pngIcon/"$buildDir/scalable"/"$buildDir/resolution/scalable"}"
        rebuildList+=("$pngIcon")
      fi
    done
  done

  #Generate the new icons
  make "${rebuildList[@]}" "-j$(nproc)"
}

generateImage() {
  inputFile="$1"
  read -ra iconResolutions <<< "$2"
  buildDir="$3"

  #Filter authors out of the path, generate outputFile
  outputFile="$inputFile"

  #Generate $inputFile
  inputFile="${inputFile//png/svg}"
  inputFile="${inputFile/resolution\/}"

  origOutputFile="$outputFile"
  for resolution in "${iconResolutions[@]}"; do
    outputFile="${outputFile//resolution\/scalable/$resolution\x$resolution}"
    echo "$inputFile -> $outputFile"
    mkdir -p "${outputFile%/*}"
    inkscape "--export-filename=$outputFile" -w "$resolution" -h "$resolution" "$inputFile" > /dev/null 2>&1
    optipng -strip all "$outputFile"
    outputFile="$origOutputFile"
  done
}

createIndex() {
  buildDir="$1"
  read -ra iconResolutions <<< "$2"
  cp "./templates/index.theme.template" "$buildDir/index.theme"
  for iconType in "./$buildDir/8x8/"*; do
    iconType="${iconType##*/}"
    for resolution in "${iconResolutions[@]}" scalable; do
      if [[ "$resolution" != "scalable" ]]; then
        resolution="${resolution}x${resolution}"
      fi
      sed "s|^Directories=.*|&$resolution/$iconType,|" "./$buildDir/index.theme" > "./$buildDir/index.theme.temp"
      resolution="${resolution%%x*}"
      echo "" >> "./$buildDir/index.theme.temp"
      fileContent="$(cat ./templates/directory.template)"
      fileContent="${fileContent//icontype/$iconType}"
      if [[ "$resolution" != "scalable" ]]; then
        fileContent="${fileContent//Size=/Size=$resolution}"
        fileContent="${fileContent//resolution/$resolution\x$resolution}"
        fileContent="${fileContent//Type=/Type=Threshold}"
      else
        fileContent="${fileContent//Size=/Size=256}"
        fileContent="${fileContent//resolution/$resolution}"
        fileContent="${fileContent//Type=/Type=Scalable}"
      fi
      echo "$fileContent" >> "./$buildDir/index.theme.temp"
      mv "./$buildDir/index.theme.temp" "./$buildDir/index.theme"
    done
  done

  sed "s|^Directories=.*|&symbolic/actions,|" "./$buildDir/index.theme" > "./$buildDir/index.theme.temp"
  fileContent="$(cat ./templates/directory.template)"
  fileContent="${fileContent//resolution/symbolic}"
  fileContent="${fileContent//icontype/actions}"
  fileContent="${fileContent//Size=/Size=256}"
  fileContent="${fileContent//Context=Applications/Context=Actions}"
  fileContent="${fileContent//Type=/Type=Scalable}"
  echo "" >> "./$buildDir/index.theme.temp"
  echo "$fileContent" >> "./$buildDir/index.theme.temp"
  mv "./$buildDir/index.theme.temp" "./$buildDir/index.theme"

  sed 's/,$//' "./$buildDir/index.theme" > "./$buildDir/index.theme.temp"
  mv "./$buildDir/index.theme.temp" "./$buildDir/index.theme"
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

case $1 in
  -a|--autoclean) autoclean "$2"; exit;;
  -g|--generate) generateNewImages "$2" "$3"; exit;;
  -i|--images) generateImage "$2" "$3" "$4"; exit;;
  -t|--theme-index) createIndex "$2" "$3"; exit;;
esac
