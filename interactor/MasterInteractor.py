import tkinter
from datetime import datetime
from tkinter import Button
from tkinter import Radiobutton
from tkinter import Tk
from tkinter import messagebox
from tkinter import scrolledtext

from archiever import FileArchiver
from comparer import FileComparision
from database_expert import MySQL
from database_expert import SQLite
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
    window.geometry('500x500')
    txt = scrolledtext.ScrolledText(window, width=60, height=20)
    txt.grid(column=0, row=5)
    selected = tkinter.IntVar()

    # rad1 = Radiobutton(window, text=RUN_MODE.CREATE_ACTUAL, value=1, variable=selected)

    # rad2 = Radiobutton(window, text=RUN_MODE.CREATE_EXPECTED, value=2, variable=selected)

    # rad3 = Radiobutton(window, text=RUN_MODE.CREATE_ACTUAL_COMPARE_EXPECTED, value=3, variable=selected)

    # rad4 = Radiobutton(window, text=RUN_MODE.COMPARE_EXPECTED_ACTUAL, value=4, variable=selected)

    rad2 = Radiobutton(window, text='Create', value=2, variable=selected)

    rad3 = Radiobutton(window, text='Create And Compare', value=3, variable=selected)

    rad4 = Radiobutton(window, text='Compare', value=4, variable=selected)

    # rad1.grid(sticky="W", column=0, row=0)

    rad2.grid(sticky="W", column=0, row=0)

    rad3.grid(sticky="W", column=0, row=1)

    rad4.grid(sticky="W", column=0, row=2)

    start_button = Button(window, text="Start Application", command=lambda: application_start(selected.get(), txt))
    start_button.grid(sticky="E", column=0, row=3)
    window.mainloop()
    try:
        window.destroy()
    except tkinter.TclError:
        pass


def application_start(mode, logger):
    modes = {'1': RUN_MODE.CREATE_ACTUAL, '2': RUN_MODE.CREATE_EXPECTED,
             '3': RUN_MODE.CREATE_ACTUAL_COMPARE_EXPECTED, '4': RUN_MODE.COMPARE_EXPECTED_ACTUAL}
    microsecond = datetime.now().microsecond
    result_excel_name = 'Results\\TimeMachine_Result_{}.xlsx'.format(microsecond)
    result_excel_sheet_name = 'Summary'
    ReadWriteExcel.create_excel_workbook(result_excel_name, result_excel_sheet_name)
    logger.insert(tkinter.INSERT, 'Scenario,result,error_row_count,error_count' + '\n')
    ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'A1', 'Scenario')
    ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'B1', 'result')
    ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'C1', 'error_row_count')
    ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'D1', 'error_count')
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
                if RUN_MODE.CREATE_ACTUAL == modes[str(mode)]:
                    create_file(scenario, database)
                    FileArchiver.archive_file(scenario.actual_file, scenario.name, 'Actual')
                elif RUN_MODE.CREATE_EXPECTED == modes[str(mode)]:
                    res = messagebox.askyesno("Are you sure?",
                                              "This option will overwrite any existing expected files.")
                    if res:
                        create_file(scenario, database)
                        FileArchiver.archive_file(scenario.expected_file, scenario.name, 'Expected')
                elif RUN_MODE.COMPARE_EXPECTED_ACTUAL == modes[str(mode)]:
                    scenario.error_row_count, scenario.error_count = compare_file(scenario)
                    FileArchiver.archive_file(scenario.result_file, scenario.name, 'Result')
                elif RUN_MODE.CREATE_ACTUAL_COMPARE_EXPECTED == modes[str(mode)]:
                    create_file(scenario, database)
                    FileArchiver.archive_file(scenario.actual_file, scenario.name, 'Actual')
                    scenario.error_row_count, scenario.error_count = compare_file(scenario)
                    FileArchiver.archive_file(scenario.result_file, scenario.name, 'Result')
                scenario.compute_result()
                logger.insert(tkinter.INSERT, '{},{},{},{}'.format(scenario.name, scenario.result,
                                                                   scenario.error_row_count,
                                                                   scenario.error_count) + '\n')
                ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'A' + row_number, scenario.name)
                ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'B' + row_number, scenario.result)
                ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'C' + row_number,
                                          scenario.error_row_count)
                ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'D' + row_number,
                                          scenario.error_count)
                row_number += 1
            except Exception as e:
                row_number += 1
                print(e)
                if scenario.name is not None:
                    logger.insert(tkinter.INSERT, '{},Error,N/A,N/A'.format(scenario.name) + '\n')
                    ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'A' + row_number,
                                              scenario.name)
                else:
                    logger.insert(tkinter.INSERT, '{},Error,N/A,N/A'.format(row_number) + '\n')
                    ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'A' + row_number, row_number)
                ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'B' + row_number, 'Error')
                ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'C' + row_number,
                                          'N/A')
                ReadWriteExcel.write_cell(result_excel_name, result_excel_sheet_name, 'D' + row_number, 'N/A')
                continue
    except Exception as e:
        print(e)
        messagebox.showerror('Failed', 'Operation Failed\n' + str(e))
    messagebox.showinfo('Success', 'Operation Completed Successfully')


def create_file(scenario, database):
    try:
        if DATABASE_TYPE.MY_SQL == database.database_type:
            connection = MySQL.get_connection(database.host_name, database.user_name, database.password,
                                              database.database_name)
        elif DATABASE_TYPE.SQLite == database.database_type:
            connection = SQLite.get_connection(database.database_name)
        else:
            connection = None
        DatabaseToFile.save_query_to_file(connection, scenario.query, scenario.actual_file, database.database_type)
    except Exception as e:
        print("Couldn't get the data from database.", e)
        raise


def compare_file(scenario):
    try:
        temp_result_file = "temp_res.json"
        exp_file = open(Path.get_base_path() + scenario.expected_file)
        act_file = open(Path.get_base_path() + scenario.actual_file)
        exp_header = exp_file.readline()
        act_header = act_file.readline()
        if act_header.rstrip() == exp_header.rstrip():
            FileComparision.compare(scenario.expected_file, scenario.actual_file, temp_result_file)
            return GenerateReport.write_to_report(temp_result_file, exp_header.rstrip(), scenario.result_format,
                                                  scenario.result_file)
        else:
            print("Header didn't match.\nExpected : {}\nActual : {}".format(exp_header, act_header))
            return -1, 0
    except Exception as e:
        print("Couldn't compare the given files.", e)
        raise


open_user_interface()
