#!/usr/bin/python3
#Remove rubbish from svg files

import glob
import xml.etree.ElementTree as et
from icon_builder import getResolutionDirs

buildDir = "argon"
et = et.ElementTree()

def cleanFile(inputFile):
  #Find metadata tag in document
  root = et.parse(inputFile)
  metadata = root.find("{http://www.w3.org/2000/svg}metadata")

  #Remove if present
  if metadata != None:
    root.remove(metadata)
    et.write(inputFile)
  else:
    print(f"{file} has no metadata tag")

#Loop through all svgs
for file in glob.glob(f"{buildDir}/scalable/*/*"):
  cleanFile(file)

print("Cleaned all files")
