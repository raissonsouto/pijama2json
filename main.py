import PyPDF2
import json
import re


cadeiras_por_curso = r'^(\d+) - (.+) - [A-Z] (\d+) \/ (\d+)(.*)$'
rodape = r'^\d{2}\/\d{2}\/\d{4}\s\d{2}:\d{2}:\d{2}\s\d+\s\/\s\d+$'

EXCLUDE_PATTERNS = [
    "UNIVERSIDADE FEDERAL DE CAMPINA GRANDE",
    "PRÓ-REITORIA DE ENSINO",
    "Disciplina Turma CR CH Horários"
]

data = []
scraped_data = []


def get_week_day(day: int) -> str:
    """
    Given a day of the week represented as an integer (2-6 for Monday-Friday),
    returns the corresponding day of the week in Portuguese.

    :param day: The day of the week as an integer (2-6 for Monday-Friday).
    :type day: int

    :return:The corresponding day of the week in Portuguese, or an empty string
    if the input is not a valid day of the week.
    :rtype: str
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
    """
    Convert a string of space-separated words into camel case.

    :param text: The input string to convert.
    :type text: str

    :return: The string in camel case.
    :rtype: str
    """
    words = text.split(" ")
    capitalized_words = [word.capitalize() for word in words]

    return " ".join(capitalized_words)


def filter_data(page: list) -> None:
    for line in page:
        if line in EXCLUDE_PATTERNS or \
           re.match(rodape, line) or \
           line.startswith("TOTAL"):
            continue
        else:
            data.append(line)


def to_json(course_id: str, class_name: str, professors: list, schedule: list, vacancies: int, room: str) -> str:
    """
    Given attributes of a course, returns a JSON string representing the course.

    :param course_id: The ID of the course.
    :param class_name: The name of the class.
    :param professors: A list of the name of the professor.
    :param schedule: A list of tuples representing the schedule of the class.
    Each tuple should contain two strings representing the start and end time
    of the class.
    :param vacancies: The amount of seats available for the class.
    :param room: The room number and name where the class takes place.

    :return: A JSON string representing the course.
    :rtype: str
    """
    my_dict = {
        "id": course_id,
        "class": class_name,
        "professor": professors,
        "schedule": schedule,
        "vacancies": vacancies,
        "room": room
    }

    return json.dumps(my_dict)


def scrape_data() -> None:
    i = 1
    while i < len(data) - 1:

        id = data[i].split(" - ")[0]
        class_name = camel_case(" ".join(data[i].split(" - ")[1].split()[:-6]))
        room = data[i].split(" ")[-1]

        schedule = [data[i].split(" ")[-3:-1]]
        schedule[0][0] = get_week_day(int(schedule[0][0]))

        i += 1

        try:
            second_schedule = data[i].split(" ")[0:2]
            second_class_day = get_week_day(int(second_schedule[0]))
            schedule.append([second_class_day, second_schedule[1]])

        except ValueError:
            pass

        i += 1

        while not data[i].startswith("14102100"):
            i += 1

        vacancies = data[i].split(" ")[-1]

        i += 1

        while re.match(cadeiras_por_curso, data[i]):
            i += 1

        professor = []

        while data[i].startswith("- ") and i < len(data) - 1:
            professor.append(camel_case(data[i].replace("- ", "")))
            i += 1

        to_json(id, class_name, professor, schedule, vacancies, room)


def read_pdf(pdf_path: str) -> None:
    """
    Read a PDF file and print its text.

    :param pdf_path: The path to the PDF file to read.
    :type pdf_path: str
    """
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_num in range(len(pdf_reader.pages)):
            pdf_page = pdf_reader.pages[page_num]
            page_text = pdf_page.extract_text().split("\n")

            filter_data(page_text)


if __name__ == "__main__":

    read_pdf("pdfs/computer-science/2022.2.pdf")
    scrape_data()

    with open("sample.json", "w") as outfile:
        outfile.write(str(data))
