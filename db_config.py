import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='localhost',
        database='tkinter_app'
    )
