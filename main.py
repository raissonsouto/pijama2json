from util import get_week_day, is_romanian_numeral
import PyPDF2
import json
import re
import os


VACANCIES_FOR_COURSE_IN_DISCIPLINE = r"^(\d+) - (.+) - [A-Z] (\d+) \/ (\d+)(.*)$"
FOOTER = r"^\d{2}\/\d{2}\/\d{4}\s\d{2}:\d{2}:\d{2}\s\d+\s\/\s\d+$"

CONNECTIVES_ARTICLES_CONTRACTIONS = ["o", "a", "e", "p", "os", "as", "do", "da", "dos", "das", "em", "no", "na", "nos",
                                     "nas", "de", "do", "da", "dos", "das", "por", "para", "com"]


EXCLUDE_PATTERNS = [
    "UNIVERSIDADE FEDERAL DE CAMPINA GRANDE",
    "PRÓ-REITORIA DE ENSINO",
    "Disciplina Turma CR CH Horários"
]


def camel_case(text: str) -> str:
    """
    Convert a string of space-separated words into camel case.

    :param text: The input string to convert.
    :type text: str

    :return: The string in camel case.
    :rtype: str
    """
    words = text.split(" ")
    print(words)
    capitalized_words = ""

    for word in words:

        l_word = word.lower()

        if l_word in CONNECTIVES_ARTICLES_CONTRACTIONS:
            capitalized_words += " " + l_word

        elif is_romanian_numeral(l_word):
            capitalized_words += " " + word.upper()
        else:
            capitalized_words += " " + word.capitalize()

    return capitalized_words.strip()


def filter_data(page: list, data: list) -> None:
    """
    Filter unwanted lines from a page and append the remaining lines to a list of scraped data.

    :param page: The list of lines from a page of the pdf.
    :type page: list
    :param data: The list of scraped data to which the remaining lines will be appended.
    :type data: list
    """
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


# def scrape_data(pdf_content_by_line: list) -> list:
#     result = []
#     i = 1

#     course_id = pdf_content_by_line[0].split(" ")[2]

#     while i < len(pdf_content_by_line) - 1:
#         print(pdf_content_by_line[len(pdf_content_by_line)-10:len(pdf_content_by_line)])

#         id = pdf_content_by_line[i].split(" - ")[0]
#         class_name = camel_case(" ".join(pdf_content_by_line[i].split(" - ")[1].split()[:-6]))
#         room = pdf_content_by_line[i].split(" ")[-1]

#         schedule = [pdf_content_by_line[i].split(" ")[-3:-1]]
#         schedule[0][0] = get_week_day(int(schedule[0][0]))

#         i += 1

#         try:
#             second_schedule = pdf_content_by_line[i].split(" ")[0:2]
#             second_class_day = get_week_day(int(second_schedule[0]))
#             schedule.append([second_class_day, second_schedule[1]])

#         except ValueError:
#             pass

#         i += 1

#         while i < len(pdf_content_by_line) - 1 and not pdf_content_by_line[i].startswith(course_id):
#             i += 1

#         vacancies = pdf_content_by_line[i].split(" ")[-1]

#         i += 1

#         while i < len(pdf_content_by_line) - 1 and re.match(VACANCIES_FOR_COURSE_IN_DISCIPLINE, pdf_content_by_line[i]):
#             i += 1

#         professor = []

#         while i < len(pdf_content_by_line) - 1 and pdf_content_by_line[i].startswith("- "):
#             professor.append(camel_case(pdf_content_by_line[i].replace("- ", "")))
#             i += 1

#         result.append(to_json(id, class_name, professor, schedule, vacancies, room))

#     return result

def parse_schedule(schedule_info: list, pdf_content_by_line: list, current_index: int) -> tuple:
    """
    Parses the schedule information from the given line of the PDF content.

    :param schedule_info: The initial schedule information extracted.
    :param pdf_content_by_line: The entire PDF content split into lines.
    :param current_index: The current index in the PDF content.

    :return: A tuple containing the parsed schedule and the updated index.
    """
    schedule = [schedule_info]
    schedule[0][0] = get_week_day(int(schedule[0][0]))

    current_index += 1

    try:
        second_schedule = pdf_content_by_line[current_index].split(" ")[0:2]
        if len(second_schedule) == 2:
            second_class_day = get_week_day(int(second_schedule[0]))
            schedule.append([second_class_day, second_schedule[1]])
    except (ValueError, IndexError):
        # Handling ValueError for int conversion and IndexError for list access
        pass

    current_index += 1

    return schedule, current_index

