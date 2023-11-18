import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase


# Define the MariaDb engine using MariaDB Connector/Python
host = '172.10.10.2'
port = '3306'
user = 'client'
password = "ClientPassword!5"

engine = sa.create_engine(f'mariadb+mariadbconnector://{user}:{password}@{host}:{port}/Organizations')

class Base(DeclarativeBase):
    pass

def get_session():
    Session = sa.orm.sessionmaker()
    Session.configure(bind=engine)
    Session = Session()
    return Session