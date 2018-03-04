import sqlite3

from utilities import Path


def create_table():
    con = sqlite3.connect(Path.get_base_path() + 'local.db')

    con.execute('create table user (id int, name text);')
    con.execute("insert into user (id, name) values (1,'Aingaran');")
    con.execute("insert into user (id, name) values (2,'Mark');")
    con.execute("insert into user (id, name) values (3,'Jane');")
    con.execute("insert into user (id, name) values (4,'Someone');")
    con.commit()
    con.close()


def modify_data():
    con = sqlite3.connect(Path.get_base_path() + 'local.db')

    con.execute("update user SET name='Aingaran Elango' where id=1;")
    con.execute("update user SET name='Avinash', id=6 where id=4;")
    con.commit()
    con.close()


modify_data()
