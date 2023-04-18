import io
import math
from dataclasses import dataclass
from typing import List, NoReturn

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import neurokit2 as nk
from numpy._typing import NDArray
from scipy.io import loadmat


@dataclass
class Wave:
    start: int
    end: int


@dataclass
class Heartbeat:
    t_wave: Wave
    p_wave: Wave
    r_wave: Wave


def point_finder(start_r: List[int], end_r: List[int], start_t: List[int], end_t: List[int], start_p: List[int],
                 end_p: List[int], signal_cwt: dict) -> NoReturn:
    # all this does is finds the starts and endpoints for every heartbeat found in the signal
    for i in range(5000):
        if signal_cwt['ECG_R_Onsets'][i] != 0:
            start_r.append(i)

        if signal_cwt['ECG_R_Offsets'][i] != 0:
            end_r.append(i)

        if signal_cwt['ECG_T_Onsets'][i] != 0:
            start_t.append(i)

        if signal_cwt['ECG_T_Offsets'][i] != 0:
            end_t.append(i)

        if signal_cwt['ECG_P_Onsets'][i] != 0:
            start_p.append(i)

        if signal_cwt['ECG_P_Offsets'][i] != 0:
            end_p.append(i)


def clean_arrays(start: List[int], end: List[int], leeway: int) -> List[Wave]:
    list_waves = []
    # finds the shorter of the two, so we don't run into overflows
    if len(start) < len(end):
        j = len(start)
    else:
        j = len(end)
    # separate pointer variables
    x = 0
    y = 0

    while x < j or y < j:
        # if we have a valid wave
        if 0 < end[y] - start[x] < leeway:
            list_waves.append(Wave(start=start[x], end=end[y]))
            x += 1
            y += 1
        # if the algorithm missed the start of the wave. Ex. algorithm found end[0] but start[0] corresponds
        # to heartbeat 2
        elif end[y] - start[x] < 0:
            y += 1
        # if the algorithm missed the end of the wave
        elif end[y] - start[x] > leeway:
            x += 1

    return list_waves


def create_heartbeats(t_wave: List[Wave], p_wave: List[Wave], r_wave: List[Wave]) -> List[Heartbeat]:
    # Finding the smallest array
    j = min(len(t_wave), len(p_wave), len(r_wave)) - 1

    x = 0
    y = 0
    z = 0
    heartbeat_list = []
    while x < j or y < j or z < j:
        throw_error = True

        # if missing P-wave
        # validating that P-wave is higher than the other two waves and that the other two waves are correct
        if r_wave[y].start < p_wave[x].start and p_wave[x].start > t_wave[z].start and r_wave[y].start < t_wave[
            z].start:
            throw_error = False
            # if the p-wave is higher than the other two, the other two waves become invalid, and we iterate
            y += 1
            z += 1

        # if missing R-wave
        # Validating start of RWave is greater than TWave and the other two waves are valid
        elif r_wave[y].start > t_wave[z].start > p_wave[x].start:
            throw_error = False
            x += 1
            z += 1

        # If P-Wave and R-Wave are missing
        elif p_wave[x].start > t_wave[z].start and r_wave[y].start > t_wave[z].start:
            throw_error = False
            z += 1

        # if missing T-Wave
        # if T-Wave is in the next heartbeat
        elif t_wave[z].start > p_wave[x + 1].start:
            throw_error = False
            # if P-Wave is in the next heartbeat
            if p_wave[x].start > r_wave[y].start:
                y += 1

            # If R-Wave is in the next heartbeat
            elif r_wave[y].start > p_wave[x + 1].start:
                x += 1

            # Just the T-Wave is in the next heartbeat
            else:
                x += 1
                y += 1

        # if wave is valid
        elif t_wave[z].start > r_wave[y].start > p_wave[x].start:
            throw_error = False
            heartbeat_list.append(Heartbeat(t_wave[z], p_wave[x], r_wave[y]))
            x += 1
            y += 1
            z += 1

        if throw_error:
            raise RuntimeError("Possible infinite loop")

    return heartbeat_list


