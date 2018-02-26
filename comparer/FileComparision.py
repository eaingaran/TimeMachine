import json
import os

from utilities import Path


def compare(old_file, new_file, compare_result):
    try:
        print(os.path.dirname(Path.get_base_path() + compare_result))
        os.makedirs(os.path.dirname(Path.get_base_path() + compare_result), exist_ok=True)
        data = []
        line_number = 1
        with open(Path.get_base_path() + compare_result, "w+") as result, \
                open(Path.get_base_path() + old_file, 'r') as old, \
                open(Path.get_base_path() + new_file, 'r') as new:
            for old_line, new_line in zip(old, new):
                if old_line.rstrip() != new_line.rstrip():
                    item = {'LineNumber': line_number, 'Expected': old_line.rstrip(), 'Actual': new_line.rstrip()}
                    data.append(item)
                line_number += 1
            json.dump(data, result)
    except Exception as e:
        print(e)
