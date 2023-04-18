from backend.annotations import plot_12_ecgs
from backend.arrhythmia_annotation import get_arrhythmia_annotation, get_supported_arrhythmias
from backend.sqlite_setup import get_sqlite_connection


def convert_name(arrhythmia_id: int) -> str:
    return get_arrhythmia_annotation(arrhythmia_id).rhythm_name


"""
cullDatabase
input arguments
    arrhythmiaIDs
        An array of integers which are the arrhythmia_ids wanted in the database
Result
    Delete all other database entries not pertaining to the ECGs which function and of particular diagnosis
    Any ECG diagnosis besides the one that the ECG is selected for will be deleted
"""


def cull_database():
    con = get_sqlite_connection()
    cur = con.cursor()
    arrhythmias = get_supported_arrhythmias()

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

    # Loop through all input arrhythmia IDs
    for arrhythmia in arrhythmias:
        # Number of diagnosed arrhythmias besides the one of interest
        # This will increase by one until 200 ECGs are found
        additional_diagnosis = -1
        # The number of ECGs that have been found which function with plot12ECGs
        num_selected = 0

        while num_selected < 200:
            additional_diagnosis = additional_diagnosis + 1
            query_res = cur.execute("""
            SELECT p1.id, p1.ecg
            FROM patient p1, diagnosis d1
            WHERE p1.id = d1.patient_id AND
                d1.arrhythmia_id = """ + str(arrhythmia.id) + """ AND
                (
                    SELECT COUNT(*)
                    FROM patient p2, diagnosis d2
                    WHERE p2.id = d2.patient_id AND
                    p2.id = p1.id AND
                    d2.arrhythmia_id <> """ + str(arrhythmia.id) + """
                ) = """ + str(additional_diagnosis)
                                    ).fetchall()

            for ecg_data in query_res:
                try:
                    _ = plot_12_ecgs(ecg_data[1], arrhythmia.rhythm_name)
                    # Insert into non-delete table
                    cur.execute("INSERT INTO goodecgs VALUES(NULL, ?, ?)", (ecg_data[0], arrhythmia.id))
                    con.commit()
                    num_selected = num_selected + 1
                    print("temp_id = " + str(arrhythmia.id))
                    print("num_selected = " + str(num_selected))
                    print("--------------")
                    if num_selected >= 200:
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


if __name__ == '__main__':
    cull_database()
