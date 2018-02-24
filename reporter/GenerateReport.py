import json

from utilities import FILE_FORMAT
from utilities import Path
from utilities import ReadWriteExcel


def write_to_report(result_file, header_string, report_format, out_file_name, excel_sheet_name='result'):
    try:
        row_number = 1
        if FILE_FORMAT.EXCEL == report_format:
            ReadWriteExcel.create_excel_workbook(out_file_name, excel_sheet_name)
            ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'A' + str(row_number),
                                      "Expected".rstrip())
            ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'B' + str(row_number),
                                      "Actual".rstrip())
            row_number += 1
            ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'A' + str(row_number),
                                      header_string.rstrip())
            ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'B' + str(row_number),
                                      header_string.rstrip())
            row_number += 1
        result_data = json.load(open(Path.get_base_path() + result_file, 'r'))
        for item in result_data:
            print(("Expected : " + item['Expected']).rstrip())
            print(("Actual : " + item['Actual']).rstrip())
            if FILE_FORMAT.EXCEL == report_format:
                ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'A' + str(row_number),
                                          item['Expected'].rstrip())
                ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'B' + str(row_number),
                                          item['Actual'].rstrip())
                row_number += 1
    except Exception as e:
        print(e)
