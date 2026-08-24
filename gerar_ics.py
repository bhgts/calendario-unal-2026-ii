#!/usr/bin/env python3
"""Gera um .ics com as aulas de Parasitología 2026-II e los parciales de Patología."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / "calendario-unal-2026-ii.ics"

TZID = "America/Bogota"
PROD_ID = "-//UNAL Medicina 2026-II//Calendar//ES"
CAL_NAME = "UNAL Medicina 2026-II"
CAL_DESC = (
    "Parasitología (sesiones martes y miércoles 14:00-16:00) "
    "y evaluaciones de Patología. Periodo 2026-II, Bogotá."
)

LOC_PARA = (
    "Facultad de Medicina UNAL — Auditorio 313 / Laboratorios 314-315 "
    "/ Salas de informática, Bogotá"
)
LOC_PATO = "Patología — lugar por confirmar, UNAL Bogotá"


def esc(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def fold(line: str) -> str:
    """RFC 5545 line folding at 75 octets."""
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
        limit = 74  # continuation lines: space + 74
    out = [parts[0]]
    for p in parts[1:]:
        out.append(" " + p)
    return "\r\n".join(out)


def fmt_local(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%S")


def fmt_utc(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%SZ")


NOW = datetime.now(timezone.utc).replace(microsecond=0)


def vevent(
    uid: str,
    summary: str,
    start: datetime,
    end: datetime,
    description: str,
    location: str,
    alarms: list[str],
    categories: str,
) -> list[str]:
    lines = [
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{fmt_utc(NOW)}",
        f"DTSTART;TZID={TZID}:{fmt_local(start)}",
        f"DTEND;TZID={TZID}:{fmt_local(end)}",
        f"SUMMARY:{esc(summary)}",
        f"DESCRIPTION:{esc(description)}",
        f"LOCATION:{esc(location)}",
        f"CATEGORIES:{esc(categories)}",
        "STATUS:CONFIRMED",
        "TRANSP:OPAQUE",
        "SEQUENCE:0",
    ]
    for trigger, desc in alarms:
        lines += [
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            f"DESCRIPTION:{esc(desc)}",
            f"TRIGGER:{trigger}",
            "END:VALARM",
        ]
    lines.append("END:VEVENT")
    return lines


def dt(y, m, d, hh, mm=0) -> datetime:
    return datetime(y, m, d, hh, mm)


CLASS_ALARMS = [("-PT30M", "En 30 min")]
EVAL_ALARMS = [
    ("-P1D", "Mañana: evaluación"),
    ("-PT1H", "En 1 hora: evaluación"),
]


def para(uid, summary, start, end, description, eval_event=False):
    prefix = "🔴 " if eval_event else "📘 "
    cats = "Parasitología,Evaluación" if eval_event else "Parasitología,Clase"
    return vevent(
        uid=f"{uid}@parasitologia-unal-2026ii",
        summary=prefix + summary,
        start=start,
        end=end,
        description=description,
        location=LOC_PARA,
        alarms=EVAL_ALARMS if eval_event else CLASS_ALARMS,
        categories=cats,
    )


def pato(uid, summary, start, end, description):
    return vevent(
        uid=f"{uid}@patologia-unal-2026ii",
        summary="🔴 " + summary,
        start=start,
        end=end,
        description=description,
        location=LOC_PATO,
        alarms=EVAL_ALARMS,
        categories="Patología,Evaluación",
    )


events: list[list[str]] = []

# --- Parasitología 2026-II ---
events.append(
    para(
        "s01a",
        "Parasitología · S1 Inauguración",
        dt(2026, 8, 11, 14, 0),
        dt(2026, 8, 11, 14, 30),
        "Inauguración del curso. Presentación de los docentes. Revisión del programa, "
        "normatividad y contenidos. Vías de comunicación. Objeto de estudio de la parasitología.\n"
        "Docente: Prof. María Clara Echeverry.\n"
        "Campus: https://micampus.unal.edu.co/",
    )
)
events.append(
    para(
        "s01b",
        "Parasitología · S1 Evolución de ciclos biológicos",
        dt(2026, 8, 11, 14, 30),
        dt(2026, 8, 11, 16, 0),
        "Evolución de ciclos biológicos.\nDocente: Prof. Vladimir Corredor.",
    )
)
events.append(
    para(
        "s02",
        "Parasitología · S2 Generalidades sobre las parasitosis",
        dt(2026, 8, 12, 14, 0),
        dt(2026, 8, 12, 16, 0),
        "Relación hospedero-parásito, glosario de términos médicos. "
        "Infección/enfermedad. Síndromes clínicos.\n"
        "Docente: Prof. Angélica Knudson.",
    )
)
events.append(
    para(
        "s03",
        "Parasitología · S3 Leishmaniasis",
        dt(2026, 8, 18, 14, 0),
        dt(2026, 8, 18, 16, 0),
        "Protozoarios transmitidos por vectores: leishmaniasis. Ciclos biológicos, "
        "epidemiología, relación hospedero–parásito, patogénesis, patología, "
        "cuadros clínicos, diagnóstico, tratamiento, control.\n"
        "Docente: Prof. María Clara Echeverry.",
    )
)
events.append(
    para(
        "s04",
        "Parasitología · S4 Enfermedad de Chagas",
        dt(2026, 8, 19, 14, 0),
        dt(2026, 8, 19, 16, 0),
        "Protozoarios transmitidos por vectores: enfermedad de Chagas. Ciclo biológico "
        "y epidemiología. Relación hospedero–parásito, patogénesis, patología, "
        "cuadros clínicos, diagnóstico, tratamiento, control.\n"
        "Docentes: Prof. María Clara Echeverry y Dr. Sergio Velasco (invitado).",
    )
)
events.append(
    para(
        "s05",
        "Parasitología · S5 PRÁCTICA CALIFICABLE Trypanosoma y Leishmania",
        dt(2026, 8, 25, 14, 0),
        dt(2026, 8, 25, 16, 0),
        "Práctica de laboratorio calificable: Trypanosoma y Leishmania.\n"
        "Docentes: María Clara Echeverry, Yulieth Alexandra Upegui, Patricia Reyes, "
        "Angélica Knudson, Martha Quiñonez.\n"
        "Llevar bata. Sin comida ni bebida. Guantes si hay especímenes clínicos.\n"
        "Prácticas de laboratorio = 20% del curso.",
        eval_event=True,
    )
)
events.append(
    para(
        "s06",
        "Parasitología · S6 Vectores de Trypanosoma y Leishmania",
        dt(2026, 8, 26, 14, 0),
        dt(2026, 8, 26, 16, 0),
        "Vectores de Trypanosoma y Leishmania.\nDocente: Prof. Martha Quiñones.",
    )
)
events.append(
    para(
        "s07",
        "Parasitología · S7 Accidente ofídico",
        dt(2026, 9, 1, 14, 0),
        dt(2026, 9, 1, 16, 0),
        "Accidente ofídico. Cuadros clínicos. Accidentes por animales venenosos: "
        "generalidades, morfología, epidemiología, fisiopatología y cuadros clínicos.\n"
        "Docente: Prof. Javier Rodríguez.",
    )
)
events.append(
    para(
        "s08",
        "Parasitología · S8 Práctica fauna venenosa y ofídico",
        dt(2026, 9, 2, 14, 0),
        dt(2026, 9, 2, 16, 0),
        "Práctica de integración básica–clínica. Accidentes por fauna venenosa y accidente ofídico.\n"
        "Docentes: Javier Rodríguez, Yulieth Alexandra Upegui, Patricia Reyes, Angélica Knudson.",
    )
)
events.append(
    para(
        "s09",
        "Parasitología · S9 Apicomplexa",
        dt(2026, 9, 8, 14, 0),
        dt(2026, 9, 8, 16, 0),
        "Introducción a las características biológicas de parásitos del orden "
        "Apicomplexa que infectan a humanos.\n"
        "Docente: Yulieth Alexandra Upegui.\n"
        "Horario no explícito en el programa; se usa el horario regular 14:00–16:00.",
    )
)
events.append(
    para(
        "s10",
        "Parasitología · S10 Toxoplasmosis I",
        dt(2026, 9, 9, 14, 0),
        dt(2026, 9, 9, 16, 0),
        "Toxoplasmosis I. Ciclo biológico y epidemiología: relación hospedero-parásito, "
        "patogénesis, patología y diagnóstico de laboratorio.\n"
        "Docente: Prof. Yulieth Alexandra Upegui.",
    )
)
events.append(
    para(
        "s11",
        "Parasitología · S11 Toxoplasmosis II",
        dt(2026, 9, 15, 14, 0),
        dt(2026, 9, 15, 16, 0),
        "Toxoplasmosis II. Presentación clínica. Casos clínicos de diagnóstico.\n"
        "Docente: Prof. Patricia Reyes.",
    )
)
events.append(
    para(
        "s12",
        "Parasitología · S12 Parásitos oportunistas",
        dt(2026, 9, 16, 14, 0),
        dt(2026, 9, 16, 16, 0),
        "Parásitos oportunistas: ciclo biológico y epidemiología, relación hospedero-parásito, "
        "patogénesis, patología, cuadros clínicos, diagnóstico y prevención.\n"
        "Docentes: Patricia Reyes y Yulieth Upegui.",
    )
)
events.append(
    para(
        "s13",
        "Parasitología · S13 PRÁCTICA CALIFICABLE Apicomplexa",
        dt(2026, 9, 22, 14, 0),
        dt(2026, 9, 22, 16, 0),
        "Práctica calificable sobre Apicomplexa y parásitos oportunistas.\n"
        "Docentes: Yulieth Alexandra Upegui, Patricia Reyes, Angélica Knudson.\n"
        "Prácticas de laboratorio = 20% del curso.",
        eval_event=True,
    )
)
events.append(
    para(
        "s14",
        "Parasitología · PRIMER PARCIAL (15%)",
        dt(2026, 9, 23, 14, 0),
        dt(2026, 9, 23, 16, 0),
        "PRIMER PARCIAL (15%). Todos los contenidos revisados hasta la fecha.\n"
        "Sin dispositivos electrónicos (tablet, smartwatch, audífonos).",
        eval_event=True,
    )
)
events.append(
    para(
        "s15",
        "Parasitología · S15 TALLER CALIFICABLE Apicomplexa",
        dt(2026, 9, 29, 14, 0),
        dt(2026, 9, 29, 16, 0),
        "Taller calificable sobre Apicomplexa y parásitos oportunistas.\n"
        "Docentes: Yulieth Alexandra Upegui, Patricia Reyes, Angélica Knudson "
        "y Dr. José Camilo Alvarez (invitado).\n"
        "Talleres = 10% del curso.",
        eval_event=True,
    )
)
events.append(
    para(
        "s16",
        "Parasitología · S16 Ciclo biológico de la malaria",
        dt(2026, 9, 30, 14, 0),
        dt(2026, 9, 30, 16, 0),
        "Ciclo biológico de la malaria y patogénesis.\nDocente: profesor invitado.",
    )
)
events.append(
    para(
        "s17",
        "Parasitología · S17 Malaria clínica",
        dt(2026, 10, 6, 14, 0),
        dt(2026, 10, 6, 16, 0),
        "Malaria: compromiso clínico, diagnóstico y tratamiento.\n"
        "Docente: Angélica Knudson.",
    )
)
events.append(
    para(
        "s18",
        "Parasitología · S18 Vectores y eliminación de la malaria",
        dt(2026, 10, 7, 14, 0),
        dt(2026, 10, 7, 16, 0),
        "Vectores y programa de eliminación de la malaria.\n"
        "Docente: Martha Lucía Quiñones.",
    )
)
events.append(
    para(
        "s19",
        "Parasitología · S19 Práctica de malaria",
        dt(2026, 10, 13, 14, 0),
        dt(2026, 10, 13, 16, 0),
        "Práctica de malaria.\n"
        "Docentes: María Clara Echeverry, Yulieth Alexandra Upegui, Patricia Reyes, "
        "Angélica Knudson, Martha Quiñonez.",
    )
)
events.append(
    para(
        "s20",
        "Parasitología · S20 PRÁCTICA CALIFICABLE de malaria",
        dt(2026, 10, 14, 14, 0),
        dt(2026, 10, 14, 16, 0),
        "Práctica calificable de malaria.\n"
        "Docentes: María Clara Echeverry, Yulieth Alexandra Upegui, Patricia Reyes, "
        "Angélica Knudson, Martha Quiñonez.\n"
        "Prácticas de laboratorio = 20% del curso.",
        eval_event=True,
    )
)
events.append(
    para(
        "s21",
        "Parasitología · SEGUNDO PARCIAL (15%)",
        dt(2026, 10, 20, 14, 0),
        dt(2026, 10, 20, 16, 0),
        "SEGUNDO PARCIAL (15%): todos los contenidos revisados entre el parcial 1 "
        "y la sesión 20 del curso.\n"
        "Sin dispositivos electrónicos.",
        eval_event=True,
    )
)
events.append(
    para(
        "s22",
        "Parasitología · S22 Protozoos intestinales I",
        dt(2026, 10, 21, 14, 0),
        dt(2026, 10, 21, 16, 0),
        "Generalidades de los protozoos. Entamoeba histolytica, Blastocystis sp, "
        "Balantidium coli: ciclos biológicos, patología, relación hospedero-parásito, "
        "cuadros clínicos, tratamiento, prevención.\n"
        "Docente: Prof. Yulieth Upegui.",
    )
)
events.append(
    para(
        "s23",
        "Parasitología · S23 Protozoos intestinales II",
        dt(2026, 10, 27, 14, 0),
        dt(2026, 10, 27, 16, 0),
        "Giardia, amibas de vida libre. Ciclos biológicos, patología, relación "
        "hospedero-parásito, cuadros clínicos, tratamiento, prevención.\n"
        "Docente: Prof. Patricia Reyes.\n"
        "Nota: el mismo día hay parcial de Patología a las 8:00 a.m.",
    )
)
events.append(
    para(
        "s24",
        "Parasitología · S24 Práctica de protozoos",
        dt(2026, 10, 28, 14, 0),
        dt(2026, 10, 28, 16, 0),
        "Práctica de protozoos (intestinales y parásitos intestinales oportunistas). "
        "Diagnóstico e identificación de especies y de formas parasitarias.\n"
        "Docentes: Patricia Reyes, Angélica Knudson y Yulieth Upegui.",
    )
)
events.append(
    para(
        "s25",
        "Parasitología · S25 Helmintiasis intestinales I",
        dt(2026, 11, 3, 14, 0),
        dt(2026, 11, 3, 16, 0),
        "Geohelmintiasis. Ciclos biológicos y epidemiología, patogenia y patología, "
        "cuadros clínicos, diagnóstico.\n"
        "Docentes: Patricia Reyes y Yulieth Upegui.",
    )
)
events.append(
    para(
        "s26",
        "Parasitología · S26 Helmintiasis intestinales II",
        dt(2026, 11, 4, 14, 0),
        dt(2026, 11, 4, 16, 0),
        "E. vermicularis, síndromes de migración larvaria cutánea y visceral. "
        "Eliminación de las geohelmintiasis.\n"
        "Docentes: Patricia Reyes y Yulieth Upegui.",
    )
)
events.append(
    para(
        "s27",
        "Parasitología · S27 Helmintiasis zoonóticas I — trematodos",
        dt(2026, 11, 10, 14, 0),
        dt(2026, 11, 10, 16, 0),
        "Fasciola hepática, Paragonimus sp, Schistosoma mansoni: ciclos biológicos, "
        "epidemiología, patología, cuadros clínicos, diagnóstico, tratamiento, control.\n"
        "Docente: Prof. Patricia Reyes.",
    )
)
events.append(
    para(
        "s28",
        "Parasitología · S28 Filariasis",
        dt(2026, 11, 11, 14, 0),
        dt(2026, 11, 11, 16, 0),
        "Ciclos biológicos y epidemiología, patología, cuadros clínicos, diagnóstico, "
        "prevención, tratamiento y programa de eliminación de la oncocercosis en Colombia.\n"
        "Docentes: Patricia Reyes y profesor invitado.",
    )
)
events.append(
    para(
        "s29",
        "Parasitología · S29 Helmintiasis zoonóticas II — cestodos",
        dt(2026, 11, 17, 14, 0),
        dt(2026, 11, 17, 16, 0),
        "Taenia solium, Taenia saginata, Hymenolepis nana, H. diminuta, Echinococcus sp: "
        "ciclos biológicos, epidemiología, patología, cuadros clínicos, diagnóstico, "
        "tratamiento, control.\n"
        "Docente: Prof. Patricia Reyes.",
    )
)
events.append(
    para(
        "s30",
        "Parasitología · S30 Taller diarrea en pediatría",
        dt(2026, 11, 18, 14, 0),
        dt(2026, 11, 18, 16, 0),
        "Taller de integración clínica básica: diarrea en pediatría I.\n"
        "Docentes: Rafael Guerrero, Mary Isabel Vanegas, Angélica Knudson y Patricia Reyes.\n"
        "Talleres = 10% del curso.",
        eval_event=True,
    )
)
events.append(
    para(
        "s31",
        "Parasitología · S31 Práctica helmintiasis y filariasis",
        dt(2026, 11, 24, 14, 0),
        dt(2026, 11, 24, 16, 0),
        "Práctica. Helmintiasis intestinal (geohelmintos, E. vermicularis), "
        "filariasis y helmintiasis zoonóticas.\n"
        "Docentes: Yulieth Upegui, Patricia Reyes y Angélica Knudson.\n"
        "Horario no explícito en el programa; se usa el horario regular 14:00–16:00.",
    )
)
events.append(
    para(
        "s32",
        "Parasitología · TERCER PARCIAL (15%)",
        dt(2026, 11, 25, 14, 0),
        dt(2026, 11, 25, 16, 0),
        "TERCER PARCIAL (15%): todos los contenidos revisados entre las sesiones 22 y 30.\n"
        "Horario no explícito en el programa; se usa el horario regular 14:00–16:00.\n"
        "Sin dispositivos electrónicos.",
        eval_event=True,
    )
)
events.append(
    para(
        "s33",
        "Parasitología · S33 PRÁCTICA INTEGRATIVA (10%)",
        dt(2026, 12, 1, 14, 0),
        dt(2026, 12, 1, 16, 0),
        "Práctica integrativa (10%). Integra Epidemiología, Inmunología, Microbiología, "
        "Patología, Parasitología e introducción a la medicina interna. Casos clínicos "
        "e interpretación de pruebas diagnósticas.\n"
        "Horario no explícito en el programa; se usa el horario regular 14:00–16:00.",
        eval_event=True,
    )
)
events.append(
    para(
        "s34",
        "Parasitología · EXAMEN FINAL (15%)",
        dt(2026, 12, 2, 14, 0),
        dt(2026, 12, 2, 16, 0),
        "Examen final. Incluye TODOS los contenidos revisados del curso (15%).\n"
        "Horario no explícito en el programa; se usa el horario regular 14:00–16:00.\n"
        "Sin dispositivos electrónicos.",
        eval_event=True,
    )
)

# --- Patología (tabla de evaluaciones) ---
events.append(
    pato(
        "p1",
        "Patología · 1.er parcial teórico-práctico (20%)",
        dt(2026, 9, 7, 9, 0),
        dt(2026, 9, 7, 11, 0),
        "Primer parcial teórico-práctico (20%).\n"
        "Temas: Neuropatología, Renal, Genital masculino.\n"
        "14 actividades. Docente: Dr. Franco.",
    )
)
events.append(
    pato(
        "p2",
        "Patología · 2.º parcial teórico-práctico (20%)",
        dt(2026, 9, 28, 9, 0),
        dt(2026, 9, 28, 11, 0),
        "Segundo parcial teórico-práctico (20%).\n"
        "Temas: Genital femenino y seno, Respiratorio.\n"
        "13 actividades. Docente: Dra. Olaya.",
    )
)
events.append(
    pato(
        "p3",
        "Patología · 3.er parcial teórico-práctico (23%)",
        dt(2026, 10, 27, 8, 0),
        dt(2026, 10, 27, 10, 0),
        "Tercer parcial teórico-práctico (23%).\n"
        "Temas: Digestivo, Cardiovascular.\n"
        "16 actividades. Docente: Dra. Roa.\n"
        "Nota: el mismo día hay clase de Parasitología a las 14:00.",
    )
)
events.append(
    pato(
        "p4",
        "Patología · 4.º parcial teórico-práctico (20%)",
        dt(2026, 11, 26, 8, 0),
        dt(2026, 11, 26, 10, 0),
        "Cuarto parcial teórico-práctico (20%).\n"
        "Temas: Hematolinfoide, Endocrino, Dermatopatología, "
        "Tejidos blandos y osteoarticular.\n"
        "14 actividades. Docente: Dra. Acosta.",
    )
)
events.append(
    pato(
        "p5",
        "Patología · EXAMEN FINAL teórico (17%)",
        dt(2026, 12, 3, 8, 0),
        dt(2026, 12, 3, 10, 0),
        "Examen final teórico (17%). Todos los temas. 58 actividades.\n"
        "Docente: Dra. Roa.",
    )
)


header = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    f"PRODID:{PROD_ID}",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    f"X-WR-CALNAME:{esc(CAL_NAME)}",
    f"X-WR-CALDESC:{esc(CAL_DESC)}",
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

lines: list[str] = []
for block in [header, *[e for e in events], ["END:VCALENDAR"]]:
    for line in block:
        lines.append(fold(line))

ics = "\r\n".join(lines) + "\r\n"
OUTPUT.write_bytes(ics.encode("utf-8"))
print(f"Wrote {OUTPUT}")
print(f"Events: {len(events)}")
print(f"Bytes: {OUTPUT.stat().st_size}")
