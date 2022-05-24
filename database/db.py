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
        self.table = table
        self.database = database

        try:
            self.connection = mysql.connector.connect(host=self._host, user=self._user, password=self._password)
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                #print("Connected to MySQL Server version ", db_Info)
                self.cursor = self.connection.cursor()

                #print("Check Database: ", self.databaseExists(database))
                if not self.databaseExists():
                    self.database = None
                #print("Check Table: ", self.tableExists(table))
                if not self.tableExists():
                    self.table = None

                record = self.cursor.fetchone()
                #print("You're connected to database: ", record[0])
                return

        except Error as e:
            #print("Error while connecting to MySQL", e)
            return

# ------------------------------------------------------------------------------
# ------------------------ Database Functions ----------------------------------
# ------------------------------------------------------------------------------

    '''
    obj.switchDatabase(database_name)
    arg:
        database_name (req) = name of database to switch to
    returns:
        None
    '''
    def switchDatabase(self, database=None):
        if database is None and self.database is not None:
            database = self.database
        if self.databaseExists(database):
            self.database = database
            return True
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
        database_tuples = self.cursor.fetchall()
        databases = []
        for d in database_tuples:
            databases.append(d[0])
        return databases

    '''
    obj.databaseExists(table_name):
    arg:
        database_name (opt)
    returns:
        boolian
    '''
    def databaseExists(self, database=None):
        if database is None and self.database is not None:
            database = self.database

        if database in self.getDatabases():
            return True
        return False

# ------------------------------------------------------------------------------
# ------------------------ Table Functions -------------------------------------
# ------------------------------------------------------------------------------

    '''
    obj.switchTable(table_name)
    arg:
        table_name (req) = name of table to switch to
    returns:
        None
    '''
    def switchTable(self, table=None, database=None):
        if database is None and self.database is not None:
            database = self.database
        else:
            if not self.databaseExists(database):
                return False

        if table is None and self.table is None:
            return False
        else:
            if self.tableExists(table=table, database=database):
                self.table = table
                return True

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
        if database is None and self.database is not None:
            database = self.database
        else:
            if not self.databaseExists(database):
                return []

        sql_query = "SHOW TABLES FROM %(database)s;"

        self.cursor.execute(sql_query % {'database':database})
        tables_tuples = self.cursor.fetchall()
        tables = []
        for t in tables_tuples:
            tables.append(t[0])
        #print("tables: ", tables)
        return tables

    '''
    obj.tableExists(table_name):
    arg:
        table_name (opt)
    returns:
        boolian
    '''
    def tableExists(self, table=None, database=None):
        if database is None and self.database is not None:
            database = self.database
        else:
            if not self.databaseExists(database):
                return False
        if table is None and self.table is not None:
            table = self.table
        else:
            if table is None:
                return False

        if table not in self.getTables(database=database):
            return False
        return True

