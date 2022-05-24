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
                  first_name VARCHAR(255),
                  last_name VARCHAR(255),
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

        sql_query_temp = 'INSERT INTO store.customers(first_name, last_name, age) VALUES ( %s, %s, %s );'
        data = [
        ('billy','tanner',22),
        ('paul','anderson',40),
        ('tom','victor',35),
        ('jimmy','bawlen',34)
        ]

        self.cursor.executemany(sql_query_temp, data)
        self.connection.commit()

        sql_query_temp = 'INSERT INTO store.orders(customer_id, sku, quantity) VALUES ( %s, %s, %s );'
        data = [
        (1,'HBO34523',1),
        (3,'134SBE2341',2),
        (2,'NLS2q34345',4),
        (1,'NLS2q34345',1),
        (2,'134SBE2341',3),
        (3,'NLS2q34345',4),
        (1,'HBO34523',1),
        (2,'HBO34523',1),
        (3,'NLS2q34345',4),
        ]

        self.cursor.executemany(sql_query_temp, data)
        self.connection.commit()

        self.cursor.close()
        self.connection.close()

    '''
    TEST CONNECTION
    '''

    def test__init__(self):
        db = Database()
        self.assertTrue(db.connection.is_connected(), "Database Connection Failed")
        return

    '''
    TEST DATABASE
    '''
    #@unittest.skip("Test Not Ready")
    def test_getCurrentDatabase(self):
        db1 = Database()
        self.assertIsNone(db1.getCurrentDatabase())
        db2 = Database(database='store')
        self.assertNotEqual(db2.getCurrentDatabase(),'dogs')
        self.assertEqual(db2.getCurrentDatabase(),'store')

    #@unittest.skip("Test Not Ready")
    def test_getDatabases(self):
        db = Database()
        self.assertEqual(db.getDatabases(),['information_schema','mysql','performance_schema','store','sys'])

    #@unittest.skip("Test Not Ready")
    def test_databaseExists(self):
        db = Database()
        self.assertFalse(db.databaseExists())
        self.assertFalse(db.databaseExists('trololololo'))
        self.assertTrue(db.databaseExists('store'))

    #@unittest.skip("Test Not Ready")
    def test_getCurrentDatabase(self):
        db1 = Database()
        self.assertIsNone(db1.getCurrentDatabase())
        db2 = Database(database='store')
        self.assertEqual(db2.getCurrentDatabase(),'store')

    #@unittest.skip("Test Not Ready")
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

    #@unittest.skip("Test Not Ready")
    def test_getCurrentTable(self):
        #print('test_getCurrentTable')
        db1 = Database()
        self.assertIsNone(db1.getCurrentTable())

        db2 = Database(database='store', table='orders')
        self.assertNotEqual(db2.getCurrentTable(),'dogs')
        self.assertEqual(db2.getCurrentTable(),'orders')

    #@unittest.skip("Test Not Ready")
    def test_getTables(self):
        db1 = Database()
        self.assertEqual(db1.getTables(),[])
        self.assertEqual(db1.getTables('Dogs'),[])
        self.assertEqual(db1.getTables('store'), ['customers', 'orders', 'products'])

        db2 = Database(database='store')
        self.assertEqual(db2.getTables('Dogs'),[])
        self.assertEqual(db2.getTables(), ['customers', 'orders', 'products'])

    #@unittest.skip("Test Not Ready")
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

    #@unittest.skip("Test Not Ready")
    def test_switchTable(self):
        db = Database(database="store")
        self.assertFalse(db.switchTable(), "Table switched.")
        self.assertFalse(db.switchTable(table="no_table"), "Table switched.")
        self.assertTrue(db.switchTable(table="orders"), "Table did not switch.")

    '''
    TEST COLUMNS
    '''
    #@unittest.skip("Test Not Ready")
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

    #@unittest.skip("Test Not Ready")
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

    #@unittest.skip("Test Not Ready")
    def test_getPKcolumn(self):
        db1 = Database()
        self.assertIsNone(db1.getPKcolumn())
        self.assertIsNone(db1.getPKcolumn(database='store'))
        self.assertIsNone(db1.getPKcolumn(table='products'))
        self.assertEqual(db1.getPKcolumn(database='store', table='products', all=True),{'Field': 'sku', 'Type': b'varchar(255)', 'Null': 'NO', 'Key': 'PRI', 'Default': None, 'Extra': ''})
        self.assertEqual(db1.getPKcolumn(database='store', table='products'), 'sku')

    #@unittest.skip("Test Not Ready")
    def test_getFKcolumns(self):
        db1 = Database()
        self.assertIsNone(db1.getFKcolumns())
        self.assertIsNone(db1.getFKcolumns(database='store'))
        self.assertIsNone(db1.getFKcolumns(table='orders'))
        self.assertEqual(db1.getFKcolumns(database='store', table='orders', all=True),[{'Field': 'customer_id', 'Type': b'int', 'Null': 'YES', 'Key': 'MUL', 'Default': None, 'Extra': ''}, {'Field': 'sku', 'Type': b'varchar(255)', 'Null': 'YES', 'Key': 'MUL', 'Default': None, 'Extra': ''}])
        self.assertEqual(db1.getFKcolumns(database='store', table='orders'), ['customer_id', 'sku'])

    #@unittest.skip("Test Not Ready")
    def test_getFKParentTable(self):
        db1 = Database()
        self.assertIsNone(db1.getFKParentTable())
        self.assertEqual(db1.getFKParentTable('sku'), {'REFERENCED_TABLE_SCHEMA': 'store', 'REFERENCED_TABLE_NAME': 'products', 'REFERENCED_COLUMN_NAME': 'sku'})
        self.assertIsNone(db1.getFKParentTable('not a column'))

    '''
    TEST ITEMS
    '''

    #@unittest.skip("Test Not Ready")
    def test_getItem(self):
        db1 = Database()
        self.assertEqual(db1.getItem(),{})

        db2 = Database(database='store')
        self.assertEqual(db2.getItem(),{})

        db3 = Database(table='customers')
        self.assertEqual(db3.getItem(),{})

        db4 = Database(database='store', table='customers')
        self.assertEqual(db4.getItem(),{})
        self.assertEqual(db4.getItem(columns=['first_name']),{})
        self.assertEqual(db4.getItem(item_id = 1),{'customer_id':1, 'first_name':'billy', 'last_name':'tanner', 'age':22, 'is_deleted':0})
        self.assertEqual(db4.getItem(item_id = 1, columns=['first_name']),{'first_name':'billy'})
        self.assertEqual(db4.getItem(item_id = 1, columns=['first_name', 'last_name']),{'first_name':'billy', 'last_name':'tanner'})

    #@unittest.skip("Test Not Ready")
    def test_getItemsByFK(self):
        db1 = Database()
        self.assertEqual(db1.getItemsByFK(FK='1', FK_col='customer_id'),{})

        db2 = Database(database='store')
        self.assertEqual(db2.getItemsByFK(FK='1', FK_col='customer_id'),{})

        db3 = Database(table='orders')
        self.assertEqual(db3.getItemsByFK(FK='1', FK_col='customer_id'),{})

        db4 = Database(database='store', table='orders')
        self.assertEqual(db4.getItemsByFK(FK='2', FK_col='customer_id'),{3: {'order_id': 3, 'customer_id': 2, 'sku': 'NLS2q34345', 'quantity': 4, 'is_deleted': 0}, 5: {'order_id': 5, 'customer_id': 2, 'sku': '134SBE2341', 'quantity': 3, 'is_deleted': 0}, 8: {'order_id': 8, 'customer_id': 2, 'sku': 'HBO34523', 'quantity': 1, 'is_deleted': 0}})
        self.assertEqual(db4.getItemsByFK(FK='HBO34523', FK_col='sku', condition="customer_id=2"),{8: {'order_id': 8, 'customer_id': 2, 'sku': 'HBO34523', 'quantity': 1, 'is_deleted': 0}})
        self.assertEqual(db4.getItemsByFK(FK='3', FK_col='customer_id', condition="sku='HBO34523'"),{})
        self.assertEqual(db4.getItemsByFK(FK='4', FK_col='customer_id', condition="sku='HBO34523'"),{})
        self.assertEqual(db4.getItemsByFK(FK='4', FK_col='customer_id', condition="sku='HBO34523'", showDeleted=True),{})
        self.assertEqual(db4.getItemsByFK(FK='1', FK_col='customer_id', showDeleted=True),{1: {'customer_id': 1,'is_deleted': 0,'order_id': 1,'quantity': 1,'sku': 'HBO34523'},4: {'customer_id': 1,'is_deleted': 0,'order_id': 4,'quantity': 1,'sku': 'NLS2q34345'},7: {'customer_id': 1,'is_deleted': 0,'order_id': 7,'quantity': 1,'sku': 'HBO34523'}})
        self.assertEqual(db4.getItemsByFK(FK='4', FK_col='not_a_column'),{})
        self.assertEqual(db4.getItemsByFK(FK='4'),{})
        self.assertEqual(db4.getItemsByFK(FK_col='customer_id'),{})

    @unittest.skip("Test Not Ready")
    def test_insertItem(self):
        db = Database(database='store', table='customers')
        self.assertTrue(db.insertItem(({'first_name':'tommy','last_name':'tyson','age':26})))

    @unittest.skip("Test Not Ready")
    def test_insertItems(self):
        pass

    @unittest.skip("Test Not Ready")
    def test_updateItem(self):
        pass

    @unittest.skip("Test Not Ready")
    def test_updateItems(self):
        pass

    @unittest.skip("Test Not Ready")
    def getItemPK(self):
        pass

    @unittest.skip("Test Not Ready")
    def getItemFK(self):
        pass

    @unittest.skip("Test Not Ready")
    def deleteItem(self):
        pass

    @unittest.skip("Test Not Ready")
    def deleteItems(self):
        pass

    '''
    CUSTOM
    '''
    @unittest.skip("Test Not Ready")
    def customChangeQuery(self):
        pass

    @unittest.skip("Test Not Ready")
    def customInsertQuery(self):
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
    unittest.main()
