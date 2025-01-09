#!/usr/bin/python3
import sys, glob, os, shutil

def createSymlinkDict(buildDir):
  #Read all the symlinks to create into memory and create a data structure for them
  #  symlinkDict["apps"][0]["symlink"] would return the name of a symlink to create
  symlinkLists = glob.glob(buildDir + "/symlinks/*")
  symlinkDict = {}

  for listFile in symlinkLists:
    contextDir = os.path.basename(listFile)
    contextDir = "".join(contextDir.rsplit(".list", 1))

    isSymbolic = contextDir.endswith("-symbolic")
    iconType = "scalable"
    if isSymbolic:
      contextDir = contextDir.removesuffix("-symbolic")
      iconType = "symbolic"

    processedSymlinks = []
    with open(listFile) as file:
      for line in file.readlines():

        #Strip newline before checking for contents, otherwise empty lines aren't caught
        line = line.replace("\n", "")

        if line != "":
          line = line.split(" -> ")
          line = {
            "type": iconType,
            "symlink": line[0],
            "target": line[1]
          }
          processedSymlinks.append(line)
        else:
          print(f"Empty line in '{listFile}', please fix this")

    if contextDir in symlinkDict:
      symlinkDict[contextDir] += processedSymlinks
    else:
      symlinkDict[contextDir] = processedSymlinks
  return symlinkDict

def makeSymlinks(buildDir, installDir):
  #Create dictionary with symlink information
  symlinkDict = createSymlinkDict(buildDir)

  #Check permissions for creating symlinks
  if not os.access(installDir, os.W_OK):
    print(f"No write permission for {installDir}, try running with root")
    exit(1)

  #Install the icons for the contexts
  for contextDir in symlinkDict:
    for symlinkObject in symlinkDict[contextDir]:
      #Get resolutions to generate symlinks for specific context
      path = f"{installDir}/{symlinkObject['type']}/{contextDir}/"

      #Create context directory if missing
      if not os.path.isdir(path):
        os.makedirs(path)

      shutil.copy(f"{path}{symlinkObject['target']}", f"{path}{symlinkObject['symlink']}")

def checkSymlinks(buildDir):
  #Create dictionary with symlink information
  symlinkDict = createSymlinkDict(buildDir)
  failed = False

  #Loop through every symlink info object, and validate the contents
  for context in symlinkDict:
    for symlinkObject in symlinkDict[context]:
      contextPath = f"{buildDir}/{symlinkObject['type']}/{context}"
      symlinkPath = f"{contextPath}/{symlinkObject['symlink']}"
      symlinkTarget = f"{contextPath}/{symlinkObject['target']}"

      #If the context would need to be created, generate an alternative path
      if not os.path.exists(f"{contextPath}/"):
        symlinkTarget = symlinkTarget.replace(f"{contextPath}/../",
                                              f"{buildDir}/{symlinkObject['type']}/")

      #Check the file to be created doesn't exist
      if os.path.exists(symlinkPath):
        print(f"  {symlinkPath} failed: File exists in place of symlink path")
        failed = True
      #Check the file to link to exists
      if not os.path.exists(symlinkTarget):
        print(f"  {symlinkTarget} failed: Symlink target doesn't exist")
        failed = True

  if failed:
    exit(1)

#Handle arguments
if sys.argv[1] == "--install-symlinks":
  #Pass makeSymlinks() the build and install directory
  print("Installing symlinks...")
  makeSymlinks(str(sys.argv[2]), str(sys.argv[3]))
elif sys.argv[1] == "--check-symlinks":
  #Pass checkSymlinks() the build directory
  checkSymlinks(str(sys.argv[2]))
