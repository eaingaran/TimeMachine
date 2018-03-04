import sqlite3

from utilities import Path

con = sqlite3.connect(Path.get_base_path() + 'local.db')

con.execute('create table user (id int, name text);')
con.execute("insert into user (id, name) values (1,'Aingaran');")
con.execute("insert into user (id, name) values (2,'Mark');")
con.execute("insert into user (id, name) values (3,'Jane');")
con.execute("insert into user (id, name) values (4,'Someone');")
con.commit()
con.close()
