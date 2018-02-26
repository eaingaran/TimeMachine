import json

from yattag import Doc

from utilities import FILE_FORMAT
from utilities import Path
from utilities import ReadWriteExcel


def write_to_report(result_file, header_string, report_format, out_file_name, excel_sheet_name='result'):
    if FILE_FORMAT.EXCEL == report_format:
        return generate_excel_report(result_file, header_string, out_file_name, excel_sheet_name)
    elif FILE_FORMAT.HTML == report_format:
        return generate_html_report(result_file, header_string, out_file_name)
    else:
        print("Selected Report format '" + report_format + "' not supported.")


def generate_excel_report(result_file, header_string, out_file_name, excel_sheet_name):
    try:
        row_number = 1
        ReadWriteExcel.create_excel_workbook(out_file_name, excel_sheet_name)
        ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'A' + str(row_number),
                                  "Line Number".rstrip())
        ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'B' + str(row_number),
                                  "Expected".rstrip())
        ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'C' + str(row_number),
                                  "Actual".rstrip())
        row_number += 1
        ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'B' + str(row_number),
                                  header_string.rstrip())
        ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'C' + str(row_number),
                                  header_string.rstrip())
        row_number += 1
        result_data = json.load(open(Path.get_base_path() + result_file, 'r'))
        for item in result_data:
            print(("Line No. : " + item['LineNumber']).rstrip())
            print(("Expected : " + item['Expected']).rstrip())
            print(("Actual : " + item['Actual']).rstrip())
            ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'A' + str(row_number),
                                      item['LineNumber'].rstrip())
            ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'B' + str(row_number),
                                      item['Expected'].rstrip())
            ReadWriteExcel.write_cell(out_file_name, excel_sheet_name, 'C' + str(row_number),
                                      item['Actual'].rstrip())
            row_number += 1
            print(row_number - 3, 'N/A')
        return row_number - 3, 'N/A'
    except Exception as e:
        print(e)
        return -1, 0


def generate_html_report(result_file, header_string, out_file_name):
    mismatch_row_count = 0
    mismatch_count = 0
    doc, tag, text = Doc().tagtext()
    print("Header : " + header_string.rstrip())
    title = out_file_name.split(".")[0]
    result_data = json.load(open(Path.get_base_path() + result_file, 'r'))
    for item in result_data:
        print(("Line No. : " + item['LineNumber']).rstrip())
        print(("Expected : " + item['Expected']).rstrip())
        print(("Actual : " + item['Actual']).rstrip())

    with tag('html'):
        with tag('head'):
            with tag('title'):
                text(title)
        with tag('body'):
            with tag('table', style='width:100%', border="1"):
                with tag('tr'):
                    with tag('th'):
                        text("Line Number")
                    for header in header_string.split(';'):
                        with tag('th'):
                            text(header.upper())
                for item in result_data:
                    value_ref = {}
                    with tag('tr'):
                        with tag('td', rowspan='2', align="center"):
                            text(item['LineNumber'].rstrip())
                            mismatch_row_count += 1
                        col_num = 1
                        for column_value in item['Expected'].rstrip().split(';'):
                            with tag('td', align="center"):
                                text(column_value)
                                value_ref[col_num] = column_value
                            col_num += 1
                        col_num = 1
                    with tag('tr'):
                        for column_value in item['Actual'].rstrip().split(';'):
                            with tag('td', align="center"):
                                if column_value == value_ref[col_num]:
                                    text(column_value)
                                else:
                                    with tag('font', color="red"):
                                        text(column_value)
                                        mismatch_count += 1
                            col_num += 1

    result = doc.getvalue()
    print(result)
    with open(Path.get_base_path() + out_file_name, 'w+') as html_file:
        html_file.writelines("<!DOCTYPE html>")
        html_file.writelines(result)
    print(mismatch_row_count, mismatch_count)
    return mismatch_row_count, mismatch_count

# generate_html_report('test.json', 'name;id', 'test.html')
# generate_excel_report('test.json', 'name;id', 'test.xlsx', 'test')