# ------------------------------------------------------------------------------
# ------------------------ Column Functions ------------------------------------
# ------------------------------------------------------------------------------

    '''
    obj.getColumns(table_name, all)
    arg:
        table_name (opt) = name of a table in the database (str)
        all (opt) = true to get all information for each column (bool)
    returns:
        default -> column field names in a list or None if table_name
                   doesn't exist
        all = True -> all column information in a list of dict
    '''
    def getColumns(self, table=None, database=None, all=False):
        # check the database
        if database is None and self.database is not None:
            database = self.database
        else:
            if not self.databaseExists(database):
                return None

        # check the table
        if table is None and self.table is not None:
            table = self.table
        else:
            if not self.tableExists(database=database, table=table):
                return None

        # get column data
        sql_query_temp = "SHOW COLUMNS FROM %(database)s.%(table)s;"
        temp_dict = {'database':database, 'table':table}
        sql_query = sql_query_temp % temp_dict
        self.cursor.execute(sql_query)
        columns = self.cursor.fetchall()
        field_names = [i[0] for i in self.cursor.description]
        data = []
        for i in range(len(columns)):
            data.append(self._tupletodic(columns[i], field_names))

        # return all column info
        if all is True:
            return data

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
        bool -> true if exists, false if not
    '''
    def columnExists(self, database=None, table=None, column=None):
        if column is None:
            return False
        columns = self.getColumns(database=database, table=table)
        if not columns:
            return False
        if column not in columns:
            return False
        return True

    '''
    Obj.getPKcolumn(table, database, all)
    arg:
        table (opt) = name of the working table (string)
        database (opt) = name of the working database (string)
        all (opt) = boolian option to get all column information
    returns:
        default -> string of the name of the primary key
        all=True -> dictionary of all primary key column info
    '''
    def getPKcolumn(self, table=None, database=None, all=False):
        columns = self.getColumns(table, database, True)
        if not columns:
            return None
        PK_col = {}
        for i in range(len(columns)):
            if 'PRI' in columns[i]['Key']:
                PK_col = columns[i]
                break
        if all is True:
            return PK_col
        else:
            return PK_col['Field']

    '''
    Obj.getFKcolumns(table, database, all)
    arg:
        table (opt) = name of working table (str)
        database (opt) = name of working database (str)
        all (opt) = boolian option to get all column information
    returns:
        default -> list of strings for each FK column header
        all=True -> list of dict for each FK column containing detailed info
    '''
    def getFKcolumns(self, table=None, database=None, all=False):
        columns = self.getColumns(table, database, True)
        if not columns:
            return None
        FK_col = []
        FK_col_Fields = []
        for i in range(len(columns)):
            if 'MUL' in columns[i]['Key']:
                FK_col.append(columns[i])
                FK_col_Fields.append(columns[i]['Field'])
        if not FK_col:
            return None
        if all is True:
            return FK_col
        else:
            return FK_col_Fields

    '''
    Obj.getFKParentTable(column)
    arg:
        column (req) = string of the FK column name
    returns:
        dict containing the FK reference info for the selected column
    '''
    def getFKParentTable(self, column=''):
        if not column:
            return None
        # get column data
        sql_query_temp = "SELECT REFERENCED_TABLE_SCHEMA, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE COLUMN_NAME = '%(column)s' AND CONSTRAINT_NAME LIKE 'fk_%%';"
        temp_dict = {'column':column}
        sql_query = sql_query_temp % temp_dict
        self.cursor.execute(sql_query)
        columns = self.cursor.fetchone()
        if not columns:
            return None
        field_names = [i[0] for i in self.cursor.description]
        data = self._tupletodic(columns, field_names)
        return data

# ------------------------------------------------------------------------------
# ------------------------ Items Functions -------------------------------------
# ------------------------------------------------------------------------------

    '''
    Obj.insertItem(data)
    arg:
        Data = Dictionary of columns and data
    return:
        boolians
    '''
    def insertItem(self, data={}):

        if self.database is None or self.table is None:
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
        #print(sql_query)
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

    '''
    Obj.getItem(item_id, columns)
    arg:
        item_id (req) = the id of the item in a string, int, or float
        columns (opt) = a list of column headers of data you specifically want
    returns:
        - a dictionary of each value paired with the column header as a key
        - an empy dictionary
    '''
    def getItem(self, item_id=None, columns=["*"]):
        if item_id is None:
            return {}
        # check database and table
        if self.database is None or self.table is None:
            return {}

        table_columns = self.getColumns(database=self.database, table=self.table)
        # check columns

        custom_col = False
        if columns == ["*"]:
            col_string = '*'
        else:
            custom_col = True
            col_string = ""
            for col in columns:
                if col not in table_columns:
                    return {}
                col_string += col + ", "
            col_string = col_string[:-2] + " "


        condition = table_columns[0] + " = " + str(item_id)
        sql_query_temp = "SELECT %(columns)s FROM %(database)s.%(table)s WHERE %(condition)s;"
        inputs = {'columns':col_string, 'database':self.database, 'table':self.table, 'condition':condition}


        sql_query = sql_query_temp % inputs
        data = {}

        try:
            self.cursor.execute(sql_query)
            data = self.cursor.fetchone()
            #print("Query Successful")
            if custom_col:
                return self._tupletodic(data, columns)
            else:
                return self._tupletodic(data, table_columns)
        except Error as err:
            print(f"Error: '{err}'")
            return {}

    '''
    Obj._tubletodic(data, keys)
    arg:
        data (req) = list containing data
        keys (req) = list conaining keys
    returns
        dictionary
    '''
    def _tupletodic(self, data, keys):
        dic = {}
        if len(data) == len(keys):
            for i in range(len(keys)):
                dic[keys[i]] = data[i]
        return dic

    '''
    Obj.getItemsByFK(FK, FK_col, condition, showDeleted)
    arg:
        FK (req) = string of the forign key to search by
        FK_col (req) = string of the column name of the forign key to search by
        condition (opt) = string of additional conditions to select items by
        showDeleted (opt) = boolian, gather deleted items as well as current
                            items default is to leave out deleted items
    return:
        requested Items in dict of dicts, empty dict if query failed
    '''
    def getItemsByFK(self, FK="", FK_col="", condition="", showDeleted=False):
        # check database and table
        if self.database is None or self.table is None:
            return {}

        # get table columns
        table_columns = self.getColumns(database=self.database, table=self.table)

        sql_query_temp = "SELECT * FROM %(database)s.%(table)s WHERE %(FK_col)s='%(FK)s'"
        inputs = {'database':self.database, 'table':self.table, 'FK_col':FK_col, 'FK':FK}

        if condition:
            sql_query_temp += " AND %(condition)s"
            inputs['condition'] = condition

        if not showDeleted:
            sql_query_temp += " AND is_deleted=0"

        sql_query_temp += ";"

        sql_query = sql_query_temp % inputs
        data = {}

        try:
            self.cursor.execute(sql_query)
            data = self.cursor.fetchall()
            #print("Query Successful")
        except Error as err:
            #print(f"Error: '{err}'")
            return {}

        table = {}
        for i in data:
            row = self._tupletodic(i, table_columns)
            table[row[table_columns[0]]] = row
        return table

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
