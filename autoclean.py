#!/usr/bin/python3
import sys, glob, os

buildDir = str(sys.argv[1])

#Generate a list of directories matching buildDir/*x*
resolutionDirs = []
for directory in glob.glob(buildDir + "/*x*"):
  directory = directory.replace(buildDir + "/", "")
  if os.path.isfile(buildDir + "/" + directory) == False:
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

    #Check if the file is actually a symlink, and schedule deletion if it's broken
    if os.path.islink(file):
      #Generate path to symlink target
      linkPath = str(file.rsplit("/", 1)[0]) + "/" + str(os.readlink(file))
      if os.path.isfile(linkPath) == False:
        deletionList.append(file)

#Delete everything marked for deletion
for file in deletionList:
  print("  Delete " + file)
  if os.path.isfile(file):
    os.remove(file)
  elif os.path.isdir(file):
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
