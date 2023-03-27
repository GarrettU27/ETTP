import numpy as np
import pandas as pd
import neurokit2 as nk
from mat4py import loadmat
import scipy.io
import matplotlib.pyplot as plt
import sys
import io


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


class Heartbeat:

    def __init__(self, TWave, PWave, RWave):
        self.TWave = TWave
        self.PWave = PWave
        self.RWave = RWave


class wave:
    def __init__(self, start, end):
        self.start = start
        self.end = end


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

def makeRWaveAnnotation(validHeartbeats, start, offset, ax):
    for i in range(0, 3):
        ax.axvspan(validHeartbeats[start+i].RWave.start - offset, validHeartbeats[start+i].RWave.end - offset, facecolor = 'orange', alpha = 0.5, label = 'R-Wave' if i == 0 else "")

def makeTWaveAnnotation(validHeartbeats, start, offset, ax):
    for i in range(0, 3):
        ax.axvspan(validHeartbeats[start + i].TWave.start - offset, validHeartbeats[start + i].TWave.end - offset,facecolor='red', alpha=0.5, label='T-Wave' if i == 0 else "")

def makePWaveAnnotation(validHeartbeats, start, offset, ax):
    for i in range(0, 3):
        ax.axvspan(validHeartbeats[start+i].PWave.start - offset, validHeartbeats[start+i].PWave.end - offset, facecolor = 'green', alpha = 0.5, label = 'P-Wave' if i == 0 else "")

def scanData(np_array):

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

    # declares where the startPoint is
    startPoint = validHeartbeats[start].PWave.start - 100
    endPoint = validHeartbeats[start + 2].TWave.end + 200

    return startPoint, validHeartbeats, start, endPoint

def return_svg_bytes():
    fig = plt.gcf()
    plt.ioff()

    buf = io.BytesIO()
    fig.savefig(buf, format="svg")
    buf.seek(0)

    return buf.read()

def plotLead1(ax, data, annotate, startPoint, endPoint):
    ax.set_title('Lead 1')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint])


def plotLead2(ax, data, annotate, startPoint, endPoint):
    ax.set_title('Lead 2')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint])

    elif annotate == 'basic':

        startPoint, validHeartbeats, start, endPoint = scanData(data)
        ax.plot(data[startPoint:endPoint])

        makeRWaveAnnotation(validHeartbeats, start, startPoint, ax)
        makeTWaveAnnotation(validHeartbeats, start, startPoint, ax)
        makePWaveAnnotation(validHeartbeats, start, startPoint, ax)

        ax.legend()


def plotLead3(ax, data, annotate, startPoint, endPoint):
    ax.set_title('Lead 3')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint])


def plotLeadaVR(ax, data, annotate, startPoint, endPoint):
    ax.set_title('Lead aVR')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint])


def plotLeadaVL(ax, data, annotate, startPoint, endPoint):
    ax.set_title('Lead aVL')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint])


def plotLeadaVF(ax, data, annotate, startPoint, endPoint):
    ax.set_title('Lead aVF')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint])


def plotLeadV1(ax, data, annotate, startPoint, endPoint):
    ax.set_title('Lead V1')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint])


def plotLeadV2(ax, data, annotate, startPoint, endPoint):
    ax.set_title('Lead V2')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint])


def plotLeadV3(ax, data, annotate, startPoint, endPoint):
    ax.set_title('Lead V3')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint])

def plotLeadV4(ax, data, annotate, startPoint, endPoint):
    ax.set_title('Lead V4')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint])


def plotLeadV5(ax, data, annotate, startPoint, endPoint):
    ax.set_title('Lead V5')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint])


def plotLeadV6(ax, data, annotate, startPoint, endPoint):
    ax.set_title('Lead V6')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint])


def plot12ECGs(data, nameOfArrhythmia):
    annotations = []
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(20, 20))

    # Sets up our 12 axis
    ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12 = axs.flatten()

    #setting it to basic for now
    nameOfArrhythmia = 'basic'

    # This is where we will change what each arrhythmia does
    if nameOfArrhythmia == 'basic':
        annotations = ['none', 'none', 'none', 'none', 'basic', 'none', 'none', 'none', 'none', 'none', 'none', 'none']

        # We need to get the startpoint and endpoints for the graphs first
        # In the basic example, we are annotating lead 2 so we will get those start/endpoints for the whole graph
        startPoint, _, _, endPoint = scanData(data['val'][1])

    # Plotting leads in order
    # We will have to custom code the annotations array for every annotation we do
    # This means that setting the annotations must be done for every case
    # And every case we do must be added to the plotting functions above
    plotLead1(ax1, data['val'][0], annotations[0], startPoint, endPoint)
    plotLeadaVR(ax2, data['val'][3], annotations[1], startPoint, endPoint)
    plotLeadV1(ax3, data['val'][6], annotations[2], startPoint, endPoint)
    plotLeadV4(ax4, data['val'][9], annotations[3], startPoint, endPoint)
    plotLead2(ax5, data['val'][1], annotations[4], startPoint, endPoint)
    plotLeadaVL(ax6, data['val'][4], annotations[5], startPoint, endPoint)
    plotLeadV2(ax7, data['val'][7], annotations[6], startPoint, endPoint)
    plotLeadV5(ax8, data['val'][10], annotations[7], startPoint, endPoint)
    plotLead3(ax9, data['val'][2], annotations[8], startPoint, endPoint)
    plotLeadaVF(ax10, data['val'][5], annotations[9], startPoint, endPoint)
    plotLeadV3(ax11, data['val'][8], annotations[10], startPoint, endPoint)
    plotLeadV6(ax12, data['val'][11], annotations[11], startPoint, endPoint)

    plt.show()

    # getting the svgbites of our figure and returning it
    svgBites = return_svg_bytes()
    return svgBites

