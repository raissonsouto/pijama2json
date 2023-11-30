import os
import json
from src.util import remove_file_from_path


def write_json(path: str, scraped_data) -> None:
    """
       Write scraped data to a JSON file.

       :param path: The file path of the JSON file to be written.
       :type path: str
       :param scraped_data: The scraped data to be written to the JSON file.
       """

    try:
        with open(path, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(scraped_data, ensure_ascii=False))

    except FileNotFoundError:
        os.mkdir(remove_file_from_path(path))
        write_json(path, scraped_data)
