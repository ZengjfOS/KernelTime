import sys
import csv
import configparser
from os import walk
import re
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

    config = configparser.ConfigParser()
    config.read("config.ini")
    print(config["grepInterval"]["row"])
    print(config["grepInterval"]["col"])

    inputFilesCount = len(inputFiles)
    currentInputFileIndex = 0
    if (inputFilesCount > 0):
        for filename in inputFiles:
            triggerTime, averageTime = getCurveData("input/" + filename, config["grepInterval"]["row"], config["grepInterval"]["col"])
            if len(triggerTime) > 1:

                # 绘制实际触发时间
                plt.subplot(inputFilesCount,  2,  currentInputFileIndex * 2 + 1)
                X1 = list(range(len(triggerTime)))
                plt.plot(X1, triggerTime)
                plt.xlabel("trigger time")

                # 绘制实际间隔触发时间
                plt.subplot(inputFilesCount,  2,  currentInputFileIndex * 2 + 2)
                X2 = list(range(len(averageTime)))
                plt.plot(X2, averageTime, color="m")

                # 计算平均间隔时间线
                average = (sum(averageTime) / len(averageTime))
                # 绘制平均间隔时间，x轴数组，y轴数组
                plt.plot([0, X2[len(averageTime) - 1]], [average, average], "r")

                # 绘制最小间隔时间线
                minData = min(averageTime)
                plt.plot([0, X2[len(averageTime) - 1]], [minData, minData], "g")

                # 绘制最大间隔时间线
                maxData = max(averageTime)
                plt.plot([0, X2[len(averageTime) - 1]], [maxData, maxData], "g")

                plt.xlabel("average time")

                currentInputFileIndex += 1

            else:
                print(triggerTime)
                print(averageTime)
                print("Please check for more data to analysis")
                exit(-1)

        plt.show()

    else:
        print("Please check input file at input dir")


if __name__ == "__main__" :
    sys.exit(main())