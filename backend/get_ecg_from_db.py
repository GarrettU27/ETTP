import math
import random
from dataclasses import dataclass
from sqlite3 import Cursor
from typing import List, Final

import numpy.typing

from backend.arrhythmia_annotation import ArrhythmiaAnnotation, get_arrhythmia_annotation
from backend.sqlite_setup import get_sqlite_connection

SINUS_RHYTHM_ID: Final[int] = 54


@dataclass
class Arrhythmia:
    id: str
    amount: int


@dataclass
class Question:
    ecg: numpy.typing.NDArray[float]
    correct_answer: str
    choices: List[str]


@dataclass
class Flashcard:
    ecg: numpy.typing.NDArray[float]
    arrhythmia_annotation: ArrhythmiaAnnotation


def get_training_flashcards(arrhythmia_id_array: List[int], number_of_flashcards: int) -> List[Flashcard]:
    total_arrhythmias = len(arrhythmia_id_array)
    if number_of_flashcards < total_arrhythmias:
        raise ValueError("numEcg >= len(idArray) must be true")

    # Decide number of ECGs for each arrhythmia
    random.seed()

    # Calculate the number of ECGs each arrhythmia can have while keeping below the requested number of ECGs
    flashcards_per_arrhythmia = math.floor(number_of_flashcards / total_arrhythmias)
    arrhythmia_amounts = [flashcards_per_arrhythmia] * total_arrhythmias  # Each arrhythmia gets base number of ECGs

    # Distribute any extra question slots amongst the different
    # arrhythmias. This happens when the number of arrhythmias
    # doesn't divide the number of questions nicely. For example,
    # a user may want to test on 6 arrhythmias but ask for 20 questions
    # In that case, there will be 2 questions which will have an ECG
    # randomly assigned
    for i in range(number_of_flashcards - (flashcards_per_arrhythmia * total_arrhythmias)):
        j = random.randrange(0, total_arrhythmias)
        while arrhythmia_amounts[j] > flashcards_per_arrhythmia:
            j = random.randrange(0, total_arrhythmias)
        arrhythmia_amounts[j] = arrhythmia_amounts[j] + 1

    trained_arrhythmias = []
    for (i, arrhythmia_id) in enumerate(arrhythmia_id_array):
        trained_arrhythmias.append(Arrhythmia(id=str(arrhythmia_id), amount=arrhythmia_amounts[i]))

    con = get_sqlite_connection()
    cur = con.cursor()

    flashcards = []

    for arrhythmia in trained_arrhythmias:
        for i in range(arrhythmia.amount):
            patient_id = get_random_patient_id(cur, arrhythmia.id)
            ecg = get_patients_ecg(cur, patient_id)
            flashcards.append(Flashcard(
                ecg=ecg,
                arrhythmia_annotation=get_arrhythmia_annotation(arrhythmia.id)
            ))

    return flashcards


def get_testing_questions(arrhythmia_id_array: List[int], number_of_questions: int) -> List[Question]:
    total_arrhythmias = len(arrhythmia_id_array) + 1
    if number_of_questions < total_arrhythmias:
        raise ValueError("numEcg >= len(idArray) must be true")

    # Decide number of ecgs for each arrhythmia
    random.seed()
    arrhythmia_amounts = [1] * total_arrhythmias  # Make sure each arrhythmia has at least one ecg

    # The sum of all elements of arrhythmia amount must be equal to total_ecgs
    # However, each element in arrhythmia amount is already one, so we only
    # need to add total_ecgs - (total_arrhythmias + 1) more to the sum
    for i in range(number_of_questions - total_arrhythmias):
        j = random.randrange(0, total_arrhythmias)
        arrhythmia_amounts[j] = arrhythmia_amounts[j] + 1

    tested_arrhythmia_ids = arrhythmia_id_array
    tested_arrhythmia_ids.append(SINUS_RHYTHM_ID)
    tested_arrhythmias = []
    for (i, arrhythmia_id) in enumerate(tested_arrhythmia_ids):
        tested_arrhythmias.append(Arrhythmia(id=str(arrhythmia_id), amount=arrhythmia_amounts[i]))

    con = get_sqlite_connection()
    cur = con.cursor()

    questions = []
    possible_choices = [get_arrhythmia_annotation(arrhythmia.id).rhythm_name for arrhythmia in tested_arrhythmias]

    for arrhythmia in tested_arrhythmias:
        for i in range(arrhythmia.amount):
            patient_id = get_random_patient_id(cur, arrhythmia.id)
            ecg = get_patients_ecg(cur, patient_id)

            choices = []
            current_name = get_arrhythmia_annotation(arrhythmia.id).rhythm_name
            possible_choices.remove(current_name)
            choices.append(current_name)
            other_choices = random.sample(possible_choices, min(len(possible_choices), 3))
            possible_choices.append(current_name)
            choices.extend(other_choices)
            random.shuffle(choices)

            questions.append(Question(
                ecg=ecg,
                correct_answer=get_arrhythmia_annotation(arrhythmia.id).rhythm_name,
                choices=choices
            ))

    random.shuffle(questions)
    return questions


def get_random_patient_id(cur: Cursor, arrhythmia_id: str) -> str:
    """
    Returns the patient id of a patient with the proper arrhythmia and
    only that arrhythmia
    """

    return str(cur.execute("""
                SELECT patient_id, arrhythmia_id
                FROM diagnosis
                WHERE arrhythmia_id = ?
                ORDER BY RANDOM()
            """, (arrhythmia_id,)).fetchone()[0])


def get_patients_ecg(cur: Cursor, patient_id: str) -> numpy.typing.NDArray[float]:
    return cur.execute("""
                SELECT patient.ecg 
                FROM patient 
                WHERE patient.id = ? 
                """, (patient_id,)).fetchone()[0]
