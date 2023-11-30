from util import camel_case, get_week_day, course_as_dict


VACANCIES_FOR_COURSE_IN_DISCIPLINE = r"^(\d+) - (.+) - [A-Z] (\d+) \/ (\d+)(.*)$"


def extract_course_details(line: str, pdf_content_by_line: list, current_index: int) -> tuple:
    course_id = extract_class_id(line)
    class_name = extract_class_name(line)
    room = line.split(" ")[-1]

    initial_schedule_info = line.split(" ")[-3:-1]
    schedule, current_index = parse_schedule(initial_schedule_info, pdf_content_by_line, current_index)

    vacancies, current_index = extract_vacancies(pdf_content_by_line, current_index)

    professors, current_index = extract_professors(pdf_content_by_line, current_index)

    dict_class = course_as_dict(course_id, class_name, professors, schedule, vacancies, room)

    return dict_class, current_index


def scrape_data(pdf_content_by_line: list) -> list:
    result = []
    i = 1

    while i < len(pdf_content_by_line) - 1:
        course_details, i = extract_course_details(pdf_content_by_line[i], pdf_content_by_line, i)
        result.append(course_as_dict(**course_details))

    return result


def extract_professors(pdf_content_by_line: list, current_index: int) -> tuple:

    professors = []
    while current_index < len(pdf_content_by_line) - 1 and pdf_content_by_line[current_index].startswith("- "):
        professors.append(camel_case(pdf_content_by_line[current_index].replace("- ", "")))
        current_index += 1

    return professors, current_index


def extract_class_name(line: str) -> str:

    return camel_case(" ".join(line.split(" - ")[1].split()[:-6]))


def extract_vacancies(pdf_content_by_line: list, current_index: int) -> tuple:

    vacancies = pdf_content_by_line[current_index].split(" ")[-1]
    current_index += 1
    return vacancies, current_index


def extract_class_id(line: str) -> str:

    return line.split(" - ")[0]


def parse_schedule(schedule_info: list, pdf_content_by_line: list, current_index: int) -> tuple:

    schedule = [schedule_info]
    schedule[0][0] = get_week_day(int(schedule[0][0]))

    current_index += 1

    try:
        second_schedule = pdf_content_by_line[current_index].split(" ")[0:2]
        if len(second_schedule) == 2:
            second_class_day = get_week_day(int(second_schedule[0]))
            schedule.append([second_class_day, second_schedule[1]])
    except (ValueError, IndexError):
        pass

    current_index += 1

    return schedule, current_index
