from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import Column
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON

import datetime
import enum

from connector import Base

from formulas import Formula_Master, Formula_Detail

class ExpirationTypes(enum.Enum):
    Best_By = "Best_By"
    Exp = "Exp"

class ComponentTypes(enum.Enum):
    powder = 'powder'
    liquid = 'liquid'
    container = 'container'
    pouch = 'pouch'
    shrink_band = 'shrink_band'
    lid = 'lid'
    label = 'label'
    capsule = 'capsule'
    misc = 'misc'
    scoop = 'scoop'
    desiccant = 'desiccant'
    box = 'box'
    carton = 'carton'
    packaging_material = 'packaging_material'

class UnitTypes(enum.Enum):
    grams = 'grams'
    kilograms = 'kilograms'
    units = 'units'
    boxes = 'boxes'
    pallets = 'pallets'
    liters = 'liters'
    rolls = 'rolls'
    totes = 'totes'
    barrels = 'barrels'
    pounds = 'pounds'

class Components(Base):
    __tablename__ = 'Inventory'
    __table_args__ = {'schema': 'Inventory'}
    
    # Table Columns
    component_id: Mapped[int] = mapped_column(primary_key=True)
    component_type: Mapped[Enum(ComponentTypes)] = mapped_column()
    certified_usda_organic: Mapped[bool] = mapped_column(default=False)
    certified_halal: Mapped[bool] = mapped_column(default=False)
    certified_kosher: Mapped[bool] = mapped_column(default=False)
    certified_gluten_free: Mapped[bool] = mapped_column(default=False)
    certified_national_sanitation_foundation: Mapped[bool] = mapped_column(default=False)
    certified_us_pharmacopeia: Mapped[bool] = mapped_column(default=False)
    certified_non_gmo: Mapped[bool] = mapped_column(default=False)
    certified_vegan: Mapped[bool] = mapped_column(default=False)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    units: Mapped[Enum(UnitTypes)] = mapped_column(default=UnitTypes.kilograms)
    
    doc = Column(JSON, nullable=True)
    
    # Relationsips
    item_id: Mapped[List["Item_id"]] = relationship()
    components: Mapped[List["Components"]] = relationship()
    component_names: Mapped[List["Component_Names"]] = relationship()
    formula_detail: Mapped[List["Formula_Detail"]] = relationship()
    purchase_order_detail: Mapped[List["Purchase_Order_Detail"]] = relationship()
    formula_master: Mapped[List["Formula_Master"]] = relationship()
    
    def __init__(self, component_id, component_type, certified_usda_organic, certified_halal, certified_kosher, certified_gluten_free, certified_national_sanitation_foundation, certified_us_pharmacopeia, certified_non_gmo, certified_vegan, date_entered, brand_id, units, doc):
        self.component_id = component_id
        self.component_type = component_type
        self.certified_usda_organic = certified_usda_organic
        self.certified_halal = certified_halal
        self.certified_kosher = certified_kosher
        self.certified_gluten_free = certified_gluten_free
        self.certified_national_sanitation_foundation = certified_national_sanitation_foundation
        self.certified_us_pharmacopeia = certified_us_pharmacopeia
        self.certified_non_gmo = certified_non_gmo
        self.certified_vegan = certified_vegan
        self.date_entered = date_entered
        self.brand_id = brand_id
        self.units = units
        self.doc = doc
    
    def __repr__(self):
        return f'<Inventory.Component component_id:{self.component_id} {self.component_type} brand:{self.brand_id}>'
    

class Component_Names(Base):
    __tablename__ = 'Component_Names'
    __table_args__ = {'schema': 'Inventory'}
    
    # Table Columns
    name_id: Mapped[int] = mapped_column(primary_key=True)
    component_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Component_Names.component_id'))
    Component_name: Mapped[str] = mapped_column()
    primary_name: Mapped[bool] = mapped_column(default=False)
    
    # Relationships
    
    def __init__(self, name_id, component_id, Component_name, primary_name):
        self.name_id = name_id
        self.component_id = component_id
        self.Component_name = Component_name
        self.primary_name = primary_name
        
    def __repr__(self):
        return f'<Inventory.Component_Names name_id:{self.name_id} component_id:{self.component_id} Component_name:{self.Component_name}>'

