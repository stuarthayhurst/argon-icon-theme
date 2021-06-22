#!/usr/bin/python3
import sys, glob, os
from icon_builder import isSymlinkBroken

buildDir = str(sys.argv[1])

#Generate a list of directories matching buildDir/*x*
resolutionDirs = []
for directory in glob.glob(buildDir + "/*x*"):
  directory = directory.replace(buildDir + "/", "")
  if os.path.isdir(buildDir + "/" + directory):
    resolutionDirs.append(directory)

#Loop through every file in each resolution directory, and delete if it's missing a matching svg, or it's a broken symlink
deletionList = []
for resolutionDir in resolutionDirs:
  #Iterate through each file, and check criteria
  for file in glob.glob(buildDir + "/" + resolutionDir + "/*/*"):
    #Check if there's a matching svg, schedule deletion otherwise
    svgFile = file.replace(resolutionDir, "scalable")
    svgFile = svgFile.replace(".png", ".svg")
    if os.path.exists(svgFile) == False:
      deletionList.append(file)
    #If the file is a broken symlink, schedule deletion
    elif isSymlinkBroken(file):
      deletionList.append(file)

#Delete everything marked for deletion
for file in deletionList:
  print("  Delete " + file)
  if (os.path.exists(file) or isSymlinkBroken(file)) and (os.path.isdir(file) == False):
    os.remove(file)
  elif (os.path.exists(file) or isSymlinkBroken(file)):
    os.rmdir(file)

#Find empty directories and delete, repeat until no empty directories are found
def listEmptyDirs(dirName):
  emptyDirs = []
  for (dirPath, dirNames, filenames) in os.walk(dirName):
    if len(dirNames) == 0 and len(filenames) == 0 :
      emptyDirs.append(dirPath)
  return emptyDirs

emptyDirs = listEmptyDirs(buildDir)
while emptyDirs != []:
  for emptyDir in emptyDirs:
    print("  Delete " + emptyDir)
    os.rmdir(emptyDir)
  emptyDirs = listEmptyDirs(buildDir)
