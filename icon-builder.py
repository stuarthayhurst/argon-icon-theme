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
    for row in reader:
      #contextDict stores the pretty name and array of max resolutions for the context
      #contextDict["context"]=["pretty name", ["allowed", "resolutions"]]
      contextDict[row[0]]=[row[1], getMaxResolutionList(row[2], iconResolutions)]
  return contextDict

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

#Handle arguments
if sys.argv[1] == "--list":
  #Create context dictionary for future reference
  contextDict = createContextDict(sys.argv[3].split())
  #Pass listChangedIcons() the build directory and make command
  listChangedIcons(str(sys.argv[2]), str(sys.argv[4]))
