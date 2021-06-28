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
                if (filename.startswith("kernel_")):
                    f.append(filename)

    for file in f:
        print(file)

    return f

def main(argv=None) :

    inputFiles = getFiles()
    print(inputFiles)

    config = configparser.ConfigParser()
    config.read("config.ini")
    print(config["sleepWakeup"]["begin"])
    print(config["sleepWakeup"]["end"])

    inputFilesCount = len(inputFiles)
    currentInputFileIndex = 0
    if (inputFilesCount > 0):
        for filename in inputFiles:

            dataArray = []
            sleepWakeupArray = []
            wakeupCount = 0
            sleepWakeupData = []
            with open("input/" + filename, mode="r", encoding='UTF-8') as fd:
                for line in fd:
                    if line.strip().find("CPU1: shutdown") > -1:
                        # print(line)
                        dataArray.append(line.strip())

                    if line.strip().find("suspend wake up by") > -1:
                        # print(line)
                        dataArray.append(line.strip())
                
                # 这里主要检查出系统休眠了多少次，排除没有进入休眠的部分
                for i in range(len(dataArray) - 1):
                    if dataArray[i].strip().find("CPU1: shutdown") > -1:
                        if dataArray[i + 1].strip().find("suspend wake up by") > -1:
                            # print(dataArray[i])
                            # print(dataArray[i + 1])
                            sleepWakeupArray.append(dataArray[i].strip())
                            sleepWakeupArray.append(dataArray[i + 1].strip())

                # for data in sleepWakeupArray:
                #     print(data)

                for i in range(len(sleepWakeupArray) - 1):
                    if sleepWakeupArray[i].strip().find("suspend wake up by") > -1:
                        if sleepWakeupArray[i + 1].strip().find("CPU1: shutdown") > -1:
                            # print(sleepWakeupArray[i])
                            # print(sleepWakeupArray[i + 1])
                            beginEnd = []

                            res = re.search(r'\s+\d+\.\d+',sleepWakeupArray[i])
                            beginEnd.append(float(res.group(0).strip()))
                            # print(float(res.group(0).strip()))

                            res = re.search(r'\s+\d+\.\d+',sleepWakeupArray[i + 1])
                            beginEnd.append(float(res.group(0).strip()))
                            # print(float(res.group(0).strip()))

                            beginEnd.append(beginEnd[1] - beginEnd[0])
                            beginEnd.append(sleepWakeupArray[i])
                            beginEnd.append(sleepWakeupArray[i + 1])
                            # print(beginEnd)

                            sleepWakeupData.append(beginEnd)

            with open("output/" + filename, mode="w", encoding='UTF-8') as fd:
                for data in sleepWakeupData:
                    print(str(data[0]) + ", " + str(data[1]) + ", " + str(data[2]))

                    wakeupCount += 1
                    plt.text(data[0] + 0.2, wakeupCount + 0.1, str(data[2])[:5], fontsize=9)
                    plt.plot([data[0], data[1]], [wakeupCount, wakeupCount], marker='o')

                    fd.write(data[3] + "\n")
                    fd.write(data[4] + "\n")

            print("wake up count: " + str(len(sleepWakeupData)))

            plt.xlabel("Kernel Wakeup Time")
            plt.ylabel("Kernel Wakeup Number")
            plt.title("Kernel Wakeup Status Info")

        plt.show()

    else:
        print("Please check input file at input dir")


if __name__ == "__main__" :
    sys.exit(main())