def extract_course_details(line: str, pdf_content_by_line: list, current_index: int) -> tuple:
    """
    Extracts course details from a given line of the PDF content with enhanced schedule parsing.

    :param line: The current line from the PDF content.
    :param pdf_content_by_line: The entire PDF content split into lines.
    :param current_index: The current index in the PDF content.

    :return: A tuple containing extracted course details and the updated index.
    """
    course_id = line.split(" - ")[0]
    class_name = camel_case(" ".join(line.split(" - ")[1].split()[:-6]))
    room = line.split(" ")[-1]

    initial_schedule_info = line.split(" ")[-3:-1]
    schedule, current_index = parse_schedule(initial_schedule_info, pdf_content_by_line, current_index)

    while current_index < len(pdf_content_by_line) - 1 and not pdf_content_by_line[current_index].startswith(course_id):
        current_index += 1

    vacancies = pdf_content_by_line[current_index].split(" ")[-1]

    current_index += 1

    while current_index < len(pdf_content_by_line) - 1 and re.match(VACANCIES_FOR_COURSE_IN_DISCIPLINE, pdf_content_by_line[current_index]):
        current_index += 1

    professor = []

    while current_index < len(pdf_content_by_line) - 1 and pdf_content_by_line[current_index].startswith("- "):
        professor.append(camel_case(pdf_content_by_line[current_index].replace("- ", "")))
        current_index += 1

    return (course_id, class_name, room, schedule, vacancies, professor), current_index

def scrape_data(pdf_content_by_line: list) -> list:
    result = []
    i = 1

    while i < len(pdf_content_by_line) - 1:
        course_details, i = extract_course_details(pdf_content_by_line[i], pdf_content_by_line, i)
        result.append(to_json(*course_details))

    return result


def read_pdf(pdf_path: str, pdf_content_by_line: list) -> None:
    """
    Read a PDF file and print its text.

    :param pdf_path: The path to the PDF file to read.
    :type pdf_path: str

    :param pdf_content_by_line:
    :type pdf_content_by_line: list
    """
    print(f"    [*] Reading PDF ...")
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        print(f"    [*] Filtering data")
        for page_num in range(len(pdf_reader.pages)):
            pdf_page = pdf_reader.pages[page_num]
            page_text = pdf_page.extract_text().split("\n")

            filter_data(page_text, pdf_content_by_line)


def write_in_json(path: str, scraped_data: list) -> None:
    """
       Write scraped data to a JSON file.

       :param path: The file path of the JSON file to be written.
       :type path: str
       :param scraped_data: The list of scraped data to be written to the JSON file.
       :type scraped_data: list
       """
    try:
        with open(path, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(scraped_data, ensure_ascii=False))

    except FileNotFoundError:
        os.mkdir(f"jsons/{path.split('/')[2]}")

        with open(path, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(scraped_data, ensure_ascii=False))


def generate_json(pdf_path: str, json_path: str) -> None:
    """
    Get a PDF and generate a JSON from it

    :param pdf_path: The file path of the PDF file to be scraped.
    :type pdf_path: str
    :param json_path: The file path of the JSON file to be generated.
    :type json_path: str
    """
    pdf_content_by_line = []
    read_pdf(pdf_path, pdf_content_by_line)

    print("    [*] Generating JSON")
    scraped_data = scrape_data(pdf_content_by_line)
    write_in_json(json_path, scraped_data)
    print("    [*] JSON done")


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

    print("[*] Scanning PDFs folder searching for unprocessed PDFs")

    for directory_path, _, filenames in os.walk(path):  # _ == directories_name
        for filename in filenames:

            if filename.endswith('.pdf'):
                course_name = os.path.basename(directory_path)
                json_path = os.path.join(jsons_path, course_name, filename[:-4] + '.json')

                if not os.path.exists(json_path):
                    pdf_path = os.path.join(path, course_name, filename)
                    print(f"[*] Unprocessed PDF found: {pdf_path}")
                    generate_json(pdf_path, json_path)


if __name__ == "__main__":
    print("\n-- PIJAMA2JSON --\n")
    scan()
    print("[*] All done :)")
