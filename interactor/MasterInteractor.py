from tkinter import *

from archiever import FileArchiver
from comparer import FileComparision
from database_expert import MySQL
from interactor import Database
from interactor import Scenario
from reporter import GenerateReport
from retriever import DatabaseToFile
from utilities import DATABASE_TYPE
from utilities import Path
from utilities import RUN_MODE
from utilities import ReadWriteExcel


def open_user_interface():
    window = Tk()
    window.geometry("500x500")
    variable = StringVar(window)
    variable.set(RUN_MODE.CREATE_ACTUAL)  # default value

    w = OptionMenu(window, variable, RUN_MODE.CREATE_ACTUAL_COMPARE_EXPECTED,
                   RUN_MODE.CREATE_ACTUAL, RUN_MODE.COMPARE_EXPECTED_ACTUAL,
                   RUN_MODE.CREATE_EXPECTED)
    w.pack()
    start_button = Button(window, text="Start Application", command=lambda: application_start(variable))
    start_button.place(x=250, y=250)
    window.mainloop()


def application_start(mode):
    try:
        application_config_file = "MasterConfig.xlsx"
        application_scenario_sheet = "scenario"
        application_config_sheet = "config"
        row_number = 2
        database = Database.Database(application_config_file, application_config_sheet)
        while ReadWriteExcel.read_cell(application_config_file, application_scenario_sheet,
                                       'A' + str(row_number)) is not None:
            try:
                scenario = Scenario.Scenario(application_config_file, application_scenario_sheet, row_number)
                if RUN_MODE.CREATE_ACTUAL == mode:
                    create_file(scenario, database)
                    FileArchiver.archive_file(scenario.actual_file, scenario.name, 'Actual')
                if RUN_MODE.CREATE_EXPECTED == mode:
                    create_file(scenario, database)
                    FileArchiver.archive_file(scenario.expected_file, scenario.name, 'Expected')
                if RUN_MODE.COMPARE_EXPECTED_ACTUAL == mode:
                    compare_file(scenario)
                    FileArchiver.archive_file(scenario.result_file, scenario.name, 'Result')
                if RUN_MODE.CREATE_ACTUAL_COMPARE_EXPECTED == mode:
                    create_file(scenario, database)
                    FileArchiver.archive_file(scenario.actual_file, scenario.name, 'Actual')
                    compare_file(scenario)
                    FileArchiver.archive_file(scenario.result_file, scenario.name, 'Result')
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        print(e)


def create_file(scenario, database):
    try:
        if DATABASE_TYPE.MY_SQL == database.database_type:
            connection = MySQL.get_connection(database.host_name, database.user_name, database.password,
                                              database.database_name)
        else:
            connection = None
        DatabaseToFile.save_query_to_file(connection, scenario.query, scenario.actual_file)
    except Exception as e:
        print("Couldn't get the data from database.", e)


def compare_file(scenario):
    try:
        temp_result_file = "temp_res.json"
        exp_file = open(Path.get_base_path() + scenario.expected_file)
        act_file = open(Path.get_base_path() + scenario.actual_file)
        exp_header = exp_file.readline()
        act_header = act_file.readline()
        if act_header.rstrip() == exp_header.rstrip():
            FileComparision.compare(scenario.expected_file, scenario.actual_file, temp_result_file)
            GenerateReport.write_to_report(temp_result_file, exp_header.rstrip(), scenario.result_format,
                                           scenario.result_file)
        else:
            print("Header didn't match.\nExpected : {}\nActual : {}".format(exp_header, act_header))
    except Exception as e:
        print("Couldn't compare the given files.", e)


open_user_interface()
