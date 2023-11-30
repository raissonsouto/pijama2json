from PyPDF2 import PdfReader
from re import match


def filter_data(page: list) -> list:
    """
    Filter unwanted lines from a page and return the remaining content. What is considered as unwanted:
    - Table column names, university name, etc
    - Lines with the total vacancies for a class (the script gets the total vacancies for a specific
      course in another line)
    - Page footer

    :param page: The list of lines from a page of the pdf.
    :type page: list

    :return: The PDF page content filtered.
    :rtype: list
    """

    unwanted_lines = ["UNIVERSIDADE FEDERAL DE CAMPINA GRANDE",
                      "PRÓ-REITORIA DE ENSINO",
                      "Disciplina Turma CR CH Horários"]

    footer = r"^\d{2}\/\d{2}\/\d{4}\s\d{2}:\d{2}:\d{2}\s\d+\s\/\s\d+$"

    filtered_page = []

    for line in page:
        if line in unwanted_lines or match(footer, line) or line.startswith("TOTAL"):
            filtered_page.append(line)

    return filtered_page


def read_page(pdf_reader: PdfReader, page_index: int) -> list:
    """
    Read a PDF page and return its text.

    :param pdf_reader: The PDF reader agent.
    :type pdf_reader: PdfReader

    :param page_index: The index of the page that should be read.
    :type page_index: int

    :return: The PDF page content.
    :rtype: list
    """
    pdf_page = pdf_reader.pages[page_index]
    page_text = pdf_page.extract_text().split("\n")

    return filter_data(page_text)


def read_pdf(pdf_path: str) -> list:
    """
    Read a PDF file and return its text.

    :param pdf_path: The path to the PDF file to read.
    :type pdf_path: str

    :return: The PDF file content.
    :rtype: list
    """

    pdf_content_by_line = []

    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)

        for page_index in range(len(pdf_reader.pages)):
            pdf_content_by_line += read_page(pdf_reader, page_index)

    return pdf_content_by_line
