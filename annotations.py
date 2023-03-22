# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import pandas as pd
import neurokit2 as nk
from mat4py import loadmat
import scipy.io
import matplotlib.pyplot as plt
import sys


class Heartbeat:

    def __init__(self, TWave, PWave, RWave):
        self.TWave = TWave
        self.PWave = PWave
        self.RWave = RWave


class wave:
    def __init__(self, start, end):
        self.start = start
        self.end = end


def pointFinder(startR, endR, startT, endT, startP, endP, signal_cwt):
    # all this does is finds the starts and endpoints for every heartbeat found in the signal
    for i in range(5000):
        if signal_cwt['ECG_R_Onsets'][i] != 0:
            startR.append(i)

        if signal_cwt['ECG_R_Offsets'][i] != 0:
            endR.append(i)

        if signal_cwt['ECG_T_Onsets'][i] != 0:
            startT.append(i)

        if signal_cwt['ECG_T_Offsets'][i] != 0:
            endT.append(i)

        if signal_cwt['ECG_P_Onsets'][i] != 0:
            startP.append(i)

        if signal_cwt['ECG_P_Offsets'][i] != 0:
            endP.append(i)


def cleanArrays(start, end, leeway):
    listWaves = []
    # finds the shorter of the two so we don't run into overflows
    if len(start) < len(end):
        j = len(start)
    else:
        j = len(end)
    # seperate pointer variables
    x = 0
    y = 0

    while x < j or y < j:
        # if we have a valid wave
        if 0 < end[y] - start[x] < leeway:
            listWaves.append(wave(start[x], end[y]))
            x += 1
            y += 1
        # if the algorithm missed the start of the wave. Ex. algorithm found end[0] but start[0] corresponds to heartbeat 2
        elif end[y] - start[x] < 0:
            y += 1
        # if the algorithm missed the end of the wave
        elif end[y] - start[x] > leeway:
            x += 1

    return listWaves


def createHeartbeats(TWave, PWave, RWave):
    # Finding the smallest array
    if len(TWave) - 1 < len(PWave) - 1:
        if len(TWave) - 1 < len(RWave) - 1:
            j = len(TWave) - 1
        else:
            j = len(RWave) - 1
    # If PWave is smaller than TWave
    else:
        if len(PWave) - 1 < len(RWave) - 1:
            j = len(PWave) - 1
        else:
            j = len(RWave) - 1

    x = 0
    y = 0
    z = 0
    heartbeatList = []
    while x < j or y < j or z < j:
        # if missing P-wave
        # validating that P-wave is higher than the other two waves and that the other two waves are correct
        if RWave[y].start < PWave[x].start and PWave[x].start > TWave[z].start and RWave[y].start < TWave[z].start:
            # if the p-wave is higher than the other two, the other two waves become invalid and we iterate
            y += 1
            z += 1

        # if missing R-wave
        # Validating start of RWave is greater than TWave and the other two waves are vaild
        elif RWave[y].start > TWave[z].start and PWave[x].start < TWave[z].start:
            x += 1
            z += 1

        # If P-Wave and R-Wave are missing
        elif PWave[x].start > TWave[z].start and RWave[y].start > TWave[z].start:
            z += 1

        # if missing T-Wave
        # if T-Wave is in the next heartbeat
        elif TWave[z].start > PWave[x + 1].start:
            # if P-Wave is in the next heartbeat
            if PWave[x].start > RWave[y].start:
                y += 1

            # If R-Wave is in the next heartbeat
            elif RWave[y].start > PWave[x + 1].start:
                x += 1

            # Just the T-Wave is in the next heartbeat
            else:
                x += 1
                y += 1

        # if wave is valid
        elif RWave[y].start < TWave[z].start and RWave[y].start > PWave[x].start:
            heartbeatList.append(Heartbeat(TWave[z], PWave[x], RWave[y]))
            x += 1
            y += 1
            z += 1

    return heartbeatList


def find3Waves(validHeartbeats, leeway):
    start = 0
    end = 0
    i = 0

    while i in range(0, len(validHeartbeats) - 1):
        # finds if two pwaves are together by checking it against a leeway
        if validHeartbeats[i + 1].PWave.start - validHeartbeats[i].PWave.start < leeway:
            end += 1

        # If the pwaves are not together, we reset the starting point and do it again
        else:
            start = i + 1
            end = 0

        # since the statements above checks the if the current and next heartbeat are together, we only need end to be a value of 2 here
        if end == 2:
            return start
        i += 1

def makeRWaveAnnotation(validHeartbeats, start, offset):
        for i in range(0, 3):
            plt.axvspan(validHeartbeats[start+i].RWave.start - offset, validHeartbeats[start+i].RWave.end - offset, facecolor = 'orange', alpha = 0.5, label = 'R-Wave' if i == 0 else "")

def makeTWaveAnnotation(validHeartbeats, start, offset):
    for i in range(0, 3):
        plt.axvspan(validHeartbeats[start+i].TWave.start - offset, validHeartbeats[start+i].TWave.end - offset, facecolor = 'red', alpha = 0.5, label = 'T-Wave' if i == 0 else "")

def makePWaveAnnotation(validHeartbeats, start, offset):
    for i in range(0, 3):
        plt.axvspan(validHeartbeats[start+i].PWave.start - offset, validHeartbeats[start+i].PWave.end - offset, facecolor = 'green', alpha = 0.5, label = 'P-Wave' if i == 0 else "")


# BAD DATA: 4, 6, 20, 31, 36

def makeGraph(name):
    data = scipy.io.loadmat(name)

    mat_list = []

    for j in range(5000):
        mat_list.append(data['val'][1][j])

    np_array = np.array(mat_list)
    _, rpeaks = nk.ecg_peaks(np_array, sampling_rate=500)

    signal_cwt, waves_cwt = nk.ecg_delineate(np_array, rpeaks, sampling_rate=500, method="cwt")

    startR = []
    endR = []
    startT = []
    endT = []
    startP = []
    endP = []

    # This function cleans up the starting and ending points by putting it into arrays by themselves
    pointFinder(startR, endR, startT, endT, startP, endP, signal_cwt)

    # Further cleans up the arrays and puts them into the wave classes
    PWaves = cleanArrays(startP, endP, 100)
    TWaves = cleanArrays(startT, endT, 150)
    RWaves = cleanArrays(startR, endR, 150)

    # finds and stores all valid heartbeats into the heartbeat class
    validHeartbeats = createHeartbeats(TWaves, PWaves, RWaves)

    # Finds 3 heartbeats in a row that we can output
    start = find3Waves(validHeartbeats, 700)

    # checks and gives an error statement if the matlab file cannot be used
    if start == None:
        sys.exit("There are not 3 valid heartbeats in a row")

    # offset to make the graph look better
    offset = validHeartbeats[start].PWave.start - 100

    # Matlab plotting stuff
    plt.plot(np_array[offset:validHeartbeats[start + 2].TWave.end + 200])

    #Calls the highlight annotation functions for each wave you need annotated in this ECG
    makeRWaveAnnotation(validHeartbeats, start, offset)
    makeTWaveAnnotation(validHeartbeats, start, offset)
    makePWaveAnnotation(validHeartbeats, start, offset)

    plt.title(name)
    plt.legend()
    plt.show()

    # Saves the plot as an svg file
    plt.savefig("test1", format="svg", dpi=1200)