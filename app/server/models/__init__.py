from connector import *
from organizations import *
# from products import *
# from components import *

from sqlalchemy import select
from connector import get_session



db = get_session()

stm = select(Organizations, Organization_Names)\
    .join(Organization_Names)\
    .where(Organization_Names.primary_name == True)

test = db.execute(stm).all()
print(test[0])
