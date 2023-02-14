import sqlite3
import os
from scipy.io import loadmat
import numpy as np

path = "./a-large-scale-12-lead-electrocardiogram-database-for-arrhythmia-study-1.0.0/WFDBRecords/01/"

con = sqlite3.connect("ETTP.db")
cur = con.cursor()

processed_files = set()


def process_hea_file(hea_fname):
    f = open(hea_fname, 'r')
    lines = f.readlines()
    usable_lines = [line for line in lines if ":" in line]
    return dict(usable_line.split(':') for usable_line in usable_lines)


def process_mat_file(mat_fname):
    mat = loadmat(mat_fname)
    return mat["val"]


def add_to_db(hea_data, mat_data):
    print(hea_data)
    print(mat_data)


# This for loop recursively checks all files in the path given and will output the array hea_files which has the path
# to all hea files found
for dirpath, dirs, files in os.walk(path):
    for filename in files:
        full_fname = os.path.join(dirpath, filename)
        fname, ext = os.path.splitext(full_fname)

        if fname not in processed_files:
            hea_data = process_hea_file(fname + '.hea')
            mat_data = process_mat_file(fname + '.mat')
            add_to_db(hea_data, mat_data)

            processed_files.add(fname)
            print(processed_files)