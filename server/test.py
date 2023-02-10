from ecg_plot import plot, show, return_svg_bytes
from scipy.io import loadmat
import numpy as np


def convert_to_millivolts(microvolts: int):
    # the data is in microvolts, convert to millivolts
    return microvolts/1000


mat = loadmat("./JS00001.mat")
data = mat["val"]
ecg = []

for ecg_lead in data:
    ecg.append([convert_to_millivolts(bits) for bits in ecg_lead])

ecg = np.array(ecg)

plot(ecg)
return_svg_bytes()
show()