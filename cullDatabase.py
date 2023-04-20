from annotations import plot12ECGs
from sqlite_setup import get_sqlite_connection

def convertName(arrhythmiaId):
    if(arrhythmiaId == 1):
        return('1st Degree AV Block')
    if(arrhythmiaId == 3):
        return('2nd Degree AV Block')
    if(arrhythmiaId == 52):
        return('WPW Syndrome')
    if(arrhythmiaId == 53):
        return('Sinus Bradycardia')
    if(arrhythmiaId == 54):
        return('Normal Sinus Rhythm')
    if(arrhythmiaId == 55):
        return('Atrial Fibrillation')
    if(arrhythmiaId == 56):
        return('Sinus Tachycardia')
    if(arrhythmiaId == 57):
        return('Atrial Flutter')

"""
cullDatabase
input arguments
    arrhythmiaIDs
        An array of integers which are the arrhythmia_ids wanted in the database
Result
    Delete all other database entries not pertaining to the ECGs which function and of particular diagnosis
    Any ECG diagnosis besides the one that the ECG is selected for will be deleted
"""
def cullDatabase(arrhythmiaIDs):
    con = get_sqlite_connection()
    cur = con.cursor()
    # This will store a tuple of (patient_id, arrhythmia_id)
    ecgsToSave = []

    # This table will be used within the DELETE FROM statement and then it will be dropped
    cur.execute("DROP TABLE IF EXISTS goodecgs")
    cur.execute("""
    CREATE TABLE goodecgs (
        id INTEGER PRIMARY KEY,
        patient_id INT,
        arrhythmia_id INT,
        FOREIGN KEY(patient_id) REFERENCES patient(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY(arrhythmia_id) REFERENCES arrhythmia(id) ON DELETE CASCADE ON UPDATE CASCADE
    )""")

    # Get number of arrhythmias in database. This will be used to test if we've run out of ECGs
    numArrhythmias = cur.execute("""
    SELECT COUNT(*)
    FROM arrhythmia
    """).fetchone()

    # Loop through all input arrhythmia IDs
    for tempId in arrhythmiaIDs:
        # Number of diagnosed arrhythmias besides the one of interest
        # This will increase by one until 200 ECGs are found
        additionalDiagnosis = -1
        # The number of ECGs that have been found which function with plot12ECGs
        numSelected = 0

        while numSelected < 200:
            additionalDiagnosis = additionalDiagnosis + 1
            if(additionalDiagnosis > numArrhythmias[0] - 1):
                print("Ran out of ECGs")
                break
            queryRes = cur.execute("""
            SELECT p1.id, p1.ecg
            FROM patient p1, diagnosis d1
            WHERE p1.id = d1.patient_id AND
                d1.arrhythmia_id = """ + str(tempId) + """ AND
                (
                    SELECT COUNT(*)
                    FROM patient p2, diagnosis d2
                    WHERE p2.id = d2.patient_id AND
                    p2.id = p1.id AND
                    d2.arrhythmia_id <> """ + str(tempId) + """
                ) = """ + str(additionalDiagnosis)
            ).fetchall()

            for ecgData in queryRes:
                myDict = {'val':ecgData[1]}
                try:
                    _ = plot12ECGs(myDict, convertName(tempId))
                    # Insert into non-delete table
                    cur.execute("INSERT INTO goodecgs VALUES(NULL, ?, ?)", (ecgData[0], tempId))
                    con.commit()
                    numSelected = numSelected + 1
                    print("tempId = " + str(tempId))
                    print("numSelected = " + str(numSelected))
                    print("--------------")
                    if numSelected >= 200:
                        break
                except Exception as error:
                    pass

    # Delete non-matching entries from diagnosis
    cur.execute("""
    DELETE FROM diagnosis
    WHERE NOT EXISTS (
        SELECT *
        FROM goodecgs
        WHERE diagnosis.patient_id = goodecgs.patient_id AND
        diagnosis.arrhythmia_id = goodecgs.arrhythmia_id
    )
    """)

    # Delete non-matching entries from patient
    cur.execute("""
    DELETE FROM patient
    WHERE NOT EXISTS (
        SELECT *
        FROM goodecgs
        WHERE patient.id = goodecgs.patient_id
    )
    """)

    cur.execute("DROP TABLE IF EXISTS goodecgs")
    con.commit()
    con.close()
