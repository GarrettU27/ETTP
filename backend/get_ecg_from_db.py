import io
import math
import random
from dataclasses import dataclass
from sqlite3 import Cursor
from typing import List, Callable

from backend.generate_ecg_plot import create_test_ecg, create_train_ecg
from backend.sqlite_setup import get_sqlite_connection


@dataclass
class Arrhythmia:
    id: str
    amount: int


@dataclass
class Question:
    ecg: io.BytesIO
    correct_answer: str
    choices: List[str]


def get_training_questions(arrhythmia_id_array: List[int], number_of_questions: int):
    total_arrhythmias = len(arrhythmia_id_array)
    if number_of_questions < total_arrhythmias:
        raise ValueError("numEcg >= len(idArray) must be true")

    # Decide number of ECGs for each arrhythmia
    random.seed()

    # Calculate the number of ECGs each arrhythmia can have while keeping below the requested number of ECGs
    questions_per_arrhythmia = math.floor(number_of_questions / total_arrhythmias)
    arrhythmia_amounts = [questions_per_arrhythmia] * total_arrhythmias  # Each arrhythmia gets base number of ECGs

    # Distribute any extra question slots amongst the different
    # arrhythmias. This happens when the number of arrhythmias
    # doesn't divide the number of questions nicely. For example,
    # a user may want to test on 6 arrhythmias but ask for 20 questions
    # In that case, there will be 2 questions which will have an ECG
    # randomly assigned
    for i in range(number_of_questions - (questions_per_arrhythmia * total_arrhythmias)):
        j = random.randrange(0, total_arrhythmias)
        while arrhythmia_amounts[j] > questions_per_arrhythmia:
            j = random.randrange(0, total_arrhythmias)
        arrhythmia_amounts[j] = arrhythmia_amounts[j] + 1

    tested_arrhythmias = []
    for (i, arrhythmia_id) in enumerate(arrhythmia_id_array):
        tested_arrhythmias.append(Arrhythmia(id=str(arrhythmia_id), amount=arrhythmia_amounts[i]))

    return create_return_array(tested_arrhythmias, create_train_ecg)


def get_testing_questions(arrhythmia_id_array: List[int], number_of_questions: int):
    total_arrhythmias = len(arrhythmia_id_array)
    if number_of_questions < total_arrhythmias:
        raise ValueError("numEcg >= len(idArray) must be true")

    # Decide number of ecgs for each arrhythmia
    random.seed()
    arrhythmia_amounts = [1] * total_arrhythmias  # Make sure each arrhythmia has at least one ecg

    # The sum of all elements of arrhythmia amount must be equal to total_ecgs
    # However, each element in arrhythmia amount is already one, so we only
    # need to add total_ecgs - total_arrhythmias more to the sum
    for i in range(number_of_questions - total_arrhythmias):
        j = random.randrange(0, total_arrhythmias)
        arrhythmia_amounts[j] = arrhythmia_amounts[j] + 1

    tested_arrhythmias = []
    for (i, arrhythmia_id) in enumerate(arrhythmia_id_array):
        tested_arrhythmias.append(Arrhythmia(id=str(arrhythmia_id), amount=arrhythmia_amounts[i]))

    questions = create_return_array(tested_arrhythmias, create_test_ecg)
    random.shuffle(questions)

    return questions


def create_return_array(arrhythmias: List[Arrhythmia], grapher: Callable) -> List[Question]:
    con = get_sqlite_connection()
    cur = con.cursor()

    questions = []
    choices = [get_arrhythmia_name(cur, arrhythmia.id) for arrhythmia in arrhythmias]

    # add sinus rhythm to choices
    choices.append(get_arrhythmia_name(cur, "54"))

    for arrhythmia in arrhythmias:
        for i in range(arrhythmia.amount):
            patient_id = get_random_patient_id(cur, arrhythmia.id)
            ecg = get_patients_ecg(cur, patient_id)
            questions.append(Question(
                ecg=grapher(ecg),
                correct_answer=get_arrhythmia_name(cur, arrhythmia.id),
                choices=choices
            ))

    return questions


def get_random_patient_id(cur: Cursor, arrhythmia_id: str) -> str:
    """
    Returns the patient id of a patient with the proper arrhythmia and
    only that arrhythmia
    """

    return str(cur.execute("""
                SELECT patient_id, arrhythmia_id, COUNT(patient_id) c
                FROM diagnosis
                WHERE arrhythmia_id = ?
                GROUP BY patient_id HAVING c = 1
                ORDER BY RANDOM()
            """, (arrhythmia_id,)).fetchone()[0])


def get_patients_ecg(cur: Cursor, patient_id: str) -> io.BytesIO:
    return cur.execute("""
                SELECT patient.ecg 
                FROM patient 
                WHERE patient.id = ? 
                """, (patient_id,)).fetchone()[0]


def get_arrhythmia_name(cur: Cursor, arrhythmia_id: str) -> str:
    return cur.execute("""
                    SELECT arrhythmia.name
                    FROM arrhythmia
                    WHERE arrhythmia.id = ? 
                    """, (arrhythmia_id,)).fetchone()[0]
