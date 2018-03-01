import pymysql


def get_connection(host, user, pwd, database_name):
    return pymysql.connect(host, user, pwd, database_name)
