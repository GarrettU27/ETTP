import sqlite3
import os
from scipy.io import loadmat
from sqlite_setup import get_sqlite_connection
import csv

def getFirstEntry(abbreviationName):
    con = get_sqlite_connection()
    cur = con.cursor()

    res = cur.execute(
        "SELECT * "
            "FROM ecg, diagnosis, arrhythmia "
            "WHERE ecg.id = diagnosis.ecg_id "
                "AND diagnosis.arrhythmia_id = arrhythmia.id "
                "AND arrhythmia.abbreviation = '" + abbreviationName + "'"
    )
    myEntry = res.fetchone()
    con.close()
    return myEntry

def getAllEntries(abbreviationName):
    con = get_sqlite_connection()
    cur = con.cursor()

    res = cur.execute(
        "SELECT * "
            "FROM ecg, diagnosis, arrhythmia "
            "WHERE ecg.id = diagnosis.ecg_id "
                "AND diagnosis.arrhythmia_id = arrhythmia.id "
                "AND arrhythmia.abbreviation = '" + abbreviationName + "'"
    )
    myEntries = res.fetchall()
    con.close()
    return myEntries


print(type(getAllEntries("JEB")[0][0]))
