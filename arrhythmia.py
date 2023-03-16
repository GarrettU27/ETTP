import typing


class Arrhythmia(typing.NamedTuple):
    id: int
    name: str


supported_arrhythmias = [
    Arrhythmia(id=53, name="Sinus Bradycardia"),
    Arrhythmia(id=57, name="Atrial Flutter"),
    Arrhythmia(id=54, name="Sinus Rhythm"),
    Arrhythmia(id=56, name="Sinus Tachycardia"),
    Arrhythmia(id=55, name="Atrial Fibrillation")
]
