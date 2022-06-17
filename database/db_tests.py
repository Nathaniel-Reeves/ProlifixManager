import unittest
import mysql

from db import Database
from db import HOST
from db import USER
from db import PASSWORD

class Test_DB(unittest.TestCase):
	maxDiff = None

	'''
	SETUP
	'''
	def setUp(self):

		self.connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
		if self.connection.is_connected():

			db_Info = self.connection.get_server_info()
			#print("Connected to MySQL Server version ", db_Info)
			self.cursor = self.connection.cursor()
		else:
			#print("Could not connect to database!")
			self.stop()


		# setup Database
		sql_query_temp = 'CREATE DATABASE store;'
		self.cursor.execute(sql_query_temp)
		self.connection.commit()

		# setup tables in Database
		sql_query_temp = 'CREATE TABLE %(database)s.%(table)s ( %(columns)s );'

		# customers
		columns = '''
				  customer_id INT AUTO_INCREMENT PRIMARY KEY,
				  first_name VARCHAR(255) NOT NULL,
				  last_name VARCHAR(255) NOT NULL,
				  age TINYINT(120),
				  is_deleted BOOL NOT NULL DEFAULT 0
				  '''
		table = {'database':'store','table':'customers','columns':columns}
		#print(sql_query_temp%table)
		self.cursor.execute(sql_query_temp%table)
		self.connection.commit()

		# products
		columns = '''
				  sku VARCHAR(255)PRIMARY KEY,
				  product_name VARCHAR(255),
				  brand_name VARCHAR(255),
				  is_deleted BOOL NOT NULL DEFAULT 0
				  '''

		table = {'database':'store','table':'products','columns':columns}
		#print(sql_query_temp%table)
		self.cursor.execute(sql_query_temp%table)
		self.connection.commit()

		# orders
		columns = '''
				  order_id INT AUTO_INCREMENT PRIMARY KEY,
				  customer_id INT,
				  sku VARCHAR(255),
				  CONSTRAINT fk_sku
				  FOREIGN KEY (sku) REFERENCES products(sku),
				  CONSTRAINT fk_customer_id
				  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
				  quantity INT,
				  is_deleted BOOL NOT NULL DEFAULT 0
				  '''

		table = {'database':'store','table':'orders','columns':columns}
		#print(sql_query_temp%table)
		self.cursor.execute(sql_query_temp%table)
		self.connection.commit()

		# setup data in tables
		sql_query_temp = 'INSERT INTO store.products(sku, product_name, brand_name) VALUES ( %s, %s, %s );'
		data = [
		('HBO34523','Toothpaste','NumberOne'),
		('NLS2q34345','Milk','MerryGold'),
		('134SBE2341','Cake','BabyBens')
		]

		self.cursor.executemany(sql_query_temp, data)
		self.connection.commit()

		sql_query_temp = 'INSERT INTO store.customers(first_name, last_name, age, is_deleted) VALUES ( %s, %s, %s, %s );'
		data = [
		('billy','tanner',22, 0),
		('paul','anderson',40, 0),
		('tom','victor',35, 0),
		('paul','joe',40, 1),
		('jimmy','bawlen',34, 0)
		]

		self.cursor.executemany(sql_query_temp, data)
		self.connection.commit()

		sql_query_temp = 'INSERT INTO store.orders(customer_id, sku, quantity, is_deleted) VALUES ( %s, %s, %s, %s );'
		data = [
		(1,'HBO34523',1,0),
		(3,'134SBE2341',2,0),
		(2,'NLS2q34345',4,1),
		(1,'NLS2q34345',1,0),
		(2,'134SBE2341',3,0),
		(3,'NLS2q34345',4,1),
		(1,'HBO34523',1,0),
		(2,'HBO34523',1,0),
		(3,'NLS2q34345',4,0),
		]

		self.cursor.executemany(sql_query_temp, data)
		self.connection.commit()

		self.cursor.close()
		self.connection.close()

	'''
	TEST CONNECTION
	'''
	@unittest.skip("Test Passes")
	def test__init__(self):
		db = Database()
		self.assertTrue(db.connection.is_connected(), "Database Connection Failed")
		return

	'''
	TEST DATABASE
	'''
	@unittest.skip("Test Passes")
	def test_getCurrentDatabase(self):
		db1 = Database()
		self.assertIsNone(db1.getCurrentDatabase())
		db2 = Database(database='store')
		self.assertNotEqual(db2.getCurrentDatabase(),'dogs')
		self.assertEqual(db2.getCurrentDatabase(),'store')

	@unittest.skip("Test Passes")
	def test_getDatabases(self):
		db = Database()
		list = db.getDatabases()
		self.assertIn('store',list)

	@unittest.skip("Test Passes")
	def test_databaseExists(self):
		db = Database()
		self.assertFalse(db.databaseExists())
		self.assertFalse(db.databaseExists('trololololo'))
		self.assertTrue(db.databaseExists('store'))

	@unittest.skip("Test Passes")
	def test_getCurrentDatabase(self):
		db1 = Database()
		self.assertIsNone(db1.getCurrentDatabase())
		db2 = Database(database='store')
		self.assertEqual(db2.getCurrentDatabase(),'store')

	@unittest.skip("Test Passes")
	def test_switchDatabase(self):
		db1 = Database()
		self.assertFalse(db1.switchDatabase())
		self.assertIsNone(db1.getCurrentDatabase())
		self.assertTrue(db1.connection.is_connected())
		self.assertTrue(db1.switchDatabase(database="store"))
		self.assertEqual(db1.getCurrentDatabase(),"store")

		db2 = Database(database="store")
		self.assertIsNotNone(db2.getCurrentDatabase())
		self.assertEqual(db2.getCurrentDatabase(),"store")
		self.assertFalse(db2.switchDatabase("Trolololo"))
		self.assertTrue(db2.switchDatabase("sys"))
		self.assertEqual(db2.getCurrentDatabase(),"sys")
		self.assertTrue(db2.switchDatabase("store"))
		self.assertEqual(db2.getCurrentDatabase(),"store")

	'''
	TEST TABLES
	'''
	@unittest.skip("Test Passes")
	def test_getCurrentTable(self):
		db1 = Database()
		self.assertIsNone(db1.getCurrentTable())

		db2 = Database(database='store', table='orders')
		self.assertNotEqual(db2.getCurrentTable(),'dogs')
		self.assertEqual(db2.getCurrentTable(),'orders')

	@unittest.skip("Test Passes")
	def test_getTables(self):
		db1 = Database()
		self.assertEqual(db1.getTables(),[])
		self.assertEqual(db1.getTables('Dogs'),[])
		self.assertEqual(db1.getTables('store'), ['customers', 'orders', 'products'])

		db2 = Database(database='store')
		self.assertEqual(db2.getTables('Dogs'),[])
		self.assertEqual(db2.getTables(), ['customers', 'orders', 'products'])

	@unittest.skip("Test Passes")
	def test_tableExists(self):
		db1 = Database(database='store', table='orders')
		self.assertTrue(db1.tableExists())
		self.assertFalse(db1.tableExists('Dogs'))
		self.assertTrue(db1.tableExists(database='store'))
		self.assertTrue(db1.tableExists(table='orders', database='store'))

		db2 = Database()
		self.assertFalse(db2.tableExists())
		self.assertFalse(db2.tableExists(table='Dogs'))
		self.assertFalse(db2.tableExists(table='Dogs',database='Cats'))
		self.assertFalse(db2.tableExists(database='store'))
		self.assertFalse(db2.tableExists(table='orders'))
		self.assertTrue(db1.tableExists(table='orders', database='store'))

	@unittest.skip("Test Passes")
	def test_switchTable(self):
		db = Database(database="store")
		self.assertFalse(db.switchTable(), "Table switched.")
		self.assertFalse(db.switchTable("no_table"), "Table switched.")
		self.assertTrue(db.switchTable("orders"), "Table did not switch.")

	'''
	TEST COLUMNS
	'''
	@unittest.skip("Test Passes")
	def test_getColumns(self):
		db1 = Database()
		self.assertIsNone(db1.getColumns())
		self.assertIsNone(db1.getColumns(database='store'))
		self.assertIsNone(db1.getColumns(table='products'))
		self.assertEqual(db1.getColumns(database='store', table='products'),['sku', 'product_name', 'brand_name', 'is_deleted'])

		db2 = Database(database='store')
		self.assertIsNone(db2.getColumns())
		self.assertIsNone(db2.getColumns(database='store'))
		self.assertEqual(db2.getColumns(table='products'),['sku', 'product_name', 'brand_name', 'is_deleted'])
		self.assertEqual(db2.getColumns(database='store', table='products'),['sku', 'product_name', 'brand_name', 'is_deleted'])

		db3 = Database(database='store',table='products')
		self.assertEqual(db3.getColumns(),['sku', 'product_name', 'brand_name', 'is_deleted'])
		self.assertEqual(db3.getColumns(database='store'),['sku', 'product_name', 'brand_name', 'is_deleted'])
		self.assertEqual(db3.getColumns(table='products'),['sku', 'product_name', 'brand_name', 'is_deleted'])
		self.assertEqual(db3.getColumns(database='store', table='products'),['sku', 'product_name', 'brand_name', 'is_deleted'])

	@unittest.skip("Test Passes")
	def test_columnExists(self):
		db1 = Database()
		self.assertFalse(db1.columnExists())
		self.assertFalse(db1.columnExists(database='store'))
		self.assertFalse(db1.columnExists(table='products'))
		self.assertFalse(db1.columnExists(database='store', table='products'))
		self.assertFalse(db1.columnExists(database='store', table='products', column='noColumn'))
		self.assertTrue(db1.columnExists(database='store', table='products', column='sku'))
		self.assertFalse(db1.columnExists(database='store', column='sku'))
		self.assertFalse(db1.columnExists(table='products', column='sku'))

	@unittest.skip("Test Passes")
	def test_getPKcolumn(self):
		db1 = Database()
		self.assertIsNone(db1.getPKcolumn())
		self.assertIsNone(db1.getPKcolumn(database='store'))
		self.assertIsNone(db1.getPKcolumn(table='products'))
		self.assertEqual(db1.getPKcolumn(database='store', table='products', all=True),{'Field': 'sku', 'Type': b'varchar(255)', 'Null': 'NO', 'Key': 'PRI', 'Default': None, 'Extra': ''})
		self.assertEqual(db1.getPKcolumn(database='store', table='products'), 'sku')

	@unittest.skip("Test Passes")
	def test_getFKcolumns(self):
		db1 = Database()
		self.assertIsNone(db1.getFKcolumns())
		self.assertIsNone(db1.getFKcolumns(database='store'))
		self.assertIsNone(db1.getFKcolumns(table='orders'))
		self.assertEqual(db1.getFKcolumns(database='store', table='orders', all=True),[{'Field': 'customer_id', 'Type': b'int', 'Null': 'YES', 'Key': 'MUL', 'Default': None, 'Extra': ''}, {'Field': 'sku', 'Type': b'varchar(255)', 'Null': 'YES', 'Key': 'MUL', 'Default': None, 'Extra': ''}])
		self.assertEqual(db1.getFKcolumns(database='store', table='orders'), ['customer_id', 'sku'])

	@unittest.skip("Test Passes")
	def test_getFKParentTable(self):
		db1 = Database()
		self.assertIsNone(db1.getFKParentTable())
		self.assertEqual(db1.getFKParentTable('sku'), {'REFERENCED_TABLE_SCHEMA': 'store', 'REFERENCED_TABLE_NAME': 'products', 'REFERENCED_COLUMN_NAME': 'sku'})
		self.assertIsNone(db1.getFKParentTable('not a column'))

	@unittest.skip("Test Passes")
	def test_getBottomRowPK(self):
		db1 = Database()
		self.assertIsNone(db1.getBottomRowPK())

		db2 = Database(database='store')
		self.assertIsNone(db2.getBottomRowPK())

		db3 = Database(table='customers')
		self.assertIsNone(db3.getBottomRowPK())

		db4 = Database(table='customers', database='store')
		self.assertEqual(db4.getBottomRowPK(),5)

	'''
	TEST ITEMS
	'''
	@unittest.skip("Test Passes")
	def test_getItem(self):
		db1 = Database()
		self.assertEqual(db1.getItem(),[])
		self.assertEqual(db1.getItem(returnDicts=True),{})

		db2 = Database(database='store')
		self.assertEqual(db2.getItem(),[])
		self.assertEqual(db2.getItem(returnDicts=True),{})

		db3 = Database(table='customers')
		self.assertEqual(db3.getItem(),[])
		self.assertEqual(db2.getItem(returnDicts=True),{})

		db4 = Database(database='store', table='customers')
		self.assertEqual(db4.getItem(),[])
		self.assertEqual(db4.getItem(returnDicts=True),{})
		self.assertEqual(db4.getItem(columns=['first_name'], returnDicts=True),{})
		self.assertEqual(db4.getItem(item_id = 1, returnDicts=True),{'customer_id':1, 'first_name':'billy', 'last_name':'tanner', 'age':22, 'is_deleted':0})
		self.assertEqual(db4.getItem(item_id = 1, columns=['first_name'], returnDicts=True),{'first_name':'billy'})
		self.assertEqual(db4.getItem(item_id = 1, columns=['first_name', 'last_name'], returnDicts=True),{'first_name':'billy', 'last_name':'tanner'})

		db5 = Database(database='store', table='orders')
		self.assertEqual(db5.getItem(item_id = 3),[])
		self.assertEqual(db5.getItem(item_id = 3, showDeleted=True, returnDicts=True),{'order_id':3, 'customer_id':2, 'sku':'NLS2q34345', 'quantity':4, 'is_deleted':1})
		self.assertEqual(db5.getItem(item_id = 1, returnDicts=True),{'order_id':1, 'customer_id':1, 'sku':'HBO34523', 'quantity':1, 'is_deleted':0})
		self.assertEqual(db5.getItem(item_id = 1, showDeleted=True, returnDicts=True),{'order_id':1, 'customer_id':1, 'sku':'HBO34523', 'quantity':1, 'is_deleted':0})

		db6 = Database(database='store', table='orders')
		self.assertEqual(db6.getItem(item_id = 3, showDeleted=True),(3, 2, 'NLS2q34345', 4, 1))
		self.assertEqual(db6.getItem(item_id = 1),(1, 1, 'HBO34523', 1, 0))
		self.assertEqual(db6.getItem(item_id = 1, showDeleted=True),(1, 1, 'HBO34523', 1, 0))

	@unittest.skip("Test Passes")
	def test_getItems(self):
		db1 = Database()
		self.assertEqual(db1.getItems(),[])
		self.assertEqual(db1.getItems(returnDicts=True),{})

		db2 = Database(database='store')
		self.assertEqual(db2.getItems(),[])
		self.assertEqual(db2.getItems(returnDicts=True),{})

		db3 = Database(table='customers')
		self.assertEqual(db3.getItems(),[])
		self.assertEqual(db2.getItems(returnDicts=True),{})

		db4 = Database(database='store', table='customers')
		self.assertEqual(db4.getItems(),[(1, 'billy', 'tanner', 22, 0),(2, 'paul', 'anderson', 40, 0),(3, 'tom', 'victor', 35, 0),(4, 'paul', 'joe', 40, 1),(5, 'jimmy', 'bawlen', 34, 0)])
		self.assertEqual(db4.getItems(returnDicts=True),[{'customer_id':1, 'first_name':'billy', 'last_name':'tanner', 'age':22, 'is_deleted':0},{'customer_id':2, 'first_name':'paul', 'last_name':'anderson', 'age':40, 'is_deleted':0},{'customer_id':3, 'first_name':'tom', 'last_name':'victor', 'age':35, 'is_deleted':0},{'customer_id':4, 'first_name':'paul', 'last_name':'joe', 'age':40, 'is_deleted':1},{'customer_id':5, 'first_name':'jimmy', 'last_name':'bawlen', 'age':34, 'is_deleted':0}])
		self.assertEqual(db4.getItems(columns=['first_name'], returnDicts=True),[{'first_name': 'billy'}, {'first_name': 'paul'}, {'first_name': 'tom'}, {'first_name': 'paul'}, {'first_name': 'jimmy'}])
		self.assertEqual(db4.getItems(returnDicts=True),[{'customer_id': 1, 'first_name': 'billy', 'last_name': 'tanner', 'age': 22, 'is_deleted': 0}, {'customer_id': 2, 'first_name': 'paul', 'last_name': 'anderson', 'age': 40, 'is_deleted': 0}, {'customer_id': 3, 'first_name': 'tom', 'last_name': 'victor', 'age': 35, 'is_deleted': 0}, {'customer_id': 4, 'first_name': 'paul', 'last_name': 'joe', 'age': 40, 'is_deleted': 1}, {'customer_id': 5, 'first_name': 'jimmy', 'last_name': 'bawlen', 'age': 34, 'is_deleted': 0}])
		self.assertEqual(db4.getItems(columns=['first_name'], returnDicts=True),[{'first_name': 'billy'}, {'first_name': 'paul'}, {'first_name': 'tom'}, {'first_name': 'paul'}, {'first_name': 'jimmy'}])
		self.assertEqual(db4.getItems(columns=['first_name', 'last_name']),[('billy', 'tanner'), ('paul', 'anderson'), ('tom', 'victor'), ('paul', 'joe'), ('jimmy', 'bawlen')])

	@unittest.skip("Test Passes")
	def test_getItemPKs(self):
		db1 = Database(database='store', table='orders')
		self.assertIsNone(db1.getItemPKs("sku = '2'"))
		self.assertEqual(db1.getItemPKs(""), [1, 2, 4, 5, 7, 8, 9])
		self.assertIsNone(db1.getItemPKs("this shouldn't make sense"))
		self.assertEqual(db1.getItemPKs("WHERE sku = 'HBO34523'"),[1, 7, 8])
		self.assertEqual(db1.getItemPKs("WHERE customer_id = '2'", showDeleted=True),[3, 5, 8])
		self.assertEqual(db1.getItemPKs("WHERE customer_id = '2'"),[5, 8])
		self.assertEqual(db1.getItemPKs("WHERE customer_id = '2' AND sku = 'HBO34523'"),[8])

	@unittest.skip("Test Passes")
	def test_getItemFKs(self):
		db1 = Database(database='store', table='orders')
		self.assertEqual(db1.getItemFKs("sku = '2'"),[])
		self.assertEqual(db1.getItemFKs(""),[])
		self.assertEqual(db1.getItemFKs("this is not a key"),[])
		self.assertEqual(db1.getItemFKs("2"),{'customer_id': 3, 'sku': '134SBE2341'})
		self.assertEqual(db1.getItemFKs("1"),{'customer_id': 1, 'sku': 'HBO34523'})
		self.assertEqual(db1.getItemFKs(3),[])
		self.assertEqual(db1.getItemFKs(3, showDeleted=True),{'customer_id': 2, 'sku': 'NLS2q34345'})

	@unittest.skip("Test Passes")
	def test_getItemsByFK(self):
		db1 = Database()
		self.assertEqual(db1.getItemsByFK(FK='1', FK_col='customer_id'),[])
		self.assertEqual(db1.getItemsByFK(FK='1', FK_col='customer_id', returnDicts=True),{})

		db2 = Database(database='store')
		self.assertEqual(db2.getItemsByFK(FK='1', FK_col='customer_id'),[])
		self.assertEqual(db1.getItemsByFK(FK='1', FK_col='customer_id', returnDicts=True),{})

		db3 = Database(table='orders')
		self.assertEqual(db3.getItemsByFK(FK='1', FK_col='customer_id'),[])
		self.assertEqual(db1.getItemsByFK(FK='1', FK_col='customer_id', returnDicts=True),{})

		db4 = Database(database='store', table='orders')
		self.assertEqual(db4.getItemsByFK(FK='2', FK_col='customer_id', showDeleted=True),[(3, 2, 'NLS2q34345', 4, 1), (5, 2, '134SBE2341', 3, 0), (8, 2, 'HBO34523', 1, 0)])
		self.assertEqual(db4.getItemsByFK(FK='2', FK_col='customer_id', returnDicts=True),[{'order_id': 5, 'customer_id': 2, 'sku': '134SBE2341', 'quantity': 3, 'is_deleted': 0}, {'order_id': 8, 'customer_id': 2, 'sku': 'HBO34523', 'quantity': 1, 'is_deleted': 0}])
		self.assertEqual(db4.getItemsByFK(FK='HBO34523', FK_col='sku', condition="AND customer_id=2"),[(8, 2, 'HBO34523', 1, 0,)])
		self.assertEqual(db4.getItemsByFK(FK='3', FK_col='customer_id', condition="AND sku='HBO34523'"),[])
		self.assertEqual(db4.getItemsByFK(FK='4', FK_col='customer_id', condition="AND sku='HBO34523'"),[])
		self.assertEqual(db4.getItemsByFK(FK='4', FK_col='customer_id', condition="AND sku='HBO34523'", showDeleted=True),[])
		self.assertEqual(db4.getItemsByFK(FK='1', FK_col='customer_id', showDeleted=True, returnDicts=True),[{'customer_id': 1,'is_deleted': 0,'order_id': 1,'quantity': 1,'sku': 'HBO34523'},{'customer_id': 1,'is_deleted': 0,'order_id': 4,'quantity': 1,'sku': 'NLS2q34345'},{'customer_id': 1,'is_deleted': 0,'order_id': 7,'quantity': 1,'sku': 'HBO34523'}])
		self.assertEqual(db4.getItemsByFK(FK='4', FK_col='not_a_column'),[])
		self.assertEqual(db4.getItemsByFK(FK='4'),[])
		self.assertEqual(db4.getItemsByFK(FK_col='customer_id'),[])

	@unittest.skip("Test Passes")
	def test_insertItem(self):
		db = Database(database='store', table='customers')
		self.assertFalse(db.insertItem())
		self.assertFalse(db.insertItem(({'first_name':'tommy'})))
		self.assertFalse(db.insertItem(({'first_name':'tommy','last_name':'tyson','age':26, 'extra_column':'not_data'})))
		self.assertTrue(db.insertItem(({'first_name':'tommy','last_name':'tyson','age':26})))
		#print(db.getLastInsertId())

	@unittest.skip("Test Passes")
	def test_insertItems(self):
		db = Database(database='store', table='products')
		self.assertFalse(db.convertDictstoTuples([]))
		self.assertFalse(db.convertDictstoTuples([{"brand": "Ford", "type": "Mustang", "date": 1964},{"brand": "Ford","year": 1964}]))
		self.assertFalse(db.convertDictstoTuples([{"brand": "Ford", "model": "Mustang", "year": 1964},{"brand": "Ford","year": 1964}]))
		self.assertFalse(db.convertDictstoTuples([{"brand": "Ford", "model": "Mustang", "year": 1964},{"brand": "Ford","year": 1964,"model": "Mustang"}]))
		self.assertTrue(db.insertItems([{'sku': 'new_product1', 'product_name': 'new_product1', 'brand_name': 'new_product1'},{'sku': 'new_product2', 'product_name': 'new_product2', 'brand_name': 'new_product2'},{'sku': 'new_product3', 'product_name': 'new_product3', 'brand_name': 'new_product3'}]))
		self.assertTrue(db.insertItems([{'sku': 'new_product4', 'product_name': 'new_product4', 'brand_name': 'new_product4'}]))

	@unittest.skip("Test Passes")
	def test_convertDictstoTuples(self):
		db = Database()
		self.assertIsNone(db.convertDictstoTuples([]))
		self.assertIsNone(db.convertDictstoTuples([{"brand": "Ford", "type": "Mustang", "date": 1964},{"brand": "Ford","year": 1964}]))
		self.assertIsNone(db.convertDictstoTuples([{"brand": "Ford", "model": "Mustang", "year": 1964},{"brand": "Ford","year": 1964}]))
		self.assertIsNone(db.convertDictstoTuples([{"brand": "Ford", "model": "Mustang", "year": 1964},{"brand": "Ford","year": 1964,"model": "Mustang"}]))
		self.assertEqual(db.convertDictstoTuples([{"brand": "Ford", "model": "Mustang", "year": 1964},{"brand": "chevy", "model": "catelack", "year": 1970}]),(('brand', 'model', 'year'), [("Ford", "Mustang", 1964),("chevy", "catelack", 1970)]))
		self.assertEqual(db.convertDictstoTuples([{"brand": "Ford", "model": "Mustang", "year": 1964}]),(('brand', 'model', 'year'), [("Ford", "Mustang", 1964)]))

	@unittest.skip("Test Passes")
	def test_updateItem(self):
		db1 = Database()
		self.assertFalse(db1.updateItem(3, {'last_name':'george'}))
		self.assertFalse(db1.updateItem(1, {'first_name':'billy', 'age':2}))
		self.assertFalse(db1.updateItem(2, {}))
		self.assertFalse(db1.updateItem(9, {'last_name':'george','age':46}))

		db2 = Database(database='store', table='customers')
		self.assertTrue(db2.updateItem(3, {'last_name':'george'}))
		self.assertTrue(db2.updateItem(1, {'first_name':'billy', 'age':2}))
		self.assertFalse(db2.updateItem(2, {}))
		self.assertFalse(db2.updateItem(50, {'last_name':'george','age':46}))

	@unittest.skip("Test Passes")
	def test_updateItems(self):
		db1 = Database()
		self.assertFalse(db1.updateItems(condition="WHERE age > '34'", dict={'last_name':'george'}))
		self.assertFalse(db1.updateItems(condition="WHERE age > '34'", dict={'first_name':'billy', 'age':2}))
		self.assertFalse(db1.updateItems(condition="WHERE age > '34'", dict={}))
		self.assertFalse(db1.updateItems(condition="This doesn't make sense", dict={'last_name':'george','age':46}))

		db2 = Database(database='store', table='customers')
		self.assertTrue(db2.updateItems(condition="WHERE age > '34'", dict={'last_name':'george'}))
		self.assertTrue(db2.updateItems(condition="WHERE age > '34'", dict={'first_name':'billy', 'age':2}))
		self.assertFalse(db2.updateItems(condition="WHERE age > '34'", dict={}))
		self.assertFalse(db2.updateItems(condition="This doesn't make sense", dict={'last_name':'george','age':46}))

	@unittest.skip("Test Passes")
	def test_deleteItem(self):
		db1 = Database()
		self.assertFalse(db1.deleteItem(3))
		self.assertFalse(db1.deleteItem(50))

		db2 = Database(database='store', table='customers')
		self.assertTrue(db2.deleteItem(1))
		self.assertFalse(db2.deleteItem(50))

	@unittest.skip("Test Passes")
	def test_deleteItems(self):
		db1 = Database()
		self.assertFalse(db1.deleteItems("WHERE age > '34'"))
		self.assertFalse(db1.deleteItems("This doesn't make sense"))

		db2 = Database(database='store', table='customers')
		self.assertTrue(db2.deleteItems("WHERE age > '34'"))
		self.assertFalse(db2.deleteItems("This doesn't make sense"))

	'''
	CUSTOM
	'''
	@unittest.skip("Test Passes")
	def test_customChangeQuery(self):
		db = Database()
		self.assertTrue(db.customChangeQuery("UPDATE store.orders SET quantity = quantity + 2 WHERE order_id = '7';"))
		self.assertFalse(db.customChangeQuery("UPDATE store.orders SET (INVALID QUERY) quantity = quantity + 2 WHERE order_id = '7';"))

	@unittest.skip("Test Passes")
	def test_customSelectQuery(self):
		db = Database()
		self.assertEqual(db.customSelectQuery("SELECT first_name, last_name FROM store.customers WHERE last_name LIKE 'p%';"),[])
		self.assertEqual(db.customSelectQuery("SELECT first_name, last_name FROM store.customers WHERE first_name LIKE 'p%';"),[{'first_name':'paul','last_name':'anderson'},{'first_name':'paul','last_name':'joe'}])
		self.assertIsNone(db.customSelectQuery("SELECT first_name, last_name FROM store.customers (INVALID QUERY) WHERE last_name = 'p%';"))

	'''
	ACTUAL USE TEST CASES
	'''
	@unittest.skip("Test Passes")
	def test_useCase1(self):
		# Prolouge (Database Functions)
		# Initialize Connection
		db_i = Database()
		self.assertIsNone(db_i.getCurrentDatabase())
		self.assertFalse(db_i.switchDatabase('Fake_database'))
		self.assertTrue(db_i.switchDatabase('store'))
		self.assertTrue(db_i.getCurrentDatabase(),'store')
		del db_i

	#@unittest.skip("TODO:")
	def test_useCase2(self):
		# PART ONE (Uncommitted Changes)
		# Initialize Connection to not auto commit
		db_1a = Database(database='store', autoCommit=False)
		# Test first set of Get Queries
		self.assertEqual(db_1a.getItem(),[])
		self.assertFalse(db_1a.switchTable('Fake_table'))
		self.assertEqual(db_1a.getItem(item_id=1),[])
		self.assertTrue(db_1a.switchTable('customers'))
		self.assertEqual(db_1a.getItem(item_id=1, columns=['first_name', 'last_name']),('billy', 'tanner'))
		self.assertEqual(db_1a.getItemPKs(),[1, 2, 3, 5])
		self.assertEqual(db_1a.getItemFKs(id=3),[])
		self.assertEqual(db_1a.getItems(),[(1, 'billy', 'tanner', 22, 0), (2, 'paul', 'anderson', 40, 0), (3, 'tom', 'victor', 35, 0), (4, 'paul', 'joe', 40, 1), (5, 'jimmy', 'bawlen', 34, 0)])
		self.assertEqual(db_1a.getRowCount(),5)
		self.assertTrue(db_1a.switchTable('products'))
		self.assertEqual(db_1a.getItem(item_id='NLS2q34345', columns=['product_name', 'brand_name']),('Milk', 'MerryGold'))
		self.assertEqual(db_1a.getItemPKs(),['134SBE2341', 'HBO34523', 'NLS2q34345'])
		self.assertEqual(db_1a.getItemFKs(id='NLS2q34345'),[])
		self.assertTrue(db_1a.switchTable('orders'))
		self.assertEqual(db_1a.getItem(item_id=1, columns=['customer_id']),(1,))
		self.assertEqual(db_1a.getItemPKs(condition='ORDER BY order_id', showDeleted=True),[1, 2, 3, 4, 5, 6, 7, 8, 9])
		self.assertEqual(db_1a.getItemFKs(id=2, showDeleted=True),{'customer_id': 3, 'sku': '134SBE2341'})
		self.assertEqual(db_1a.getRowCount(),1)
		self.assertEqual(db_1a.getItemsByFK(FK=2,FK_col='customer_id', columns=['sku','customer_id'],showDeleted=True, returnDicts=True),[{'sku': 'NLS2q34345', 'customer_id': 2}, {'sku': '134SBE2341', 'customer_id': 2}, {'sku': 'HBO34523', 'customer_id': 2}])
		self.assertEqual(db_1a.getItemsByFK(FK=2,FK_col='customer_id',columns=['sku','customer_id'], showDeleted=True),[('NLS2q34345', 2), ('134SBE2341', 2), ('HBO34523', 2)])
		# Test Insert Queries
		self.assertTrue(db_1a.switchTable('customers'))
		self.assertFalse(db_1a.insertItem({}))
		self.assertFalse(db_1a.insertItem({'first_name':'kevin','NOT_A_COLUMN':'fake data'}))
		self.assertIsNone(db_1a.getLastInsertId())
		self.assertTrue(db_1a.insertItem({'age':52,'first_name':'kevin','last_name':'bernard'}))
		self.assertEqual(db_1a.getLastInsertId(),6)
		# Test Update Queries
		# Test Delete Queries
		# Test second set of Get Queries
		self.assertTrue(db_1a.switchTable('customers'))
		self.assertEqual(db_1a.getItem(item_id=1, columns=['first_name', 'last_name']),('billy', 'tanner'))
		self.assertEqual(db_1a.getItemPKs(),[1, 2, 3, 5, 6])
		self.assertEqual(db_1a.getItemFKs(id=3),[])
		self.assertEqual(db_1a.getItems(),[(1, 'billy', 'tanner', 22, 0), (2, 'paul', 'anderson', 40, 0), (3, 'tom', 'victor', 35, 0), (4, 'paul', 'joe', 40, 1), (5, 'jimmy', 'bawlen', 34, 0), (6, 'kevin', 'bernard', 52, 0)])
		self.assertTrue(db_1a.switchTable('products'))
		self.assertEqual(db_1a.getItem(item_id='NLS2q34345', columns=['product_name', 'brand_name']),('Milk', 'MerryGold'))
		self.assertEqual(db_1a.getItemPKs(),['134SBE2341', 'HBO34523', 'NLS2q34345'])
		self.assertEqual(db_1a.getItemFKs(id='NLS2q34345'),[])
		self.assertTrue(db_1a.switchTable('orders'))
		self.assertEqual(db_1a.getItem(item_id=1, columns=['customer_id']),(1,))
		self.assertEqual(db_1a.getItemPKs(condition='ORDER BY order_id', showDeleted=True),[1, 2, 3, 4, 5, 6, 7, 8, 9])
		self.assertEqual(db_1a.getItemFKs(id=2, showDeleted=True),{'customer_id': 3, 'sku': '134SBE2341'})
		self.assertEqual(db_1a.getItemsByFK(FK=2, FK_col='customer_id', columns=['sku','customer_id'], showDeleted=True, returnDicts=True),[{'sku': 'NLS2q34345', 'customer_id': 2}, {'sku': '134SBE2341', 'customer_id': 2}, {'sku': 'HBO34523', 'customer_id': 2}])
		self.assertEqual(db_1a.getItemsByFK(FK=2, FK_col='customer_id', columns=['sku','customer_id'], showDeleted=True),[('NLS2q34345', 2), ('134SBE2341', 2), ('HBO34523', 2)])
		db_1a.rollback()
		# Test Insert Queries
		# Close Connection
		del db_1a
		# Test changes were not commited
		db_1b = Database(database='store')
		self.assertEqual(db_1b.getItem(),[])
		self.assertFalse(db_1b.switchTable('Fake_table'))
		self.assertEqual(db_1b.getItem(item_id=1),[])
		self.assertTrue(db_1b.switchTable('customers'))
		self.assertEqual(db_1b.getItem(item_id=1, columns=['first_name', 'last_name']),('billy', 'tanner'))
		self.assertEqual(db_1b.getItemPKs(),[1, 2, 3, 5])
		self.assertEqual(db_1b.getItemFKs(id=3),[])
		self.assertEqual(db_1b.getItems(),[(1, 'billy', 'tanner', 22, 0), (2, 'paul', 'anderson', 40, 0), (3, 'tom', 'victor', 35, 0), (4, 'paul', 'joe', 40, 1), (5, 'jimmy', 'bawlen', 34, 0)])
		self.assertTrue(db_1b.switchTable('products'))
		self.assertEqual(db_1b.getItem(item_id='NLS2q34345', columns=['product_name', 'brand_name']),('Milk', 'MerryGold'))
		self.assertEqual(db_1b.getItemPKs(),['134SBE2341', 'HBO34523', 'NLS2q34345'])
		self.assertEqual(db_1b.getItemFKs(id='NLS2q34345'),[])
		self.assertTrue(db_1b.switchTable('orders'))
		self.assertEqual(db_1b.getItem(item_id=1, columns=['customer_id']),(1,))
		self.assertEqual(db_1b.getItemPKs(condition='ORDER BY order_id', showDeleted=True),[1, 2, 3, 4, 5, 6, 7, 8, 9])
		self.assertEqual(db_1b.getItemFKs(id=2, showDeleted=True),{'customer_id': 3, 'sku': '134SBE2341'})
		self.assertEqual(db_1b.getItemsByFK(FK=2,FK_col='customer_id', columns=['sku','customer_id'],showDeleted=True, returnDicts=True),[{'sku': 'NLS2q34345', 'customer_id': 2}, {'sku': '134SBE2341', 'customer_id': 2}, {'sku': 'HBO34523', 'customer_id': 2}])
		self.assertEqual(db_1b.getItemsByFK(FK=2,FK_col='customer_id',columns=['sku','customer_id'], showDeleted=True),[('NLS2q34345', 2), ('134SBE2341', 2), ('HBO34523', 2)])

	@unittest.skip("Test Not Ready")
	def test_useCase3(self):
		# PART TWO (Auto-Commited Changes)
		# Initialize Connection to auto commit
		db_2a = Database(database='store')
		# Test first set of Get Queries
		self.assertEqual(db_2a.getItem(),[])
		self.assertFalse(db_2a.switchTable('Fake_table'))
		self.assertEqual(db_2a.getItem(item_id=1),[])
		self.assertTrue(db_2a.switchTable('customers'))
		self.assertEqual(db_2a.getItem(item_id=1, columns=['first_name', 'last_name']),('billy', 'tanner'))
		self.assertEqual(db_2a.getItemPKs(),[1, 2, 3, 5])
		self.assertEqual(db_2a.getItemFKs(id=3),[])
		self.assertEqual(db_2a.getItems(),[(1, 'billy', 'tanner', 22, 0), (2, 'paul', 'anderson', 40, 0), (3, 'tom', 'victor', 35, 0), (4, 'paul', 'joe', 40, 1), (5, 'jimmy', 'bawlen', 34, 0)])
		self.assertTrue(db_2a.switchTable('products'))
		self.assertEqual(db_2a.getItem(item_id='NLS2q34345', columns=['product_name', 'brand_name']),('Milk', 'MerryGold'))
		self.assertEqual(db_2a.getItemPKs(),['134SBE2341', 'HBO34523', 'NLS2q34345'])
		self.assertEqual(db_2a.getItemFKs(id='NLS2q34345'),[])
		self.assertTrue(db_2a.switchTable('orders'))
		self.assertEqual(db_2a.getItem(item_id=1, columns=['customer_id']),(1,))
		self.assertEqual(db_2a.getItemPKs(condition='ORDER BY order_id', showDeleted=True),[1, 2, 3, 4, 5, 6, 7, 8, 9])
		self.assertEqual(db_2a.getItemFKs(id=2, showDeleted=True),{'customer_id': 3, 'sku': '134SBE2341'})
		self.assertEqual(db_2a.getItemsByFK(FK=2,FK_col='customer_id', columns=['sku','customer_id'],showDeleted=True, returnDicts=True),[{'sku': 'NLS2q34345', 'customer_id': 2}, {'sku': '134SBE2341', 'customer_id': 2}, {'sku': 'HBO34523', 'customer_id': 2}])
		self.assertEqual(db_2a.getItemsByFK(FK=2,FK_col='customer_id',columns=['sku','customer_id'], showDeleted=True),[('NLS2q34345', 2), ('134SBE2341', 2), ('HBO34523', 2)])
		# Test Insert Queries
		# Test Update Queries
		# Test Delete Queries
		# Test second set of Get Queries
		self.assertTrue(db_2a.switchTable('customers'))
		self.assertEqual(db_2a.getItem(item_id=1, columns=['first_name', 'last_name']),('billy', 'tanner'))
		self.assertEqual(db_2a.getItemPKs(),[1, 2, 3, 5])
		self.assertEqual(db_2a.getItemFKs(id=3),[])
		self.assertEqual(db_2a.getItems(),[(1, 'billy', 'tanner', 22, 0), (2, 'paul', 'anderson', 40, 0), (3, 'tom', 'victor', 35, 0), (4, 'paul', 'joe', 40, 1), (5, 'jimmy', 'bawlen', 34, 0)])
		self.assertTrue(db_2a.switchTable('products'))
		self.assertEqual(db_2a.getItem(item_id='NLS2q34345', columns=['product_name', 'brand_name']),('Milk', 'MerryGold'))
		self.assertEqual(db_2a.getItemPKs(),['134SBE2341', 'HBO34523', 'NLS2q34345'])
		self.assertEqual(db_2a.getItemFKs(id='NLS2q34345'),[])
		self.assertTrue(db_2a.switchTable('orders'))
		self.assertEqual(db_2a.getItem(item_id=1, columns=['customer_id']),(1,))
		self.assertEqual(db_2a.getItemPKs(condition='ORDER BY order_id', showDeleted=True),[1, 2, 3, 4, 5, 6, 7, 8, 9])
		self.assertEqual(db_2a.getItemFKs(id=2, showDeleted=True),{'customer_id': 3, 'sku': '134SBE2341'})
		self.assertEqual(db_2a.getItemsByFK(FK=2,FK_col='customer_id', columns=['sku','customer_id'],showDeleted=True, returnDicts=True),[{'sku': 'NLS2q34345', 'customer_id': 2}, {'sku': '134SBE2341', 'customer_id': 2}, {'sku': 'HBO34523', 'customer_id': 2}])
		self.assertEqual(db_2a.getItemsByFK(FK=2,FK_col='customer_id',columns=['sku','customer_id'], showDeleted=True),[('NLS2q34345', 2), ('134SBE2341', 2), ('HBO34523', 2)])
		# Close Connection
		del db_2a
		# Test changes were commited
		db_2b = Database(database='store')
		self.assertEqual(db_2b.getItem(),[])
		self.assertFalse(db_2b.switchTable('Fake_table'))
		self.assertEqual(db_2b.getItem(item_id=1),[])
		self.assertTrue(db_2b.switchTable('customers'))
		self.assertEqual(db_2b.getItem(item_id=1, columns=['first_name', 'last_name']),('billy', 'tanner'))
		self.assertEqual(db_2b.getItemPKs(),[1, 2, 3, 5])
		self.assertEqual(db_2b.getItemFKs(id=3),[])
		self.assertEqual(db_2b.getItems(),[(1, 'billy', 'tanner', 22, 0), (2, 'paul', 'anderson', 40, 0), (3, 'tom', 'victor', 35, 0), (4, 'paul', 'joe', 40, 1), (5, 'jimmy', 'bawlen', 34, 0)])
		self.assertTrue(db_2b.switchTable('products'))
		self.assertEqual(db_2b.getItem(item_id='NLS2q34345', columns=['product_name', 'brand_name']),('Milk', 'MerryGold'))
		self.assertEqual(db_2b.getItemPKs(),['134SBE2341', 'HBO34523', 'NLS2q34345'])
		self.assertEqual(db_2b.getItemFKs(id='NLS2q34345'),[])
		self.assertTrue(db_2b.switchTable('orders'))
		self.assertEqual(db_2b.getItem(item_id=1, columns=['customer_id']),(1,))
		self.assertEqual(db_2b.getItemPKs(condition='ORDER BY order_id', showDeleted=True),[1, 2, 3, 4, 5, 6, 7, 8, 9])
		self.assertEqual(db_2b.getItemFKs(id=2, showDeleted=True),{'customer_id': 3, 'sku': '134SBE2341'})
		self.assertEqual(db_2b.getItemsByFK(FK=2,FK_col='customer_id', columns=['sku','customer_id'],showDeleted=True, returnDicts=True),[{'sku': 'NLS2q34345', 'customer_id': 2}, {'sku': '134SBE2341', 'customer_id': 2}, {'sku': 'HBO34523', 'customer_id': 2}])
		self.assertEqual(db_2b.getItemsByFK(FK=2,FK_col='customer_id',columns=['sku','customer_id'], showDeleted=True),[('NLS2q34345', 2), ('134SBE2341', 2), ('HBO34523', 2)])

	@unittest.skip("Test Not Ready")
	def test_useCase4(self):
		# PART THREE (Changes Maunally Commited)
		# Initialize Connection to not auto commit
		# Create a New User
		# Add New Items in Store
		# Place Order
		pass

	'''
	TEAR DOWN
	'''
	def tearDown(self):

		self.connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
		if self.connection.is_connected():
			db_Info = self.connection.get_server_info()
			#print("Connected to MySQL Server version ", db_Info)
			self.cursor = self.connection.cursor()

		#print("Deleting Test Database")
		# delete Database
		sql_query_temp = 'DROP DATABASE store;'
		self.cursor.execute(sql_query_temp)

		# close connections
		self.cursor.close()
		self.connection.close()

if __name__ == '__main__':
	unittest.main(failfast=True)
