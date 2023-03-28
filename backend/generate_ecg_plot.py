import io

import numpy as np
from scipy.io import loadmat

from backend.annotations import plot12ECGs
from backend.ecg_plot import plot, return_png_bytes


def convert_to_millivolts(microvolts: int):
    # the data is in microvolts, convert to millivolts
    return microvolts / 1000


def get_ecg_svg():
    mat = loadmat("./JS00001.mat")
    data = mat["val"]
    ecg = []

    for ecg_lead in data:
        ecg.append([convert_to_millivolts(bits) for bits in ecg_lead][0:1300])

    ecg = np.array(ecg)

    plot(ecg, columns=4)
    return return_png_bytes()


def create_train_ecg(data) -> io.BytesIO:
    return plot12ECGs(data)


def create_test_ecg(data) -> io.BytesIO:
    ecg = []

    for ecg_lead in data:
        ecg.append([convert_to_millivolts(bits) for bits in ecg_lead][0:1300])

    ecg = np.array(ecg)

    plot(ecg, columns=4)
    return return_png_bytes()
