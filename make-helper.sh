#!/bin/bash
generateImage() {
  filename="$1"
  read -ra iconResolutions <<< "$2"
  filterList=("Argon/" "Papirus/")
  for resolution in "${iconResolutions[@]}"; do
    inputFile="argon${filename/build\/resolution}"
    inputFile="${inputFile//.png/.svg}"
    outputFile="${filename//resolution/$resolution\x$resolution}"
    for filter in "${filterList[@]}"; do
      outputFile="${outputFile//$filter}"
    done
    iconType="${outputFile%/*}"
    iconType="${iconType##*/}"
    echo "$inputFile -> $outputFile"
    mkdir -p "./${outputFile%/*}"
    inkscape "--export-filename=$outputFile" -w "$resolution" -h "$resolution" "$inputFile" > /dev/null 2>&1
    optipng -strip all "$outputFile"
  done
  mkdir -p "./build/scalable/$iconType"
  cp "$inputFile" "./build/scalable/$iconType/"
}

createIndex() {
  read -ra iconResolutions <<< "$2"
  cp "./argon/index.theme" "$1/"
  for iconType in ./build/8x8/*; do
    iconType="${iconType##*/}"
    for resolution in "${iconResolutions[@]}" scalable; do
      if [[ "$resolution" != "scalable" ]]; then
        resolution="${resolution}x${resolution}"
      fi
      sed "s|^Directories=.*|&$resolution/$iconType,|" ./build/index.theme > ./build/index.theme.temp
      resolution="${resolution%%x*}"
      echo "" >> ./build/index.theme.temp
      fileContent="$(cat ./argon/directory.template)"
      fileContent="${fileContent//Size=/Size=$resolution}"
      fileContent="${fileContent//icontype/$iconType}"
      if [[ "$resolution" != "scalable" ]]; then
        fileContent="${fileContent//resolution/$resolution\x$resolution}"
        fileContent="${fileContent//Type=/Type=Threshold}"
      else
        fileContent="${fileContent//resolution/$resolution}"
        fileContent="${fileContent//Type=/Type=Scalable}"
      fi
      echo "$fileContent" >> ./build/index.theme.temp
      mv ./build/index.theme.temp ./build/index.theme
    done
  done
  sed 's/,$//' ./build/index.theme > ./build/index.theme.temp
  mv ./build/index.theme.temp ./build/index.theme
}

case $1 in
  -i|--images) generateImage "$2" "$3"; exit;;
  -t|--theme-index) createIndex "$2" "$3"; exit;;
esac
