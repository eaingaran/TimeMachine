from reporter import GenerateReport
from utilities import FILE_FORMAT


def test_report():
    GenerateReport.write_to_report("test.json", "name,id", FILE_FORMAT.EXCEL, "out.xlsx", "Compare_result")


test_report()
