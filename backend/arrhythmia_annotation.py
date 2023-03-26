from dataclasses import dataclass


@dataclass
class ArrhythmiaAnnotation:
    id: int
    rhythm_name: str
    bpm: str
    rhythm: str
    p_wave: str
    pr_interval: str
    qrs_complex: str
    note: str


hr_data = [
    ArrhythmiaAnnotation(
        id=54,
        rhythm_name="Normal Sinus Rhythm",
        bpm="60 - 100",
        rhythm="Regular, evenly spaced",
        p_wave="Before each QRS, identical waves",
        pr_interval="0.12 - 0.20",
        qrs_complex="< 0.12",
        note="This is the rhythm of a normal healthy heart. The sinus node is triggering the cardiac activation."
    ),
    ArrhythmiaAnnotation(
        id=53,
        rhythm_name="Sinus Bradycardia",
        bpm="< 60",
        rhythm="Regular, evenly spaced",
        p_wave="Before each QRS, identical waves",
        pr_interval="0.12 - 0.20",
        qrs_complex="< 0.12",
        note="In this rhythm, the impulses originate at the SA node at a slow rate. This may be caused by increased vagal or parasympathetic tones."
    ),
    ArrhythmiaAnnotation(
        id=56,
        rhythm_name="Sinus Tachycardia",
        bpm="> 100",
        rhythm="Regular, evenly spaced",
        p_wave="Before each QRS, identical waves",
        pr_interval="0.12 - 0.20",
        qrs_complex="< 0.12",
        note="In this rhythm, the impulses originate at the SA node at a rapid rate. This may be caused by physical exercise, physical stress, or congestive heart failure."
    ),
    ArrhythmiaAnnotation(
        id=55,
        rhythm_name="Atrial Fibrillation",
        bpm="A: 350-650, V: slow to rapid",
        rhythm="Irregular spacing",
        p_wave="very rapid irregular",
        pr_interval="0.12 - 0.20",
        qrs_complex="< 0.12",
        note="In this rhythm, the impulses travel on chaotic, random pathways in the atria. This may be caused by rheumatic disease, atherosclerotic disease, hyperthyroidism, and pericarditis."
    )
]


def get_arrhythmia_annotation(arrhythmia_id: str):
    for annotation in hr_data:
        if int(arrhythmia_id) == annotation.id:
            return annotation
