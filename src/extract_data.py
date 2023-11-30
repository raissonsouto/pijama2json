from src.util import typographical_convention, get_week_day, class_as_dict
from re import match


def extract_class_id(line: str) -> str:
    return line.split(" - ")[0]


def extract_class_name(line: str) -> str:
    class_name = " ".join(line.split(" - ")[1].split()[:-6])
    return typographical_convention(class_name)


def extract_class_room(line: str) -> str:
    return line.split(" ")[-1]


def extract_schedule(pdf_content_by_line: list, current_index: int) -> tuple:
    schedule = []

    first_day_info = pdf_content_by_line[current_index].split(" ")[-3:-1]
    first_day_info[0] = get_week_day(int(first_day_info[0]))

    schedule.append(first_day_info)

    current_index += 1
    second_day_line = pdf_content_by_line[current_index].split(" ")

    if len(second_day_line[0]) == 1:
        second_day_info = second_day_line[0:2]
        second_day_info[0] = get_week_day(int(second_day_info[0]))

        schedule.append(second_day_info)

    current_index += 1

    return schedule, current_index


def extract_vacancies(pdf_content_by_line: list, current_index: int) -> tuple:
    vacancies = pdf_content_by_line[current_index].split(" ")[-3]
    current_index += 1
    return vacancies, current_index


def extract_professors(pdf_content_by_line: list, current_index: int) -> tuple:
    professors = []
    class_first_line = r'^\d{7}\s-\s.*$'

    while not current_index == len(pdf_content_by_line) and not match(class_first_line, pdf_content_by_line[current_index]):

        if pdf_content_by_line[current_index].startswith("- "):
            professor_name = pdf_content_by_line[current_index].replace("- ", "")
            professors.append(typographical_convention(professor_name))

        current_index += 1

    return professors, current_index


def extract_course_details(pdf_content_by_line: list, current_index: int) -> tuple:
    current_line = pdf_content_by_line[current_index]

    course_id = extract_class_id(current_line)
    class_name = extract_class_name(current_line)
    room = extract_class_room(current_line)

    schedule, current_index = extract_schedule(pdf_content_by_line, current_index)
    vacancies, current_index = extract_vacancies(pdf_content_by_line, current_index)
    professors, current_index = extract_professors(pdf_content_by_line, current_index)

    dict_class = class_as_dict(course_id, class_name, professors, schedule, vacancies, room)

    return dict_class, current_index


def scrape_data(pdf_content_by_line: list) -> list:
    result = []
    index = 1

    while index < len(pdf_content_by_line) - 1:
        class_dict, index = extract_course_details(pdf_content_by_line, index)
        result.append(class_dict)

    return result
