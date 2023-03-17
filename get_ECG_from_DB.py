from sqlite_setup import get_sqlite_connection
import random, math
import csv

#Argument: arrhythmia IDs (array of ints)
def get_train_ecgs(idArray, numEcg):
    numArrhy = len(idArray)
    if(type(idArray) != list):
        print("get_test_ecgs: Invalid argument. idArray must by of type list")
        return
    elif(type(numEcg) != int):
        print("get_test_ecgs: Invalid argument. numEcg must by of type int")
        return
    elif(numEcg < numArrhy):
        print("get_test_ecgs: Invalid argument. numEcg >= len(idArray) must be true")
        return

    random.seed()
    # Decide number of ECGs for each arrhythmia
    # Calculate the number of ECGs each arrhythmia can have while keeping below the requested number of ECGs
    numEqualEcgs = math.floor(numEcg / numArrhy)
    arrhyCount = [numEqualEcgs] * numArrhy #Each arrhythmia gets base number of ECGs
    for i in range(numEcg - numEqualEcgs * numArrhy):
        tempInd = random.randrange(0, numArrhy)
        while arrhyCount[tempInd] > numEqualEcgs:
            tempInd = random.randrange(0, numArrhy)
        arrhyCount[tempInd] = arrhyCount[tempInd] + 1
    #Set up return array
    #returnedEcgs is a list where the ecgs stored at the index i have the arrhythmia which was given at index i of
    # idArray. Each element at index i of returnedEcgs is a list of length equal to the value of arrhyCount[i]. Each of
    # the elements within returnedEcgs[i] is an ecg with the arrhythmia given at idArray[i].
    returnedEcgs = [0] * numArrhy
    for i in range(numArrhy):
        returnedEcgs[i] = [0] * arrhyCount[i]
    #Get ecgs from database
    con = get_sqlite_connection()
    cur = con.cursor()
    for i in range(numArrhy): #For each type of arrhythmia given
        for j in range(arrhyCount[i]): #For each ecg that will be fetched for a particular arrhythmia
            tempECGID = cur.execute(
                "SELECT ecg.id "
                "FROM ecg, diagnosis "
                "WHERE ecg.id = diagnosis.ecg_id "
                    "AND diagnosis.arrhythmia_id = " + str(idArray[i]) + " "
                "ORDER BY RANDOM() "
                "LIMIT 1"
            ).fetchone()[0]
            diags = cur.execute(
                "SELECT diagnosis.arrhythmia_id "
                "FROM diagnosis "
                "WHERE diagnosis.ecg_id = " + str(tempECGID)
            ).fetchall()
            getNewECG = False
            for k in range(diags.__len__()):
                for l in range(numArrhy):
                    if i == l: #If current arrhythmia is equal to comparing one
                        pass
                    if diags[k] == idArray[l]: #If diagnosed arrhythmia is the same as a different requested arrhythmia
                        j = j - 1 #Decrement j (don't count this arrhythmia
                        getNewECG = True
                        break
                if getNewECG:
                    break
            if getNewECG:
                pass
            tempECGGraph = cur.execute(
                "SELECT ecg.graph "
                "FROM ecg "
                "WHERE ecg.id = " + str(tempECGID)
            ).fetchone()[0]
            returnedEcgs[i][j] = tempECGGraph
    return returnedEcgs

def get_test_ecgs(idArray, numEcg):
    numArrhy = len(idArray)
    if(type(idArray) != list):
        print("get_train_ecgs: Invalid argument. idArray must by of type list")
        return
    elif(type(numEcg) != int):
        print("get_train_ecgs: Invalid argument. numEcg must by of type int")
        return
    elif(numEcg < numArrhy):
        print("get_train_ecgs: Invalid argument. numEcg >= len(idArray) must be true")
        return

    random.seed()
    #Decide number of ecgs for each arrhythmia
    arrhyCount = [1] * numArrhy #Make sure each arrhythmia has at least one ecg
    for i in range(numEcg - numArrhy):
        tempInd = random.randrange(0, numArrhy)
        arrhyCount[tempInd] = arrhyCount[tempInd] + 1
    # Set up return array
    # returnedEcgs is a list where the ecgs stored at the index i have the arrhythmia which was given at index i of
    # idArray. Each element at index i of returnedEcgs is a list of length equal to the value of arrhyCount[i]. Each of
    # the elements within returnedEcgs[i] is an ecg with the arrhythmia given at idArray[i].
    returnedEcgs = [0] * numArrhy
    for i in range(numArrhy):
        returnedEcgs[i] = [0] * arrhyCount[i]
    # Get ecgs from database
    con = get_sqlite_connection()
    cur = con.cursor()
    for i in range(numArrhy): # For each type of arrhythmia given
        for j in range(arrhyCount[i]): # For each ecg that will be fetched for a particular arrhythmia
            tempECGID = cur.execute(
                "SELECT ecg.id "
                "FROM ecg, diagnosis "
                "WHERE ecg.id = diagnosis.ecg_id "
                    "AND diagnosis.arrhythmia_id = " + str(idArray[i]) + " "
                "ORDER BY RANDOM() "
                "LIMIT 1"
            ).fetchone()[0]
            diags = cur.execute(
                "SELECT diagnosis.arrhythmia_id "
                "FROM diagnosis "
                "WHERE diagnosis.ecg_id = " + str(tempECGID)
            ).fetchall()
            getNewECG = False
            for k in range(diags.__len__()):
                for l in range(numArrhy):
                    if i == l: #If current arrhythmia is equal to comparing one
                        pass
                    if diags[k] == idArray[l]: #If diagnosed arrhythmia is the same as a different requested arrhythmia
                        j = j - 1 #Decrement j (don't count this arrhythmia
                        getNewECG = True
                        break
                if getNewECG:
                    break
            if getNewECG:
                pass
            tempECGGraph = cur.execute(
                "SELECT ecg.graph "
                "FROM ecg "
                "WHERE ecg.id = " + str(tempECGID)
            ).fetchone()[0]
            returnedEcgs[i][j] = tempECGGraph
    return returnedEcgs

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