def find_3_waves(valid_heartbeats: List[Heartbeat], leeway: int) -> int:
    start = 0
    end = 0
    i = 0

    while i in range(0, len(valid_heartbeats) - 1):
        # finds if two p waves are together by checking it against a leeway
        if valid_heartbeats[i + 1].p_wave.start - valid_heartbeats[i].p_wave.start < leeway:
            end += 1

        # If the p waves are not together, we reset the starting point and do it again
        else:
            start = i + 1
            end = 0

        # since the statements above checks the if the current and next heartbeat are together,
        # we only need end to be a value of 2 here
        if end == 2:
            return start
        i += 1


def make_r_wave_annotation(valid_heartbeats: List[Heartbeat], start: int, offset: int, ax: plt.Axes,
                           number_highlights: int) -> NoReturn:
    for i in range(0, number_highlights):
        ax.axvspan(valid_heartbeats[start + i].r_wave.start - offset, valid_heartbeats[start + i].r_wave.end - offset,
                   zorder=2, facecolor='blue', alpha=0.3, label='R-Wave' if i == 0 else "")


def make_t_wave_annotation(valid_heartbeats: List[Heartbeat], start: int, offset: int, ax: plt.Axes,
                           number_highlights: int) -> NoReturn:
    for i in range(0, number_highlights):
        ax.axvspan(valid_heartbeats[start + i].t_wave.start - offset, valid_heartbeats[start + i].t_wave.end - offset,
                   zorder=2, facecolor='red', alpha=0.5, label='T-Wave' if i == 0 else "")


def make_p_wave_annotation(valid_heartbeats: List[Heartbeat], start: int, offset: int, ax: plt.Axes,
                           number_highlights: int) -> NoReturn:
    for i in range(0, number_highlights):
        ax.axvspan(valid_heartbeats[start + i].p_wave.start - offset, valid_heartbeats[start + i].r_wave.start - offset,
                   zorder=2, facecolor='green', alpha=0.5, label='P-Wave' if i == 0 else "")


def scan_data(np_array: NDArray[float]) -> (int, List[Heartbeat], int, int):
    _, rpeaks = nk.ecg_peaks(np_array, sampling_rate=500)

    signal_cwt, waves_cwt = nk.ecg_delineate(np_array, rpeaks, sampling_rate=500, method="cwt")

    start_r = []
    end_r = []
    start_t = []
    end_t = []
    start_p = []
    end_p = []

    # This function cleans up the starting and ending points by putting it into arrays by themselves
    point_finder(start_r, end_r, start_t, end_t, start_p, end_p, signal_cwt)

    # Further cleans up the arrays and puts them into the wave classes
    p_waves = clean_arrays(start_p, end_p, 100)
    t_waves = clean_arrays(start_t, end_t, 150)
    r_waves = clean_arrays(start_r, end_r, 150)

    # finds and stores all valid heartbeats into the heartbeat class
    valid_heartbeats = create_heartbeats(t_waves, p_waves, r_waves)

    # Finds 3 heartbeats in a row that we can output
    start = find_3_waves(valid_heartbeats, 700)

    # checks and gives an error statement if the matlab file cannot be used
    if start is None:
        raise RuntimeError("There are not 3 valid heartbeats in a row")

    # declares where the start_point is
    start_point = valid_heartbeats[start].p_wave.start - 100
    end_point = start_point + 1300

    return start_point, valid_heartbeats, start, end_point


def return_svg_bytes() -> bytes:
    fig = plt.gcf()
    plt.ioff()

    buf = io.BytesIO()
    fig.savefig(buf, format="svg")
    buf.seek(0)

    return buf.read()


