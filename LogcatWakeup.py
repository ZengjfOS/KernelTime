import sys
import csv
import configparser
from os import walk
import re
from matplotlib import pyplot as plt
import datetime
import time

def getFiles() :

    f = []
    for (dirpath, dirnames, filenames) in walk("input") :
        for filename in filenames:
            if filename != "empty":
                if (filename.startswith("main_")):
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
    print(config["logcatWakeup"]["begin"])
    print(config["logcatWakeup"]["end"])

    inputFilesCount = len(inputFiles)
    currentInputFileIndex = 0
    if (inputFilesCount > 0):
        for filename in inputFiles:

            preTime = None
            currentTime = None
            preLine = None
            lineArray = []
            dateXArray = []
            dateYArray = []
            with open("input/" + filename, mode="r", encoding='UTF-8') as fd:
                for line in fd:

                    res = re.search(r'\d+-\d+\s\d+:\d+:\d+\.\d+', line.strip())
                    if res != None:
                        timeString = "2021-" + res.group(0).strip()
                        print(timeString)

                        [t_second, t_microsecond] = timeString.split('.')
                        t_second = time.mktime(datetime.datetime.strptime(t_second, "%Y-%m-%d %H:%M:%S").timetuple())
                        # a_time = str(t_second + 8 * 60 * 60) + t_microsecond
                        a_time = str(t_second).split('.')[0] + "." + t_microsecond
                        print("a_time " + a_time)

                        currentTime = float(a_time)
                        if preTime == None:
                            preTime = currentTime
                        print(currentTime)
                        print(preTime)

                        if (currentTime - preTime) > 0.4:
                            lineArray.append(preLine.strip())
                            lineArray.append(line.strip())
                        else:
                            if line.strip().find("BatteryStatsService: In wakeup_callback: resumed from suspend") > -1:
                                lineArray.append(line.strip())
                            
                        preTime = currentTime
                        preLine = line

                    else:
                        continue
                
                preLine = None
                with open("output/" + filename, mode="w", encoding='UTF-8') as fd:
                    for line in lineArray:
                        print(line)

                        if preLine == None:
                            preLine = line
                            fd.write(line + "\n")
                        else:
                            if preLine != line:
                                fd.write(line + "\n")
                        
                        preLine = line

                wakeupCount = 0
                with open("output/" + filename, mode="r", encoding='UTF-8') as fd:
                    for line in fd:
                        if line.strip().find("BatteryStatsService: In wakeup_callback: resumed from suspend") > -1:
                            # res = re.search(r'\d+:\d+:\d+\.\d+', line)
                            res = re.search(r'\d+-\d+\s\d+:\d+:\d+\.\d+', line.strip())
                            timeString = "2021-" + res.group(0).strip()
                            print(line.strip())
                            print(timeString)

                            wakeupCount += 1
                            
                            currentDate = datetime.datetime.strptime(timeString.split(".")[0], "%Y-%m-%d %H:%M:%S")
                            plt.plot(currentDate, wakeupCount, 'o')
                            plt.plot([currentDate, currentDate], [wakeupCount, 0])

            print("wake up count: " + str(wakeupCount))

        plt.xlabel("X Date Time")
        plt.ylabel("Y Wakeup Number")
        plt.title("Logcat Wakeup Status Info")
        plt.show()

    else:
        print("Please check input file at input dir")


if __name__ == "__main__" :
    sys.exit(main())
