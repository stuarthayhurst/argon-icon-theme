#!/usr/bin/python3
import sys, subprocess, glob, os, csv

def getCommandExitCode(command):
  return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode

def getMaxResolutionList(maxResolution, iconResolutions):
  #Loop through given resolutions, add to a return array if it's less than the max
  allowedResolutions = []
  for resolution in iconResolutions:
    if int(resolution) <= int(maxResolution):
      allowedResolutions.append(resolution)

  #Return an array of valid resolutions to build for
  return allowedResolutions

def createContextDict(iconResolutions):
  #Load info from index/context.csv into a dictionary
  contextDict = {}
  with open('index/context.csv', 'r') as file:
    reader = csv.reader(file)
    if iconResolutions != None:
      for row in reader:
        #contextDict stores the pretty name and array of max resolutions for the context
        #contextDict["context"]=["pretty name", ["allowed", "resolutions"]]
        contextDict[row[0]]=[row[1], getMaxResolutionList(row[2], iconResolutions)]
    else:
      for row in reader:
        contextDict[row[0]]=[row[1]]
  return contextDict

#Lists all changed, new and missing icons
def listChangedIcons(buildDir, makeCommand):
  #Check git is present, and .git exists
  if getCommandExitCode(["git", "status"]):
    print("Either git isn't installed, or .git missing")
    print("This feature isn't available on releases, use 'sudo make install' to install")
    print("index.theme can be generated using 'make index'")
    exit(1)

  #Create an array with any new svgs, svgs with missing pngs, or svgs with modifications
  buildList = []
  for svgFile in glob.glob(str(buildDir) + "/scalable/*/*.svg"):
    #Add icon to array if the file has changes
    if getCommandExitCode(["git", "diff", "--exit-code", "-s", svgFile]):
      rebuildIcon = True
    #Add the icon to the array if it's new / untracked
    elif getCommandExitCode(["git", "ls-files", "--error-unmatch", svgFile]):
      rebuildIcon = True
    else:
      rebuildIcon = False

    #Work out the highest resolution to check for
    iconContext = svgFile.split("scalable/", 1)[1]
    iconContext = iconContext.split("/", 1)[0]

    #Set iconResolutions to predetermined array of valid resolutions
    iconResolutions = contextDict[iconContext][1]

    #Check all resolutions of the icon are present
    for resolution in iconResolutions:
      resolution = str(resolution) + "x" + str(resolution)
      pngFile = svgFile.replace(buildDir + "/scalable", buildDir + "/" + str(resolution))
      pngFile = pngFile.replace(".svg", ".png")
      if os.path.isfile(pngFile) == False:
        rebuildIcon = True

    #Check if the file is a broken symlink, and ignore
    if os.path.islink(svgFile):
      #Generate path to symlink target
      linkPath = str(svgFile.rsplit("/", 1)[0]) + "/" + str(os.readlink(svgFile))
      if os.path.isfile(linkPath) == False:
        print(svgFile + " is a broken symlink, ignoring")
        print("Nothing is critically broken, but this shouldn't be the case, unless run under special circumstances")
        print("Please run 'make autoclean', and then try again")
        print("If the issue persists, please report it")
        rebuildIcon = False

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

  #Generate output file for each resolution allowed
  outputFileOrig = outputFile
  for resolution in iconResolutions:
    #Generate path to outputFile for specific resolution
    outputFile = outputFileOrig.replace("resolution/scalable", str(resolution) + "x" + str(resolution))

    #Create the directories for the output file if missing
    outputDir = os.path.dirname(outputFile)
    if os.path.exists(outputDir) == False:
      os.makedirs(outputDir, exist_ok=True)

    #Get process ID for use as a temporary file, if required
    tempFile = outputDir + "/" + str(os.getpid()) + ".png"

    #For symlinks, delete the output, and create a symlink between the output file and the output symlink target
    if os.path.islink(inputFile):
      #If the output file exists, delete it
      if (os.path.exists(outputFile)):
        os.remove(outputFile)

      #Generate output target based off of input symlink target
      outputLinkTarget = os.readlink(inputFile)
      outputLinkTarget = outputLinkTarget.replace(".svg", ".png")

      #Make a symlink to link the output file to the output symlink target
      print(f"Symlink: {outputFile} -> {outputLinkTarget}")
      os.symlink(outputLinkTarget, outputFile)
    else:
      #Generate the icon
      print(f"Processing {inputFile} -> {outputFile} ({tempFile})")
      getCommandExitCode(["inkscape", f"--export-filename={tempFile}", "-w", resolution, "-h", resolution, inputFile])

      #Compress the icon and move to final destination
      print(f"Compressing {outputFile}...")
      getCommandExitCode(["optipng", "-quiet", "-strip", "all", tempFile])
      os.rename(tempFile, outputFile)

#Required, because generate-index.py imports createContextDict from this file, and this code breaks the other script
if __name__ == '__main__':
  #Create context dictionary for future reference
  contextDict = createContextDict(sys.argv[3].split())

  #Handle arguments
  if sys.argv[1] == "--list":
    #Pass listChangedIcons() the build directory and make command
    listChangedIcons(str(sys.argv[2]), str(sys.argv[4]))
  elif sys.argv[1] == "--generate":
    #Pass generateIcon() the build directory and icon to build
    generateIcon(str(sys.argv[2]), str(sys.argv[4]))
