from __future__ import annotations
from typing import List, Literal, get_args

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

ExpirationTypes = Literal["Best_By", "Exp"]

ComponentTypes = Literal['powder', 'liquid', 'container', 'pouch','shrink_band', 'lid', 'label', 'capsule','misc','scoop', 'desiccant','box', 'carton', 'packaging_material']

UnitTypes = Literal['grams', 'kilograms', 'units', 'boxes', 'pallets', 'liters', 'rolls', 'totes', 'barrels', 'pounds']

class InventoryComponents(Base):
    __tablename__ = 'Components'
    __table_args__ = {'schema': 'Inventory'}
    
    # Primary Key
    component_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationsips
    item_id: Mapped[List["Item_id"]] = relationship()
    component_names: Mapped[List["Component_Names"]] = relationship()
    # formula_detail: Mapped[List["Formula_Detail"]] = relationship()
    # purchase_order_detail: Mapped[List["Purchase_Order_Detail"]] = relationship()
    # formula_master: Mapped[List["Formula_Master"]] = relationship()
    # components: Mapped[List["ProductComponents"]] = relationship()
    
    # Table Columns
    component_type: Mapped[ComponentTypes] = mapped_column(Enum(
        *get_args(ComponentTypes),
        name="ComponentTypes",
        create_constraint=True,
        validate_strings=True,
        ))
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
    units: Mapped[UnitTypes] = mapped_column(Enum(
        *get_args(UnitTypes),
        name="UnitTypes",
        create_constraint=True,
        validate_strings=True,
        ))
    
    doc = Column(JSON, nullable=True)
    
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
    component_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
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

InventoryStates = Literal["Ordered", "Revised_Order_Decreased", "Revised_Order_Increased", "InTransit", "Back_Order", "Checkin_Quarantine", "Received", "Produced", "CycleCount", "Released", "Returned", "Allocated", "Batched", "Used", "Quarantined", "Lost", "Expired", "Wasted", "Damaged", "Destroyed", "Shipped"]
    
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
    state: Mapped[InventoryStates] = mapped_column(Enum(
        *get_args(InventoryStates),
        name="InventoryStates",
        create_constraint=True,
        validate_strings=True,
        ))
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
        
    