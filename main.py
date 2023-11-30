from src.self_scrapper import self_scrap
from src.util import remove_file_extension
from src.pdf_reader import read_pdf
from src.extract_data import scrape_data
from src.json_writer import write_json
import os


def generate_json(pdf_path: str, json_path: str) -> None:
    """
    Get a PDF and generate a JSON from it.

    :param pdf_path: The file path of the PDF file to be scraped.
    :type pdf_path: str
    :param json_path: The file path of the JSON file to be generated.
    :type json_path: str
    """
    pdf_content_by_line = read_pdf(pdf_path)
    scraped_data = scrape_data(pdf_content_by_line)
    write_json(json_path, scraped_data)


def scan(path='./pdfs', jsons_path='./jsons') -> None:
    """
    Recursively search for all PDF files in the given path, and for each course folder found,
    check if there is a corresponding JSON file in the specified JSON path. If there isn't,
    create a new JSON file using the given file name and path.

    :param path: The path to search for PDF files in (default is './pdfs')
    :type path: str
    :param jsons_path: The path to look for or create JSON files in (default is './jsons')
    :type jsons_path: str
    """

    for directory_path, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.pdf'):
                course_name = os.path.basename(directory_path)
                json_path = os.path.join(jsons_path, course_name, remove_file_extension(filename) + '.json')

                if not os.path.exists(json_path):
                    pdf_path = os.path.join(path, course_name, filename)
                    generate_json(pdf_path, json_path)

    self_scrap(jsons_path)


if __name__ == "__main__":
    scan()
