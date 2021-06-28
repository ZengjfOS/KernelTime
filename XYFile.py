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

def charIndexs(data, ch):
    pos = []

    for i in range(len(data)):
        if ch == data[i]:
            pos.append(i)    
    
    return pos

def main(argv=None) :

    inputFiles = getFiles()
    print(inputFiles)

    inputFilesCount = len(inputFiles)
    if (inputFilesCount > 0):
        for filename in inputFiles:
            inLines = []
            outLines = []
            lineCount = 0
            maxColumn = 0

            outputFileName = "output/" + filename.split(".")[0] + ".txt"
            if os.path.exists(outputFileName):
                os.remove(outputFileName)

            with open("input/" + filename, "r") as inputfile:
                with open(outputFileName, "w+") as outputfile:
                        
                    # 计算所有的行以及最大的列
                    for line in inputfile:
                        line = line.replace("\n", "")
                        inLines.append(line)
                        currentColumn = len(line)

                        if maxColumn < currentColumn:
                            maxColumn = currentColumn

                        lineCount += 1

                    print(maxColumn)

                    # 填充列，因为要转成行，列变行
                    for index in range(0, lineCount):
                        line = inLines[index].ljust(maxColumn, "-")
                        inLines[index] = line

                    print(inLines)

                    # 添加输出行
                    for index in range(0, maxColumn):
                        outLines.append("")

                    # 行变列
                    for colum in range(0, maxColumn):
                        for row in range(0, lineCount):
                            outLines[colum] += (inLines[row][colum])
                    
                    print(outLines)

                    # xy文件
                    # for colum in range(0, maxColumn):
                    #     outputfile.write(outLines[colum] + "\n")

                    intervalLine = 2
                    for index in range(0, maxColumn - intervalLine):

                        if (index % intervalLine == 0):
                            print(outLines[index])
                            currentStarList = charIndexs(outLines[index], "*")
                            nextStarList = charIndexs(outLines[index + intervalLine], "*")

                            print(str(currentStarList) + ", " + str(nextStarList))

                            if len(currentStarList) > 0 and len(nextStarList) > 0:
                                if len(currentStarList) == 1 :
                                    for number in range(currentStarList[0], nextStarList[-1]):
                                        outLines[index].replace()

                    for colum in range(0, maxColumn):
                        outputfile.write(outLines[colum] + "\n")


    else:
        print("Please check input file at input dir")

    return 0


if __name__ == "__main__" :
    sys.exit(main())