import json
import os

from utilities import Path


def compare(old_file, new_file, compare_result):
    try:
        print(os.path.dirname(Path.get_base_path() + compare_result))
        os.makedirs(os.path.dirname(Path.get_base_path() + compare_result), exist_ok=True)
        data = []
        with open(Path.get_base_path() + compare_result, "w+") as result, \
                open(Path.get_base_path() + old_file, 'r') as old, \
                open(Path.get_base_path() + new_file, 'r') as new:
            for old_line, new_line in zip(old, new):
                if old_line != new_line:
                    item = {'Expected': old_line, 'Actual': new_line}
                    data.append(item)
            json.dump(data, result)
    except Exception as e:
        print(e)
