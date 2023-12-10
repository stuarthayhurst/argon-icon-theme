#!/usr/bin/python3
import sys, glob, os
from common import getResolutionDirs

def isSymlinkBroken(path):
  if os.path.islink(path):
    #Generate path to symlink target
    linkPath = str(os.path.dirname(path)) + "/" + str(os.readlink(path))
    if os.path.isfile(linkPath) == False:
      #Symlink is broken
      return True
  #Either not a symlink, or not broken
  return False

#Find empty directories and delete, repeat until no empty directories are found
def listEmptyDirs(dirName):
  emptyDirs = []
  for (dirPath, dirNames, filenames) in os.walk(dirName):
    if len(dirNames) == 0 and len(filenames) == 0 :
      emptyDirs.append(dirPath)
  return emptyDirs

#Generate a list of directories matching buildDir/*x*
buildDir = str(sys.argv[1])
resolutionDirs = getResolutionDirs(buildDir)

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

emptyDirs = listEmptyDirs(buildDir)
while emptyDirs != []:
  for emptyDir in emptyDirs:
    print("  Delete " + emptyDir)
    os.rmdir(emptyDir)
  emptyDirs = listEmptyDirs(buildDir)

#Print success message if it was already clean
if len(deletionList) == 0 and len(emptyDirs) == 0:
  print("Directories already clean")
