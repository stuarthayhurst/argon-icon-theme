#!/usr/bin/python3
import sys, glob, os, shutil
import common

def createSymlinkDict(buildDir):
  #Read all the symlinks to create into memory and create a data structure for them
  #  symlinkDict["apps"][0]["symlink"] would return the name of a symlink to create
  symlinkLists = glob.glob(buildDir + "/symlinks/*")
  symlinkDict = {}

  for listFile in symlinkLists:
    contextDir = os.path.basename(listFile)
    contextDir = "".join(contextDir.rsplit(".list", 1))

    processedSymlinks = []
    with open(listFile) as file:
      for line in file.readlines():

        #Strip newline before checking for contents, otherwise empty lines aren't caught
        line = line.replace("\n", "")

        if line != "":
          #Remove file extensions (filled in later)
          line = line.replace(".svg", "")

          line = line.split(" -> ")
          line = {
            "symlink": line[0],
            "target": line[1]
          }
          processedSymlinks.append(line)
        else:
          print(f"Empty line in '{listFile}', please fix this")

    symlinkDict[contextDir] = processedSymlinks
  return symlinkDict

def makeSymlinks(buildDir, installDir):
  #Create dictionary with symlink information
  symlinkDict = createSymlinkDict(buildDir)

  #Check permissions for creating symlinks
  if not os.access(installDir, os.W_OK):
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
      if not os.path.isdir(path):
        os.mkdir(path)

      for symlinkObject in symlinkDict[contextDir]:
        if resolutionDir == "scalable":
          shutil.copy(f"{path}{symlinkObject['target']}.svg", f"{path}{symlinkObject['symlink']}.svg")
        else:
          shutil.copy(f"{path}{symlinkObject['target']}.png", f"{path}{symlinkObject['symlink']}.png")

def checkSymlinks(buildDir):
  #Create dictionary with symlink information
  symlinkDict = createSymlinkDict(buildDir)
  failed = False

  #Loop through every symlink info object, and validate the contents
  for context in symlinkDict:
    for symlinkObject in symlinkDict[context]:
      contextPath = f"{buildDir}/scalable/{context}"
      symlinkPath = f"{contextPath}/{symlinkObject['symlink']}.svg"
      symlinkTarget = f"{contextPath}/{symlinkObject['target']}.svg"

      #If the context would need to be created, generate an alternative path
      if not os.path.exists(f"{contextPath}/"):
        symlinkTarget = symlinkTarget.replace(f"{contextPath}/../", f"{buildDir}/scalable/")

      #Check the file to be created doesn't exist
      if os.path.exists(symlinkPath):
        print(f"  {symlinkPath} failed: File exists in place of symlink path")
        failed = True
      #Check the file to link to exists
      if not os.path.exists(symlinkTarget):
        print(f"  {symlinkTarget} failed: Symlink target doesn't exist")
        failed = True

  if failed == True:
    exit(1)


if __name__ == "__main__":
  #Create context dictionary for future reference
  if len(sys.argv) >= 4:
    contextDict = common.createContextDict(sys.argv[3].split())

  #Handle arguments
  if sys.argv[1] == "--install-symlinks":
    #Pass makeSymlinks() the build and install directory
    print("Installing symlinks...")
    makeSymlinks(str(sys.argv[2]), str(sys.argv[4]))
  elif sys.argv[1] == "--check-symlinks":
    #Pass checkSymlinks() the build directory
    checkSymlinks(str(sys.argv[2]))
