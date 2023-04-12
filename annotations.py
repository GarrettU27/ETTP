import io
import math
import sys

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import neurokit2 as nk
from scipy.io import loadmat


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


def createHeartbeats(t_waves, p_waves, r_waves):
    # Finding the smallest array
    j = min(len(t_waves), len(p_waves), len(r_waves)) - 1

    pwave_index = 0
    rwave_index = 0
    twave_index = 0
    heartbeat_list = []

    # This goes through all our waves and tries to find valid triplets, where there's first a t wave, then an r wave
    # and finally a p wave. Once it finds a valid triplet, its added to the list of heartbeats
    while pwave_index < j or rwave_index < j or twave_index < j:
        r_wave_start_index = r_waves[rwave_index].start
        p_wave_start_index = p_waves[pwave_index].start
        t_wave_start_index = t_waves[twave_index].start

        # if missing P-wave
        # validating that P-wave is higher than the other two waves and that the other two waves are correct
        if r_wave_start_index < p_wave_start_index and p_wave_start_index > t_wave_start_index > r_wave_start_index:
            # if the p-wave is higher than the other two, the other two waves become invalid and we iterate
            rwave_index += 1
            twave_index += 1

        # if missing R-wave
        # Validating start of RWave is greater than TWave and the other two waves are vaild
        elif r_wave_start_index > t_wave_start_index > p_wave_start_index:
            pwave_index += 1
            twave_index += 1

        # If P-Wave and R-Wave are missing
        elif p_wave_start_index > t_wave_start_index and r_wave_start_index > t_wave_start_index:
            twave_index += 1

        # if missing T-Wave
        # if T-Wave is in the next heartbeat
        elif t_wave_start_index > p_waves[pwave_index + 1].start:
            # if P-Wave is in the next heartbeat
            if p_wave_start_index > r_wave_start_index:
                rwave_index += 1

            # If R-Wave is in the next heartbeat
            elif r_wave_start_index > p_waves[pwave_index + 1].start:
                pwave_index += 1

            # Just the T-Wave is in the next heartbeat
            else:
                pwave_index += 1
                rwave_index += 1

        # if wave is valid
        elif t_wave_start_index > r_wave_start_index > p_wave_start_index:
            heartbeat_list.append(Heartbeat(t_waves[twave_index], p_waves[pwave_index], r_waves[rwave_index]))
            pwave_index += 1
            rwave_index += 1
            twave_index += 1

    return heartbeat_list


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


def makeRWaveAnnotation(validHeartbeats, start, offset, ax, numHighlights):
    for i in range(0, numHighlights):
        ax.axvspan(validHeartbeats[start + i].RWave.start - offset, validHeartbeats[start + i].RWave.end - offset,
                   zorder=2, facecolor='blue', alpha=0.3, label='R-Wave' if i == 0 else "")


def makeTWaveAnnotation(validHeartbeats, start, offset, ax, numHighlights):
    for i in range(0, numHighlights):
        ax.axvspan(validHeartbeats[start + i].TWave.start - offset, validHeartbeats[start + i].TWave.end - offset,
                   zorder=2, facecolor='red', alpha=0.5, label='T-Wave' if i == 0 else "")


def makePWaveAnnotation(validHeartbeats, start, offset, ax, numHighlights):
    for i in range(0, numHighlights):
        ax.axvspan(validHeartbeats[start + i].PWave.start - offset, validHeartbeats[start + i].RWave.start - offset,
                   zorder=2, facecolor='green', alpha=0.5, label='P-Wave' if i == 0 else "")


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
    endPoint = startPoint + 1300

    return startPoint, validHeartbeats, start, endPoint


def return_svg_bytes():
    fig = plt.gcf()
    plt.ioff()

    buf = io.BytesIO()
    fig.savefig(buf, format="svg")
    buf.seek(0)

    return buf.read()


