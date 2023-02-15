import base64
from ecg_plot import plot, plot_12, plot_1, show, return_svg_bytes, return_png_bytes
from scipy.io import loadmat
import numpy as np


def convert_to_millivolts(microvolts: int):
    # the data is in microvolts, convert to millivolts
    return microvolts/1000


def get_ecg_svg():
    mat = loadmat("JS00001.mat")
    data = mat["val"]
    ecg = []

    for ecg_lead in data:
        ecg.append([convert_to_millivolts(bits) for bits in ecg_lead][0:1300])

    ecg = np.array(ecg)

    plot(ecg, columns=3)
    return return_svg_bytes()


def get_ecg_png():
    mat = loadmat("JS00001.mat")
    data = mat["val"]
    ecg = []

    for ecg_lead in data:
        ecg.append([convert_to_millivolts(bits) for bits in ecg_lead])

    ecg = np.array(ecg)

    plot(ecg)

    return return_png_bytes()