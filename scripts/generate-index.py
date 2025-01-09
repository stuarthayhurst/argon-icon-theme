#!/usr/bin/python3
import sys, shutil, csv

def createContextDict():
  #Load info from index/context.csv into a dictionary
  contextDict = {}
  with open("index/context.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
      #contextDict stores the pretty name of the context
      contextDict[row[0]] = row[1]

  return contextDict

def generateIndex(buildDir):
  #Copy index/index.theme.template to buildDir/index.theme
  shutil.copy("index/index.theme.template", buildDir + "/index.theme")

  #Arrays / variables for next loop
  directoryAccumulator = []
  directoryInfo = []

  #Loop through all contexts to build the index
  for iconDir in contextDict:
    #Set icon size
    iconSize = 256
    if (iconDir == "status"):
      iconSize = 16

    #Keep running total of all directories processed
    directoryAccumulator.append("scalable" + "/" + iconDir)

    #Fill in directory.template and index.theme
    directoryInfo.append("")
    directoryInfo.append("[" + "scalable" + "/" + iconDir + "]")
    directoryInfo.append("Size=" + str(iconSize))
    directoryInfo.append("MinSize=8")
    directoryInfo.append("MaxSize=512")
    directoryInfo.append("Context=" + contextDict[iconDir])
    directoryInfo.append("Type=" + "Scalable")

  #Prepare arrays to be written to file
  outputData = [""] + ["Directories=" + ",".join(directoryAccumulator)] + directoryInfo

  #Write outputData to buildDir/index.theme
  with open(buildDir + "/index.theme", "a") as file:
    for line in outputData:
      file.write(line + "\n")

#Load info from index/context.csv into a dictionary
contextDict = createContextDict()

#Pass generateIndex() the build directory
generateIndex(str(sys.argv[1]))
