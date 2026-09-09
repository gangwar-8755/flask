import mysql.connector
def get_db_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="company_db"
    )