import matplotlib.pyplot as plt
import numpy as np
import os

def analyseClickFile(path):
    dataFile = open(path, "r") #Open file in read mode
    cl = 0 #Number of clicks
    er = 0 #Number of errors
    clicks = np.zeros(4) #STA1, STA2, PRE1, PRE2
    meanTimes = np.zeros(4)
    errors = np.zeros(4)
    preTestType = 0
    testType = 0
    while True:
        line = dataFile.readline()
        if (len(line) == 0): #End of file if length of line is 0 so break loop
            break
        readData = line.split(",") #Split data by commas into a list
        preTestType = testType
        if (readData[0].lower() == "standard test1"): #First column indicates what test type it is
            testType = 0
        elif (readData[0].lower() == "standard test2"):
            testType = 1
        elif (readData[0].lower() == "predictive test1"):
            testType = 2
        elif (readData[0].lower() == "predictive test2"):
            testType = 3
        else:
            continue #Skip if not any of the valid tests
        if (preTestType != testType): #If test type has changed, record number of clicks and errors for test type
            clicks[preTestType] = cl
            errors[preTestType] = er
            cl = 0 #Reset for next test type
            er = 0
        cl += 1
        meanTimes[testType] += float(readData[2])
        if (readData[3].lower() == "true\n"):
            er += 1
    clicks[testType] = cl
    errors[testType] = er
    for i in range(len(meanTimes)): #Once all data has been read, calculate mean time between clicks
        meanTimes[i] = meanTimes[i] / clicks[i]
    return meanTimes, errors

def clickResultsAnalysis():
    meanTimes = []
    errors = []
    dir = "./click_results"
    clickFiles = os.listdir(dir) #Store click_results folder and completion folder in same folder as code
    for i in range(len(clickFiles)):
        mt, er = analyseClickFile(dir + "/" + clickFiles[i])
        meanTimes.append(mt)
        errors.append(er)
    meanTimes = np.array(meanTimes) #STA1, STA2, PRE1, PRE2
    errors = np.array(errors)
    meanT = np.mean(meanTimes, axis = 0) #Get mean of each column which represents each test type
    meanE = np.mean(errors, axis = 0)
    stdT = np.std(meanTimes, axis = 0)
    stdE = np.std(errors, axis = 0)
    plotViolinPlot(meanTimes[:, 0], meanTimes[:, 2], "Violin plots comparing Task 1 mean time between clicks between standard and predictive UI", "Time (ms)")
    plotViolinPlot(meanTimes[:, 1], meanTimes[:, 3], "Violin plots comparing Task 2 mean time between clicks between standard and predictive UI", "Time (ms)")
    return meanT, stdT, meanE, stdE

def analyseCompletionFile(path):
    dataFile = open(path, "r") #Open file in read mode
    taskTimes = np.zeros(4)
    clicks = np.zeros(4) #STA1, STA2, PRE1, PRE2
    while True:
        line = dataFile.readline()
        if (len(line) == 0): #End of file if length of line is 0 so break loop
            break
        readData = line.split(",") #Split data by commas into a list
        if (readData[0].lower() == "standard test1"):
            testType = 0
        elif (readData[0].lower() == "standard test2"):
            testType = 1
        elif (readData[0].lower() == "predictive test1"):
            testType = 2
        elif (readData[0].lower() == "predictive test2"):
            testType = 3
        else:
            continue
        taskTimes[testType] = readData[1]
        clicks[testType] = readData[2]
    return taskTimes, clicks


def completionResultsAnalysis():
    taskTimes = []
    clicks = []
    dir = "./completion"
    clickFiles = os.listdir(dir) #Store click_results folder and completion folder in same folder as code
    for i in range(len(clickFiles)):
        tt, cl = analyseCompletionFile(dir + "/" + clickFiles[i])
        taskTimes.append(tt)
        clicks.append(cl)
    taskTimes = np.array(taskTimes)
    clicks = np.array(clicks)
    meanT = np.mean(taskTimes, axis = 0)
    meanC = np.mean(clicks, axis = 0)
    stdT = np.std(taskTimes, axis = 0)
    stdC = np.std(clicks, axis = 0)
    plotViolinPlot(taskTimes[:, 0], taskTimes[:, 2], "Violin plots comparing Task 1 completion times between standard and predictive UI", "Time (ms)")
    plotViolinPlot(taskTimes[:, 1], taskTimes[:, 3], "Violin plots comparing Task 2 completion times between standard and predictive UI", "Time (ms)")
    plotViolinPlot(clicks[:, 0], clicks[:, 2], "Violin plots comparing Task 1 number of taps between standard and predictive UI", "Taps")
    plotViolinPlot(clicks[:, 1], clicks[:, 3], "Violin plots comparing Task 2 number of taps between standard and predictive UI", "Taps")
    return meanT, stdT, meanC, stdC

def plotViolinPlot(dat1, dat2, title, yLabel):
    plt.figure()
    plt.violinplot([dat1, dat2], showmedians = True)
    plt.title(title)
    plt.xticks([1, 2], labels = ["Standard", "Predictive"])
    plt.ylabel(yLabel)
    plt.show()

meanT, stdT, meanE, stdE = clickResultsAnalysis()
print("Format =", ["STA1", "STA2", "PRE1", "PRE2"])
print("Mean time between clicks = ", meanT)
print("Standard deviation of time between clicks", stdT)
print("Mean number of errors = ", meanE)
print("Standard deviation of errors", stdE)

meanT, stdT, meanC, stdC = completionResultsAnalysis()
print("Mean of task completion time = ", meanT)
print("Standard deviation of task completion time", stdT)
print("Mean number of clicks = ", meanC)
print("Standard deviation of clicks", stdC)