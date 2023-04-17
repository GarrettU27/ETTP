from annotations import plot12ECGs
from sqlite_setup import get_sqlite_connection

def convertName(arrhythmiaId):
    if(arrhythmiaId == 1):
        return('1st Degree AV Block')
    if(arrhythmiaId == 55):
        return('Atrial Fibrillation')
    if(arrhythmiaId == 54):
        return('Normal Sinus Rhythm')
    if(arrhythmiaId == 56):
        return('Sinus Tachycardia')

con = get_sqlite_connection()
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS goodecgs")
cur.execute("DROP TABLE IF EXISTS badecgs")

cur.execute("""
CREATE TABLE goodecgs (
    id INTEGER PRIMARY KEY,
    patient_id INT,
    arrhythmia_id INT,
    FOREIGN KEY(patient_id) REFERENCES patient(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(arrhythmia_id) REFERENCES arrhythmia(id) ON DELETE CASCADE ON UPDATE CASCADE
)""")

cur.execute("""
CREATE TABLE badecgs (
    id INTEGER PRIMARY KEY,
    patient_id INT,
    arrhythmia_id INT,
    error_text TINYTEXT,
    FOREIGN KEY(patient_id) REFERENCES patient(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(arrhythmia_id) REFERENCES arrhythmia(id) ON DELETE CASCADE ON UPDATE CASCADE
)""")

goodecgsId = 1
badecgsId = 1

# Array of arrhythmia ids of interest
arrhyIds = [1, 54, 55, 56]

for tempId in arrhyIds:
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
        ) = 0
    """).fetchall()

    numInserted = 0
    for ecgData in queryRes:
        print("--- patientId = " + str(ecgData[0]) + " ---")
        print("arrhythmia id = " + str(tempId))
        myDict = {'val':ecgData[1]}
        try:
            _ = plot12ECGs(myDict, convertName(tempId))
            cur.execute("INSERT INTO goodecgs VALUES(?, ?, ?)", (goodecgsId, ecgData[0], tempId))
            con.commit()
            numInserted = numInserted + 1
            goodecgsId = goodecgsId + 1
            if numInserted >= 200:
                break
            print("No errors")
        except Exception as error:
            print("Yes errors")
            cur.execute("INSERT INTO badecgs VALUES(?, ?, ?, ?)", (badecgsId, ecgData[0], tempId, str(error)))
            con.commit()
            badecgsId = badecgsId + 1

con.commit()
con.close()