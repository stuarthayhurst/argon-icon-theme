#!/usr/bin/python3
import sys, subprocess, glob, os
import multiprocessing as mp
import common

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
    print("\nERROR: " + "\n".join(errorOutput) + "\n")

  output = rawOutput.stdout.decode("utf-8").split("\n")
  if "" in output:
    output.remove("")
  return output

def generateIconList(buildDir):
  #Check every source icon has present and current icons built
  iconList = []
  for sourceIcon in glob.glob(f"./{buildDir}/scalable/*/*.svg"):
    #Get icon dir and name, then check which resolutions it should have
    [iconDir, iconName] = sourceIcon.rsplit("/", 1)
    iconDir = iconDir.rsplit("/", 1)[1]
    expectedResolutions = contextDict[iconDir][1]

    #Get modification timestamp of source file
    svgTime = os.stat(sourceIcon).st_mtime

    #Iterate over expected icons
    for resolution in expectedResolutions:
      if resolution == "scalable":
        continue

      #Generate the expected icon path
      pngName = iconName.replace("svg", "png")
      iconPath = f"{buildDir}/{resolution}/{iconDir}/{pngName}"

      #Check the icon exists
      if not os.path.isfile(iconPath):
        #Rebuild the icon later
        resolution = resolution.split("x")[0]
        iconList.append([sourceIcon, iconPath, resolution])
        continue

      #Check the icon is the latest
      pngTime = os.stat(iconPath).st_mtime
      if pngTime < svgTime:
        #Rebuild the icon later
        resolution = resolution.split("x")[0]
        iconList.append([sourceIcon, iconPath, resolution])
        continue

  return iconList

def generateIcon(iconInfo):
  sourceIcon = iconInfo[0]
  newIcon = iconInfo[1]
  resolution = iconInfo[2]

  #Create the directories for the output file if missing
  outputDir = os.path.dirname(newIcon)
  if not os.path.exists(outputDir):
    os.makedirs(outputDir, exist_ok=True)

  #Generate the icon
  print(f"Processing {sourceIcon} -> {newIcon}")
  exitCode = getCommandExitCode(["inkscape", f"{inkscapeExport}={newIcon}",
                                 "-w", resolution, "-h", resolution, sourceIcon])
  if exitCode != 0:
    print("ERROR: Failed to generate icon, exiting")
    exit(1)

  #Compress the icon and move to final destination
  print(f"Compressing {newIcon}...")
  exitCode = getCommandExitCode(["optipng", "-quiet", "-strip", "all", newIcon])
  if exitCode != 0:
    print("ERROR: Failed to compress icon, exiting")
    exit(1)

def generateIcons(iconList):
  with mp.Pool(mp.cpu_count()) as pool:
    result = pool.map(generateIcon, iconList)

#Prevent Inkscape crashing when multiple cores are used
os.environ["SELF_CALL"] = "1"

#Check Inkscape and optipng are present
if getCommandExitCode(["inkscape", "--version"]):
  print("ERROR: Inkscape required to build icons")
  print("If you're installing without making any changes, use 'make install'")
  exit(1)

if getCommandExitCode(["optipng", "--version"]):
  print("ERROR: Optipng required to build icons")
  print("If you're installing without making any changes, use 'make install'")
  exit(1)

#Handle older versions of Inkscape
inkscapeVersion = getCommandOutput(["inkscape", "--version"])[0].split(" ")[1]
inkscapeVersion = inkscapeVersion.split(".")
inkscapeVersion = float(f"{inkscapeVersion[0]}.{inkscapeVersion[1]}")
if inkscapeVersion >= 1.0:
  inkscapeExport = "--export-filename"
else:
  inkscapeExport = "--export-png"

#Create context dictionary for future reference
contextDict = common.createContextDict()
buildDir = str(sys.argv[1])

#Rebuild changed icons, generate missing icons
generateIcons(generateIconList(buildDir))