def plotSetup(ax, startPoint, endPoint, leadName):
    # This is something we may want to pass in. It could be an extra feature for extra flexibility
    y_min = -1200
    y_max = 1200

    # hide x axis
    ax.get_xaxis().set_visible(False)

    # hide y-axis
    ax.get_yaxis().set_visible(False)

    # get rid of the border
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plotRedLines(ax, startPoint, endPoint, y_min, y_max)
    # Adds the name for each lead
    ax.text(15, -300, leadName, fontsize=30)

    # Adds the black border around the entire ECG
    if leadName == 'I':
        ax.axhline(y=y_max, linestyle='-', linewidth=4, color='black', zorder=4)
        ax.axvline(x=0, linestyle='-', linewidth=4, color='black', zorder=4)
    elif leadName == 'II':
        ax.axvline(x=0, linestyle='-', linewidth=4, color='black', zorder=4)
    elif leadName == 'III':
        ax.axvline(x=0, linestyle='-', linewidth=4, color='black', zorder=4)
        ax.axhline(y=y_min, linestyle='-', linewidth=4, color='black', zorder=4)
    elif leadName == 'aVR':
        ax.axhline(y=y_max, linestyle='-', linewidth=4, color='black', zorder=4)
    elif leadName == 'aVF':
        ax.axhline(y=y_min, linestyle='-', linewidth=4, color='black', zorder=4)
    elif leadName == 'V1':
        ax.axhline(y=y_max, linestyle='-', linewidth=4, color='black', zorder=4)
    elif leadName == 'V3':
        ax.axhline(y=y_min, linestyle='-', linewidth=4, color='black', zorder=4)
    elif leadName == 'V4':
        ax.axhline(y=y_max, linestyle='-', linewidth=4, color='black', zorder=4)
        ax.axvline(x=endPoint - startPoint, linestyle='-', linewidth=4, color='black', zorder=4)
    elif leadName == 'V5':
        ax.axvline(x=endPoint - startPoint, linestyle='-', linewidth=4, color='black', zorder=4)
    elif leadName == 'V6':
        ax.axhline(y=y_min, linestyle='-', linewidth=4, color='black', zorder=4)
        ax.axvline(x=endPoint - startPoint, linestyle='-', linewidth=4, color='black', zorder=4)


def plotRedLines(ax, startPoint, endPoint, y_min, y_max):
    x_min = 0
    x_max = endPoint - startPoint

    ax.set_ylim(y_min, y_max)
    ax.set_xlim(x_min, x_max)

    # Vertical Line plotting
    ax.axvline(x=x_min, linestyle='-', linewidth=2, color='red', zorder=3)
    # This double for loop will plot all vertical red lines. We start off by plotting the major lines
    # major lines = bold lines
    for i in range(0, 13):

        ax.axvline(x=(i / 13) * x_max, linestyle='-', linewidth=2, color='red', zorder=3)
        # This for loop will go through and plot all the minor lines
        for j in range(1, 5):

            if i == 0:
                x1 = x_max * (1 / 13) * (j / 5)

            else:
                x1 = x_max * (i / 13) + x_max * (1 / 13) * (j / 5)

            ax.axvline(x=x1, linestyle='-', linewidth=1, color=(1, 0.7, 0.7), zorder=1)

            # Horizontal Line plotting
    # basically same stuff as above
    for i in range(0, 4):
        ax.axhline(y=(y_max) * (i / 3), linestyle='-', linewidth=2, color='red', zorder=3)
        ax.axhline(y=(y_min) * (i / 3), linestyle='-', linewidth=2, color='red', zorder=3)

        for j in range(1, 5):
            if i == 0:
                y1 = y_max * (1 / 3) * (j / 5)
                y2 = y_min * (1 / 3) * (j / 5)
            else:
                y1 = y_max * (i / 3) + y_max * (1 / 3) * (j / 5)
                y2 = y_min * (i / 3) + y_min * (1 / 3) * (j / 5)
            ax.axhline(y=y1, linestyle='-', linewidth=1, color=(1, 0.7, 0.7), zorder=1)
            ax.axhline(y=y2, linestyle='-', linewidth=1, color=(1, 0.7, 0.7), zorder=1)