def plot_setup(ax: plt.Axes, start_point: int, end_point: int, lead_name: str) -> NoReturn:
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

    plot_red_lines(ax, start_point, end_point, y_min, y_max)
    # Adds the name for each lead
    ax.text(15, -300, lead_name, fontsize=30)

    # Adds the black border around the entire ECG
    if lead_name == 'I':
        ax.axhline(y=y_max, linestyle='-', linewidth=4, color='black', zorder=4)
        ax.axvline(x=0, linestyle='-', linewidth=4, color='black', zorder=4)
    elif lead_name == 'II':
        ax.axvline(x=0, linestyle='-', linewidth=4, color='black', zorder=4)
    elif lead_name == 'III':
        ax.axvline(x=0, linestyle='-', linewidth=4, color='black', zorder=4)
        ax.axhline(y=y_min, linestyle='-', linewidth=4, color='black', zorder=4)
    elif lead_name == 'aVR':
        ax.axhline(y=y_max, linestyle='-', linewidth=4, color='black', zorder=4)
    elif lead_name == 'aVF':
        ax.axhline(y=y_min, linestyle='-', linewidth=4, color='black', zorder=4)
    elif lead_name == 'V1':
        ax.axhline(y=y_max, linestyle='-', linewidth=4, color='black', zorder=4)
    elif lead_name == 'V3':
        ax.axhline(y=y_min, linestyle='-', linewidth=4, color='black', zorder=4)
    elif lead_name == 'V4':
        ax.axhline(y=y_max, linestyle='-', linewidth=4, color='black', zorder=4)
        ax.axvline(x=end_point - start_point, linestyle='-', linewidth=4, color='black', zorder=4)
    elif lead_name == 'V5':
        ax.axvline(x=end_point - start_point, linestyle='-', linewidth=4, color='black', zorder=4)
    elif lead_name == 'V6':
        ax.axhline(y=y_min, linestyle='-', linewidth=4, color='black', zorder=4)
        ax.axvline(x=end_point - start_point, linestyle='-', linewidth=4, color='black', zorder=4)


def plot_red_lines(ax: plt.Axes, start_point: int, end_point: int, y_min: int, y_max: int) -> NoReturn:
    x_min = 0
    x_max = end_point - start_point

    ax.set_ylim(y_min, y_max)
    ax.set_xlim(x_min, x_max)

    # Vertical Line plotting
    ax.axvline(x=x_min, linestyle='-', linewidth=2, color='red', zorder=3)
    # This double for loop will plot all vertical red lines. We start off by plotting the major lines (bold lines)
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
        ax.axhline(y=y_max * (i / 3), linestyle='-', linewidth=2, color='red', zorder=3)
        ax.axhline(y=y_min * (i / 3), linestyle='-', linewidth=2, color='red', zorder=3)

        for j in range(1, 5):
            if i == 0:
                y1 = y_max * (1 / 3) * (j / 5)
                y2 = y_min * (1 / 3) * (j / 5)
            else:
                y1 = y_max * (i / 3) + y_max * (1 / 3) * (j / 5)
                y2 = y_min * (i / 3) + y_min * (1 / 3) * (j / 5)
            ax.axhline(y=y1, linestyle='-', linewidth=1, color=(1, 0.7, 0.7), zorder=1)
            ax.axhline(y=y2, linestyle='-', linewidth=1, color=(1, 0.7, 0.7), zorder=1)


def plot_lead_1(ax: plt.axes, data: NDArray[float], annotate: str, start_point: int, end_point: int,
                valid_heartbeats: List[Heartbeat], start: int, length: int, rpeaks: dict) -> NoReturn:
    plot_setup(ax, start_point, end_point, 'I')

    # These if statements are where the custom arrhythmia code will go
    # the 'none' annotation will be baseline and will not annotate the lead
    # For specific arrhythmia's we will pass in the name of the arryhthmia and then create
    # extra elif line's for each arrhythmia
    if annotate == 'none':
        ax.plot(data[start_point:end_point], color='black', zorder=4)
    elif annotate == '1st Degree AV Block':
        make_r_wave_annotation(valid_heartbeats, start, start_point, ax, length)
        ax.plot(data[start_point:end_point], color='black', zorder=4)
        ax.annotate('QRS < 0.12', xy=(valid_heartbeats[start + 1].r_wave.end - start_point, 300),
                    xytext=(valid_heartbeats[start + 1].r_wave.end - start_point + 50, 800),
                    arrowprops=dict(facecolor='blue', shrink=0.05, linewidth=5),
                    zorder=5, fontsize=25)

    elif annotate == 'Atrial Fibrillation':
        ax.plot(data[start_point:end_point], color='black', zorder=4)

        # This for loop plots the highlights
        for i in range(0, length):
            ax.axvspan(rpeaks['ECG_R_Peaks'][i] - 20, rpeaks['ECG_R_Peaks'][i] + 20, zorder=2, facecolor='blue',
                       alpha=0.3)

    elif annotate == 'Sinus Tachycardia':
        ax.plot(data[start_point:end_point], color='black', zorder=4)

        _, rpeaks = nk.ecg_peaks(data, sampling_rate=500)

        length = 0
        found = 0
        setter = 1
        for i in range(0, len(rpeaks['ECG_R_Peaks'])):
            if end_point >= rpeaks['ECG_R_Peaks'][i] >= start_point:
                length += 1
                if length == 1 and setter == 1:
                    found = i
                    setter = 0
        # This for loop plots the vertical blue lines
        for i in range(found, found + length):
            ax.axvline(rpeaks['ECG_R_Peaks'][i] - start_point, zorder=2, lw=5)

        ax.text(150, 850, 'Regular HR > 100', fontsize=30, color='blue')


