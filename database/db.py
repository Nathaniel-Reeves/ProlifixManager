import mysql.connector
from mysql.connector import Error
import logging

#print(cursor.statement)
# SAFE EXAMPLES. DO THIS!
#cursor.execute("SELECT admin FROM users WHERE username = %s'", (username, ));
#cursor.execute("SELECT admin FROM users WHERE username = %(username)s", {'username': username});
HOST = 'localHost'
USER = 'client'
PASSWORD = 'clientPassword5!'

logging.basicConfig(filename='logs/database_logs.log', level=logging.ERROR, format='%(asctime)s |$| %(levelname)s |$| File:%(filename)s |$| Line:%(lineno)d |$| %(message)s')

# logging.debug('debug message')
# logging.info('info message')
# logging.warning('warn message')
# logging.error('error message')
# logging.critical('critical message')

class Database:

# ------------------------------------------------------------------------------
# ------------------------ Server Functions ------------------------------------
# ------------------------------------------------------------------------------

	'''Database(database, table)
	arg:
		host (req) = hostname/ip address of mysql server
		user (req) = username of connection account
		password (req) = password of connection account
		database (opt) = name of database to connect to
		table (opt) = name of table to connect to
	Initializes a connection to a database.
	'''
	def __init__(self, host=HOST, user=USER, password=PASSWORD, database=None, table=None, autoCommit=True):
		self._host = host
		self._user = user
		self._password = password

		self.connection = None
		self.cursor = None
		self.table = table
		self.database = database

		self.autoCommit = autoCommit

		try:
			self.connection = mysql.connector.connect(host=self._host, user=self._user, password=self._password)
			if self.connection.is_connected():
				db_Info = self.connection.get_server_info()
				logging.info("Connected to MySQL Server version "+db_Info)
				self.cursor = self.connection.cursor()

				logging.info("Check Database: "+ str(self.databaseExists(database)))
				if not self.databaseExists():
					self.database = None
				logging.info("Check Table: "+ str(self.tableExists(table)))
				if not self.tableExists():
					self.table = None
				return

		except Error as e:
			logging.critical("Error while connecting to MySQL Server")
			return

	def getRowCount(self):
		return self.cursor.rowcount

	def commit(self):
		self.connection.commit()

	def rollback(self):
		self.connection.rollback()

	'''del Operator Over-ride
	close connections to database,
	if auto commit is on, the del
	function will commit before
	closing the connection, otherwise
	it will rollback to the last commit.
	'''
	def __del__(self):
		if (self.connection is not None and self.connection.is_connected()):
			if self.autoCommit:
				logging.info("Actions Commited")
				self.connection.commit()
			else:
				self.connection.rollback()
				logging.warning("Actions Rollback")
			self.cursor.close()
			self.connection.close()
			logging.info("Connection Closed")

# ------------------------------------------------------------------------------
# ------------------------ Database Functions ----------------------------------
# ------------------------------------------------------------------------------

	'''Obj.switchDatabase(database_name)
	arg:
		database_name (req) = name of database to switch to
	returns:
		Bool
	'''
	def switchDatabase(self, database=None):
		if database is None and self.database is not None:
			database = self.database
		if self.databaseExists(database):
			self.database = database
			logging.info("Working Database Switched to: "+database)
			return True
		logging.warning("Working Database was not switched")
		return False

	'''Obj.getCurrentDatabase()
	returns:
		current Database's name
	'''
	def getCurrentDatabase(self):
		return self.database

	'''Obj.getDatabases()
	returns:
		a list of all Databases in the server
	'''
	def getDatabases(self):
		sql_query = "SHOW DATABASES;"
		try:
			self.cursor.execute(sql_query)
			logging.info("Query Executed - "+self.cursor.statement)
			database_tuples = self.cursor.fetchall()
		except Error as err:
			logging.error(f"Error: '{err}'")
			return None
		else:
			databases = []
			for d in database_tuples:
				databases.append(d[0])
			return databases

	'''Obj.databaseExists(table_name):
	arg:
		database_name (opt)
	returns:
		boolian
	'''
	def databaseExists(self, database=None):
		if database is None and self.database is not None:
			database = self.database

		if database in self.getDatabases():
			logging.info(f"Database Exists {self.database}")
			return True
		logging.warning("Database Doesn't Exist")
		return False

