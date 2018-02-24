import json
import os


def compare(old_file, new_file, compare_result):
    os.makedirs(os.path.dirname(compare_result), exist_ok=True)
    with open(compare_result, "w+") as result, open(old_file, 'r') as old, open(new_file, 'r') as new:
        old_line = old.readline()
        new_line = new.readline()
        while old_line is not None or new_line is not None:
            if old_line != new_line:
                json_object = json.dumps({'Expected': old_line, 'Actual': new_line})
                json.dump(json_object, result)
