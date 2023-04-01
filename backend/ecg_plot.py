#!/usr/bin/env python
# code pulled from https://github.com/dy1901/ecg_plot

import io
import os
from math import ceil

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator

matplotlib.use('agg')

lead_index = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']


def plot(
        ecg,
        sample_rate=500,
        title='ECG 12',
        columns=2,
        row_height=6,
):
    """Plot multi lead ECG chart.
    # Arguments
        ecg        : m x n ECG signal data, which m is number of leads and n is length of signal.
        sample_rate: Sample rate of the signal.
        title      : Title which will be shown on top off chart
        lead_index : Lead name array in the same order of ecg, will be shown on
            left of signal plot, defaults to ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        lead_order : Lead display order
        columns    : display columns, defaults to 2
        style      : display style, defaults to None, can be 'bw' which means black white
        row_height :   how many grid should a lead signal have,
        show_lead_name : show lead name
        show_grid      : show grid
        show_separate_line  : show separate line
    """

    lead_order = list(range(0, len(ecg)))
    sections = len(ecg[0]) / sample_rate
    leads = len(lead_order)
    rows = int(ceil(leads / columns))
    display_factor = 1
    line_width = 1
    fig, ax = plt.subplots(figsize=(sections * columns * display_factor, rows * row_height / 5 * display_factor))
    display_factor = display_factor ** 0.5
    fig.subplots_adjust(
        hspace=0,
        wspace=0,
        left=0,  # the left side of the subplots of the figure
        right=1,  # the right side of the subplots of the figure
        bottom=0,  # the bottom of the subplots of the figure
        top=1
    )

    fig.suptitle(title)

    x_min = 0
    x_max = columns * sections
    y_min = row_height / 4 - (rows / 2) * row_height
    y_max = row_height / 4

    color_major = (1, 0, 0)
    color_minor = (1, 0.7, 0.7)
    color_line = (0, 0, 0)

    ax.set_xticks(np.arange(x_min, x_max, 0.2))
    ax.set_yticks(np.arange(y_min, y_max, 0.5))

    ax.minorticks_on()

    ax.set_yticklabels([])
    ax.set_xticklabels([])

    ax.xaxis.set_minor_locator(AutoMinorLocator(5))

    ax.grid(which='major', linestyle='-', linewidth=0.5 * display_factor, color=color_major)
    ax.grid(which='minor', linestyle='-', linewidth=0.5 * display_factor, color=color_minor)

    ax.set_ylim(y_min, y_max)
    ax.set_xlim(x_min, x_max)

    for column in range(0, columns):
        for row in range(0, rows):
            if column * rows + row < leads:
                y_offset = -(row_height / 2) * ceil(row % rows)
                x_offset = 0
                t_lead = lead_order[column * rows + row]

                if column > 0:
                    x_offset = sections * column
                    ax.plot([x_offset, x_offset],
                            [ecg[t_lead][0] + y_offset - 0.3, ecg[t_lead][0] + y_offset + 0.3],
                            linewidth=line_width * display_factor, color=color_line)

                step = 1.0 / sample_rate
                ax.text(x_offset + 0.07, y_offset - 0.5, lead_index[t_lead], fontsize=9 * display_factor)
                ax.plot(
                    np.arange(0, len(ecg[t_lead]) * step, step) + x_offset,
                    ecg[t_lead] + y_offset,
                    linewidth=line_width * display_factor,
                    color=color_line
                )


DEFAULT_PATH = '../'
show_counter = 1


def show_svg(tmp_path=DEFAULT_PATH):
    """Plot multi lead ECG chart.
    # Arguments
        tmp_path: path for temporary saving the result svg file
    """
    global show_counter
    file_name = tmp_path + "show_tmp_file_{}.svg".format(show_counter)
    plt.savefig(file_name)
    os.system("open {}".format(file_name))
    show_counter += 1
    plt.close()


def show():
    plt.show()


def save_as_png(file_name, path=DEFAULT_PATH, dpi=100, layout='tight'):
    """Plot multi lead ECG chart.
    # Arguments
        file_name: file_name
        path     : path to save image, defaults to current folder
        dpi      : set dots per inch (dpi) for the saved image
        layout   : Set equal to "tight" to include ax labels on saved image
    """
    plt.ioff()
    plt.savefig(os.path.join(path, file_name + '.png'), dpi=dpi, bbox_inches=layout)
    plt.close()


def save_as_svg(file_name, path=DEFAULT_PATH):
    """Plot multi lead ECG chart.
    # Arguments
        file_name: file_name
        path     : path to save image, defaults to current folder
    """
    plt.ioff()
    plt.savefig(path + file_name + '.svg')
    plt.close()


def return_svg_bytes():
    fig = plt.gcf()
    plt.ioff()

    buf = io.BytesIO()
    fig.savefig(buf, format="svg")
    buf.seek(0)

    svg_bytes = buf.read()
    plt.close()
    return svg_bytes


def return_png_bytes():
    fig = plt.gcf()
    plt.ioff()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    buf.seek(0)

    # compress image
    # https://stackoverflow.com/questions/10784652/png-options-to-produce-smaller-file-size-when-using-savefig
    # https://stackoverflow.com/questions/35004067/compress-png-image-in-python-using-pil
    # image = Image.open(buf)
    # compressed_image = image.convert('RGB').convert('P', palette=Image.ADAPTIVE)
    #
    # buf2 = io.BytesIO()
    # image.save(buf2, format='PNG')
    # buf2.seek(0)

    plt.close()

    return buf.read()


def save_as_jpg(file_name, path=DEFAULT_PATH):
    """Plot multi lead ECG chart.
    # Arguments
        file_name: file_name
        path     : path to save image, defaults to current folder
    """
    plt.ioff()
    plt.savefig(path + file_name + '.jpg')
    plt.close()