def plotLead1(ax, data, annotate, startPoint, endPoint, validHeartbeats, start, length, rpeaks):
    plotSetup(ax, startPoint, endPoint, 'I')

    # These if statements are where the custom arrhythmia code will go
    # the 'none' annotation will be baseline and will not annotate the lead
    # For specific arrhythmia's we will pass in the name of the arryhthmia and then create
    # extra elif line's for each arrhythmia
    if annotate == 'none':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)
    elif annotate == '1st Degree AV Block':
        makeRWaveAnnotation(validHeartbeats, start, startPoint, ax, length)
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)
        ax.annotate('QRS < 0.12', xy=(validHeartbeats[start + 1].RWave.end - startPoint, 300),
                    xytext=(validHeartbeats[start + 1].RWave.end - startPoint + 50, 800),
                    arrowprops=dict(facecolor='blue', shrink=0.05, linewidth=5),
                    zorder=5, fontsize=25)

    elif annotate == 'Atrial Fibrillation':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)

        # This for loop plots the highlights
        for i in range(0, length):
            ax.axvspan(rpeaks['ECG_R_Peaks'][i] - 20, rpeaks['ECG_R_Peaks'][i] + 20, zorder=2, facecolor='blue',
                       alpha=0.3)

    elif annotate == 'Sinus Tachycardia':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)

        _, rpeaks = nk.ecg_peaks(data, sampling_rate=500)

        length = 0
        found = 0
        setter = 1
        for i in range(0, len(rpeaks['ECG_R_Peaks'])):
            if rpeaks['ECG_R_Peaks'][i] <= endPoint and rpeaks['ECG_R_Peaks'][i] >= startPoint:
                length += 1
                if length == 1 and setter == 1:
                    found = i
                    setter = 0
        # This for loop plots the vertical blue lines
        for i in range(found, found + length):
            ax.axvline(rpeaks['ECG_R_Peaks'][i] - startPoint, zorder=2, lw=5)

        ax.text(150, 850, 'Regular HR > 100', fontsize=30, color='blue')


def plotLead2(ax, data, annotate, startPoint, endPoint, validHeartbeats, start, length, rpeaks):
    plotSetup(ax, startPoint, endPoint, 'II')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)

    elif annotate == 'basic':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)

        makeRWaveAnnotation(validHeartbeats, start, startPoint, ax, length)
        makeTWaveAnnotation(validHeartbeats, start, startPoint, ax, length)
        makePWaveAnnotation(validHeartbeats, start, startPoint, ax, length)

    elif annotate == '1st Degree AV Block':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)
        makePWaveAnnotation(validHeartbeats, start, startPoint, ax, length)
        ax.annotate('PR Interval > 0.2', xy=(validHeartbeats[start + 1].PWave.start - startPoint, 200),
                    xytext=(validHeartbeats[start + 1].PWave.start - startPoint - 120, 800),
                    arrowprops=dict(facecolor='green', shrink=0.05, linewidth=5),
                    zorder=5, fontsize=25, ha='center')

    elif annotate == 'Atrial Fibrillation':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)

        # this for loop plots the rectangles
        for i in range(0, length - 1):
            # Create a Rectangle patch
            rect = patches.Rectangle((rpeaks['ECG_R_Peaks'][i] + 30, 300),
                                     (rpeaks['ECG_R_Peaks'][i + 1]) - (rpeaks['ECG_R_Peaks'][i] + 30) - 50, -500,
                                     linewidth=5, edgecolor='r', facecolor='none')

            # Add the patch to the Axes
            ax.add_patch(rect)

        # This for loop plots the highlights
        for i in range(0, length):
            ax.axvspan(rpeaks['ECG_R_Peaks'][i] - 20, rpeaks['ECG_R_Peaks'][i] + 20, zorder=2, facecolor='blue',
                       alpha=0.3, label='P-Wave' if i == 0 else "")

        ax.annotate('Rapid & Irregular', xy=(endPoint / 2 - endPoint / 4, -200),
                    arrowprops=dict(facecolor='blue', shrink=0.05, linewidth=5),
                    xytext=(endPoint / 2 - endPoint / 4, -700),
                    zorder=5, fontsize=30)

    elif annotate == 'Normal Sinus Rhythm':
        makeRWaveAnnotation(validHeartbeats, start, startPoint, ax, length)
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)

        ax.annotate('QRS < 0.12', xy=(validHeartbeats[start + 1].RWave.end - startPoint, 300),
                    xytext=(validHeartbeats[start + 1].RWave.end - startPoint + 50, 800),
                    arrowprops=dict(facecolor='blue', shrink=0.05, linewidth=5),
                    zorder=5, fontsize=25)

    elif annotate == 'Sinus Tachycardia':
        makeRWaveAnnotation(validHeartbeats, start, startPoint, ax, length)
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)

        ax.annotate('QRS < 0.12', xy=(validHeartbeats[start + 1].RWave.end - startPoint, 300),
                    xytext=(validHeartbeats[start + 1].RWave.end - startPoint + 50, 800),
                    arrowprops=dict(facecolor='blue', shrink=0.05, linewidth=5),
                    zorder=5, fontsize=25)


