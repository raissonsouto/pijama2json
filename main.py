import PyPDF2
import json
import re

data = []
pattern = r'^(\d{8}) - (.+) - [A-Z]\s(\d+)\s\/\s(\d+)$'
pattern2 = r'^\d{2}\/\d{2}\/\d{4}\s\d{2}:\d{2}:\d{2}\s\d+\s\/\s\d+$'

jsona = []

EXCLUDE_PATTERNS = [
    "UNIVERSIDADE FEDERAL DE CAMPINA GRANDE",
    "PRÓ-REITORIA DE ENSINO",
    "Disciplina Turma CR CH Horários"
]


def get_week_day(day: int) -> str:
    """
    Given a day of the week represented as an integer (2-6 for Monday-Friday),
    returns the corresponding day of the week in Portuguese.

    :param day: The day of the week as an integer (2-6 for Monday-Friday).

    :return:The corresponding day of the week in Portuguese, or an empty string
             if the input is not a valid day of the week.
    """
    days = {
        2: "segunda",
        3: "terça",
        4: "quarta",
        5: "quinta",
        6: "sexta"
    }
    return days.get(day, "")


def filter_page(page: list) -> None:
    for line in page:
        if line in EXCLUDE_PATTERNS or \
           re.match(pattern, line) or \
           re.match(pattern2, line):
            continue
        else:
            data.append(line)


def to_json(course_id: str, class_name: str, professor_name: str, schedule: list, room: str) -> str:
    """
    Given attributes of a course, returns a JSON string representing the course.

    :param course_id: The ID of the course.
    :param class_name: The name of the class.
    :param professor_name: The name of the professor.
    :param schedule: A list of tuples representing the schedule of the class.
    Each tuple should contain two strings representing the start and end time
    of the class.
    :param room: The room number and name where the class takes place.

    :return: A JSON string representing the course.
    """
    my_dict = {
        "id": course_id,
        "class": class_name,
        "professor": professor_name,
        "schedule": schedule,
        "room": room
    }
    print(my_dict)
    return json.dumps(my_dict)


def scraping_data():  # breaks in fmcc2
    i = 1
    while i < len(data):
        if data[i].startswith("TOTAL"):
            i += 1
        print(data[i])
        id = data[i].split(" - ")[0]
        turma = " ".join(data[i].split(" - ")[1].split()[:-6])
        professor = data[i + 3].replace("- ", "").capitalize()
        aulas = [
            data[i].split(" ")[-3:-1],
            data[i + 1].split(" ")[0:2]
        ]
        sala = data[i].split(" ")[-1]

        to_json(id, turma, professor, aulas, sala)

        i += 4


with open('2022.2.pdf', 'rb') as pdf_file:

    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page_num in range(len(pdf_reader.pages)):
        pdf_page = pdf_reader.pages[page_num]
        page_lines = pdf_page.extract_text().split('\n')
        filter_page(page_lines)

    scraping_data()
