import PyPDF2
import json
import re

data = []
pattern = r'^(\d+) - (.+) - [A-Z] (\d+) \/ (\d+)(.*)$'
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


def camel_case(text: str) -> str:
    words = text.split(" ")
    capitalized_words = [word.capitalize() for word in words]

    return "".join(capitalized_words)


def filter_page(page: list) -> None:
    for line in page:
        if line in EXCLUDE_PATTERNS or \
           re.match(pattern, line) or \
           re.match(pattern2, line) or\
           line.startswith("TOTAL"):
            continue
        else:
            data.append(line)


def to_json(course_id: str, class_name: str, professors: list, schedule: list, room: str) -> str:
    """
    Given attributes of a course, returns a JSON string representing the course.

    :param course_id: The ID of the course.
    :param class_name: The name of the class.
    :param professors: A list of the name of the professor.
    :param schedule: A list of tuples representing the schedule of the class.
    Each tuple should contain two strings representing the start and end time
    of the class.
    :param room: The room number and name where the class takes place.

    :return: A JSON string representing the course.
    """
    my_dict = {
        "id": course_id,
        "class": class_name,
        "professor": professors,
        "schedule": schedule,
        "room": room
    }
    print(my_dict)
    return json.dumps(my_dict)


def scraping_data():
    i = 1
    while i < len(data):
        id = data[i].split(" - ")[0]
        turma = camel_case(" ".join(data[i].split(" - ")[1].split()[:-6]))
        aulas = [
            data[i].split(" ")[-3:-1]
        ]
        try:
            aulas.append(data[i + 1].split(" ")[0:2])
            aulas[1][0] = get_week_day(int(aulas[1][0]))
        except Exception as e:
            pass

        sala = data[i].split(" ")[-1]

        aulas[0][0] = get_week_day(int(aulas[0][0]))


        i += 2

        professor = []

        while data[i].startswith("- "):
            professor.append(camel_case(data[i].replace("- ", "")))
            i += 1

        to_json(id, turma, professor, aulas, sala)


with open('pdfs/computer-science/2022.2.pdf', 'rb') as pdf_file:

    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page_num in range(len(pdf_reader.pages)):
        pdf_page = pdf_reader.pages[page_num]
        page_lines = pdf_page.extract_text().split('\n')
        filter_page(page_lines)

with open('temp.txt', 'w') as temp:
    for line in data:
        temp.write(f'{line}\n')

scraping_data()
