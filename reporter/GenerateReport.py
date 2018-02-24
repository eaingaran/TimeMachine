import json

from utilities import FILE_FORMAT
from utilities import ReadWriteExcel


def write_to_report(result_file, format):
    result_data = json.load(open(result_file, 'r'))
    for expected, actual in result_data:
        print("Expected : " + expected)
        print("Actual : " + actual)
        if format == FILE_FORMAT.EXCEL:
            ReadWriteExcel.read_cell()
