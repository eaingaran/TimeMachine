from utilities import ReadWriteExcel


class Database:
    # Common base class for Database connection
    database_type = ''
    host_name = ''
    user_name = ''
    password = ''
    database_name = ''

    def __init__(self, application_config_file, application_config_sheet):
        self.database_type = ReadWriteExcel.read_cell(application_config_file,
                                                      application_config_sheet, 'A2')
        self.host_name = ReadWriteExcel.read_cell(application_config_file,
                                                  application_config_sheet, 'B2')
        self.user_name = ReadWriteExcel.read_cell(application_config_file,
                                                  application_config_sheet, 'C2')
        self.password = ReadWriteExcel.read_cell(application_config_file,
                                                 application_config_sheet, 'D2')
        self.database_name = ReadWriteExcel.read_cell(application_config_file,
                                                      application_config_sheet, 'E2')
