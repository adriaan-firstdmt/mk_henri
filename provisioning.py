from mysql.connector import connect, Error
from mysqlmanager.mysqlmanager import MySQLManager 

def connect_to_database():
    database = MySQLManager('127.0.0.1','mikenskiet_db_user','1eenT0Tagt8')
    database.connect()
    database.show_databases()


def standard_script():
    try:
        with connect(
            host="localhost",
            user="mikenskiet_db_user",
            password="1eenT0Tagt8",
        ) as connection:
            print(connection)
    except Error as e:
        print(e)
    show_db_query = "SHOW DATABASES"
    with connection.cursor() as cursor:
        cursor.execute(show_db_query)
        for db in cursor:
            print(db)



def main():
    standard_script()
    print("hello world")

if __name__ == '__main__':
    main()