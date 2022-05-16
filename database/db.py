import mysql.connector
from mysql.connector import Error

#print(cursor.statement)
# SAFE EXAMPLES. DO THIS!
#cursor.execute("SELECT admin FROM users WHERE username = %s'", (username, ));
#cursor.execute("SELECT admin FROM users WHERE username = %(username)s", {'username': username});
HOST = 'localHost'
USER = 'client'
PASSWORD = 'clientPassword5!'


class Database:

    '''
    database(database, table)
    arg:
        host (req) = hostname/ip address of mysql server
        user (req) = username of connection account
        password (req) = password of connection account
        database (opt) = name of database to connect to
        table (opt) = name of table to connect to
    Initializes a connection to a database.
    '''
    def __init__(self, host=HOST, user=USER, password=PASSWORD, database=None, table=None):
        self._host = host
        self._user = user
        self._password = password

        self.connection = None
        self.cursor = None
        self.database = database
        self.table = table

        try:
            self.connection = mysql.connector.connect(host=self._host, user=self._user, password=self._password)
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.cursor = self.connection.cursor()

                if self.database is not None:
                    self.switchDatabase(self.database)

                record = self.cursor.fetchone()
                print("You're connected to database: ", record[0])
                return

        except Error as e:
            print("Error while connecting to MySQL", e)
            return

    '''
    obj.switchDatabase(database_name)
    arg:
        database_name (req) = name of database to switch to
    returns:
        None
    '''
    def switchDatabase(self, database=None, host=None, user=None, password=None):
        if database is None:
            return False
        if not self.databaseExists(database):
            return False
        if host is None:
            host = self.host
        if user is None:
            user = self.user
        if password is None:
            password = self.password
        try:
            self.connection = mysql.connector.connect(host=self._host, user=self._user, password=self._password)
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                #print("Connected to MySQL Server version ", db_Info)
                self.cursor = self.connection.cursor()
                record = self.cursor.fetchone()
                #print("You're connected to database: ", record[0])
                self.database = database
                return True
            else:
                return False
        except Error as e:
            #print("Error while connecting to MySQL", e)
            return False

    '''
    obj.getCurrentDatabase()
    returns:
        current Database's name
    '''
    def getCurrentDatabase(self):
        return self.database

    '''
    obj.getDatabases()
    returns:
        a list of all Databases in the server
    '''
    def getDatabases(self):
        sql_query = "SHOW DATABASES;"
        self.cursor.execute(sql_query)
        databases = self.cursor.fetchall()
        return databases[0]

    '''
    obj.databaseExists(table_name):
    arg:
        database_name (opt)
    returns:
        boolian
    '''
    def databaseExists(self, test=None):
        if test is None:
            test = self.database
        if test is None:
            return False
        if test not in self.getDatabases():
            return False
        return True

    '''
    obj.switchTable(table_name)
    arg:
        table_name (req) = name of table to switch to
    returns:
        None
    '''
    def switchTable(self, table=None):
        if table is None:
            return False
        if self.tableExists(table):
            self.table = table
            return True
        return False

    '''
    obj.getCurrentTable()
    returns:
        current table's name
    '''
    def getCurrentTable(self):
        return self.table

    '''
    obj.getTables()
    returns:
        a list of all tables in the database
    '''
    def getTables(self, database=None):
        if database is None:
            database = self.database
        sql_query = "SHOW %(database)s.tables;"
        if self.databaseExists(database):
            self.cursor.execute(sql_query, {'database':database})
            tables = self.cursor.fetchall()
            return tables[0]
        return None

    '''
    obj.tableExists(table_name):
    arg:
        table_name (opt)
    returns:
        boolian
    '''
    def tableExists(self, test=None):
        if not self.databaseExists():
            return False
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
            sql_query_temp = "SHOW COLUMNS FROM {}.{};"
            sql_query = sql_query_temp.format(self.database, table)
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

    '''
    Obj.columnExists(database, table, column)
    arg:
        database (Opt) = database name
        table (Opt) = table name
        column (Req) = column name
    returns:
        bool
    '''
    # TODO:
    def columntExists(self, database=None, table=None, column=None):
        pass

    '''
    Obj.insertItem(data)
    arg:
        Data = Dictionary of columns and data
    return:
        boolians
    '''
    def insertItem(self, data):

        if data is None:
            print("No Data")
            return False

        # Generate SQL Query
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql_query_temp = "INSERT INTO %s.%s ( %s ) VALUES ( %s )" % (self.database, self.table, columns, placeholders)

        try:
            self.cursor.execute(sql_query_temp, list(data.values()))
            self.connection.commit()
            print("Query Successful")
            return True
        except Error as err:
            print(f"Error: '{err}'")
            return False

    '''
    Obj.insertManyItems(columns, data)
    arg:
        columns (req) = Tuple of each column data is going into
        data (req) = list of tuples containing
                     data for each column
    return:
        boolians
    '''
    def insertItems(self, columns, data):

        # Generate SQL Query
        placeholders = ', '.join(['%s'] * (len(columns)))
        columns = ', '.join(columns)

        sql_query_temp = "INSERT INTO %(db)s.%(table)s ( %(col)s ) VALUES ( %(p)s );"
        temp_dict = {'db':self.database,'table':self.table, 'col':columns, 'p':placeholders}
        sql_query = sql_query_temp % temp_dict
        print(sql_query)
        # Execute Query

        try:
            self.cursor.executemany(sql_query, data)
            #print(self.cursor.statement)
            self.connection.commit()
            #print("Query successful")
            return True
        except Error as err:
            #print(f"Error: '{err}'")
            return False

    '''
    Obj.updateItem()

    '''
    # TODO:
    def updateItem(self):
        pass

    def updateItems(self):
        pass

    def getItem(self):
        pass

    '''
    Obj.getItems(table, query, columns)
    arg:
        table (Opt) = default is object.table, pass in a different
                      table from the database.
        query (Req) = a mysql query string.
        columns (Opt) = specific columns for the query string.
    return:
        requested Items, None if failed
    '''
    def getItems(self, table=None, sql_query='', columns='*'):

        # Check and get table_name if any
        if table is None:
            table = self.table

        if not(self.tableExists(table)):
            print(self.table + " doesn't exist in " + self.database)
            return None

        data = None
        sql_query_temp = "SELECT %(columns)s FROM %(db)s.%(table)s %(query)s;"
        temp_dict = {'db':self.database,'table':self.table, 'col':columns, 'query':sql_query}
        sql_query = sql_query_temp % temp_dict
        # Return data
        try:
            self.cursor.execute(sql_query)
            data = self.cursor.fetchall()
            print("Query Successful")
            return data
        except Error as err:
            print(f"Error: '{err}'")
            return None

    def getItemPK(self):
        pass

    def getItemFK(self):
        pass

    def deleteItem(self):
        pass

    def deleteItems(self):
        pass

    def customChangeQuery(self):
        pass

    def customInsertQuery(self):
        pass

    '''
    del Operator Over-ride
    close connections to database
    '''
    def __del__(self):
        if (self.connection is not None and self.connection.is_connected()):
            self.cursor.close()
            self.connection.close()
            #print("Connection Closed")
