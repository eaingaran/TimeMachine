import os

from pymysql import DatabaseError

from utilities import Path


def save_query_to_file(connection, query, file):
    os.makedirs(os.path.dirname(Path.get_base_path() + file), exist_ok=True)

    cursor = connection.cursor()

    with open(Path.get_base_path() + file, "w+") as out_file:
        try:
            cursor.execute(query)
            row = cursor.fetchone()
            while row is not None:
                print(row[0])
                out_file.write(row[0])
                row = cursor.fetchone()
        except DatabaseError as e:
            print("Error: Problem with database", e)
        except Exception as e:
            print("Error: Problem with something", e)
        finally:
            cursor.close()
    return "File Written"