class Item_id(Base):
    __tablename__ = 'Item_id'
    __table_args__ = {'schema': 'Inventory'}
    
    # Table Columns
    item_id: Mapped[int] = mapped_column(primary_key=True)
    component_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Component_Names.component_id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    
    # Relationships
    inventory: Mapped[List["Inventory"]] = relationship()
    
    def __init__(self, item_id, component_id, product_id):
        self.item_id = item_id
        self.component_id = component_id
        self.product_id = product_id
        
    def __repr__(self):
        return f'<Inventory.Item_id item_id:{self.item_id} component_id:{self.component_id} product_id:{self.product_id}>'
    
class Inventory(Base):
    __tablename__ = 'Inventory'
    __table_args__ = {'schema': 'Inventory'}
    
    # Table Columns
    inv_id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Item_id.item_id'), primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'), primary_key=True)
    is_component: Mapped[bool] = mapped_column(default=False)
    is_product: Mapped[bool] = mapped_column(default=False)
    actual_inventory: Mapped[float] = mapped_column(default=0.0)
    theoretical_inventory: Mapped[float] = mapped_column(default=0.0)
    recent_cycle_count_id: Mapped[int] = mapped_column(default=0)
    
    # Relationships
    inventory_log: Mapped[List["Inventory_Log"]] = relationship()
    
    def __init__(self, item_id, owner_id, is_component, is_product, actual_inventory, theoretical_inventory, recent_cycle_count_id):
        self.item_id = item_id
        self.owner_id = owner_id
        self.is_component = is_component
        self.is_product = is_product
        self.actual_inventory = actual_inventory
        self.theoretical_inventory = theoretical_inventory
        self.recent_cycle_count_id = recent_cycle_count_id
        
    def __repr__(self):
        return f'<Inventory.Inventory inv_id:{self.inv_id} item_id:{self.item_id} actual_inv:{self.actual_inventory} theoretical_inv:{self.theoretical_inventory}>'
 
class InventoryStates(enum.Enum):
    Ordered = 'Ordered'
    Revised_Order_Decreased = 'Revised_Order_Decreased'
    Revised_Order_Increased = 'Revised_Order_Increased'
    In_Transit = 'In_Transit'
    Back_Order = 'Back_Order'
    Checkin_Quarantine = 'Checkin_Quarantine'
    Received = 'Received'
    Produced = 'Produced'
    Cycle_Count = 'Cycle_Count'
    Released = 'Released'
    Returned = 'Returned'
    Allocated = 'Allocated'
    Batched = 'Batched'
    Used = 'Used'
    Quarantined = 'Quarantined'
    Lost = 'Lost'
    Expired = 'Expired'
    Wasted = 'Wasted'
    Damaged = 'Damaged'
    Destroyed = 'Destroyed'
    Shipped = 'Shipped'
    
