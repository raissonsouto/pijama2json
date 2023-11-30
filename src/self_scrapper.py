import os
from src.json_writer import write_json
from src.util import remove_file_extension


def self_scrap(path: str) -> None:
    rep_data = {}

    for directory_path, _, filenames in os.walk(path):
        if directory_path.endswith(path):
            continue

        semesters = []

        for filename in filenames:
            if filename.endswith('.json'):
                semesters.append(remove_file_extension(filename))

        rep_data[directory_path.split("/")[-1]] = semesters

    write_json(path + "/metadata.json", rep_data)