def plotLead3(ax, data, annotate, startPoint, endPoint, validHeartbeats, start, length, rpeaks):
    plotSetup(ax, startPoint, endPoint, 'III')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)

    elif annotate == 'Atrial Fibrillation':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)

        # This for loop plots the highlights
        for i in range(0, length):
            ax.axvspan(rpeaks['ECG_R_Peaks'][i] - 20, rpeaks['ECG_R_Peaks'][i] + 20, zorder=2, facecolor='blue',
                       alpha=0.3, label='P-Wave' if i == 0 else "")

    elif annotate == 'Normal Sinus Rhythm':
        makePWaveAnnotation(validHeartbeats, start, startPoint, ax, length)
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)

        ax.annotate('PR Interval: 0.12 - 0.2', xy=(validHeartbeats[start + 1].PWave.start - startPoint, 200),
                    arrowprops=dict(facecolor='green', shrink=0.05, linewidth=5),
                    xytext=(validHeartbeats[start + 1].PWave.start - startPoint - 120, 800),
                    zorder=5, fontsize=25, ha='center')

    elif annotate == 'Sinus Tachycardia':
        makePWaveAnnotation(validHeartbeats, start, startPoint, ax, length)
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)

        ax.annotate('PR Interval: 0.12 - 0.2', xy=(validHeartbeats[start + 1].PWave.end - startPoint, 200),
                    arrowprops=dict(facecolor='green', shrink=0.05, linewidth=5),
                    xytext=(validHeartbeats[start + 1].PWave.start - startPoint - 120, 800),
                    zorder=5, fontsize=25, ha='center')


def plotLeadaVR(ax, data, annotate, startPoint, endPoint, validHeartbeats, start, length):
    plotSetup(ax, startPoint, endPoint, 'aVR')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)


def plotLeadaVL(ax, data, annotate, startPoint, endPoint, validHeartbeats, start, length):
    plotSetup(ax, startPoint, endPoint, 'aVL')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)


def plotLeadaVF(ax, data, annotate, startPoint, endPoint, validHeartbeats, start, length):
    plotSetup(ax, startPoint, endPoint, 'aVF')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)


def plotLeadV1(ax, data, annotate, startPoint, endPoint, validHeartbeats, start, length):
    plotSetup(ax, startPoint, endPoint, 'V1')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)


def plotLeadV2(ax, data, annotate, startPoint, endPoint, validHeartbeats, start, length):
    plotSetup(ax, startPoint, endPoint, 'V2')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)
    elif annotate == '1st Degree AV Block':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)
        makePWaveAnnotation(validHeartbeats, start, startPoint, ax, length)


