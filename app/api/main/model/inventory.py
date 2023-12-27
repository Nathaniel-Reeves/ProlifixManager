from __future__ import annotations
from typing import List, Optional

from sqlalchemy import Integer, Enum, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON, ENUM

from .base import Base

import datetime


class Components(Base):
    __tablename__ = 'Components'
    __table_args__ = {'schema': 'Inventory'}
    
    # Primary Key
    component_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Relationsips
    item_id: Mapped[List["Item_id"]] = relationship()
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    # component_names: Mapped[List["Component_Names"]] = relationship()
    # formula_detail: Mapped[List["Formula_Detail"]] = relationship()
    # purchase_order_detail: Mapped[List["Purchase_Order_Detail"]] = relationship()
    # formula_master: Mapped[List["Formula_Master"]] = relationship()
    # components: Mapped[List["Materials"]] = relationship()
    
    # Table Columns
    ComponentTypes = ("powder", "liquid", "container", "pouch", "shrink_band", "lid", "label", "capsule", "misc", "scoop", "desiccant", "box", "carton", "packaging_material")
    component_type: Mapped[int] = mapped_column(Enum(
        *ComponentTypes,
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
    UnitTypes = ("grams", "kilograms", "units", "boxes", "poallets", "liters", "rolls", "totes", "barrels", "pounds")
    units: Mapped[int] = mapped_column(Enum(
        *UnitTypes,
        name="UnitTypes",
        create_constraint=True,
        validate_strings=True,
        ))
    
    doc = Column(JSON, nullable=True)
    
    # Common Methods
    def __repr__(self):
        return f'<Inventory.Component component_id:{self.component_id} {self.component_type} brand:{self.brand_id}>'
    
    def to_dict(self):
        return {
            "component_id": self.component_id,
            "component_type": self.component_type,
            "certified_usda_organic": self.certified_usda_organic,
            "certified_halal": self.certified_halal,
            "certified_kosher": self.certified_kosher,
            "certified_gluten_free": self.certified_gluten_free,
            "certified_national_sanitation_foundation": self.certified_national_sanitation_foundation,
            "certified_us_pharmacopeia": self.certified_us_pharmacopeia,
            "certified_non_gmo": self.certified_non_gmo,
            "certified_vegan": self.certified_vegan,
            "date_entered": self.date_entered,
            "units": self.units,
            "doc": self.doc
        }
    
    def get_id(self):
        return self.component_id
    
    def get_id_name(self):
        return "component_id"

class Component_Names(Base):
    __tablename__ = 'Component_Names'
    __table_args__ = {'schema': 'Inventory'}
    
    # Primary Key
    name_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    component_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
    
    # Table Columns
    component_name: Mapped[str] = mapped_column()
    primary_name: Mapped[bool] = mapped_column(default=False)
    
    # Common Methods   
    def __repr__(self):
        return f'<Inventory.Component_Names name_id:{self.name_id} component_id:{self.component_id} Component_name:{self.component_name}>'
    
    def to_dict(self):
        return {
            "name_id": self.name_id,
            "component_id": self.component_id,
            "component_name": self.component_name,
            "primary_name": self.primary_name
        }
    
    def get_id(self):
        return self.name_id
    
    def get_id_name(self):
        return "name_id"

class Item_id(Base):
    __tablename__ = 'Item_id'
    __table_args__ = {'schema': 'Inventory'}
    
    # Primary Key
    item_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    component_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    inventory: Mapped[List["Inventory"]] = relationship()
    
    # Table Columns
    
    # Common Methods
    def __repr__(self):
        return f'<Inventory.Item_id item_id:{self.item_id} component_id:{self.component_id} product_id:{self.product_id}>'
    
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "component_id": self.component_id,
            "product_id": self.product_id
        }
        
    def get_id(self):
        return self.item_id
    
    def get_id_name(self):
        return "item_id"
    
class Inventory(Base):
    __tablename__ = 'Inventory'
    __table_args__ = {'schema': 'Inventory'}
    
    # Primary Key
    inv_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    item_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Item_id.item_id'), primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'), primary_key=True)
    recent_cycle_count_id: Mapped[int] = mapped_column(default=0)
    inventory_log: Mapped[List["Inventory_Log"]] = relationship()
    
    # Table Columns
    is_component: Mapped[bool] = mapped_column(default=False)
    is_product: Mapped[bool] = mapped_column(default=False)
    actual_inventory: Mapped[float] = mapped_column(default=0.0)
    theoretical_inventory: Mapped[float] = mapped_column(default=0.0)

    # Common Methods
    def __repr__(self):
        return f'<Inventory.Inventory inv_id:{self.inv_id} item_id:{self.item_id} actual_inv:{self.actual_inventory} theoretical_inv:{self.theoretical_inventory}>'
    
    def to_dict(self):
        return {
            "inv_id": self.inv_id,
            "item_id": self.item_id,
            "owner_id": self.owner_id,
            "recent_cycle_count_id": self.recent_cycle_count_id,
            "is_component": self.is_component,
            "is_product": self.is_product,
            "actual_inventory": self.actual_inventory,
            "theoretical_inventory": self.theoretical_inventory
        }
        
    def get_id(self):
        return self.inv_id
    
    def get_id_name(self):
        return "inv_id"

