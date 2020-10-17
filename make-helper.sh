#!/bin/bash
generateChangedImages() {
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
    for svgIcon in "$iconType/"*.svg; do
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

  #Generate any new icons
  if [[ "${rebuildList[*]}" != "" ]]; then
    make "${rebuildList[@]}" "-j$(nproc)"
  fi
}

generateImage() {
  outputFile="$1"
  read -ra iconResolutions <<< "$2"
  buildDir="$3"

  #Generate $inputFile
  inputFile="${outputFile//png/svg}"
  inputFile="${inputFile/resolution\/}"

  origOutputFile="$outputFile"
  for resolution in "${iconResolutions[@]}"; do
    outputFile="${origOutputFile//resolution\/scalable/$resolution\x$resolution}"
    if [[ -L "./$inputFile" ]]; then
      iconTarget="$(readlink "$inputFile")"
      iconTarget="${iconTarget/svg/png}"
      echo "Symlink: $inputFile -> $iconTarget"
      mkdir -p "${outputFile%/*}"
      if [[ -f "$outputFile" ]]; then
        rm "./$outputFile"
      fi
      ln -s "$iconTarget" "$outputFile"
    else
      echo "$inputFile -> $outputFile"
      mkdir -p "${outputFile%/*}"
      inkscape "--export-filename=$outputFile" -w "$resolution" -h "$resolution" "$inputFile" > /dev/null 2>&1
      optipng -strip all "$outputFile"
    fi
  done
}

generateIndex() {
  buildDir="$1"
  #Generate list of resolutions, as directories
  read -ra resolutionDirs <<< "$(echo argon/*/ | tr " " "\n" | sort -V | tr "\n" " ")"
  read -ra resolutionDirs <<< "${resolutionDirs[*]%'/'}"
  read -ra resolutionDirs <<< "${resolutionDirs[*]//"$buildDir/"}"

  cp "./templates/index.theme.template" "$buildDir/index.theme"

  #Iterate through each resolution directory
  for iconResolution in "${resolutionDirs[@]}"; do
    #Get list of directories
    dirList=()
    for iconDir in "./$buildDir/$iconResolution/"*; do
      if [[ -d "$iconDir" ]]; then
        dirList+=("${iconDir##*/}")
      fi
    done
    #Iterate through each subdirectory, get info about it, and write to theme.index
    for iconDir in "${dirList[@]}"; do
      #Generate iconSize and iconType
      if [[ "$iconResolution" == "scalable" ]] || [[ "$iconResolution" == "symbolic" ]]; then
        iconSize="256"
        iconType="Scalable"
      else
        iconSize="${iconResolution%x*}"
        iconType="Threshold"
      fi

      while read -r line; do
        if [[ "${line%,*}" == "$iconDir" ]]; then
          iconContext="${line#*,}"
        fi
      done < templates/context.csv
      if [[ "$iconContext" == "" ]]; then
        echo "No entry in context.csv for '$iconDir', please report this"
        exit
      fi

      #Fill in template
      fileContent="$(cat ./templates/directory.template)"
      fileContent="${fileContent/"resolution/iconDir"/"$iconResolution/$iconDir"}"
      fileContent="${fileContent/"Size="/"Size=$iconSize"}"
      fileContent="${fileContent/"Context="/"Context=$iconContext"}"
      fileContent="${fileContent/"Type="/"Type=$iconType"}"

      #Write info to file
      sed -i "s|^Directories=.*|&$iconResolution/$iconDir,|" "./$buildDir/index.theme"
      echo -e "\n$fileContent" >> "./$buildDir/index.theme"
    done
  done

  #Remove trailing comma from directory list
  sed -i 's/,$//' "./$buildDir/index.theme"
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

case $1 in
  -a|--autoclean) autoclean "$2"; exit;;
  -g|--generate) generateChangedImages "$2" "$3"; exit;;
  -i|--images) generateImage "$2" "$3" "$4"; exit;;
  -t|--theme-index) generateIndex "$2"; exit;;
esac
