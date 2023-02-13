import base64
from ecg_plot import plot, show, return_svg_bytes, return_png_bytes
from scipy.io import loadmat
import numpy as np


def convert_to_millivolts(microvolts: int):
    # the data is in microvolts, convert to millivolts
    return microvolts/1000


def get_ecg_svg():
    mat = loadmat("./JS00001.mat")
    data = mat["val"]
    ecg = []

    for ecg_lead in data:
        ecg.append([convert_to_millivolts(bits) for bits in ecg_lead])

    ecg = np.array(ecg)

    plot(ecg)
    return return_svg_bytes()


def get_ecg_png():
    mat = loadmat("./JS00001.mat")
    data = mat["val"]
    ecg = []

    for ecg_lead in data:
        ecg.append([convert_to_millivolts(bits) for bits in ecg_lead])

    ecg = np.array(ecg)

    plot(ecg)

    png_bytes = return_png_bytes()
    encoded_bytes = base64.b64encode(png_bytes)
    encoded_bytes_string = encoded_bytes.decode('ascii')
    base64_string = f"data:image/png;base64,{encoded_bytes_string}"

    return base64_string