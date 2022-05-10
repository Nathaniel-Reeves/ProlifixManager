import mysql.connector
from mysql.connector import Error

class database:

    def __init__(self, database, table):
        self.connection = None
        self.database = database
        self.table = table

        try:
            self.connection = mysql.connector.connect(host='localhost', database=self.database, user='client', password='clientPassword5!')
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.cursor = self.connection.cursor()
                self.cursor.execute("select database();")
                record = self.cursor.fetchone()
                print("You're connected to database: ", record)

        except Error as e:
            print("Error while connecting to MySQL", e)

    def createLineItem(self, name, date):

        sql_query = '''INSERT INTO {}(name, date) VALUES(%s, %s);'''
        sql_query_formated = sql_query.format(self.table)

        self.cursor.execute(sql_query_formated,(name, date))
        self.connection.commit()
        return

    def __del__(self):
        if (self.connection is not None and self.connection.is_connected()):
            self.cursor.close()
            self.connection.close()
            print("Connection Closed")

names = ['joe','bill','tom','chad','henry','rick']
dates = ['2022-01-01','2022-02-02','2022-03-03','2022-06-06','2022-04-04','2022-05-05',]

test_table = database("test_database","test_table")
for i in range(6):
    test_table.createLineItem(names[i],dates[i])

del test_table