class Inventory_Log(Base):
    __tablename__ = 'Inventory_Log'
    __table_args__ = {'schema': 'Inventory'}
    
    # Table Columns
    log_id: Mapped[int] = mapped_column(primary_key=True)
    inv_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Inventory.inv_id'))
    courier_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    facility_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Facilities.facility_id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Users.user_id'))
    po_detail_id: Mapped[int] = mapped_column(ForeignKey('Orders.Purchase_Order_Detail.po_detail_id'))
    so_detail_id: Mapped[int] = mapped_column(ForeignKey('Orders.Sales_Order_Detail.so_detail_id'))
    previous_log_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Inventory_Log.log_id'))
    pre_change_actual_inventory: Mapped[float] = mapped_column(default=0.0)
    post_change_actual_inventory: Mapped[float] = mapped_column(default=0.0)
    pre_change_theoretical_inventory: Mapped[float] = mapped_column(default=0.0)
    post_change_theoretical_inventory: Mapped[float] = mapped_column(default=0.0)
    cycle_count_grade: Mapped[int] = mapped_column(default=0)
    archived_tree: Mapped[bool] = mapped_column(default=False)
    supplier_item_id: Mapped[str] = mapped_column(default=None)
    lot_number: Mapped[str] = mapped_column(default=None)
    batch_number: Mapped[str] = mapped_column(default=None)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    state: Mapped[Enum(InventoryStates)] = mapped_column()
    state_notes: Mapped[str] = mapped_column(default=None)
    
    doc = Column(JSON, nullable=True)
    
    # Relationships
    
    def __init__(self, log_id, inv_id, courier_id, facility_id, user_id, po_detail_id, so_detail_id, previous_log_id, pre_change_actual_inventory, post_change_actual_inventory, pre_change_theoretical_inventory, post_change_theoretical_inventory, cycle_count_grade, archived_tree, supplier_item_id, lot_number, batch_number, date_entered, doc, state, state_notes):
        self.log_id = log_id
        self.inv_id = inv_id
        self.courier_id = courier_id
        self.facility_id = facility_id
        self.user_id = user_id
        self.po_detail_id = po_detail_id 
        self.so_detail_id = so_detail_id 
        self.previous_log_id = previous_log_id 
        self.pre_change_actual_inventory = pre_change_actual_inventory
        self.post_change_actual_inventory = post_change_actual_inventory
        self.pre_change_theoretical_inventory = pre_change_theoretical_inventory
        self.post_change_theoretical_inventory = post_change_theoretical_inventory
        self.cycle_count_grade = cycle_count_grade
        self.archived_tree = archived_tree
        self.supplier_item_id = supplier_item_id
        self.lot_number = lot_number
        self.batch_number = batch_number
        self.date_entered = date_entered
        self.doc = doc
        self.state = state
        self.state_notes = state_notes
    
    def __repr__(self):
        return f'<Inventory_Log log_id:{self.log_id} inv_id:{self.inv_id} state:{self.state}>'
        
    

class Sales_Orders(Base):
    __tablename__ = 'Sales_Orders'
    __table_args__ = {'schema': 'Orders'}
    
    # Table Columns
    prefix: Mapped[str] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(primary_key=True)
    sec_number: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    client_po_num: Mapped[str] = mapped_column(default=None)
    order_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    target_completion_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    completion_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    billed_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    closed_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    down_payment_actual: Mapped[float] = mapped_column(default=None)
    theoretical_po_amount: Mapped[float] = mapped_column(default=None)
    total_paid: Mapped[float] = mapped_column(default=None)
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Relationships
    sales_orders_payments: Mapped[List["Sales_Order_Payments"]] = relationship()
    sales_order_detail: Mapped[List["Sales_Order_Detail"]] = relationship()
    
    def __init__(self, prefix, year, month, sec_number, organization_id, client_po_num, order_date, target_completion_date, completion_date, date_entered, billed_date, closed_date, down_payment_actual, theoretical_po_amount, total_paid, doc):
        self.prefix = prefix
        self.year = year
        self.month = month
        self.sec_number = sec_number
        self.organization_id = organization_id
        self.client_po_num = client_po_num
        self.order_date = order_date
        self.target_completion_date = target_completion_date
        self.completion_date = completion_date
        self.date_entered = date_entered
        self.billed_date = billed_date
        self.closed_date = closed_date
        self.down_payment_actual = down_payment_actual
        self.theoretical_po_amount = theoretical_po_amount
        self.total_paid = total_paid
        self.doc = doc
    
    def __repr__(self):
        return f'<Sales_Order SO#{self.prefix}{self.year}~{self.month}~{self.sec_number}>'

