import unittest
import mysql

from db import Database
from db import HOST
from db import USER
from db import PASSWORD

class Test_DB(unittest.TestCase):

    '''
    SETUP
    '''
    def setUp(self):

        self.connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
        if self.connection.is_connected():

            db_Info = self.connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            self.cursor = self.connection.cursor()
        else:
            print("Could not connect to database!")
            self.stop()


        # setup Database
        sql_query_temp = 'CREATE DATABASE store;'
        self.cursor.execute(sql_query_temp)
        print(self.cursor.statement)
        self.connection.commit()

        # setup tables in Database
        sql_query_temp = 'CREATE TABLE %(database)s.%(table)s ( %(columns)s );'

        # customers
        columns = '''customer_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        age TINYINT(120),
        '''
        table = {'database':'store','table':'customers','columns':columns}
        self.cursor.executemany(sql_query_temp, table)
        self.connection.commit()

        # products
        columns = '''sku INT PRIMARY KEY VARCHAR(255),
        product_name VARCHAR(255),
        brand_name VARCHAR(255),
        '''
        table = {'database':'store','table':'products','columns':columns}
        self.cursor.executemany(sql_query_temp, table)
        self.connection.commit()

        # orders
        columns = '''order_id INT AUTO_INCREMENT PRIMARY KEY,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (sku) REFERENCES orders(sku),
        quantity INT(1000000000),
        '''
        table = {'database':'store','table':'orders','columns':columns}
        self.cursor.executemany(sql_query_temp, table)
        self.connection.commit()

        # setup data in tables
        #self.cursor.execute(sql_query_temp, data)
        #self.connection.commit()

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
    @unittest.skip("Test Not Ready")
    def test_switchDatabase(self):
        pass

    @unittest.skip("Test Not Ready")
    def test_getCurrentDatabase(self):
        pass

    @unittest.skip("Test Not Ready")
    def test_getDatabases(self):
        pass

    @unittest.skip("Test Not Ready")
    def test_databaseExists(self):
        pass

    '''
    TEST TABLES
    '''
    @unittest.skip("Test Not Ready")
    def test_switchTable(self):
        db = Database("test_database")
        self.assertFalse(db.switchTable(), "Table switched.")
        self.assertFalse(db.switchTable("no_table"), "Table switched.")
        self.assertTrue(db.switchTable("test_table"), "Table did not switch.")

    @unittest.skip("Test Not Ready")
    def test_getCurrentTable(self):
        pass

    @unittest.skip("Test Not Ready")
    def test_getTables(self):
        pass

    @unittest.skip("Test Not Ready")
    def test_tableExists(self):
        pass

    '''
    TEST COLUMNS
    '''
    @unittest.skip("Test Not Ready")
    def test_getColumns(self):
        pass

    @unittest.skip("Test Not Ready")
    def test_columnExists(self):
        pass

    '''
    TEST ITEMS
    '''
    @unittest.skip("Test Not Ready")
    def test_insertItem(self):
        pass

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
    def test_getItem(self):
        pass

    @unittest.skip("Test Not Ready")
    def test_getItems(self):
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


        print("Deleting Test Database")
        try:
            self.connection = mysql.connector.connect(host=self._host, user=self._user, password=self._password)
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.cursor = self.connection.cursor()

                record = self.cursor.fetchone()
                print("You're connected to database: ", record[0])

        except Error as e:
            print("Error while connecting to MySQL", e)
            self.stop()
            return

        # delete Database
        sql_query_temp = 'DROP DATABASE %s;'
        self.cursor.execute(sql_query_temp, 'store')
        self.connection.commit()

        # close connections
        self.cursor.close()
        self.connection.close()

if __name__ == '__main__':
    unittest.main(failfast=True)
