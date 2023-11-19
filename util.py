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