def plotLeadV3(ax, data, annotate, startPoint, endPoint, validHeartbeats, start, length):
    plotSetup(ax, startPoint, endPoint, 'V3')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)


def plotLeadV4(ax, data, annotate, startPoint, endPoint, validHeartbeats, start, length):
    plotSetup(ax, startPoint, endPoint, 'V4')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)


def plotLeadV5(ax, data, annotate, startPoint, endPoint, validHeartbeats, start, length):
    plotSetup(ax, startPoint, endPoint, 'V5')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)


def plotLeadV6(ax, data, annotate, startPoint, endPoint, validHeartbeats, start, length):
    plotSetup(ax, startPoint, endPoint, 'V6')

    if annotate == 'none':
        ax.plot(data[startPoint:endPoint], color='black', zorder=4)


def findCorrectRpeaks(data, rpeaks1, rpeaks2, rpeaks3, endPoint, startPoint):
    length = 0
    found = 0
    setter = 1
    for i in range(0, len(rpeaks2['ECG_R_Peaks'])):
        if rpeaks2['ECG_R_Peaks'][i] <= endPoint and rpeaks2['ECG_R_Peaks'][i] >= startPoint:
            length += 1
            if length == 1 and setter == 1:
                found = i
                setter = 0
    # variables to track which rpeaks are correct in each array
    correct1 = 0
    correct2 = 0
    correct3 = 0
    # tolerance variable for the math.isclose functions
    tolerance = 0.05
    # pointer variables for each rpeak array. x = rpeaks1, y=rpeaks2
    x = found
    y = found
    z = found

    # Goes through the ranges we want for each rpeaks array
    for i in range(found, found + length):
        # if all rpeaks found the same peak
        if (math.isclose(rpeaks1['ECG_R_Peaks'][x], rpeaks2['ECG_R_Peaks'][y], rel_tol=tolerance) == True) and (
                math.isclose(rpeaks2['ECG_R_Peaks'][y], rpeaks3['ECG_R_Peaks'][z], rel_tol=tolerance) == True):
            correct1 += 1
            correct2 += 1
            correct3 += 1
            x += 1
            y += 1
            z += 1
        # if only 1 and 2 found it
        elif (math.isclose(rpeaks1['ECG_R_Peaks'][x], rpeaks2['ECG_R_Peaks'][y], rel_tol=tolerance) == True):
            correct1 += 1
            correct2 += 1
            x += 1
            y += 1
        # if only 2 and 3 found it
        elif (math.isclose(rpeaks3['ECG_R_Peaks'][z], rpeaks2['ECG_R_Peaks'][y], rel_tol=tolerance) == True):
            correct2 += 1
            correct3 += 1
            y += 1
            z += 1
        # if only 1 and 3 found it
        elif (math.isclose(rpeaks1['ECG_R_Peaks'][x], rpeaks3['ECG_R_Peaks'][z], rel_tol=tolerance) == True):
            correct1 += 1
            correct3 += 1
            x += 1
            z += 1
        # only 1 found it
        elif rpeaks1['ECG_R_Peaks'][x] < rpeaks2['ECG_R_Peaks'][y] and rpeaks1['ECG_R_Peaks'][x] < \
                rpeaks3['ECG_R_Peaks'][z]:
            correct1 += 1
            x += 1
        # only 2 found it
        elif rpeaks2['ECG_R_Peaks'][y] < rpeaks3['ECG_R_Peaks'][z] and rpeaks2['ECG_R_Peaks'][y] < \
                rpeaks1['ECG_R_Peaks'][x]:
            correct2 += 1
            y += 1
        # only 3 found it
        elif rpeaks3['ECG_R_Peaks'][z] < rpeaks2['ECG_R_Peaks'][y] and rpeaks3['ECG_R_Peaks'][z] < \
                rpeaks1['ECG_R_Peaks'][x]:
            correct3 += 1
            z += 1

    # if all rpeaks are the same, then it doesn't matter which rpeaks we pass in
    if correct1 == correct2 == correct3 == length:
        # do nothing
        rpeaks1['ECG_R_Peaks'] = rpeaks1['ECG_R_Peaks']
    # if 3 didn't find all rpeaks
    elif correct1 == correct2 == length:
        rpeaks3['ECG_R_Peaks'] = rpeaks1['ECG_R_Peaks']
    # if 1 didnt find all rpeaks
    elif correct2 == correct3 == length:
        rpeaks1['ECG_R_Peaks'] = rpeaks2['ECG_R_Peaks']

    # if 2 didn't find all rpeaks
    elif correct1 == correct3 == length:
        rpeaks3['ECG_R_Peaks'] = rpeaks1['ECG_R_Peaks']

    # if 1 and 2 didn't find all rpeaks
    elif correct3 == length:
        rpeaks1['ECG_R_Peaks'] = rpeaks3['ECG_R_Peaks']
        rpeaks2['ECG_R_Peaks'] = rpeaks3['ECG_R_Peaks']

    # if 2 and 3 didn't find all rpeaks
    elif correct1 == length:
        rpeaks3['ECG_R_Peaks'] = rpeaks1['ECG_R_Peaks']
        rpeaks2['ECG_R_Peaks'] = rpeaks1['ECG_R_Peaks']

    # if 1 and 3 didn't find all rpeaks
    elif correct2 == length:
        rpeaks1['ECG_R_Peaks'] = rpeaks2['ECG_R_Peaks']
        rpeaks3['ECG_R_Peaks'] = rpeaks2['ECG_R_Peaks']

    else:
        print("DIDN'T FIND ALL RPEAKS")
    return rpeaks1, rpeaks2, rpeaks3


