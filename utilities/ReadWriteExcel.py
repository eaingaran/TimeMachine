from openpyxl import Workbook
from openpyxl import load_workbook

from utilities import Path


def read_cell(book_name, sheet_name, cell):
    try:
        work_book = load_workbook(Path.get_base_path() + book_name)
        sheet = work_book[sheet_name]
        value = sheet[cell].value()
        print("Values of {} in sheet {} of book {} is {}".format(cell, sheet_name, book_name, value))
        return value
    except Exception as e:
        print("Couldn't get the value fo the cell {} in sheet {} of book {}".format(cell, sheet_name, book_name), e)
        return None


def write_cell(book_name, sheet_name, cell, value):
    try:
        work_book = load_workbook(Path.get_base_path() + book_name)
        sheet = work_book[sheet_name]
        sheet[cell] = value
        print("Values of {} in sheet {} of book {} is set to {}".format(cell, sheet_name, book_name, value))
        work_book.save(Path.get_base_path() + book_name)
    except FileNotFoundError as e:
        print("File {} is not found.".format(book_name), e)
        create_excel_workbook(book_name, sheet_name)
        try:
            write_cell(book_name, sheet_name, cell, value)
        except Exception as e:
            print("Tried creating a new sheet and calling the method again. Still failed.", e)
    except Exception as e:
        print("Error while trying to write.", e)


def create_excel_workbook(book_name, sheet_name):
    try:
        work_book = Workbook()
        work_sheet = work_book.active
        work_sheet.title = sheet_name
        work_book.save(filename=Path.get_base_path() + book_name)
        print("Work book with name {} with a sheet named {} created.".format(book_name, sheet_name))
    except Exception as e:
        print("Couldn't create a workbook.", e)