def plot_lead_2(ax: plt.Axes, data: NDArray[float], annotate: str, start_point: int, end_point: int,
                valid_heartbeats: List[Heartbeat], start: int, length: int, rpeaks: dict) -> NoReturn:
    plot_setup(ax, start_point, end_point, 'II')

    if annotate == 'none':
        ax.plot(data[start_point:end_point], color='black', zorder=4)

    elif annotate == 'basic':
        ax.plot(data[start_point:end_point], color='black', zorder=4)

        make_r_wave_annotation(valid_heartbeats, start, start_point, ax, length)
        make_t_wave_annotation(valid_heartbeats, start, start_point, ax, length)
        make_p_wave_annotation(valid_heartbeats, start, start_point, ax, length)

    elif annotate == '1st Degree AV Block':
        ax.plot(data[start_point:end_point], color='black', zorder=4)
        make_p_wave_annotation(valid_heartbeats, start, start_point, ax, length)
        ax.annotate('PR Interval > 0.2', xy=(valid_heartbeats[start + 1].p_wave.start - start_point, 200),
                    xytext=(valid_heartbeats[start + 1].p_wave.start - start_point - 120, 800),
                    arrowprops=dict(facecolor='green', shrink=0.05, linewidth=5),
                    zorder=5, fontsize=25, ha='center')

    elif annotate == 'Atrial Fibrillation':
        ax.plot(data[start_point:end_point], color='black', zorder=4)

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

        ax.annotate('Rapid & Irregular', xy=(end_point / 2 - end_point / 4, -200),
                    arrowprops=dict(facecolor='blue', shrink=0.05, linewidth=5),
                    xytext=(end_point / 2 - end_point / 4, -700),
                    zorder=5, fontsize=30)

    elif annotate == 'Normal Sinus Rhythm':
        make_r_wave_annotation(valid_heartbeats, start, start_point, ax, length)
        ax.plot(data[start_point:end_point], color='black', zorder=4)

        ax.annotate('QRS < 0.12', xy=(valid_heartbeats[start + 1].r_wave.end - start_point, 300),
                    xytext=(valid_heartbeats[start + 1].r_wave.end - start_point + 50, 800),
                    arrowprops=dict(facecolor='blue', shrink=0.05, linewidth=5),
                    zorder=5, fontsize=25)

    elif annotate == 'Sinus Tachycardia':
        make_r_wave_annotation(valid_heartbeats, start, start_point, ax, length)
        ax.plot(data[start_point:end_point], color='black', zorder=4)

        ax.annotate('QRS < 0.12', xy=(valid_heartbeats[start + 1].r_wave.end - start_point, 300),
                    xytext=(valid_heartbeats[start + 1].r_wave.end - start_point + 50, 800),
                    arrowprops=dict(facecolor='blue', shrink=0.05, linewidth=5),
                    zorder=5, fontsize=25)


