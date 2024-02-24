#!/usr/bin/python3
import sys, shutil
import common

def generateIndex(buildDir):
  #Copy index/index.theme.template to buildDir/index.theme
  shutil.copy("index/index.theme.template", buildDir + "/index.theme")

  #Arrays / variables for next loop
  directoryAccumulator = []
  directoryInfo = []

  #Loop through all contexts
  for iconDir in contextDict:
    #Loop through all resolutions that apply to current context
    for iconResolution in contextDict[iconDir][1]:
      #Generate values for index entry
      if iconResolution == "scalable":
        iconSize = 256
        iconType = "Scalable"
      else:
        iconSize = iconResolution.split("x")[0]
        iconType = "Fixed"

      #Keep running total of all dirs processed
      directoryAccumulator.append(iconResolution + "/" + iconDir)

      #Fill in directory.template and index.theme
      directoryInfo.append("")
      directoryInfo.append("[" + iconResolution + "/" + iconDir + "]")
      directoryInfo.append("Size=" + str(iconSize))
      directoryInfo.append("Context=" + contextDict[iconDir][0])
      directoryInfo.append("Type=" + iconType)

  #Prepare arrays to be written to file
  outputData = [""] + ["Directories=" + ",".join(directoryAccumulator)] + directoryInfo

  #Write outputData to buildDir/index.theme
  with open(buildDir + "/index.theme", "a") as file:
    for line in outputData:
      file.write(line + "\n")

#Load info from index/context.csv into a dictionary
contextDict = common.createContextDict()

#Pass generateIndex() the build directory
generateIndex(str(sys.argv[1]))
