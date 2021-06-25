#!/usr/bin/python3
import sys, subprocess, glob, os, csv

def orderDirs(dirList):
  process = os.popen("echo " + " ".join(dirList) + '| tr " " "\n" | sort -V | tr "\n" " "')
  output = process.read()
  return output.split()

def getResolutionDirs(searchPath):
  #Generate a list of directories matching searchPath/*x*
  resolutionDirs = []
  for directory in glob.glob(searchPath + "/*x*"):
    directory = directory.replace(searchPath + "/", "")
    if os.path.isdir(searchPath + "/" + directory):
      resolutionDirs.append(directory)
  resolutionDirs.append("scalable")

  return orderDirs(resolutionDirs)

def isSymlinkBroken(path):
  if os.path.islink(path):
    #Generate path to symlink target
    linkPath = str(os.path.dirname(path)) + "/" + str(os.readlink(path))
    if os.path.isfile(linkPath) == False:
      #Symlink is broken
      return True
  #Either not a symlink, or not broken
  return False

def getCommandExitCode(command):
  return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode

def getMaxResolutionList(maxResolution, iconResolutions):
  #Loop through given resolutions, add to a return array if it's less than the max
  allowedResolutions = []
  for resolution in iconResolutions:
    if int(resolution) <= int(maxResolution):
      allowedResolutions.append(f"{resolution}x{resolution}")
  allowedResolutions.append("scalable")

  #Return an array of valid resolutions to build for
  return allowedResolutions

def createContextDict(iconResolutions):
  #Load info from index/context.csv into a dictionary
  contextDict = {}
  with open("index/context.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
      #contextDict stores the pretty name and array of max resolutions for the context
      #contextDict["context"]=["pretty name", ["allowed", "resolutions"]]
      contextDict[row[0]]=[row[1], getMaxResolutionList(row[2], iconResolutions)]
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
    if "scalable" in iconResolutions:
      iconResolutions.remove("scalable")

    #Check all resolutions of the icon are present
    for resolution in iconResolutions:
      pngFile = svgFile.replace(buildDir + "/scalable", buildDir + "/" + str(resolution))
      pngFile = pngFile.replace(".svg", ".png")
      if os.path.isfile(pngFile) == False:
        rebuildIcon = True

    #Check if the file is a broken symlink, and ignore
    if isSymlinkBroken(svgFile):
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
  if "scalable" in iconResolutions:
    iconResolutions.remove("scalable")

  #Generate output file for each resolution allowed
  outputFileOrig = outputFile
  for resolution in iconResolutions:
    #Generate path to outputFile for specific resolution
    outputFile = outputFileOrig.replace("resolution/scalable", str(resolution))

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
      getCommandExitCode(["inkscape", f"--export-filename={tempFile}", "-w", resolution.split("x")[0], "-h", resolution.split("x")[0], inputFile])

      #Compress the icon and move to final destination
      print(f"Compressing {outputFile}...")
      getCommandExitCode(["optipng", "-quiet", "-strip", "all", tempFile])
      os.rename(tempFile, outputFile)

def makeSymlinks(buildDir, installDir):
  #Read all the symlinks to create into memory and create a data structure for them
  #  symlinkDict["apps"][0]["symlink"] would return the name of a smylink to create
  symlinkLists = glob.glob(buildDir + "/symlinks/*")
  symlinkDict = {}

  for listFile in symlinkLists:
    contextDir = os.path.basename(listFile)
    contextDir = "".join(contextDir.rsplit(".list", 1))

    processedSymlinks = []
    with open(listFile) as file:
      for line in file.readlines():
        line = line.replace("\n", "")

        #Remove file extensions (filled in later)
        line = line.replace(".svg", "")

        line = line.split(" -> ")
        line = {
          "symlink": line[0],
          "target": line[1]
        }
        processedSymlinks.append(line)

    symlinkDict[contextDir] = processedSymlinks

  #Check permissions for creating symlinks
  if os.access(installDir, os.W_OK) == False:
    print(f"No write permission for {installDir}, try running with root")
    exit(1)

  #Loop through contexts
  for contextDir in symlinkDict:
    #Get resolutions to generate symlinks for specific context
    resolutionDirs = contextDict[contextDir][1]
    #Loop through resolutionDirs
    for resolutionDir in resolutionDirs:
      path = (f"{installDir}/{resolutionDir}/{contextDir}/")

      #Create context dir if missing
      if os.path.isdir(path) == False:
        os.mkdir(path)

      for symlinkObject in symlinkDict[contextDir]:
        if resolutionDir == "scalable":
          os.symlink(path + symlinkObject["target"] + ".svg", path + symlinkObject["symlink"] + ".svg")
        else:
          os.symlink(path + symlinkObject["target"] + ".png", path + symlinkObject["symlink"] + ".png")

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
  elif sys.argv[1] == "--install-symlinks":
    #Pass makeSymlinks() the install directory
    makeSymlinks(str(sys.argv[2]), str(sys.argv[4]))
