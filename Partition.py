import sys
import csv
import configparser
import os
import re
from os import walk
from matplotlib import pyplot as plt

def getFiles() :

    f = []
    for (dirpath, dirnames, filenames) in walk("input") :
        for filename in filenames:
            if filename != "empty":
                f.append(filename)

    for file in f:
        print(file)

    return f

def getCurveData(file, row, col):

    triggerTime = []
    preTime = 0
    averageTime = []

    with open(file, mode="r", encoding="utf-8") as fd:
        for line in fd:
            if line.strip().find(row) > -1:
                lineText = line.strip()
                # res = re.search('\[\s*\d+\.\d+\s*\]',lineText)
                res = re.search(col,lineText)
                currentTime = float(res.group(0))
                triggerTime.append(currentTime)

                if preTime != 0 :
                    diffTime = currentTime - preTime
                    if (diffTime > 1):
                        print(line)
                    averageTime.append(diffTime)
                
                
                preTime = currentTime

    return triggerTime, averageTime

def main(argv=None) :

    inputFiles = getFiles()
    print(inputFiles)


    inputFilesCount = len(inputFiles)
    if (inputFilesCount > 0):
        for filename in inputFiles:
            outputFileName = "output/" + filename.split(".")[0] + ".csv"
            if os.path.exists(outputFileName):
                os.remove(outputFileName)

            with open("input/" + filename, "r") as inputfile:
                with open(outputFileName, "w+") as outputfile:

                    outputfile.write("Name,Start(byte),size(byte)\n")

                    for line in inputfile:
                        if "partition_name" in line \
                                or "physical_start_addr" in line:
                            print(line.split(":")[1].strip())
                            outputfile.write(line.split(":")[1].strip() + ",")

                        if "partition_size" in line:
                            print(line.split(":")[1].strip() + "\n")
                            outputfile.write(line.split(":")[1].strip() + "\n")

    else:
        print("Please check input file at input dir")

    return 0


if __name__ == "__main__" :
    sys.exit(main())