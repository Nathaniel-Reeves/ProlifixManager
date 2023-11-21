from connector import *
from organizations import *
# from orders import *
# from inventory import *
from inv_orders import *
from products import *
from formulas import *
from manufacturing import *

from sqlalchemy import select
from connector import get_session



db = get_session()

stm = select(Organizations, Organization_Names)\
    .join(Organization_Names)\
    .where(Organization_Names.primary_name == True)

test = db.execute(stm).all()
print(test[0])
