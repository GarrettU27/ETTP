import math
import random

from sqlite_setup import get_sqlite_connection


# Argument: arrhythmia IDs (array of ints)
def get_train_ecgs(id_array, num_ecg):
    num_arrhy = len(id_array)
    if type(id_array) != list:
        print("get_test_ecgs: Invalid argument. idArray must by of type list")
        return
    elif type(num_ecg) != int:
        print("get_test_ecgs: Invalid argument. numEcg must by of type int")
        return
    elif num_ecg < num_arrhy:
        print("get_test_ecgs: Invalid argument. numEcg >= len(idArray) must be true")
        return

    random.seed()
    # Decide number of ECGs for each arrhythmia
    # Calculate the number of ECGs each arrhythmia can have while keeping below the requested number of ECGs
    num_equal_ecgs = math.floor(num_ecg / num_arrhy)
    arrhy_count = [num_equal_ecgs] * num_arrhy  # Each arrhythmia gets base number of ECGs
    for i in range(num_ecg - num_equal_ecgs * num_arrhy):
        temp_ind = random.randrange(0, num_arrhy)
        while arrhy_count[temp_ind] > num_equal_ecgs:
            temp_ind = random.randrange(0, num_arrhy)
        arrhy_count[temp_ind] = arrhy_count[temp_ind] + 1
    # Set up return array
    # returned_ecgs is a list where the ecgs stored at the index i have the arrhythmia which was given at index i of
    # idArray. Each element at index i of returned_ecgs is a list of length equal to the value of arrhy_count[i]. Each of
    # the elements within returned_ecgs[i] is an ecg with the arrhythmia given at idArray[i].
    returned_ecgs = [0] * num_arrhy
    for i in range(num_arrhy):
        returned_ecgs[i] = [0] * arrhy_count[i]
    # Get ecgs from database
    con = get_sqlite_connection()
    cur = con.cursor()
    for i in range(num_arrhy):  # For each type of arrhythmia given
        for j in range(arrhy_count[i]):  # For each ecg that will be fetched for a particular arrhythmia
            temp_ecg_id = cur.execute(
                "SELECT ecg.id "
                "FROM ecg, diagnosis "
                "WHERE ecg.id = diagnosis.ecg_id "
                "AND diagnosis.arrhythmia_id = " + str(id_array[i]) + " "
                                                                     "ORDER BY RANDOM() "
                                                                     "LIMIT 1"
            ).fetchone()[0]
            diags = cur.execute(
                "SELECT diagnosis.arrhythmia_id "
                "FROM diagnosis "
                "WHERE diagnosis.ecg_id = " + str(temp_ecg_id)
            ).fetchall()
            get_new_ecg = False
            for k in range(diags.__len__()):
                for l in range(num_arrhy):
                    if i == l:  # If current arrhythmia is equal to comparing one
                        pass
                    if diags[k] == id_array[
                        l]:  # If diagnosed arrhythmia is the same as a different requested arrhythmia
                        j = j - 1  # Decrement j (don't count this arrhythmia
                        get_new_ecg = True
                        break
                if get_new_ecg:
                    break
            if get_new_ecg:
                pass
            temp_ecg_graph = cur.execute(
                "SELECT ecg.graph "
                "FROM ecg "
                "WHERE ecg.id = " + str(temp_ecg_id)
            ).fetchone()[0]
            returned_ecgs[i][j] = temp_ecg_graph
    return returned_ecgs


def get_test_ecgs(id_array, num_ecg):
    num_arrhy = len(id_array)
    if type(id_array) != list:
        print("get_train_ecgs: Invalid argument. idArray must by of type list")
        return
    elif type(num_ecg) != int:
        print("get_train_ecgs: Invalid argument. numEcg must by of type int")
        return
    elif num_ecg < num_arrhy:
        print("get_train_ecgs: Invalid argument. numEcg >= len(idArray) must be true")
        return

    random.seed()
    # Decide number of ecgs for each arrhythmia
    arrhy_count = [1] * num_arrhy  # Make sure each arrhythmia has at least one ecg
    for i in range(num_ecg - num_arrhy):
        temp_ind = random.randrange(0, num_arrhy)
        arrhy_count[temp_ind] = arrhy_count[temp_ind] + 1
    # Set up return array
    # returned_ecgs is a list where the ecgs stored at the index i have the arrhythmia which was given at index i of
    # idArray. Each element at index i of returned_ecgs is a list of length equal to the value of arrhy_count[i]. Each of
    # the elements within returned_ecgs[i] is an ecg with the arrhythmia given at idArray[i].
    returned_ecgs = [0] * num_arrhy
    for i in range(num_arrhy):
        returned_ecgs[i] = [0] * arrhy_count[i]
    # Get ecgs from database
    con = get_sqlite_connection()
    cur = con.cursor()
    for i in range(num_arrhy):  # For each type of arrhythmia given
        for j in range(arrhy_count[i]):  # For each ecg that will be fetched for a particular arrhythmia
            temp_ecg_id = cur.execute(
                "SELECT ecg.id "
                "FROM ecg, diagnosis "
                "WHERE ecg.id = diagnosis.ecg_id "
                "AND diagnosis.arrhythmia_id = " + str(id_array[i]) + " "
                                                                     "ORDER BY RANDOM() "
                                                                     "LIMIT 1"
            ).fetchone()[0]
            diags = cur.execute(
                "SELECT diagnosis.arrhythmia_id "
                "FROM diagnosis "
                "WHERE diagnosis.ecg_id = " + str(temp_ecg_id)
            ).fetchall()
            get_new_ecg = False
            for k in range(diags.__len__()):
                for l in range(num_arrhy):
                    if i == l:  # If current arrhythmia is equal to comparing one
                        pass
                    if diags[k] == id_array[
                        l]:  # If diagnosed arrhythmia is the same as a different requested arrhythmia
                        j = j - 1  # Decrement j (don't count this arrhythmia
                        get_new_ecg = True
                        break
                if get_new_ecg:
                    break
            if get_new_ecg:
                pass
            temp_ecg_graph = cur.execute(
                "SELECT ecg.graph "
                "FROM ecg "
                "WHERE ecg.id = " + str(temp_ecg_id)
            ).fetchone()[0]
            returned_ecgs[i][j] = temp_ecg_graph
    return returned_ecgs


def get_first_entry(abbreviation_name):
    con = get_sqlite_connection()
    cur = con.cursor()

    res = cur.execute(
        "SELECT * "
        "FROM ecg, diagnosis, arrhythmia "
        "WHERE ecg.id = diagnosis.ecg_id "
        "AND diagnosis.arrhythmia_id = arrhythmia.id "
        "AND arrhythmia.abbreviation = '" + abbreviation_name + "'"
    )
    myEntry = res.fetchone()
    con.close()
    return myEntry


def get_all_entries(abbreviation_name):
    con = get_sqlite_connection()
    cur = con.cursor()

    res = cur.execute(
        "SELECT * "
        "FROM ecg, diagnosis, arrhythmia "
        "WHERE ecg.id = diagnosis.ecg_id "
        "AND diagnosis.arrhythmia_id = arrhythmia.id "
        "AND arrhythmia.abbreviation = '" + abbreviation_name + "'"
    )
    myEntries = res.fetchall()
    con.close()
    return myEntries