def plot12ECGs(data, nameOfArrhythmia):
    annotations = []
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(40, 19.68), sharey=True)

    # Sets up our 12 axis
    ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12 = axs.flatten()

    # This is where we will change what each arrhythmia does
    if nameOfArrhythmia == 'basic':
        annotations = ['none', 'none', 'none', 'none', 'basic', 'none', 'none', 'none', 'none', 'none', 'none', 'none']

        # We need to get the startpoint and endpoints for the graphs first
        # In the basic example, we are annotating lead 2 so we will get those start/endpoints for the whole graph based on lead 2
        startPoint, validHeartbeats, start, endPoint = scanData(data['val'][1])

    elif nameOfArrhythmia == '1st Degree AV Block':
        annotations = ['1st Degree AV Block', 'none', 'none', 'none', '1st Degree AV Block', 'none',
                       '1st Degree AV Block', 'none', 'none', 'none', 'none', 'none']

        # We need to get the startpoint and endpoints for the graphs first
        # In the basic example, we are annotating lead 2 so we will get those start/endpoints for the whole graph based on lead 2
        startPoint, validHeartbeats, start, endPoint = scanData(data['val'][1])

    elif nameOfArrhythmia == 'Atrial Fibrillation':
        annotations = ['Atrial Fibrillation', 'none', 'none', 'none', 'Atrial Fibrillation', 'none', 'none', 'none',
                       'Atrial Fibrillation', 'none', 'none', 'none']

        # We need to manually set this because neurokit doesn't work with this arrhythmia
        # It only finds the R wave peaks which is all we need
        startPoint = 0
        endPoint = 1300
        validHeartbeats = 'none'
        start = 'none'

    elif nameOfArrhythmia == 'Normal Sinus Rhythm':
        annotations = ['none', 'none', 'none', 'none', 'Normal Sinus Rhythm', 'none', 'none', 'none',
                       'Normal Sinus Rhythm', 'none', 'none', 'none']
        startPoint, validHeartbeats, start, endPoint = scanData(data['val'][1])

    elif nameOfArrhythmia == 'Sinus Tachycardia':
        annotations = ['Sinus Tachycardia', 'none', 'none', 'none', 'Sinus Tachycardia', 'none', 'none', 'none',
                       'Sinus Tachycardia', 'none', 'none', 'none']
        startPoint, validHeartbeats, start, endPoint = scanData(data['val'][1])

    # Finds the amount of heartbeats displayed and puts them into length. This is needed because we need the
    # big boxes to have a time of 0.2 seconds per box
    _, rpeaks2 = nk.ecg_peaks(data['val'][1], sampling_rate=500)

    length = 0
    for i in range(0, len(rpeaks2['ECG_R_Peaks'])):
        if rpeaks2['ECG_R_Peaks'][i] <= endPoint and rpeaks2['ECG_R_Peaks'][i] >= startPoint:
            length += 1

    # we need to compare rpeaks found because neurokit won't always find the same rpeaks values between leads
    if nameOfArrhythmia == 'Atrial Fibrillation':
        _, rpeaks1 = nk.ecg_peaks(data['val'][0], sampling_rate=500)
        _, rpeaks3 = nk.ecg_peaks(data['val'][2], sampling_rate=500)
        rpeaks1, rpeaks2, rpeaks3 = findCorrectRpeaks(data, rpeaks1, rpeaks2, rpeaks3, endPoint, startPoint)
    # Otherwise we just want to base our annotations off of lead 2
    else:
        rpeaks1 = nk.ecg_peaks(data['val'][1], sampling_rate=500)
        rpeaks3 = nk.ecg_peaks(data['val'][1], sampling_rate=500)

    # Plotting leads in order
    # We will have to custom code the annotations array for every annotation we do
    # This means that setting the annotations must be done for every case
    # And every case we do must be added to the plotting functions above
    plotLead1(ax1, data['val'][0], annotations[0], startPoint, endPoint, validHeartbeats, start, length, rpeaks1)
    plotLeadaVR(ax2, data['val'][3], annotations[1], startPoint, endPoint, validHeartbeats, start, length)
    plotLeadV1(ax3, data['val'][6], annotations[2], startPoint, endPoint, validHeartbeats, start, length)
    plotLeadV4(ax4, data['val'][9], annotations[3], startPoint, endPoint, validHeartbeats, start, length)
    plotLead2(ax5, data['val'][1], annotations[4], startPoint, endPoint, validHeartbeats, start, length, rpeaks2)
    plotLeadaVL(ax6, data['val'][4], annotations[5], startPoint, endPoint, validHeartbeats, start, length)
    plotLeadV2(ax7, data['val'][7], annotations[6], startPoint, endPoint, validHeartbeats, start, length)
    plotLeadV5(ax8, data['val'][10], annotations[7], startPoint, endPoint, validHeartbeats, start, length)
    plotLead3(ax9, data['val'][2], annotations[8], startPoint, endPoint, validHeartbeats, start, length, rpeaks3)
    plotLeadaVF(ax10, data['val'][5], annotations[9], startPoint, endPoint, validHeartbeats, start, length)
    plotLeadV3(ax11, data['val'][8], annotations[10], startPoint, endPoint, validHeartbeats, start, length)
    plotLeadV6(ax12, data['val'][11], annotations[11], startPoint, endPoint, validHeartbeats, start, length)

    fig.subplots_adjust(
        hspace=0,
        wspace=0,
        left=0,  # the left side of the subplots of the figure
        right=1,  # the right side of the subplots of the figure
        bottom=0,  # the bottom of the subplots of the figure
        top=1
    )
    fig.suptitle('ECG 12', fontsize=30)

    #     #Calcs the time between big boxes
    #     time = (endPoint - startPoint)/(500*13)
    #     #prints them below the graph
    #     plt.text(0.0, -.025, ('Time between big boxes: '+ str(float(f'{time:.6f}')) + ' seconds'), fontsize=40, transform=plt.gcf().transFigure)

    plt.show()

    # getting the svgbites of our figure and returning it
    svgBites = return_svg_bytes()
    return svgBites


if __name__ == '__main__':
    mat = loadmat("annotation_test_data/working/JS00008.mat")
    print(mat)
    plot12ECGs(mat, 'Atrial Fibrillation')
