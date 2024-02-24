#!/usr/bin/python3
import glob, os, re, csv

allIconResolutions = [8, 16, 22, 24, 32, 48, 64, 128, 256]

def getResolutionDirs(searchPath):
  #Generate a list of directories matching searchPath/*x*
  resolutionDirs = []
  for directory in glob.glob(f"{searchPath}/*x*"):
    directory = directory.replace(f"{searchPath}/", "")
    if os.path.isdir(f"{searchPath}/{directory}"):
      if re.search("^([0-9]+x[0-9]+)", directory):
        resolutionDirs.append(directory)

  #Order directories numerically by resolution
  resolutionDirs.sort(key=lambda x: int(x.split("x")[0]))
  resolutionDirs.append("scalable")

  return resolutionDirs

def getMaxResolutionList(maxResolution):
  #Loop through given resolutions, add to a return array if it's less than the max
  allowedResolutions = []
  for resolution in allIconResolutions:
    if int(resolution) <= int(maxResolution):
      allowedResolutions.append(f"{resolution}x{resolution}")
  allowedResolutions.append("scalable")

  #Return an array of valid resolutions to build for
  return allowedResolutions

def createContextDict():
  #Load info from index/context.csv into a dictionary
  contextDict = {}
  with open("index/context.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
      #contextDict stores the pretty name and array of max resolutions for the context
      #contextDict["context"] = ["pretty name", ["allowed", "resolutions"]]
      contextDict[row[0]] = [row[1], getMaxResolutionList(row[2])]
  return contextDict