def plot_lead_3(ax: plt.Axes, data: NDArray[float], annotate: str, start_point: int, end_point: int,
                valid_heartbeats: List[Heartbeat], start: int, length: int, rpeaks: dict) -> NoReturn:
    plot_setup(ax, start_point, end_point, 'III')

    if annotate == 'none':
        ax.plot(data[start_point:end_point], color='black', zorder=4)

    elif annotate == 'Atrial Fibrillation':
        ax.plot(data[start_point:end_point], color='black', zorder=4)

        # This for loop plots the highlights
        for i in range(0, length):
            ax.axvspan(rpeaks['ECG_R_Peaks'][i] - 20, rpeaks['ECG_R_Peaks'][i] + 20, zorder=2, facecolor='blue',
                       alpha=0.3, label='P-Wave' if i == 0 else "")

    elif annotate == 'Normal Sinus Rhythm':
        make_p_wave_annotation(valid_heartbeats, start, start_point, ax, length)
        ax.plot(data[start_point:end_point], color='black', zorder=4)

        ax.annotate('PR Interval: 0.12 - 0.2', xy=(valid_heartbeats[start + 1].p_wave.start - start_point, 200),
                    arrowprops=dict(facecolor='green', shrink=0.05, linewidth=5),
                    xytext=(valid_heartbeats[start + 1].p_wave.start - start_point - 120, 800),
                    zorder=5, fontsize=25, ha='center')

    elif annotate == 'Sinus Tachycardia':
        make_p_wave_annotation(valid_heartbeats, start, start_point, ax, length)
        ax.plot(data[start_point:end_point], color='black', zorder=4)

        ax.annotate('PR Interval: 0.12 - 0.2', xy=(valid_heartbeats[start + 1].p_wave.end - start_point, 200),
                    arrowprops=dict(facecolor='green', shrink=0.05, linewidth=5),
                    xytext=(valid_heartbeats[start + 1].p_wave.start - start_point - 120, 800),
                    zorder=5, fontsize=25, ha='center')


def plot_lead_avr(ax: plt.Axes, data: NDArray[float], annotate: str, start_point: int, end_point: int,
                  valid_heartbeats: List[Heartbeat], start: int, length: int) -> NoReturn:
    plot_setup(ax, start_point, end_point, 'aVR')

    if annotate == 'none':
        ax.plot(data[start_point:end_point], color='black', zorder=4)


def plot_lead_avl(ax: plt.Axes, data: NDArray[float], annotate: str, start_point: int, end_point: int,
                  valid_heartbeats: List[Heartbeat], start: int, length: int) -> NoReturn:
    plot_setup(ax, start_point, end_point, 'aVL')

    if annotate == 'none':
        ax.plot(data[start_point:end_point], color='black', zorder=4)


def plot_lead_avf(ax: plt.Axes, data: NDArray[float], annotate: str, start_point: int, end_point: int,
                  valid_heartbeats: List[Heartbeat], start: int, length: int) -> NoReturn:
    plot_setup(ax, start_point, end_point, 'aVF')

    if annotate == 'none':
        ax.plot(data[start_point:end_point], color='black', zorder=4)


def plot_lead_v1(ax: plt.Axes, data: NDArray[float], annotate: str, start_point: int, end_point: int,
                 valid_heartbeats: List[Heartbeat], start: int, length: int) -> NoReturn:
    plot_setup(ax, start_point, end_point, 'V1')

    if annotate == 'none':
        ax.plot(data[start_point:end_point], color='black', zorder=4)


def plot_lead_v2(ax: plt.Axes, data: NDArray[float], annotate: str, start_point: int, end_point: int,
                 valid_heartbeats: List[Heartbeat], start: int, length: int) -> NoReturn:
    plot_setup(ax, start_point, end_point, 'V2')

    if annotate == 'none':
        ax.plot(data[start_point:end_point], color='black', zorder=4)
    elif annotate == '1st Degree AV Block':
        ax.plot(data[start_point:end_point], color='black', zorder=4)
        make_p_wave_annotation(valid_heartbeats, start, start_point, ax, length)


def plot_lead_v3(ax: plt.Axes, data: NDArray[float], annotate: str, start_point: int, end_point: int,
                 valid_heartbeats: List[Heartbeat], start: int, length: int) -> NoReturn:
    plot_setup(ax, start_point, end_point, 'V3')

    if annotate == 'none':
        ax.plot(data[start_point:end_point], color='black', zorder=4)


def plot_lead_v4(ax: plt.Axes, data: NDArray[float], annotate: str, start_point: int, end_point: int,
                 valid_heartbeats: List[Heartbeat], start: int, length: int) -> NoReturn:
    plot_setup(ax, start_point, end_point, 'V4')

    if annotate == 'none':
        ax.plot(data[start_point:end_point], color='black', zorder=4)