class Inventory_Log(Base):
    __tablename__ = 'Inventory_Log'
    __table_args__ = {'schema': 'Inventory'}
    
    # Primary Key
    log_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    inv_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Inventory.inv_id'))
    courier_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    facility_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Facilities.facility_id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Users.user_id'))
    po_detail_id: Mapped[int] = mapped_column(ForeignKey('Orders.Purchase_Order_Detail.po_detail_id'))
    so_detail_id: Mapped[int] = mapped_column(ForeignKey('Orders.Sale_Order_Detail.so_detail_id'))
    previous_log_id: Mapped[int] = mapped_column(default=None)
    
    # Table Columns
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
    InventoryStates = ("Ordered", "Revised Order Decreased", "Revised Order Increased", "InTransit", "Back Order", "Checkin Quarantine", "Received", "Produced", "Cycle Count", "Released", "Returned", "Allocated", "Batched", "Used", "Quarantined", "Lost", "Expired", "Wasted","Damaged","Destroyed", "Shipped")
    state: Mapped[int] = mapped_column(Enum(
        *InventoryStates,
        name="InventoryStates",
        create_constraint=True,
        validate_strings=True,
        ))
    state_notes: Mapped[str] = mapped_column(default=None)
    
    doc = Column(JSON, nullable=True)
    
    # Common Methods
    def __repr__(self):
        return f'<Inventory_Log log_id:{self.log_id} inv_id:{self.inv_id} state:{self.state}>'
    
    def to_dict(self):
        return {
            "log_id": self.log_id,
            "inv_id": self.inv_id,
            "courier_id": self.courier_id,
            "facility_id": self.facility_id,
            "user_id": self.user_id,
            "po_detail_id": self.po_detail_id,
            "so_detail_id": self.so_detail_id,
            "previous_log_id": self.previous_log_id,
            "pre_change_actual_inventory": self.pre_change_actual_inventory,
            "post_change_actual_inventory": self.post_change_actual_inventory,
            "pre_change_theoretical_inventory": self.pre_change_theoretical_inventory,
            "post_change_theoretical_inventory": self.post_change_theoretical_inventory,
            "cycle_count_grade": self.cycle_count_grade,
            "archived_tree": self.archived_tree,
            "supplier_item_id": self.supplier_item_id,
            "lot_number": self.lot_number,
            "batch_number": self.batch_number,
            "date_entered": self.date_entered,
            "state": self.state,
            "state_notes": self.state_notes,
            "doc": self.doc
        }
        
    def get_id(self):
        return self.log_id
    
    def get_id_name(self):
        return "log_id"
        
    