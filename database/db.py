import mysql.connector
from mysql.connector import Error

class database:

    '''
    database(database, table)
    arg:
    database (req) = name of database to connect to
    table (optional) = name of table to connect to
    Initializes a connection to a database.
    '''
    def __init__(self, database, table=None):
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

    '''
    obj.switchTable(table_name)
    arg:
    table_name (req) = name of table to switch to
    '''
    def switchTable(self, table):
        self.table = table

    '''
    obj.getCurrentTable()
    returns current table's name
    '''
    def getCurrentTable(self):
        return self.table

    '''
    obj.getTables()
    returns a list of all tables in the database
    '''
    def getTables(self):
        sql_query = "SHOW tables;"
        self.cursor.execute(sql_query)
        tables = self.cursor.fetchall()
        return tables[0]

    '''
    obj.tableExists(table_name):
    arg:
    table_name (opt)
    returns:
        boolian
    '''
    def tableExists(self, test=None):
        if test is None:
            test = self.table
        if test is None:
            return False
        if test not in self.getTables():
            return False
        return True

    '''
    obj.getColumns(table_name, options)
    arg:
    table_name (opt) = name of a table in the database
    options (opt)
     -a, -all = return all column info in a list of tuples
    returns (default):
        column feild names in a list or None if table_name
        doesn't exist
    '''
    def getColumns(self, *pram):
        # valid option list
        options = ['a','all']
        # check and get table_name if any
        if len(pram) == 0:
            table = self.table
        else:
            if pram[0] in options:
                table = self.table
            else:
                table = pram[0]
        # get column data
        if self.tableExists(table):
            sql_query_temp = "SHOW COLUMNS FROM {};"
            sql_query = sql_query_temp.format(table)
            self.cursor.execute(sql_query)
            columns = self.cursor.fetchall()
        else:
            return None
        # return all column info
        if len(pram) >= 1:
            if "all" in pram or "a" in pram:
                return columns
        # return column field info only
        fields = []
        for column in columns:
            fields.append(column[0])
        return fields


    def getAllItems(self):
        sql_query = '''SELECT * FROM {}'''
        sql_query_formatted = sql_query.format(self.table)

        self.cursor.execute(sql_query_formatted)

    def insertItem(self, name, date):

        sql_query = '''INSERT INTO {}(name, date) VALUES(%s, %s);'''
        sql_query_formated = sql_query.format(self.table)

        self.cursor.execute(sql_query_formated,(name, date))
        self.connection.commit()
        return

    '''
    del Operator Over-ride
    close connections to database
    '''
    def __del__(self):
        if (self.connection is not None and self.connection.is_connected()):
            self.cursor.close()
            self.connection.close()
            print("Connection Closed")

names = ['joe','bill','tom','chad','henry','rick']
dates = ['2022-01-01','2022-02-02','2022-03-03','2022-06-06','2022-04-04','2022-05-05',]

new_db = database("test_database")
print(new_db.getColumns("test_table"))
print(new_db.getColumns("test_table","all"))
del new_db
