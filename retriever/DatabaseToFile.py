import logging
import os

from pymysql import DatabaseError

from utilities import Path, DATABASE_TYPE


def save_query_to_file_my_sql(connection, query, file):
    with open(Path.get_base_path() + file, "w+") as out_file:
        try:
            connection.execute(query)
            row = connection.fetchone()
            while row is not None:
                print(row[0])
                out_file.write(row[0])
                out_file.write('\n')
                row = connection.fetchone()
        except DatabaseError as e:
            logging.error("Error: Problem with database", e)
        except Exception as e:
            logging.error("Error: Problem with something", e)
        finally:
            connection.close()
    return "File Written"


def save_query_to_file_sqlite(connection, query, file):
    with open(Path.get_base_path() + file, "w+") as out_file:
        try:
            connection.execute(query)
            row = connection.fetchone()
            while row is not None:
                print(row[0])
                out_file.write(row[0])
                out_file.write('\n')
                row = connection.fetchone()
        except DatabaseError as e:
            logging.error("Error: Problem with database", e)
        except Exception as e:
            logging.error("Error: Problem with something", e)
        finally:
            connection.close()
    return "File Written"


def save_query_to_file(connection, query, file, database_type):
    os.makedirs(os.path.dirname(Path.get_base_path() + file), exist_ok=True)

    if DATABASE_TYPE.MY_SQL == database_type:
        cursor = connection.cursor()
        return save_query_to_file_my_sql(cursor, query, file)
    elif DATABASE_TYPE.SQLite == database_type:
        cursor = connection.cursor()
        return save_query_to_file_sqlite(cursor, query, file)
    else:
        # cursor = connection
        return 'No driver found'
