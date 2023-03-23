# USAGE DETAIL: the path you decide to save to (the default
# here is Sample_ECGs, must already exist on your computer

import os.path
import numpy as np
from backend.sqlite_setup import get_sqlite_connection
from ecg_plot import plot,  save_as_png
from backend.generate_ecg_plot import convert_to_millivolts

patient_ids = [11223, 11225, 11226, 11227, 11228, 16, 29, 31, 20, 44, 65, 11, 54, 91, 103, 106, 37, 47, 57, 82, 101, 278, 396, 579, 869, 988]

con = get_sqlite_connection()
cur = con.cursor()

for patient_id in patient_ids:
    res = cur.execute("SELECT * FROM patient where id=?", (patient_id,))
    patient_row = res.fetchone()
    graph = patient_row[3]
    ecg = []

    for ecg_lead in graph:
        ecg.append([convert_to_millivolts(bits) for bits in ecg_lead][0:1300])

    ecg = np.array(ecg)

    plot(ecg, columns=4)
    save_as_png(str(patient_id), os.path.relpath("./Sample_ECGs"))
