#!/usr/bin/env python3
"""ICS do Programa de Parasitología 2026-II (PDF actualizado)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / "calendario-parasitologia-2026-ii.ics"
TZID = "America/Bogota"
LOC = (
    "Facultad de Medicina UNAL — Auditorio 313 / Laboratorios 314-315 "
    "/ Salas de informática, Bogotá"
)
NOW = datetime.now(timezone.utc).replace(microsecond=0)


def esc(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def fold(line: str) -> str:
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    parts: list[str] = []
    start = 0
    limit = 75
    while start < len(raw):
        chunk = raw[start : start + limit]
        while True:
            try:
                parts.append(chunk.decode("utf-8"))
                break
            except UnicodeDecodeError:
                chunk = chunk[:-1]
        start += len(chunk)
        limit = 74
    return "\r\n".join([parts[0], *(" " + p for p in parts[1:])])


def fmt_local(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%S")


def fmt_utc(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%SZ")


def dt(y, m, d, hh, mm=0) -> datetime:
    return datetime(y, m, d, hh, mm)


CLASS_ALARMS = [("-PT30M", "En 30 min")]
EVAL_ALARMS = [("-P1D", "Mañana: evaluación"), ("-PT1H", "En 1 hora: evaluación")]


def vevent(uid, summary, start, end, description, eval_event=False, time_note=False):
    if time_note:
        description += (
            "\nHorario no explícito en el programa; se usa el horario regular 14:00–16:00."
        )
    prefix = "🔴 " if eval_event else "📘 "
    cats = "Parasitología,Evaluación" if eval_event else "Parasitología,Clase"
    lines = [
        "BEGIN:VEVENT",
        f"UID:{uid}@parasitologia-unal-2026ii-v2",
        f"DTSTAMP:{fmt_utc(NOW)}",
        f"DTSTART;TZID={TZID}:{fmt_local(start)}",
        f"DTEND;TZID={TZID}:{fmt_local(end)}",
        f"SUMMARY:{esc(prefix + summary)}",
        f"DESCRIPTION:{esc(description)}",
        f"LOCATION:{esc(LOC)}",
        f"CATEGORIES:{esc(cats)}",
        "STATUS:CONFIRMED",
        "TRANSP:OPAQUE",
        "SEQUENCE:0",
    ]
    for trigger, desc in EVAL_ALARMS if eval_event else CLASS_ALARMS:
        lines += [
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            f"DESCRIPTION:{esc(desc)}",
            f"TRIGGER:{trigger}",
            "END:VALARM",
        ]
    lines.append("END:VEVENT")
    return lines


# (uid, summary, start, end, description, eval, time_note)
EVENTS = [
    (
        "s01a",
        "Parasitología · S1 Inauguración",
        dt(2026, 8, 11, 14, 0),
        dt(2026, 8, 11, 14, 30),
        "Inauguración del curso. Presentación de los docentes. Revisión del programa, "
        "normatividad y contenidos. Vías de comunicación. Objeto de estudio de la parasitología.\n"
        "Docente: Prof. María Clara Echeverry.\nCampus: https://micampus.unal.edu.co/",
        False,
        False,
    ),
    (
        "s01b",
        "Parasitología · S1 Evolución de ciclos biológicos",
        dt(2026, 8, 11, 14, 30),
        dt(2026, 8, 11, 16, 0),
        "Evolución de ciclos biológicos.\nDocente: Prof. Vladimir Corredor.",
        False,
        False,
    ),
    (
        "s02",
        "Parasitología · S2 Generalidades sobre las parasitosis",
        dt(2026, 8, 12, 14, 0),
        dt(2026, 8, 12, 16, 0),
        "Relación hospedero-parásito, glosario de términos médicos. "
        "Infección/enfermedad. Síndromes clínicos.\nDocente: Prof. Angélica Knudson.",
        False,
        False,
    ),
    (
        "s03",
        "Parasitología · S3 Leishmaniasis",
        dt(2026, 8, 18, 14, 0),
        dt(2026, 8, 18, 16, 0),
        "Protozoarios transmitidos por vectores: leishmaniasis. Ciclos biológicos, "
        "epidemiología, relación hospedero–parásito, patogénesis, patología, "
        "cuadros clínicos, diagnóstico, tratamiento, control.\n"
        "Docente: Prof. María Clara Echeverry.",
        False,
        False,
    ),
    (
        "s04",
        "Parasitología · S4 Enfermedad de Chagas",
        dt(2026, 8, 19, 14, 0),
        dt(2026, 8, 19, 16, 0),
        "Protozoarios transmitidos por vectores: enfermedad de Chagas. Ciclo biológico "
        "y epidemiología. Relación hospedero–parásito, patogénesis, patología, "
        "cuadros clínicos, diagnóstico, tratamiento, control.\n"
        "Docentes: Prof. María Clara Echeverry y Dr. Sergio Velasco (invitado).",
        False,
        False,
    ),
    (
        "s05",
        "Parasitología · S5 PRÁCTICA CALIFICABLE Trypanosoma y Leishmania",
        dt(2026, 8, 25, 14, 0),
        dt(2026, 8, 25, 16, 0),
        "Práctica de laboratorio calificable: Trypanosoma y Leishmania.\n"
        "Docentes: María Clara Echeverry, Yulieth Alexandra Upegui, Patricia Reyes, "
        "Angélica Knudson, Martha Quiñonez.\n"
        "Llevar bata. Sin comida ni bebida. Guantes si hay especímenes clínicos.\n"
        "Prácticas de laboratorio = 20% del curso.",
        True,
        False,
    ),
    (
        "s06",
        "Parasitología · S6 Vectores de Trypanosoma y Leishmania",
        dt(2026, 8, 26, 14, 0),
        dt(2026, 8, 26, 16, 0),
        "Vectores de Trypanosoma y Leishmania.\nDocente: Prof. Martha Quiñones.",
        False,
        False,
    ),
    (
        "s07",
        "Parasitología · S7 Apicomplexa",
        dt(2026, 9, 1, 14, 0),
        dt(2026, 9, 1, 16, 0),
        "Introducción a las características biológicas de parásitos del orden "
        "Apicomplexa que infectan a humanos.\nDocente: Yulieth Alexandra Upegui.",
        False,
        False,
    ),
    (
        "s08",
        "Parasitología · S8 Toxoplasmosis I",
        dt(2026, 9, 2, 14, 0),
        dt(2026, 9, 2, 16, 0),
        "Toxoplasmosis I. Ciclo biológico y epidemiología: relación hospedero-parásito, "
        "patogénesis, patología y diagnóstico de laboratorio.\n"
        "Docente: Prof. Yulieth Alexandra Upegui.",
        False,
        False,
    ),
    (
        "s09",
        "Parasitología · S9 Toxoplasmosis II",
        dt(2026, 9, 8, 14, 0),
        dt(2026, 9, 8, 16, 0),
        "Toxoplasmosis II. Presentación clínica. Casos clínicos de diagnóstico.\n"
        "Docente: Prof. Patricia Reyes.",
        False,
        True,
    ),
    (
        "s10",
        "Parasitología · S10 Parásitos oportunistas",
        dt(2026, 9, 9, 14, 0),
        dt(2026, 9, 9, 16, 0),
        "Parásitos oportunistas: ciclo biológico y epidemiología, relación hospedero-parásito, "
        "patogénesis, patología, cuadros clínicos, diagnóstico y prevención.\n"
        "Docentes: Patricia Reyes y Yulieth Upegui.",
        False,
        False,
    ),
    (
        "s11",
        "Parasitología · S11 PRÁCTICA CALIFICABLE Apicomplexa",
        dt(2026, 9, 15, 14, 0),
        dt(2026, 9, 15, 16, 0),
        "Práctica calificable sobre Apicomplexa y parásitos oportunistas.\n"
        "Docentes: Yulieth Alexandra Upegui, Patricia Reyes, Angélica Knudson.\n"
        "Prácticas de laboratorio = 20% del curso.",
        True,
        False,
    ),
    (
        "s12",
        "Parasitología · S12 Accidente ofídico",
        dt(2026, 9, 16, 14, 0),
        dt(2026, 9, 16, 16, 0),
        "Accidente ofídico. Cuadros clínicos. Accidentes por animales venenosos: "
        "generalidades, morfología, epidemiología, fisiopatología y cuadros clínicos.\n"
        "Docente: Prof. Javier Rodríguez.",
        False,
        False,
    ),
    (
        "s13",
        "Parasitología · S13 Práctica fauna venenosa y ofídico",
        dt(2026, 9, 22, 14, 0),
        dt(2026, 9, 22, 16, 0),
        "Práctica de integración básica–clínica. Accidentes por fauna venenosa y accidente ofídico.\n"
        "Docentes: Javier Rodríguez, Yulieth Alexandra Upegui, Patricia Reyes, Angélica Knudson.",
        False,
        False,
    ),
    (
        "s14",
        "Parasitología · PRIMER PARCIAL (15%)",
        dt(2026, 9, 23, 14, 0),
        dt(2026, 9, 23, 16, 0),
        "PRIMER PARCIAL (15%). Todos los contenidos revisados hasta la fecha.\n"
        "Sin dispositivos electrónicos (tablet, smartwatch, audífonos).",
        True,
        False,
    ),
    (
        "s15",
        "Parasitología · S15 Ciclo biológico de la malaria",
        dt(2026, 9, 29, 14, 0),
        dt(2026, 9, 29, 16, 0),
        "Ciclo biológico de la malaria y patogénesis.\nDocente: profesor invitado.",
        False,
        False,
    ),
    (
        "s16",
        "Parasitología · S16 TALLER CALIFICABLE Apicomplexa",
        dt(2026, 9, 30, 14, 0),
        dt(2026, 9, 30, 16, 0),
        "Taller calificable sobre Apicomplexa y parásitos oportunistas.\n"
        "Docentes: Yulieth Alexandra Upegui, Patricia Reyes, Angélica Knudson "
        "y Dr. José Camilo Alvarez (invitado).\nTalleres = 10% del curso.",
        True,
        False,
    ),
    (
        "s17",
        "Parasitología · S17 Malaria clínica",
        dt(2026, 10, 6, 14, 0),
        dt(2026, 10, 6, 16, 0),
        "Malaria: compromiso clínico, diagnóstico y tratamiento.\nDocente: Angélica Knudson.",
        False,
        False,
    ),
    (
        "s18",
        "Parasitología · S18 Vectores y eliminación de la malaria",
        dt(2026, 10, 7, 14, 0),
        dt(2026, 10, 7, 16, 0),
        "Vectores y programa de eliminación de la malaria.\nDocente: Martha Lucía Quiñones.",
        False,
        False,
    ),
    (
        "s19",
        "Parasitología · S19 Práctica de malaria",
        dt(2026, 10, 13, 14, 0),
        dt(2026, 10, 13, 16, 0),
        "Práctica de malaria.\nDocentes: María Clara Echeverry, Yulieth Alexandra Upegui, "
        "Patricia Reyes, Angélica Knudson, Martha Quiñonez.",
        False,
        False,
    ),
    (
        "s20",
        "Parasitología · S20 PRÁCTICA CALIFICABLE de malaria",
        dt(2026, 10, 14, 14, 0),
        dt(2026, 10, 14, 16, 0),
        "Práctica calificable de malaria.\n"
        "Docentes: María Clara Echeverry, Yulieth Alexandra Upegui, Patricia Reyes, "
        "Angélica Knudson, Martha Quiñonez.\nPrácticas de laboratorio = 20% del curso.",
        True,
        False,
    ),
    (
        "s21",
        "Parasitología · SEGUNDO PARCIAL (15%)",
        dt(2026, 10, 20, 14, 0),
        dt(2026, 10, 20, 16, 0),
        "SEGUNDO PARCIAL (15%): todos los contenidos revisados entre el parcial 1 "
        "y la sesión 20 del curso.\nSin dispositivos electrónicos.",
        True,
        False,
    ),
    (
        "s22",
        "Parasitología · S22 Protozoos intestinales I",
        dt(2026, 10, 21, 14, 0),
        dt(2026, 10, 21, 16, 0),
        "Generalidades de los protozoos. Entamoeba histolytica, Blastocystis sp, "
        "Balantidium coli: ciclos biológicos, patología, relación hospedero-parásito, "
        "cuadros clínicos, tratamiento, prevención.\nDocente: Prof. Yulieth Upegui.",
        False,
        False,
    ),
    (
        "s23",
        "Parasitología · S23 Protozoos intestinales II",
        dt(2026, 10, 27, 14, 0),
        dt(2026, 10, 27, 16, 0),
        "Giardia, amibas de vida libre. Ciclos biológicos, patología, relación "
        "hospedero-parásito, cuadros clínicos, tratamiento, prevención.\n"
        "Docente: Prof. Patricia Reyes.",
        False,
        False,
    ),
    (
        "s24",
        "Parasitología · S24 Práctica de protozoos",
        dt(2026, 10, 28, 14, 0),
        dt(2026, 10, 28, 16, 0),
        "Práctica de protozoos (intestinales y parásitos intestinales oportunistas). "
        "Diagnóstico e identificación de especies y de formas parasitarias.\n"
        "Docentes: Patricia Reyes, Angélica Knudson y Yulieth Upegui.",
        False,
        False,
    ),
    (
        "s25",
        "Parasitología · S25 Helmintiasis intestinales I",
        dt(2026, 11, 3, 14, 0),
        dt(2026, 11, 3, 16, 0),
        "Geohelmintiasis. Ciclos biológicos y epidemiología, patogenia y patología, "
        "cuadros clínicos, diagnóstico.\nDocentes: Patricia Reyes y Yulieth Upegui.",
        False,
        False,
    ),
    (
        "s26",
        "Parasitología · S26 Helmintiasis intestinales II",
        dt(2026, 11, 4, 14, 0),
        dt(2026, 11, 4, 16, 0),
        "E. vermicularis, síndromes de migración larvaria cutánea y visceral. "
        "Eliminación de las geohelmintiasis.\nDocentes: Patricia Reyes y Yulieth Upegui.",
        False,
        False,
    ),
    (
        "s27",
        "Parasitología · S27 Helmintiasis zoonóticas I — trematodos",
        dt(2026, 11, 10, 14, 0),
        dt(2026, 11, 10, 16, 0),
        "Fasciola hepática, Paragonimus sp, Schistosoma mansoni: ciclos biológicos, "
        "epidemiología, patología, cuadros clínicos, diagnóstico, tratamiento, control.\n"
        "Docente: Prof. Patricia Reyes.",
        False,
        False,
    ),
    (
        "s28",
        "Parasitología · S28 Filariasis",
        dt(2026, 11, 11, 14, 0),
        dt(2026, 11, 11, 16, 0),
        "Ciclos biológicos y epidemiología, patología, cuadros clínicos, diagnóstico, "
        "prevención, tratamiento y programa de eliminación de la oncocercosis en Colombia.\n"
        "Docentes: Patricia Reyes y profesor invitado.",
        False,
        False,
    ),
    (
        "s29",
        "Parasitología · S29 Helmintiasis zoonóticas II — cestodos",
        dt(2026, 11, 17, 14, 0),
        dt(2026, 11, 17, 16, 0),
        "Taenia solium, Taenia saginata, Hymenolepis nana, H. diminuta, Echinococcus sp: "
        "ciclos biológicos, epidemiología, patología, cuadros clínicos, diagnóstico, "
        "tratamiento, control.\nDocente: Prof. Patricia Reyes.",
        False,
        False,
    ),
    (
        "s30",
        "Parasitología · S30 Taller diarrea en pediatría",
        dt(2026, 11, 18, 14, 0),
        dt(2026, 11, 18, 16, 0),
        "Taller de integración clínica básica: diarrea en pediatría I.\n"
        "Docentes: Rafael Guerrero, Mary Isabel Vanegas, Angélica Knudson y Patricia Reyes.\n"
        "Talleres = 10% del curso.",
        True,
        False,
    ),
    (
        "s31",
        "Parasitología · S31 Práctica helmintiasis y filariasis",
        dt(2026, 11, 24, 14, 0),
        dt(2026, 11, 24, 16, 0),
        "Práctica. Helmintiasis intestinal (geohelmintos, E. vermicularis), "
        "filariasis y helmintiasis zoonóticas.\n"
        "Docentes: Yulieth Upegui, Patricia Reyes y Angélica Knudson.",
        False,
        True,
    ),
    (
        "s32",
        "Parasitología · TERCER PARCIAL (15%)",
        dt(2026, 11, 25, 14, 0),
        dt(2026, 11, 25, 16, 0),
        "TERCER PARCIAL (15%): todos los contenidos revisados entre las sesiones 22 y 30.\n"
        "Sin dispositivos electrónicos.",
        True,
        True,
    ),
    (
        "s33",
        "Parasitología · S33 PRÁCTICA INTEGRATIVA (10%)",
        dt(2026, 12, 1, 14, 0),
        dt(2026, 12, 1, 16, 0),
        "Práctica integrativa (10%). Integra Epidemiología, Inmunología, Microbiología, "
        "Patología, Parasitología e introducción a la medicina interna. Casos clínicos "
        "e interpretación de pruebas diagnósticas.",
        True,
        True,
    ),
    (
        "s34",
        "Parasitología · EXAMEN FINAL (15%)",
        dt(2026, 12, 2, 14, 0),
        dt(2026, 12, 2, 16, 0),
        "Examen final. Incluye TODOS los contenidos revisados del curso (15%).\n"
        "Sin dispositivos electrónicos.",
        True,
        True,
    ),
]


header = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//UNAL Parasitología 2026-II//Calendar//ES",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "X-WR-CALNAME:Parasitología UNAL 2026-II",
    "X-WR-CALDESC:Curso de Parasitología 2026-II (código 2018007). Martes y miércoles 14:00-16:00, Facultad de Medicina UNAL, Bogotá.",
    "X-WR-TIMEZONE:America/Bogota",
    "BEGIN:VTIMEZONE",
    "TZID:America/Bogota",
    "X-LIC-LOCATION:America/Bogota",
    "BEGIN:STANDARD",
    "TZOFFSETFROM:-0500",
    "TZOFFSETTO:-0500",
    "TZNAME:-05",
    "DTSTART:19700101T000000",
    "END:STANDARD",
    "END:VTIMEZONE",
]

blocks = [header]
for item in EVENTS:
    blocks.append(vevent(*item))
blocks.append(["END:VCALENDAR"])

lines: list[str] = []
for block in blocks:
    for line in block:
        lines.append(fold(line))

OUTPUT.write_bytes(("\r\n".join(lines) + "\r\n").encode("utf-8"))
print(f"Wrote {OUTPUT}")
print(f"Events: {len(EVENTS)}")
print(f"Bytes: {OUTPUT.stat().st_size}")