def plot_lead_v5(ax: plt.Axes, data: NDArray[float], annotate: str, start_point: int, end_point: int,
                 valid_heartbeats: List[Heartbeat], start: int, length: int) -> NoReturn:
    plot_setup(ax, start_point, end_point, 'V5')

    if annotate == 'none':
        ax.plot(data[start_point:end_point], color='black', zorder=4)


def plot_lead_v6(ax: plt.Axes, data: NDArray[float], annotate: str, start_point: int, end_point: int,
                 valid_heartbeats: List[Heartbeat], start: int, length: int) -> NoReturn:
    plot_setup(ax, start_point, end_point, 'V6')

    if annotate == 'none':
        ax.plot(data[start_point:end_point], color='black', zorder=4)


def find_correct_rpeaks(data: NDArray[float], rpeaks1: dict, rpeaks2: dict, rpeaks3: dict, end_point: int,
                        start_point: int) -> (dict, dict, dict):
    length = 0
    found = 0
    setter = 1
    for i in range(0, len(rpeaks2['ECG_R_Peaks'])):
        if end_point >= rpeaks2['ECG_R_Peaks'][i] >= start_point:
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
        if (math.isclose(rpeaks1['ECG_R_Peaks'][x], rpeaks2['ECG_R_Peaks'][y], rel_tol=tolerance) is True) and (
                math.isclose(rpeaks2['ECG_R_Peaks'][y], rpeaks3['ECG_R_Peaks'][z], rel_tol=tolerance) is True):
            correct1 += 1
            correct2 += 1
            correct3 += 1
            x += 1
            y += 1
            z += 1
        # if only 1 and 2 found it
        elif math.isclose(rpeaks1['ECG_R_Peaks'][x], rpeaks2['ECG_R_Peaks'][y], rel_tol=tolerance) is True:
            correct1 += 1
            correct2 += 1
            x += 1
            y += 1
        # if only 2 and 3 found it
        elif math.isclose(rpeaks3['ECG_R_Peaks'][z], rpeaks2['ECG_R_Peaks'][y], rel_tol=tolerance) is True:
            correct2 += 1
            correct3 += 1
            y += 1
            z += 1
        # if only 1 and 3 found it
        elif math.isclose(rpeaks1['ECG_R_Peaks'][x], rpeaks3['ECG_R_Peaks'][z], rel_tol=tolerance) is True:
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
    # if 1 didn't find all rpeaks
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


