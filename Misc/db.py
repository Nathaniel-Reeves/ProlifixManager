"""
Database Config Settings
"""
import mysqlx
from .db_conf import Config

# from .db_conf import Home_PC_To_Pi_Config as db_conf
# from .db_conf import School_Laptop_Config as db_conf
# from .db_conf import Home_PC_Config as db_conf
# from .db_conf import School_Laptop_To_Pi_Config as db_conf
# from .db_conf import Pi_Server_Config as db_conf
# from .db_conf import Production_Config as db_conf
from .db_conf import Work_Laptop_Config as db_conf

db = db_conf()
print(db.get_message())
credentials = db.get_db_credentials()
print('~~~ DATABASE CONFIG ~~~')
print('    Host:         ', credentials["host"])
print('    Port:         ', credentials["port"])
print('    SQL User:     ', credentials["user"])
print('    SQL Password: ', credentials["password"])
print()

def init_db():
    """Initilaizes Database Session"""
    conn = mysqlx.get_session(
        db.get_db_credentials()
    )
    return conn
