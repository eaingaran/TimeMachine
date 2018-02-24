from utilities import ReadWriteExcel


class Scenario:
    # Common base class for all Scenarios
    name = ''
    query = ''
    actual_file = ''
    expected_file = ''
    result_file = ''
    result_format = ''

    def __init__(self, application_config_file, application_scenario_sheet, row_number):
        self.name = ReadWriteExcel.read_cell(application_config_file, application_scenario_sheet, 'A' + str(row_number))
        self.query = ReadWriteExcel.read_cell(application_config_file, application_scenario_sheet, 'B' +
                                              str(row_number))
        self.actual_file = ReadWriteExcel.read_cell(application_config_file,
                                                    application_scenario_sheet,
                                                    'C' + str(row_number))
        self.expected_file = ReadWriteExcel.read_cell(application_config_file,
                                                      application_scenario_sheet,
                                                      'D' + str(row_number))
        self.result_file = ReadWriteExcel.read_cell(application_config_file,
                                                    application_scenario_sheet,
                                                    'E' + str(row_number))
        self.result_format = ReadWriteExcel.read_cell(application_config_file,
                                                      application_scenario_sheet,
                                                      'F' + str(row_number))
