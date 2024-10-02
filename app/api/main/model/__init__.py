from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy import select

from .organizations import *
from .orders import *
from .products import *
from .inventory import *
from .manufacturing import *
from .files import *
from .policies import *

from .connector import get_session

mapper_registry = registry()

# Connect Modules/Databases

# Components
Components.purchase_order_detail = relationship(Purchase_Order_Detail, primaryjoin=Components.component_id == Purchase_Order_Detail.component_id)

# Product_Master
Product_Master.item_id = relationship(Item_id, primaryjoin=Product_Master.product_id == Item_id.product_id)

# Purchase_Order_Detail
Purchase_Order_Detail.inventory_log = relationship(Inventory_Log, primaryjoin=Purchase_Order_Detail.po_detail_id == Inventory_Log.po_detail_id)

# Sales_Order_Detail
Sale_Order_Detail.inventory_log = relationship(Inventory_Log, primaryjoin=Sale_Order_Detail.so_detail_id == Inventory_Log.so_detail_id)


# stm = select(Organizations, Organization_Names)\
#         .join(Organizations)\
#         .join(Organization_Names)\
#         .where(Organization_Names.organization_name == "Markus")

# print(stm)

if __name__ == '__main__':
    db = get_session()

    stm = select(Product_Master.product_name, Product_Master.type)\
        .join(Organizations)\
        .join(Organization_Names)\
        .where(Organization_Names.organization_name == "Markus")

    # stm = select(Organizations, Organization_Names)\
    #       .join(Organization_Names)\
    #       .where(Organization_Names.organization_name == "Markus")

    print(stm)

    test = db.execute(stm).all()
    for i in test:
        print(i)
