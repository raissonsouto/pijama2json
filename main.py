import PyPDF2
import json
import re
import os


VACANCIES_FOR_COURSE_IN_DISCIPLINE = r"^(\d+) - (.+) - [A-Z] (\d+) \/ (\d+)(.*)$"
FOOTER = r"^\d{2}\/\d{2}\/\d{4}\s\d{2}:\d{2}:\d{2}\s\d+\s\/\s\d+$"

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


def filter_data(page: list, data: list) -> None:
    for line in page:
        if line in EXCLUDE_PATTERNS or \
           re.match(FOOTER, line) or \
           line.startswith("TOTAL"):
            continue
        else:
            data.append(line)


def to_json(course_id: str, class_name: str, professors: list, schedule: list, vacancies: int, room: str) -> dict:
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

    return my_dict


def scrape_data(pdf_content_by_line: list) -> list:
    result = []
    i = 1

    course_id = pdf_content_by_line[0].split(" ")[2]

    while i < len(pdf_content_by_line) - 1:

        id = pdf_content_by_line[i].split(" - ")[0]
        class_name = camel_case(" ".join(pdf_content_by_line[i].split(" - ")[1].split()[:-6]))
        room = pdf_content_by_line[i].split(" ")[-1]

        schedule = [pdf_content_by_line[i].split(" ")[-3:-1]]
        schedule[0][0] = get_week_day(int(schedule[0][0]))

        i += 1

        try:
            second_schedule = pdf_content_by_line[i].split(" ")[0:2]
            second_class_day = get_week_day(int(second_schedule[0]))
            schedule.append([second_class_day, second_schedule[1]])

        except ValueError:
            pass

        i += 1

        while i < len(pdf_content_by_line) - 1 and not pdf_content_by_line[i].startswith(course_id):
            i += 1

        vacancies = pdf_content_by_line[i].split(" ")[-1]

        i += 1

        while i < len(pdf_content_by_line) - 1 and re.match(VACANCIES_FOR_COURSE_IN_DISCIPLINE, pdf_content_by_line[i]):
            i += 1

        professor = []

        while i < len(pdf_content_by_line) - 1 and pdf_content_by_line[i].startswith("- "):
            professor.append(camel_case(pdf_content_by_line[i].replace("- ", "")))
            i += 1

        result.append(to_json(id, class_name, professor, schedule, vacancies, room))

    return result


def read_pdf(pdf_path: str, pdf_content_by_line: list) -> None:
    """
    Read a PDF file and print its text.

    :param pdf_path: The path to the PDF file to read.
    :type pdf_path: str

    :param pdf_content_by_line:
    :type pdf_content_by_line: list
    """
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_num in range(len(pdf_reader.pages)):
            pdf_page = pdf_reader.pages[page_num]
            page_text = pdf_page.extract_text().split("\n")

            filter_data(page_text, pdf_content_by_line)


def write_in_json(path: str, scraped_data: list) -> None:
    try:
        with open(path, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(scraped_data, ensure_ascii=False))

    except FileNotFoundError:
        os.mkdir(f"jsons/{path.split('/')[2]}")

        with open(path, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(scraped_data, ensure_ascii=False))


def generate_json(pdf_path: str, json_path: str) -> None:
    pdf_content_by_line = []
    read_pdf(pdf_path, pdf_content_by_line)

    scraped_data = scrape_data(pdf_content_by_line)
    write_in_json(json_path, scraped_data)


def scan(path='./pdfs', jsons_path='./jsons') -> None:
    """
    Recursively search for all PDF files in the given path, and for each course folder found,
    check if there is a corresponding JSON file in the specified JSON path. If there isn't,
    create a new JSON file using the given file name and path.

    :param path: The path to search for PDF files in (default is '/pdfs')
    :type path: str
    :param jsons_path: The path to look for or create JSON files in (default is '/jsons')
    :type jsons_path: str
    """
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:

            if filename.endswith('.pdf'):
                course_name = os.path.basename(dirpath)
                json_path = os.path.join(jsons_path, course_name, filename[:-4] + '.json')

                if not os.path.exists(json_path):
                    pdf_path = os.path.join(path, course_name, filename)
                    generate_json(pdf_path, json_path)


if __name__ == "__main__":
    scan()
