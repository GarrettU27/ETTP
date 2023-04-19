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
        note="This is the rhythm of a normal healthy heart. The sinus node is triggering the cardiac activation.",
    ),
    ArrhythmiaAnnotation(
        id=53,
        rhythm_name="Sinus Bradycardia",
        bpm="< 60",
        rhythm="Regular, evenly spaced",
        p_wave="Before each QRS, identical waves",
        pr_interval="0.12 - 0.20",
        qrs_complex="< 0.12",
        note="This is an atrial arrhythmia. In this rhythm, the impulses originate at the SA node at a slow rate. This may be caused by increased vagal or parasympathetic tones. It is often asymptomatic because heart rates in the 40s and 50s bpm can be tolerated.",
    ),
    ArrhythmiaAnnotation(
        id=56,
        rhythm_name="Sinus Tachycardia",
        bpm="> 100",
        rhythm="Regular, evenly spaced",
        p_wave="Before each QRS, identical waves",
        pr_interval="0.12 - 0.20",
        qrs_complex="< 0.12",
        note="This is an atrial arrhythmia. In this rhythm, the impulses originate at the SA node at a rapid rate. This may be caused by physical exercise, physical stress, or congestive heart failure.",
    ),
    ArrhythmiaAnnotation(
        id=55,
        rhythm_name="Atrial Fibrillation",
        bpm="Atrial: 350-650, Ventricular: slow to rapid",
        rhythm="Irregular spacing",
        p_wave="very rapid irregular",
        pr_interval="0.12 - 0.20",
        qrs_complex="< 0.12",
        note="This is an atrial arrhythmia. In this rhythm, the impulses travel on chaotic, random pathways in the atria. The atrial rate (between the R waves) is very fast (400-600 bpm). Low action potentials make the p waves impossible to see. This may be caused by rheumatic disease, atherosclerotic disease, hyperthyroidism, and pericarditis.",
    ),
    ArrhythmiaAnnotation(
        id=57,
        rhythm_name="Atrial Flutter",
        bpm="220 - 300",
        rhythm="Regular or varying",
        p_wave="Saw-toothed in appearance",
        pr_interval="N/A",
        qrs_complex="< 0.12",
        note="This is an atrial arrhythmia. In this rhythm, the impulses travel circularly in the atria. The HR is elevated to the point that the isoelectric interval between the end of T and beginning of P disappears, creating the sawtooth pattern of the P waves. This may be caused by a reentrant atrial pathway.",
    ),
    ArrhythmiaAnnotation(
        id=1,
        rhythm_name="1st Degree AV Block",
        bpm="60 - 100",
        rhythm="Regular, evenly spaced",
        p_wave="Before each QRS",
        pr_interval="> 0.2",
        qrs_complex="< 0.12",
        note="This is a conduction abnomality. In this rhythm, the Atrioventricular, AV, conduction is lengthened. The P-wave always preceeds the QRS complex, but the PR interval is prolonged over 0.2 seconds.",
    ),
    ArrhythmiaAnnotation(
        id=2,
        rhythm_name="2nd Degree AV Block",
        bpm="60 - 100",
        rhythm="Atrial: Regular; Ventricular: Irregular",
        p_wave="Regular Intervals",
        pr_interval="long, longer, dropped",
        qrs_complex="Periodically absent",
        note="This is a conduction abnomality. In this rhythm, the QRS complex is suddenly dropped and may not follow the P-wave. The PQ interval is longer than normal. If the PR-interval becomes longer over time until the QRS complex drops off (Commonly described as “long, longer, dropped”), and the PR-interval after the dropped QRS is the shortest. The second degree atrioventricular block is called a Wenkebach phenomenon.",
    ),
    ArrhythmiaAnnotation(
        id=5,
        rhythm_name="3rd Degree AV Block",
        bpm="20-55",
        rhythm="Irregular spacing",
        p_wave="asynchronous with QRS, regular intervals",
        pr_interval="Regular",
        qrs_complex="< 0.12",
        note="This is a conduction abnomality. In this rhythm, the impulses originate in the AV node, and proceed to the ventricles, but the atrial and ventricular sides are not synchronous. Meaning there is no relation between the P-wave and the QRS complex. This is caused by a defect somewhere in the conduction system. The Ventricular HR (R wave peaks) have severe brady cardia ~40 bpm, and the Atrial HR (P wave peaks) ~100 bpm. This may cause cardiac arrest.",
    ),
     ArrhythmiaAnnotation(
        id=36,
        rhythm_name="Right Bundle Branch Block (RBBB)",
        bpm="60 - 100, but sometimes elevated",
        rhythm="Irregular spacing",
        p_wave="Before each QRS, identical waves",
        pr_interval="0.12 - 0.20",
        qrs_complex="≥ 0.12",
        note="This is a conduction abnomality. In this rhythm, there is a defect in the right bundle-branch preventing the travel of electrical impulses to the right ventricle, making the heartbeat late and out of sync with the left bundle branch, creating an irregular heartbeat. Instead, activation travels from the left to right ventricle, then through the septal and right ventricular muscle. Therefore a larger, but normal, activation from the left ventricle is followed by a delayed activation of the right. The broad 'slurred' terminal S-wave in lead I, aVL, V5, and V6 (QRS morphology). Or this is seen as a double wide R-wave in lead VI-3 (RSR' Complex) that looks like an 'M' or bunny ears.",
     ),
     ArrhythmiaAnnotation(
        id=20,
        rhythm_name="Left Bundle Branch Block (LBBB)",
        bpm="60 - 100, but sometimes elevated",
        rhythm="Abnormal",
        p_wave="Before each QRS, identical waves",
        pr_interval="0.12 - 0.20",
        qrs_complex="≥ 0.12",
        note="This is a conduction abnomality. In this rhythm, there is a defect in the left bundle-branch preventing the electrical impulse from traveling to the left ventricle, causing abnormal heart rhythm. Instead, the activation travels from the right ventricle to the left ventricle, then through the septal and left ventricular muscle mass. There is larger, but normal, activation in the right ventricle followed by a delayed activation of the left. The broad terminal S-wave in leads V1-2 sometimes notched like a 'W', double wide positive R-wave in leads V5-6 (RSR' Complex) often notched.",
     ),
     ArrhythmiaAnnotation(
        id=52,
        rhythm_name="Wolff-Parkinson-White Syndrome (WPW)",
        bpm="> 100",
        rhythm="Varies",
        p_wave="Shortened PQ time",
        pr_interval="< 0.12",
        qrs_complex="> 0.12",
        note="In this rhythm, the QRS-complex initially exhibits an early upstroke, short PR interval and a “delta wave.“ A delta wave is slurring of the upstroke of the QRS complex. The cause of WPW is the passage of activation from the atrium directly to the ventricular muscle via an abnormal route, called the bundle of Kent, which bypasses the AV junctions. There is a pre-excitation is caused when part of the ventricular muscle is activated before normal activation reaches it before normal activation reaches it.",
    ),
]



def get_arrhythmia_annotation(arrhythmia_id: str):
    for annotation in hr_data:
        if int(arrhythmia_id) == annotation.id:
            return annotation