def plot_12_ecgs(data: NDArray[float], name_of_arrhythmia: str) -> NoReturn:
    annotations = []
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(40, 19.68), sharey='all')

    # Sets up our 12 axis
    ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12 = axs.flatten()

    # This is where we will change what each arrhythmia does
    if name_of_arrhythmia == 'basic':
        annotations = ['none', 'none', 'none', 'none', 'basic', 'none', 'none', 'none', 'none', 'none', 'none', 'none']

        # We need to get the startpoint and endpoints for the graphs first
        # In the basic example, we are annotating lead 2, so we will get those start/endpoints for the whole graph
        # based on lead 2
        start_point, valid_heartbeats, start, end_point = scan_data(data[1])

    elif name_of_arrhythmia == '1st Degree AV Block':
        annotations = ['1st Degree AV Block', 'none', 'none', 'none', '1st Degree AV Block', 'none',
                       '1st Degree AV Block', 'none', 'none', 'none', 'none', 'none']

        # We need to get the startpoint and endpoints for the graphs first
        # In the basic example, we are annotating lead 2, so we will get those start/endpoints for the whole graph
        # based on lead 2
        start_point, valid_heartbeats, start, end_point = scan_data(data[1])

    elif name_of_arrhythmia == 'Atrial Fibrillation':
        annotations = ['Atrial Fibrillation', 'none', 'none', 'none', 'Atrial Fibrillation', 'none', 'none', 'none',
                       'Atrial Fibrillation', 'none', 'none', 'none']

        # We need to manually set this because neurokit doesn't work with this arrhythmia
        # It only finds the R wave peaks which is all we need
        start_point = 0
        end_point = 1300
        valid_heartbeats = 'none'
        start = 'none'

    elif name_of_arrhythmia == 'Normal Sinus Rhythm':
        annotations = ['none', 'none', 'none', 'none', 'Normal Sinus Rhythm', 'none', 'none', 'none',
                       'Normal Sinus Rhythm', 'none', 'none', 'none']
        start_point, valid_heartbeats, start, end_point = scan_data(data[1])

    elif name_of_arrhythmia == 'Sinus Tachycardia':
        annotations = ['Sinus Tachycardia', 'none', 'none', 'none', 'Sinus Tachycardia', 'none', 'none', 'none',
                       'Sinus Tachycardia', 'none', 'none', 'none']
        start_point, valid_heartbeats, start, end_point = scan_data(data[1])

    # Finds the amount of heartbeats displayed and puts them into length. This is needed because we need the
    # big boxes to have a time of 0.2 seconds per box
    _, rpeaks2 = nk.ecg_peaks(data[1], sampling_rate=500)

    length = 0
    for i in range(0, len(rpeaks2['ECG_R_Peaks'])):
        if end_point >= rpeaks2['ECG_R_Peaks'][i] >= start_point:
            length += 1

    # we need to compare rpeaks found because neurokit won't always find the same rpeaks values between leads
    if name_of_arrhythmia == 'Atrial Fibrillation':
        _, rpeaks1 = nk.ecg_peaks(data[0], sampling_rate=500)
        _, rpeaks3 = nk.ecg_peaks(data[2], sampling_rate=500)
        rpeaks1, rpeaks2, rpeaks3 = find_correct_rpeaks(data, rpeaks1, rpeaks2, rpeaks3, end_point, start_point)
    # Otherwise we just want to base our annotations off of lead 2
    else:
        rpeaks1 = nk.ecg_peaks(data[1], sampling_rate=500)
        rpeaks3 = nk.ecg_peaks(data[1], sampling_rate=500)

    # Plotting leads in order
    # We will have to custom code the annotations array for every annotation we do
    # This means that setting the annotations must be done for every case
    # And every case we do must be added to the plotting functions above
    plot_lead_1(ax1, data[0], annotations[0], start_point, end_point, valid_heartbeats, start, length, rpeaks1)
    plot_lead_avr(ax2, data[3], annotations[1], start_point, end_point, valid_heartbeats, start, length)
    plot_lead_v1(ax3, data[6], annotations[2], start_point, end_point, valid_heartbeats, start, length)
    plot_lead_v4(ax4, data[9], annotations[3], start_point, end_point, valid_heartbeats, start, length)
    plot_lead_2(ax5, data[1], annotations[4], start_point, end_point, valid_heartbeats, start, length, rpeaks2)
    plot_lead_avl(ax6, data[4], annotations[5], start_point, end_point, valid_heartbeats, start, length)
    plot_lead_v2(ax7, data[7], annotations[6], start_point, end_point, valid_heartbeats, start, length)
    plot_lead_v5(ax8, data[10], annotations[7], start_point, end_point, valid_heartbeats, start, length)
    plot_lead_3(ax9, data[2], annotations[8], start_point, end_point, valid_heartbeats, start, length, rpeaks3)
    plot_lead_avf(ax10, data[5], annotations[9], start_point, end_point, valid_heartbeats, start, length)
    plot_lead_v3(ax11, data[8], annotations[10], start_point, end_point, valid_heartbeats, start, length)
    plot_lead_v6(ax12, data[11], annotations[11], start_point, end_point, valid_heartbeats, start, length)

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
    #     time = (end_point - start_point)/(500*13)
    #     #prints them below the graph
    #     plt.text(0.0, -.025, ('Time between big boxes: '+ str(float(f'{time:.6f}')) + ' seconds'), fontsize=40, transform=plt.gcf().transFigure)

    # plt.show()
    plt.close('all')

    # getting the svgbites of our figure and returning it
    svgBites = return_svg_bytes()
    return svgBites


if __name__ == '__main__':
    mat = loadmat("../annotation_test_data/working/JS00008.mat")
    # print(mat)
    plot_12_ecgs(mat['val'], 'Atrial Fibrillation')
