from mysql.connector import connect, Error

class MySQLManager:
    def __init__(self,host,user,password) -> None:
        self.host = host
        self.user = user
        self.password = password

    def connect(self):
        try:
            with connect(
                host= self.host,
                user=self.user,
                password=self.password,
            ) as connection:
                self.connection = connection
                return self.connection
        except Error as e:
            print(e)
    
    def show_databases(self):
        show_db_query = "SHOW DATABASES"
        with self.connection.cursor() as cursor:
            cursor.execute(show_db_query)
            for db in cursor:
                print(db)