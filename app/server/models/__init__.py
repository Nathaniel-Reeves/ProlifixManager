from connector import *
import organizations as org
import orders as ord
import inventory as inv
import products as prod
import manufacturing as man
import formulas as form

from sqlalchemy import select
from connector import get_session
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

mapper_registry = registry()

# Connect Modules/Databases

# int.InventoryComponents
inv.InventoryComponents.formula_detail = relationship(form.Formula_Detail, primaryjoin=inv.InventoryComponents.component_id == form.Formula_Detail.ingredient_id)
inv.InventoryComponents.purchase_order_detail = relationship(ord.Purchase_Order_Detail, primaryjoin=inv.InventoryComponents.component_id == ord.Purchase_Order_Detail.component_id)
inv.InventoryComponents.formula_master = relationship(form.Formula_Master, primaryjoin=inv.InventoryComponents.component_id == form.Formula_Master.label_id)
inv.InventoryComponents.product_components = relationship(prod.ProductComponents, primaryjoin=inv.InventoryComponents.component_id == prod.ProductComponents.materials_id)

# prod.Product_Master
prod.Product_Master.formula_master = relationship(form.Formula_Master, primaryjoin=prod.Product_Master.product_id == form.Formula_Master.product_id)
prod.Product_Master.log_numbers = relationship(ord.Lot_Numbers, primaryjoin=prod.Product_Master.product_id == ord.Lot_Numbers.product_id)
prod.Product_Master.item_id = relationship(inv.Item_id, primaryjoin=prod.Product_Master.product_id == inv.Item_id.item_id)

# ord.Purchase_Order_Detail
ord.Purchase_Order_Detail.inventory_log = relationship(inv.Inventory_Log, primaryjoin=ord.Purchase_Order_Detail.po_detail_id == inv.Inventory_Log.po_detail_id)

# ord.Sales_Order_Detail
ord.Sale_Order_Detail.inventory_log = relationship(inv.Inventory_Log, primaryjoin=ord.Sale_Order_Detail.so_detail_id == inv.Inventory_Log.so_detail_id)


db = get_session()

stm = select(org.Organizations, org.Organization_Names)\
    .join(org.Organization_Names)\
    .where(org.Organization_Names.primary_name == True)

test = db.execute(stm).all()
print(test[0])