class Sales_Order_Detail(Base):
    __tablename__ = 'Sales_Order_Detail'
    __table_args__ = {'schema': 'Sales_Orders'}
    
    # Table Columns
    so_detail_id: Mapped[int] = mapped_column(primary_key=True)
    prefix: Mapped[str] = mapped_column(ForeignKey('Sales_Orders.Sales_Orders.prefix'))
    year: Mapped[int] = mapped_column(ForeignKey('Sales_Orders.Sales_Orders.year'))
    month: Mapped[str] = mapped_column(ForeignKey('Sales_Orders.Sales_Orders.month'))
    sec_number: Mapped[int] = mapped_column(ForeignKey('Sales_Orders.Sales_Orders.sec_number'))
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    unit_order_qty: Mapped[int] = mapped_column(default=None)
    kilos_order_qty: Mapped[float] = mapped_column(default=None)
    special_instructions: Mapped[str] = mapped_column(default=None)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    bit_price_per_unit: Mapped[float] = mapped_column(default=None)
    final_ship_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Relationships
    lot_numbers: Mapped[List["Lot_Numbers"]] = relationship()
    inventory_log: Mapped[List["Inventory_Log"]] = relationship()
    
    def __init__(self, so_detail_id, prefix, year, month, sec_number, product_id, unit_order_qty, kilos_order_qty, special_instructions, date_entered, bit_price_per_unit, final_ship_date, doc):
        self.so_detail_id = so_detail_id
        self.prefix = prefix
        self.year = year
        self.month = month
        self.sec_number = sec_number
        self.product_id = product_id
        self.unit_order_qty = unit_order_qty
        self.kilos_order_qty = kilos_order_qty
        self.special_instructions = special_instructions
        self.date_entered = date_entered
        self.bit_price_per_unit = bit_price_per_unit
        self.final_ship_date = final_ship_date
        self.doc = doc
    
    def __repr__(self):
        return f'<Sales_Order_Detail SO#{self.prefix}{self.year}~{self.month}~{self.sec_number} Product_id:{self.product_id} Qty:{self.unit_order_qty}{self.kilos_order_qty}>'

class PaymentTypes(enum.Enum):
    down_payment = "down_payment"
    other = "other"
    final_payment = "final_payment"
    
class Sales_Order_Payments(Base):
    __tablename__ = 'Sales_Order_Payments'
    __table_args__ = {'schema': 'Sales_Orders'}
    
    # Table Columns
    so_detail_id: Mapped[int] = mapped_column(primary_key=True)
    prefix: Mapped[str] = mapped_column(ForeignKey('Sales_Orders.Sales_Orders.prefix'))
    year: Mapped[int] = mapped_column(ForeignKey('Sales_Orders.Sales_Orders.year'))
    month: Mapped[str] = mapped_column(ForeignKey('Sales_Orders.Sales_Orders.month'))
    sec_number: Mapped[int] = mapped_column(ForeignKey('Sales_Orders.Sales_Orders.sec_number'))
    payment_amount: Mapped[float] = mapped_column(default=None)
    payment_type: Mapped[Enum(PaymentTypes)] = mapped_column(default=None)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    doc = Column(MutableDict.as_mutable(JSON))

    # Relationships
    
    def __init__(self, so_detail_id, prefix, year, month, sec_number, payment_amount, payment_type, date_entered, doc):
        self.so_detail_id = so_detail_id
        self.prefix = prefix
        self.year = year
        self.month = month
        self.sec_number = sec_number
        self.payment_amount = payment_amount
        self.payment_type = payment_type
        self.date_entered = date_entered
        self.doc = doc
        
    def __repr__(self):
        return f'<Sales_Order_Payments SO#{self.prefix}{self.year}~{self.month}~{self.sec_number} Type:{self.payment_type} Amount:{self.payment_amount}>'
    
