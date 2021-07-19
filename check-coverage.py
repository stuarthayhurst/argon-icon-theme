#!/usr/bin/python3
import sys, os
from icon_builder import getResolutionDirs

def listFiles(path):
  return [f.path for f in os.scandir(path)]

def processIcon(icon):
  icon = icon.replace(".symbolic", "")
  icon = icon.rsplit(".", 1)[0]
  return icon

def appendSymlinkDefs(path, context, iconList):
  #Return early if the symlinks doesn't exist
  symlinkDefPath = f"{path}/symlinks/{context}.list"
  if os.path.exists(symlinkDefPath) == False:
    return iconList

  processedSymlinks = []
  with open(symlinkDefPath) as file:
    for line in file.readlines():
      line = line.replace("\n", "")

      #Remove file extensions (filled in later)
      icon = line.split(" -> ")[0]
      icon = processIcon(icon)
      iconList[context][icon] = False

  return iconList

def getIconList(themePath):
  iconList = {}

  #Find all the icons in the given theme
  for resolutionDir in getResolutionDirs(themePath):
    for contextDir in listFiles(f"{themePath}/{resolutionDir}"):
      contextString = f"{contextDir.rsplit('/', 1)[1]}"
      if contextString not in iconList:
        iconList[contextString] = {}
        iconList = appendSymlinkDefs(themePath, contextString, iconList)

      #List the icons in the context and strip down to icon name
      for file in listFiles(f"{contextDir}"):
        icon = file.rsplit("/", 1)[1]
        icon = processIcon(icon)
        iconList[contextString][icon] = False

  return iconList

#Argument handling
if len(sys.argv) <= 1:
  print("A path to a theme is required")
  exit(1)
else:
  if sys.argv[1] == "-h" or sys.argv[1] == "--help": #Display help page
    print("Help:")
    print("  -x | --exclude : Exclude certain context directories from comparison")
    print("  -h | --help    : Display this help page")
    exit(1)

excludedContexts = []
if len(sys.argv) >= 3:
  if sys.argv[2] == "-x" or sys.argv[2] == "--exclude": #Get contexts to exclude
    if len(sys.argv) == 3:
      print("Contexts must be specified to exclude")
      exit(1)
    else:
      for i in range(3, len(sys.argv)):
        excludedContexts.append(sys.argv[i])
else:
  excludeContext = False

#Set the external theme path
externalThemePath = str(sys.argv[1])
if externalThemePath.endswith("/"):
  externalThemePath = externalThemePath.rsplit("/", 1)[0]
if os.path.exists(externalThemePath) == False:
  print(f"Path to theme is invalid ('{externalThemePath}')")
  exit(1)

#Get a full list of icons for the internal and external theme
externalIconList = getIconList(externalThemePath)
internalIconList = getIconList("argon")

totalIconCount = 0
missingIconCount = 0

#Remove excluded contexts
for excludedContext in excludedContexts:
  if excludedContext in externalIconList:
    del externalIconList[excludedContext]

#Work out which icons are missing
for context in list(internalIconList.keys()):
  if context in externalIconList:
    for icon in list(internalIconList[context].keys()):
      externalIconList[context][icon] = True

#Loop through contexts of external icon theme and compare against internal icons theme
for context in list(externalIconList.keys()):
  missingIcons = []

  #Separate missing icons
  for icon in list(externalIconList[context].keys()):
    if externalIconList[context][icon] == False:
      missingIcons.append(icon)

  #Alphabetically sort and display missing icons
  if missingIcons != []:
    print(f"{context.capitalize()}:")
    missingIcons.sort()
    for icon in missingIcons:
      print(f" - {icon}")
    missingIconCount += len(missingIcons)

for i in list(externalIconList.keys()):
  totalIconCount += len(list(externalIconList[i].keys()))

print(f"\n{totalIconCount - missingIconCount}/{totalIconCount} icons themed")
print(f"{missingIconCount}/{totalIconCount} icons missing")
print(f"{round((((totalIconCount - missingIconCount) / totalIconCount) * 100), 2)}% theme coverage")
