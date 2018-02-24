from database_expert import MySQL


def test_mysql():
    # Open database connection
    db = MySQL.get_connection("localhost", "root", "1506", "localdb")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print("Database version : %s " % data)
    assert data is None

    # disconnect from server
    db.close()


test_mysql()
