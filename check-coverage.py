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
  #Return early if the symlink definitions don't exist
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
        if file.endswith('.png') or file.endswith('.svg'):
          icon = file.rsplit("/", 1)[1]
          icon = processIcon(icon)
          iconList[contextString][icon] = False

  return iconList

#Attempt to find the theme on the system and return a valid path, or return False
def findTheme(themePath):
  themeName = themePath.rsplit("/", 1)
  themeName = themeName[len(themeName) - 1]
  if os.path.exists(f"/usr/share/icons/{themeName}"):
    return f"/usr/share/icons/{themeName}"
  else:
    return False

#Argument handling
if len(sys.argv) <= 1:
  print("A path to a theme is required")
  exit(1)
else:
  if sys.argv[1] == "-h" or sys.argv[1] == "--help": #Display help page
    print("Help:")
    print("  -i | --include : Only use certain contexts in comparison")
    print("  -x | --exclude : Exclude certain contexts from comparison")
    print("  -h | --help    : Display this help page")
    exit(1)

contextsMode = False
customContexts = []
if len(sys.argv) >= 3:
  if sys.argv[2] == "-x" or sys.argv[2] == "--exclude": #Get contexts to exclude
    if len(sys.argv) == 3:
      print("Contexts must be specified to exclude")
      exit(1)
    else:
      contextsMode = "exclude"
  elif sys.argv[2] == "-i" or sys.argv[2] == "--include": #Get contexts to include
    if len(sys.argv) == 3:
      print("Contexts must be specified to exclude")
      exit(1)
    else:
      contextsMode = "include"

  #Save the specific contexts to include / exclude
  for i in range(3, len(sys.argv)):
    customContexts.append(sys.argv[i])

#Set the external theme path
externalThemePath = str(sys.argv[1])
if externalThemePath.endswith("/"):
  externalThemePath = externalThemePath.rsplit("/", 1)[0]

externalThemePath = findTheme(externalThemePath)
if externalThemePath == False:
  print(f"Path to theme is invalid ('{sys.argv[1]}')")
  exit(1)

#Get a full list of icons for the internal and external theme
externalIconList = getIconList(externalThemePath)
internalIconList = getIconList("argon")

totalIconCount = 0
missingIconCount = 0

#Remove excluded contexts
if contextsMode == "exclude":
  for customContext in customContexts:
    if customContext in externalIconList:
      del externalIconList[customContext]
#If any of the keys from externalIconList are in customContexts, remove them
elif contextsMode == "include":
  #Iterate through keys beforehand, to avoid dictionary changing size while being iterated
  keys = [ i for i in externalIconList.keys() ]
  for customContext in keys:
    if customContext not in customContexts:
      del externalIconList[customContext]

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
  else:
    print(f"No missing icons in '{context}'")

for i in list(externalIconList.keys()):
  totalIconCount += len(list(externalIconList[i].keys()))

if totalIconCount > 0:
  print(f"\n{totalIconCount - missingIconCount}/{totalIconCount} icons themed")
  print(f"{missingIconCount}/{totalIconCount} icons missing")
  print(f"{round((((totalIconCount - missingIconCount) / totalIconCount) * 100), 2)}% theme coverage")
else:
  print("No icons found matching the requirements")
