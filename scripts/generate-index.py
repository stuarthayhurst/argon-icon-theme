#!/usr/bin/python3
import sys, shutil, csv

def createContextList():
  #Load info from index/context.csv into a list
  contextList = []
  with open("index/context.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
      contextList.append({
        "context": row[0],
        "name": row[1],
        "type": row[2],
        "size": row[3]
      })

  return contextList

def generateIndex(buildDir):
  #Copy index/index.theme.template to buildDir/index.theme
  shutil.copy("index/index.theme.template", buildDir + "/index.theme")

  #Arrays / variables for next loop
  directoryAccumulator = []
  directoryInfo = []

  #Loop through all contexts to build the index
  for dirInfo in contextList:
    #Keep running total of all directories processed
    directoryAccumulator.append(f"{dirInfo['type']}/{dirInfo['context']}")

    #Fill in directory.template and index.theme
    directoryInfo.append("")
    directoryInfo.append(f"[{dirInfo['type']}/{dirInfo['context']}]")
    directoryInfo.append(f"Size={dirInfo['size']}")
    directoryInfo.append("MinSize=8")
    directoryInfo.append("MaxSize=512")
    directoryInfo.append(f"Context={dirInfo['name']}")
    directoryInfo.append("Type=Scalable")

  #Prepare arrays to be written to file
  outputData = [""] + ["Directories=" + ",".join(directoryAccumulator)] + directoryInfo

  #Write outputData to buildDir/index.theme
  with open(buildDir + "/index.theme", "a") as file:
    for line in outputData:
      file.write(line + "\n")

#Load info from index/context.csv into a list
contextList = createContextList()

#Pass generateIndex() the build directory
generateIndex(str(sys.argv[1]))