# ------------------------------------------------------------------------------
# ------------------------ Table Functions -------------------------------------
# ------------------------------------------------------------------------------

	'''Obj.switchTable(table_name)
	arg:
		table_name (req) = name of table to switch to
	returns:
		None
	'''
	def switchTable(self, table=None, database=None):
		if database is None and self.database is not None:
			database = self.database

		if not self.databaseExists(database):
			logging.warning("Working Table was not Switched")
			return False


		if table is None and self.table is None:
			logging.warning("Working Table was not Switched")
			return False
		else:
			if self.tableExists(table=table, database=database):
				self.table = table
				logging.info("Working Table Switched to: "+table)
				return True

	'''Obj.getCurrentTable()
	returns:
		current table's name
	'''
	def getCurrentTable(self):
		return self.table

	'''Obj.getTables()
	returns:
		a list of all tables in the database
	'''
	def getTables(self, database=None):
		if database is None and self.database is not None:
			database = self.database
		else:
			if not self.databaseExists(database):
				logging.warning("Database Doesn't Exist")
				return []

		sql_query = "SHOW TABLES FROM %(database)s;"

		try:
			self.cursor.execute(sql_query % {'database':database})
			tables_tuples = self.cursor.fetchall()
			logging.info("Query Executed - "+self.cursor.statement)
		except Error as err:
			logging.error(f"Error: '{err}'")
			return None
		else:
			tables = []
			for t in tables_tuples:
				tables.append(t[0])
			#print("tables: ", tables)
			return tables

	'''Obj.tableExists(table_name):
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
				logging.warning("Table doesn't Exist")
				return False

		if table not in self.getTables(database=database):
			logging.warning("Table doesn't Exist")
			return False
		logging.info(f"Table Exists - {self.database}.{table}")
		return True

# ------------------------------------------------------------------------------
# ------------------------ Column Functions ------------------------------------
# ------------------------------------------------------------------------------

	'''Obj.getColumns(table_name, all)
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

		# generate query
		sql_query_temp = "SHOW COLUMNS FROM %(database)s.%(table)s;"
		temp_dict = {'database':database, 'table':table}
		sql_query = sql_query_temp % temp_dict

		try:
			self.cursor.execute(sql_query)
			logging.info("Query Executed - "+self.cursor.statement)
			columns = self.cursor.fetchall()
		except Error as err:
			print(f"Error: '{err}'")
			return None
		else:
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

	'''Obj.columnExists(database, table, column)
	arg:
		database (Opt) = database name
		table (Opt) = table name
		column (Req) = column name
	returns:
		bool -> true if exists, false if not
	'''
	def columnExists(self, database=None, table=None, column=None):
		if column is None:
			logging.warning("No Column was Inputted/Selected")
			return False
		columns = self.getColumns(database=database, table=table)
		if not columns:
			logging.warning("Get Columns Returned Empty")
			return False
		if column not in columns:
			logging.warning("Column Doesn't Exist")
			return False
		logging.info(f"Column Exists - {self.database}.{self.table} col = {column}")
		return True

	'''Obj.getPKcolumn(table, database, all)
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

	'''Obj.getFKcolumns(table, database, all)
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

	'''Obj.getFKParentTable(column)
	arg:
		column (req) = string of the FK column name
	returns:
		dict containing the FK reference info for the selected column
	'''
	def getFKParentTable(self, column=''):
		if not column:
			return None

		# generate query
		sql_query_temp = "SELECT REFERENCED_TABLE_SCHEMA, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE COLUMN_NAME = '%(column)s' AND CONSTRAINT_NAME LIKE 'fk_%%';"
		temp_dict = {'column':column}
		sql_query = sql_query_temp % temp_dict

		try:
			self.cursor.execute(sql_query)
			logging.info("Query Executed - "+self.cursor.statement)
			columns = self.cursor.fetchone()
		except Error as err:
			logging.error(f"Error: '{err}'")
			return None
		else:
			if not columns:
				return None
			field_names = [i[0] for i in self.cursor.description]
			data = self._tupletodic(columns, field_names)
			return data

	'''Obj.getBottomRowPK()
	arg:
		None
	returns:
		the primary key of the last row in the working table in the
		working database.
	'''
	def getBottomRowPK(self):
		PK_col = self.getPKcolumn()
		sql_query_temp = "SELECT %(col)s FROM %(database)s.%(table)s ORDER BY %(col)s DESC LIMIT 1;"
		inputs = {'database':self.database, 'table':self.table, 'col':PK_col}
		sql_query = sql_query_temp % inputs

		try:
			self.cursor.execute(sql_query)
			logging.info("Query Executed - "+self.cursor.statement)
			data = self.cursor.fetchone()
		except Error as err:
			logging.error(f"Error: '{err}'")
			return None
		else:
			return data[0]


