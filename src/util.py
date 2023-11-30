def get_week_day(day: int) -> str:
    """
    Given a day of the week represented as an integer and returns the corresponding day of the week in Portuguese.

    :param day: The day of the week as an integer (1-7 for Saturday-Sunday).
    :type day: int

    :return:The corresponding day of the week in Portuguese, or an empty string
    if the input is not a valid day of the week.
    :rtype: str
    """
    days = {
        1: "domingo",
        2: "segunda",
        3: "terça",
        4: "quarta",
        5: "quinta",
        6: "sexta",
        7: "sábado"
    }
    return days.get(day, "")


def is_romanian_numeral(input_string: str) -> bool:
    """
    Check if the input string represents a Romanian numeral.

    :param input_string: The string to check.
    :type input_string: str

    :return: True if the input string represents a Romanian numeral, False otherwise.
    :rtype: bool
    """
    romanian_numerals = ["I", "V", "X", "L", "C", "D", "M"]

    for char in input_string:
        if char.upper() not in romanian_numerals:
            return False

    return True


def class_as_dict(course_id: str, class_name: str, professors: list, schedule: list, vacancies: int, room: str) -> dict:

    """
    Given attributes of a class, returns a dict representing the class.

    :param course_id: The ID of the class.
    :param class_name: The name of the class.
    :param professors: A list of the name of the professor.
    :param schedule: A list of tuples representing the schedule of the class.
    Each tuple should contain two strings representing the start and end time
    of the class.
    :param vacancies: The amount of seats available for the class.
    :param room: The room number and name where the class takes place.

    :return: A JSON string representing the class.
    :rtype: dict
    """
    class_dict = {
        "id": course_id,
        "name": class_name,
        "professor": professors,
        "schedule": schedule,
        "vacancies": vacancies,
        "room": room
    }

    return class_dict


def remove_file_from_path(path: str) -> str:
    return "/".join(path.split("/").pop())


def remove_file_extension(filename: str) -> str:
    return ".".join(filename.split(".")[0:2])


def typographical_convention(text: str) -> str:
    """
    Convert a string of space-separated words into camel case.

    :param text: The input string to convert.
    :type text: str

    :return: The string in camel case.
    :rtype: str
    """

    CONNECTIVES_ARTICLES_CONTRACTIONS = ["o", "a", "e", "p", "os", "as", "do", "da", "dos", "das", "em", "no", "na",
                                         "nos", "nas", "de", "do", "da", "dos", "das", "por", "para", "com"]

    words = text.split(" ")
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