class Lot_Numbers(Base):
    __tablename__ = 'Lot_Numbers'
    __table_args__ = {'schema': 'Sales_Orders'}
    
    # Table Columns
    prefix: Mapped[str] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[str] = mapped_column(primary_key=True)
    sec_number: Mapped[int] = mapped_column(primary_key=True)
    suffix: Mapped[str] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    so_detail_id: Mapped[int] = mapped_column(ForeignKey('Orders.Sales_Order_Detail.so_detail_id'))
    target_unit_yield: Mapped[int] = mapped_column(default=None)
    actual_unit_yield: Mapped[int] = mapped_column(default=None)
    retentions: Mapped[int] = mapped_column(default=None)
    total_shippable_product: Mapped[int] = mapped_column(default=None)
    batch_printed: Mapped[bool] = mapped_column(default=False)
    bpr_printed: Mapped[bool] = mapped_column(default=False)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    exp_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    exp_type: Mapped[Enum(ExpirationTypes)] = mapped_column(default=None)
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    def __init__(self, prefix, year, month, sec_number, suffix, product_id, so_detail_id, target_unit_yield, actual_unit_yield, retentions, total_shippable_product, batch_printed, bpr_printed, date_entered, exp_date, exp_type, doc):
        self.prefix = prefix
        self.year = year
        self.month = month
        self.sec_number = sec_number
        self.suffix = suffix
        self.product_id = product_id
        self.so_detail_id = so_detail_id
        self.target_unit_yield = target_unit_yield
        self.actual_unit_yield = actual_unit_yield
        self.retentions = retentions
        self.total_shippable_product = total_shippable_product
        self.batch_printed = batch_printed
        self.bpr_printed = bpr_printed
        self.date_entered = date_entered
        self.exp_date = exp_date
        self.exp_type = exp_type
        self.doc = doc
    
    def __repr__(self):
        return f'<Lot_Numbers Lot#:{self.prefix} {self.year}{self.month}{self.sec_number} {self.suffix} Product_id:{self.product_id} >'
    
class Purchase_Orders(Base):
    __tablename__ = 'Purchase_Orders'
    __table_args__ = {'schema': 'Orders'}
    
    # Table Columns
    prefix: Mapped[str] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(primary_key=True)
    sec_number: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    supplier_so_num: Mapped[str] = mapped_column(default=None)
    order_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    eta_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Relationships
    purchase_order_details: Mapped[List["Purchase_Order_Detail"]] = relationship()
    
    def __init__(self, prefix, year, month, sec_number, organization_id, supplier_so_num, order_date, eta_date, date_entered, doc):
        self.prefix = prefix
        self.year = year
        self.month = month
        self.sec_number = sec_number
        self.organization_id = organization_id
        self.supplier_so_num = supplier_so_num
        self.order_date = order_date
        self.eta_date = eta_date
        self.date_entered = date_entered
        self.doc = doc
    
    def __repr__(self):
        return f'<Purchase_Orders PO#:{self.prefix} {self.year}{self.month}{self.sec_number} >'

class Purchase_Order_Detail(Base):
    __tablename__ = 'Purchase_Order_Detail'
    __table_args__ = {'schema': 'Purchase_Orders'}
    
    # Table Columns
    po_detail_id: Mapped[int] = mapped_column(primary_key=True)
    prefix: Mapped[str] = mapped_column(ForeignKey('Purchase_Orders.Purchase_Orders.prefix'))
    year: Mapped[int] = mapped_column(ForeignKey('Purchase_Orders.Purchase_Orders.year'))
    month: Mapped[int] = mapped_column(ForeignKey('Purchase_Orders.Purchase_Orders.month'))
    sec_number: Mapped[int] = mapped_column(ForeignKey('Purchase_Orders.Purchase_Orders.sec_number'))
    component_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
    unit_order_qty: Mapped[int] = mapped_column(default=None)
    kilos_order_qty: Mapped[float] = mapped_column(default=None)
    special_instructions: Mapped[str] = mapped_column(default=None)
    datetime_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    bid_price_per_unit: Mapped[float] = mapped_column(default=None)
    bid_price_per_kilo: Mapped[float] = mapped_column(default=None)
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Relationships
    inventory_log: Mapped[List["Inventory_Log"]] = relationship()
    
    def __init__(self, po_detail_id, prefix, year, month, sec_number, component_id, unit_order_qty, kilos_order_qty, special_instructions, datetime_entered, bid_price_per_unit, bid_price_per_kilo, doc):
        self.po_detail_id = po_detail_id
        self.prefix = prefix
        self.year = year
        self.month = month
        self.sec_number = sec_number
        self.component_id = component_id
        self.unit_order_qty = unit_order_qty
        self.kilos_order_qty = kilos_order_qty
        self.special_instructions = special_instructions
        self.datetime_entered = datetime_entered
        self.bid_price_per_unit = bid_price_per_unit
        self.bid_price_per_kilo = bid_price_per_kilo
        self.doc = doc
    
    def __repr__(self):
        return f'<Purchase_Order_Detail PO#:{self.prefix} {self.year}{self.month}{self.sec_number} >'
    
    