# ------------------------------------------------------------------------------
# ------------------------ Items Functions -------------------------------------
# ------------------------------------------------------------------------------

	'''Obj.insertItem(data)
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
			logging.info("Query Executed - "+self.cursor.statement)
			self.connection.commit()
		except Error as err:
			logging.error(f"Error: '{err}'")
			return False
		else:
			return True

	'''Obj.convertDicttoTuples(data):
	arg:
		data (req) = list of dicts, keys are column headers.  All dicts must
					 contain the same headers in the same order.
	returns:
		correct case -> a tuple of a tuple and list of tuples.  The first
						tuple contains the columns in order, the list contains
						the data in tuples.
						i.e.((column, column),[(data, data), (data, data)])

	Note:
		this function is a child/helper function to Obj.insertItems()
	'''
	def convertDictstoTuples(self, data=None):
		if len(data) <= 0:
			return None
		if data is None:
			return None

		columns = tuple(data[0])
		tupleData = []
		for i in range(len(data)):
			# check columns against the first set
			if columns == tuple(data[i]):
				tupleData.append(tuple(data[i].values()))
			else:
				return None

		return (columns, tupleData)

	'''Obj.insertManyItems(columns, data)
	arg:
		data (req) = list containing dicts with key values as columns.
	return:
		boolians -> true if the data was entered, false if not
	'''
	def insertItems(self, data=[]):
		if self.database is None or self.table is None:
			return False

		output = self.convertDictstoTuples(data)
		if not output:
			return False

		# Generate SQL Query
		placeholders = ', '.join(['%s'] * len(output[0]))
		columns = ', '.join(output[0])
		sql_query_temp = "INSERT INTO %(db)s.%(table)s ( %(col)s ) VALUES (%(p)s);"

		temp_dict = {'db':self.database,'table':self.table, 'col':columns, 'p':placeholders}
		sql_query = sql_query_temp % temp_dict

		# Execute Query
		try:
			self.cursor.executemany(sql_query, output[1])
			logging.info("Query Executed - "+self.cursor.statement)
			self.connection.commit()
		except Error as err:
			logging.error(f"Error: '{err}'")
			return False
		else:
			return True

	'''Obj.getItem(item_id, columns)
	arg:
		item_id (req) = the id of the item in a string, int, or float
		columns (opt) = a list of column headers of data you specifically want
	returns:
		- a dictionary of each value paired with the column header as a key
		- an empy dictionary
	'''
	def getItem(self, item_id=None, columns=["*"], showDeleted=False):
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
		if not showDeleted:
			condition += " AND is_deleted=0"
		sql_query_temp = "SELECT %(columns)s FROM %(database)s.%(table)s WHERE %(condition)s;"
		inputs = {'columns':col_string, 'database':self.database, 'table':self.table, 'condition':condition}


		sql_query = sql_query_temp % inputs
		data = {}

		try:
			self.cursor.execute(sql_query)
			logging.info("Query Executed - "+self.cursor.statement)
			data = self.cursor.fetchone()
		except Error as err:
			logging.error(f"Error: '{err}'")
			return {}
		else:
			if not data:
				return None
			if custom_col:
				return self._tupletodic(data, columns)
			else:
				return self._tupletodic(data, table_columns)

	'''Obj._tubletodic(data, keys)
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

	'''Obj.getItemsByFK(FK, FK_col, condition, showDeleted)
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

		# generate query
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
			logging.info("Query Executed - "+self.cursor.statement)
			data = self.cursor.fetchall()
		except Error as err:
			logging.error(f"Error: '{err}'")
			return {}
		else:
			table = {}
			for i in data:
				row = self._tupletodic(i, table_columns)
				table[row[table_columns[0]]] = row
			return table

	'''Obj.getLastInsertId()
	arg: None
	Returns:
		the last id/PK of a record that was inserted recently.
	'''
	def getLastInsertId(self):
		# Generate SQL Query
		sql_query = "SELECT LAST_INSERT_ID();"

		# Execute Query
		try:
			self.cursor.execute(sql_query)
			logging.info("Query Executed - "+self.cursor.statement)
			id = self.cursor.fetchone()
		except Error as err:
			logging.error(f"Error: '{err}'")
			return None
		else:
			return id

	'''Obj.getItemIds(condition)
	arg:
		condition (req) = a query string to sort out items in a db
	returns:
		a list containing keys that match the specific conditions,
		if no conditions match or no database and or table is
		selected/invalid, returns None
	'''
	def getItemPKs(self, condition, showDeleted=False):
		# check database and table
		if self.database is None or self.table is None:
			return None

		PK_col = self.getPKcolumn(self.table, self.database)
		if not PK_col:
			return None

		if not showDeleted:
			condition += " AND is_deleted=0"

		# generate query
		sql_query_temp = "SELECT %(columns)s FROM %(database)s.%(table)s WHERE %(condition)s;"
		inputs = {'columns':PK_col, 'database':self.database, 'table':self.table, 'condition':condition}
		sql_query = sql_query_temp % inputs

		# Execute Query
		try:
			self.cursor.execute(sql_query)
			logging.info("Query Executed - "+self.cursor.statement)
			ids = self.cursor.fetchall()
		except Error as err:
			logging.error(f"Error: '{err}'")
			return None
		else:
			if not ids:
				return None
			return_list = []
			for id in ids:
				return_list.append(id[0])
			return return_list

	'''Obj.getItemFks(id)
	arg:
		id (req) = the PK/id of a record
		showDeleted (opt) = sorts out deleted records
	returns:
		a dict with the keys being the FK column headers
	'''
	def getItemFKs(self, id='', showDeleted=False):
		# check database and table
		if self.database is None or self.table is None:
			return None

		# get FK column headers
		FK_cols = self.getFKcolumns(table=self.table, database=self.database)
		if not FK_cols:
			return None
		columns = ', '.join(FK_cols)

		# create conditional statement
		PK_col = self.getPKcolumn(table=self.table, database=self.database)
		condition_temp = PK_col + " = '%s'"
		condition = condition_temp % str(id)

		if not showDeleted:
			condition += " AND is_deleted=0"

		# Generate Query
		sql_query_temp = "SELECT %(columns)s FROM %(database)s.%(table)s WHERE %(condition)s;"
		inputs = {'columns':columns, 'database':self.database, 'table':self.table, 'condition':condition}
		sql_query = sql_query_temp % inputs

		# Execute Query
		try:
			self.cursor.execute(sql_query)
			logging.info("Query Executed - "+self.cursor.statement)
			ids = self.cursor.fetchall()
		except Error as err:
			logging.error(f"Error: '{err}'")
			return None
		else:
			if not ids:
				return None
			return self._tupletodic(ids[0], FK_cols)

	'''Obj.deleteItem(id)
	arg:
		id (req) = id to be deleted
	returns:
		bool
	Note: this is a soft delete.
	'''
	def deleteItem(self, id):
		return self.updateItem(id, {'is_deleted':'1'})

	'''Obj.deleteItems(condition)
	arg:
		condition (req) = sql condition to delete a group of items
	returns:
		bool
	Note: this is a soft delete
	'''
	def deleteItems(self, condition):
		return self.updateItems(condition, {'is_deleted':'1'})

	'''Obj.updateItem(item_id, dict)
	arg:
		item_id (req) = the id of the item to be updated
		dict (req) = a dictionary containing column headers as keys and the
					 the values is the data to be updated
	returns:
		bool
	'''
	def updateItem(self, item_id, dict):
		if item_id is None:
			return False

		# check database and table
		if self.database is None or self.table is None:
			return False

		table_columns = self.getColumns(database=self.database, table=self.table)

		# Test if the Id exists
		sql_query_temp = "SELECT EXISTS(SELECT * from %(database)s.%(table)s WHERE %(column)s=%(id)s);"
		inputs = {'database':self.database, 'table':self.table, 'column':table_columns[0], 'id': item_id}
		sql_query = sql_query_temp % inputs
		try:
			self.cursor.execute(sql_query)
			logging.info("Query Executed - "+self.cursor.statement)
			id_exists = self.cursor.fetchone()
		except Error as err:
			logging.error(f"Error: '{err}'")
			return False
		else:
			if id_exists[0] == 0:
				return False

			# check columns
			update_columns = tuple(dict.keys())
			data_temp = "%s = '%s', "
			data = ''
			for col in update_columns:
				if col not in table_columns:
					return False
				data += data_temp % (col, dict[col])

			data = data[:-2]

			condition = table_columns[0] + " = " + str(item_id)
			sql_query_temp = "UPDATE %(database)s.%(table)s SET %(data)s WHERE %(condition)s;"
			inputs = {'database':self.database, 'table':self.table, 'condition':condition, 'data': data}
			sql_query = sql_query_temp % inputs

			try:
				self.cursor.execute(sql_query)
				logging.info("Query Executed - "+self.cursor.statement)
				data = self.cursor.fetchone()
			except Error as err:
				logging.error(f"Error: '{err}'")
				return False
			else:
				return True

	'''Obj.updateItems(condition, dict)
	arg:
		condition (req) = the condition to select which items are updated.
		dict (req) = a dictionary containing column headers as keys and the
					 the values is the data to be updated
	returns:
		bool
	'''
	def updateItems(self, condition, dict):
		if not condition:
			return False

		# check database and table
		if self.database is None or self.table is None:
			return False

		table_columns = self.getColumns(database=self.database, table=self.table)

		# check columns
		update_columns = tuple(dict.keys())
		data_temp = "%s = '%s', "
		data = ''
		for col in update_columns:
			if col not in table_columns:
				return False
			data += data_temp % (col, dict[col])

		data = data[:-2]

		sql_query_temp = "UPDATE %(database)s.%(table)s SET %(data)s WHERE %(condition)s;"
		inputs = {'database':self.database, 'table':self.table, 'condition':condition, 'data': data}
		sql_query = sql_query_temp % inputs

		try:
			self.cursor.execute(sql_query)
			logging.info("Query Executed - "+self.cursor.statement)
			data = self.cursor.fetchone()
		except Error as err:
			logging.error(f"Error: '{err}'")
			return False
		else:
			return True

	'''Obj.customChangeQuery(sql_query)
	arg:
		sql_query (req) = a sql query string that will be executed
	returns:
		bool, True of completed, False otherwise
	'''
	def customChangeQuery(self, sql_query):
		try:
			self.cursor.execute(sql_query)
			logging.info("Query Executed - "+self.cursor.statement)
		except Error as err:
			logging.error(f"Error: '{err}'")
			return False
		else:
			return True

	'''Obj.customSelectQuery(sql_query)
	arg:
		sql_query (req) = a sql query string that will be executed
	returns:
		selected data in a list of dicts with the column headers
		as the key values. None otherwise
	'''
	def customSelectQuery(self, sql_query):
		try:
			self.cursor.execute(sql_query)
			logging.info("Query Executed - "+self.cursor.statement)
			data = self.cursor.fetchall()
			columns = self.cursor.column_names
		except Error as err:
			logging.error(f"Error: '{err}'")
			return None
		else:
			output = []
			if data is None:
				return None
			if data == []:
				return []
			for row in data:
				output.append(dict(zip(columns, row)))
			return output
