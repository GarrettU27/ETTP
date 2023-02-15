import sqlite3
import os
from scipy.io import loadmat
from sqlite_setup import get_sqlite_connection
import csv

path = "./a-large-scale-12-lead-electrocardiogram-database-for-arrhythmia-study-1.0.0/WFDBRecords"
conditions_path = "./a-large-scale-12-lead-electrocardiogram-database-for-arrhythmia-study-1.0.0/ConditionNames_SNOMED-CT.csv"
con = get_sqlite_connection()
cur = con.cursor()

# drop the table if it exists
cur.execute("DROP TABLE IF EXISTS ecg")
cur.execute("DROP TABLE IF EXISTS diagnosis")
cur.execute("DROP TABLE IF EXISTS arrhythmia")


cur.execute("""
CREATE TABLE ecg (
    id INTEGER PRIMARY KEY, 
    age, 
    sex, 
    graph ARRAY
)""")

cur.execute("""
CREATE TABLE diagnosis (
    id INTEGER PRIMARY KEY, 
    ecg_id INT,
    arrhythmia_id INT,
    FOREIGN KEY(ecg_id) REFERENCES ecg(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(arrhythmia_id) REFERENCES arrhythmia(id) ON DELETE CASCADE ON UPDATE CASCADE 
)""")

cur.execute("""
CREATE TABLE arrhythmia(
    id INTEGER PRIMARY KEY,
    abbreviation,
    name,
    code
)""")


processed_files = set()


def process_hea_file(hea_fname):
    f = open(hea_fname, 'r')
    lines = f.readlines()
    usable_lines = [line for line in lines[1:] if ':' in line]
    return dict(map(str.strip, usable_line[1:].split(':')) for usable_line in map(str.strip, usable_lines))


def process_mat_file(mat_fname):
    mat = loadmat(mat_fname)
    return mat["val"]


def add_to_db(hea_data, mat_data):
    cur.execute("INSERT INTO ecg VALUES(NULL, ?, ?, ?)",
                (hea_data['Age'], hea_data['Sex'], mat_data))
    ecg_row_id = cur.lastrowid

    arrhythmia_codes = hea_data['Dx'].split(',')

    for code in arrhythmia_codes:
        res = cur.execute("SELECT * FROM arrhythmia WHERE code=?", (code,))
        arrhythmia_row = res.fetchone()

        if arrhythmia_row is not None:
            arrhythmia_row_id = arrhythmia_row[0]
            cur.execute("INSERT INTO diagnosis VALUES(NULL, ?, ?)", (ecg_row_id, arrhythmia_row_id))




with open(conditions_path, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)

    for row in csvreader:
        cur.execute("INSERT INTO arrhythmia VALUES(NULL, ?, ?, ?)", (row[0], row[1].upper().replace(u'\xc2\xa0', ' '), row[2]))

# This for loop recursively checks all files in the path given and will output the array hea_files which has the path
# to all hea files found
for dirpath, dirs, files in os.walk(path):
    for filename in files:
        full_fname = os.path.join(dirpath, filename)
        fname, ext = os.path.splitext(full_fname)

        if fname not in processed_files and (ext == '.hea' or ext == '.mat'):
            hea_data = process_hea_file(fname + '.hea')
            mat_data = process_mat_file(fname + '.mat')
            add_to_db(hea_data, mat_data)

            processed_files.add(fname)

con.commit()
con.close()