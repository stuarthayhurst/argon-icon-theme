#!/usr/bin/python3
import sys, subprocess, glob, os
from common import createContextDict

def getCommandExitCode(command):
  try:
    return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
  except FileNotFoundError:
    return 1

def getCommandOutput(command):
  rawOutput = subprocess.run(command, capture_output=True)

  #Check for errors and print
  errorOutput = rawOutput.stderr.decode("utf-8").split("\n")
  if "" in errorOutput:
    errorOutput.remove("")
  if len(errorOutput) != 0:
    print("\nError: " + "\n".join(errorOutput) + "\n")

  output = rawOutput.stdout.decode("utf-8").split("\n")
  if "" in output:
    output.remove("")
  return output

#Lists all changed, new and missing icons
def listChangedIcons(buildDir, makeCommand):
  #Check git is present, and .git exists
  if getCommandExitCode(["git", "status"]):
    print("\nDifferential build unsupported")
    if os.path.exists(".git"):
      print("git couldn't be found, so changed files could not be detected")
    else:
      print("This feature isn't available on releases, use 'sudo make install' to install")
    exit(1)

  buildList = []

  #Parse git status --porcelain to find any new or changed svgs
  for line in getCommandOutput(["git", "status", "--porcelain"]):
    splitLine = line.split(" ")

    #Ignore deleted files
    if splitLine[0] == "D" or splitLine[1] == "D":
      continue

    filename = splitLine[len(splitLine) - 1]
    if filename.endswith(".svg"):
      #Convert svg path to png path
      filename = filename.replace(f"{buildDir}/scalable", f"{buildDir}/resolution/scalable")
      filename = filename.replace(".svg", ".png")
      #Add to rebuild list
      buildList.append(filename)

  #Add any svgs with missing pngs to rebuild list
  for svgFile in glob.glob(str(buildDir) + "/scalable/*/*.svg"):
    rebuildIcon = False

    #Work out the highest resolution to check for
    iconContext = svgFile.split("scalable/", 1)[1]
    iconContext = iconContext.split("/", 1)[0]

    #Set iconResolutions to predetermined array of valid resolutions
    iconResolutions = contextDict[iconContext][1]
    if "scalable" in iconResolutions:
      iconResolutions.remove("scalable")

    #Check all resolutions of the icon are present
    for resolution in iconResolutions:
      pngFile = svgFile.replace(buildDir + "/scalable", buildDir + "/" + str(resolution))
      pngFile = pngFile.replace(".svg", ".png")
      if not os.path.isfile(pngFile):
        rebuildIcon = True

    #Convert file into the string used to build
    if rebuildIcon == True:
      pngFile = svgFile.replace(buildDir + "/scalable", buildDir + "/resolution/scalable")
      pngFile = pngFile.replace(".svg", ".png")

      buildList.append(pngFile)

  #Add index to the build list
  buildList.append("index")
  #Allow makeCommand to be combined with another array
  makeCommand = makeCommand.split()
  #Combine make command and icons to start build
  subprocess.run(makeCommand + buildList, close_fds=False)

#Generates the given icon for all required resolutions
def generateIcon(buildDir, outputFile):
  #Generate input file path by swapping to an svg and removing "resolution/"
  inputFile = outputFile.replace("resolution/", "")
  inputFile = inputFile.replace(".png", ".svg")

  #Work out the icon context
  iconContext = inputFile.split("scalable/", 1)[1]
  iconContext = iconContext.split("/", 1)[0]

  #Set iconResolutions to predetermined array of valid resolutions to build for
  iconResolutions = contextDict[iconContext][1]
  if "scalable" in iconResolutions:
    iconResolutions.remove("scalable")

  #Generate output file for each resolution allowed
  outputFileOrig = outputFile
  for resolution in iconResolutions:
    #Generate path to outputFile for specific resolution
    outputFile = outputFileOrig.replace("resolution/scalable", str(resolution))

    #Create the directories for the output file if missing
    outputDir = os.path.dirname(outputFile)
    if not os.path.exists(outputDir):
      os.makedirs(outputDir, exist_ok=True)

    #Get process ID for use as a temporary file, if required
    tempFile = outputDir + "/" + str(os.getpid()) + ".png"

    #Generate the icon
    print(f"Processing {inputFile} -> {outputFile} ({tempFile})")
    getCommandExitCode(["inkscape", f"{inkscapeExport}={tempFile}", "-w", resolution.split("x")[0], "-h", resolution.split("x")[0], inputFile])

    #Compress the icon and move to final destination
    print(f"Compressing {outputFile}...")
    getCommandExitCode(["optipng", "-quiet", "-strip", "all", tempFile])
    os.rename(tempFile, outputFile)

#Figure out inkscape generation option
os.environ["SELF_CALL"] = "1"
inkscapeVersion = getCommandOutput(["inkscape", "--version"])[0].split(" ")[1]
inkscapeVersion = inkscapeVersion.split(".")
inkscapeVersion = float(f"{inkscapeVersion[0]}.{inkscapeVersion[1]}")

if inkscapeVersion >= 1.0:
  inkscapeExport = "--export-filename"
else:
  inkscapeExport = "--export-png"

if __name__ == "__main__":
  #Create context dictionary for future reference
  if len(sys.argv) >= 4:
    contextDict = createContextDict(sys.argv[3].split())

  #Handle arguments
  if sys.argv[1] == "--list":
    #Pass listChangedIcons() the build directory and make command
    listChangedIcons(str(sys.argv[2]), str(sys.argv[4]))
  elif sys.argv[1] == "--generate":
    #Pass generateIcon() the build directory and icon to build
    generateIcon(str(sys.argv[2]), str(sys.argv[4]))
