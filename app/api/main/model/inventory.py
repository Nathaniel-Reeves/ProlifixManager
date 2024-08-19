from __future__ import annotations
from typing import List

from sqlalchemy import Enum, ForeignKey, Column, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.mysql import JSON

from .base import Base

import datetime


class Components(Base):
    """Components ORM Model"""
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
    certified_fda: Mapped[bool] = mapped_column(default=False)
    certified_gmp: Mapped[bool] = mapped_column(default=False)
    certified_made_with_organic: Mapped[bool] = mapped_column(default=False)
    certified_wildcrafted: Mapped[bool] = mapped_column(default=False)
    certified_usda_organic: Mapped[bool] = mapped_column(default=False)
    certified_halal: Mapped[bool] = mapped_column(default=False)
    certified_kosher: Mapped[bool] = mapped_column(default=False)
    certified_gluten_free: Mapped[bool] = mapped_column(default=False)
    certified_national_sanitation_foundation: Mapped[bool] = mapped_column(default=False)
    certified_us_pharmacopeia: Mapped[bool] = mapped_column(default=False)
    certified_non_gmo: Mapped[bool] = mapped_column(default=False)
    certified_vegan: Mapped[bool] = mapped_column(default=False)
    UnitTypes = ("grams", "kilograms", "units", "boxes", "pallets", "liters", "rolls", "totes", "barrels", "pounds")
    units: Mapped[int] = mapped_column(Enum(
        *UnitTypes,
        name="UnitTypes",
        create_constraint=True,
        validate_strings=True,
        ))
    primary_name_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Component_Names.name_id'))
    is_label: Mapped[bool] = mapped_column(default=False)
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    doc = Column(JSON, default={}, deferred_raiseload=False)

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Inventory.Component component_id:{self.component_id} {self.component_type} brand:{self.brand_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        try:
            doc =self.doc
        except SQLAlchemyError:
            doc = {}
        return {
            "component_id": self.component_id,
            "component_type": self.component_type,
            "certified_fda": self.certified_fda,
            "certified_gmp": self.certified_gmp,
            "certified_made_with_organic": self.certified_made_with_organic,
            "certified_wildcrafted": self.certified_wildcrafted,
            "certified_usda_organic": self.certified_usda_organic,
            "certified_halal": self.certified_halal,
            "certified_kosher": self.certified_kosher,
            "certified_gluten_free": self.certified_gluten_free,
            "certified_national_sanitation_foundation": self.certified_national_sanitation_foundation,
            "certified_us_pharmacopeia": self.certified_us_pharmacopeia,
            "certified_non_gmo": self.certified_non_gmo,
            "certified_vegan": self.certified_vegan,
            "units": self.units,
            "primary_name_id": self.primary_name_id,
            "is_label": self.is_label,
            "brand_id": self.brand_id,
            "doc": doc,
            "timestamp_entered": self.timestamp_entered,
            "timestamp_modified": self.timestamp_modified,
            "timestamp_fetched": datetime.datetime.now(datetime.timezone.utc)
        }

    def get_id(self):
        """Get Row Id"""
        return self.component_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "component_id"

class Component_Names(Base):
    """Component Names ORM Model"""
    __tablename__ = 'Component_Names'
    __table_args__ = {'schema': 'Inventory'}

    # Primary Key
    name_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    component_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))

    # Table Columns
    component_name: Mapped[str] = mapped_column()
    primary_name: Mapped[bool] = mapped_column(default=False)
    botanical_name: Mapped[bool] = mapped_column(default=False)
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Inventory.Component_Names name_id:{self.name_id} component_id:{self.component_id} Component_name:{self.component_name}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "name_id": self.name_id,
            "component_id": self.component_id,
            "component_name": self.component_name,
            "primary_name": self.primary_name,
            "botanical_name": self.botanical_name,
            "timestamp_entered": self.timestamp_entered,
            "timestamp_modified": self.timestamp_modified,
            "timestamp_fetched": datetime.datetime.now(datetime.timezone.utc)
        }

    def get_id(self):
        """Get Row Id"""
        return self.name_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "name_id"

class Item_id(Base):
    """Item ID ORM Model"""
    __tablename__ = 'Item_id'
    __table_args__ = {'schema': 'Inventory'}

    # Primary Key
    item_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    component_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    inventory: Mapped[List["Inventory"]] = relationship()

    # Table Columns
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Inventory.Item_id item_id:{self.item_id} component_id:{self.component_id} product_id:{self.product_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "item_id": self.item_id,
            "component_id": self.component_id,
            "product_id": self.product_id,
            "timestamp_entered": self.timestamp_entered,
            "timestamp_modified": self.timestamp_modified,
            "timestamp_fetched": datetime.datetime.now(datetime.timezone.utc)
        }

    def get_id(self):
        """Get Row Id"""
        return self.item_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "item_id"

class Inventory(Base):
    """Inventory ORM Model"""
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
    lot_number: Mapped[str] = mapped_column(primary_key=True)
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Inventory.Inventory inv_id:{self.inv_id} item_id:{self.item_id} actual_inv:{self.actual_inventory} theoretical_inv:{self.theoretical_inventory}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "inv_id": self.inv_id,
            "item_id": self.item_id,
            "owner_id": self.owner_id,
            "recent_cycle_count_id": self.recent_cycle_count_id,
            "is_component": self.is_component,
            "is_product": self.is_product,
            "actual_inventory": self.actual_inventory,
            "theoretical_inventory": self.theoretical_inventory,
            "lot_number": self.lot_number,
            "timestamp_entered": self.timestamp_entered,
            "timestamp_modified": self.timestamp_modified,
            "timestamp_fetched": datetime.datetime.now(datetime.timezone.utc)
        }

    def get_id(self):
        """Get Row Id"""
        return self.inv_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "inv_id"

class Inventory_Log(Base):
    """Inventory Log ORM Model"""
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
    InventoryStates = ("Ordered", "Revised Order Decreased", "Revised Order Increased", "InTransit", "Back Order", "Checkin Quarantine", "Received", "Produced", "Cycle Count", "Released", "Returned", "Allocated", "Batched", "Used", "Quarantined", "Lost", "Expired", "Wasted","Damaged","Destroyed", "Shipped")
    state: Mapped[int] = mapped_column(Enum(
        *InventoryStates,
        name="InventoryStates",
        create_constraint=True,
        validate_strings=True,
        ))
    state_notes: Mapped[str] = mapped_column(default=None)
    position: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    doc = Column(JSON, nullable=True)

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Inventory_Log log_id:{self.log_id} inv_id:{self.inv_id} state:{self.state}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "log_id": self.log_id,
            "inv_id": self.inv_id,
            "courier_id": self.courier_id,
            "facility_id": self.facility_id,
            "user_id": self.user_id,
            "po_detail_id": self.po_detail_id,
            "so_detail_id": self.so_detail_id,
            "pre_change_actual_inventory": self.pre_change_actual_inventory,
            "post_change_actual_inventory": self.post_change_actual_inventory,
            "pre_change_theoretical_inventory": self.pre_change_theoretical_inventory,
            "post_change_theoretical_inventory": self.post_change_theoretical_inventory,
            "cycle_count_grade": self.cycle_count_grade,
            "archived_tree": self.archived_tree,
            "supplier_item_id": self.supplier_item_id,
            "lot_number": self.lot_number,
            "batch_number": self.batch_number,
            "state": self.state,
            "state_notes": self.state_notes,
            "doc": self.doc,
            "position": self.position,
            "type": self.type,
            "timestamp_entered": self.timestamp_entered,
            "timestamp_modified": self.timestamp_modified,
            "timestamp_fetched": datetime.datetime.now(datetime.timezone.utc)
        }

    def get_id(self):
        """Get Row Id"""
        return self.log_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "log_id"

class Inventory_Log_Edges(Base):
    """Inventory Log Edges ORM Model"""
    __tablename__ = 'Inventory_Log_Edges'

    # Primary Key
    source: Mapped[int] = mapped_column(primary_key=True)
    target: Mapped[int] = mapped_column(primary_key=True)

    __table_args__ = (ForeignKeyConstraint([source, target],
                                           [Inventory_Log.log_id, Inventory_Log.log_id]),
                      {'schema': 'Inventory'})

    # Relationships
    inv_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Inventory.inv_id'))

    # Table Columns
    label: Mapped[str] = mapped_column()
    animated: Mapped[bool] = mapped_column(default=False)
    ArrowStates = ("Arrow","ArrowClosed")
    marker_end: Mapped[int] = mapped_column(Enum(
        *ArrowStates,
        name="ArrowStates",
        create_constraint=True,
        validate_strings=True,
    ))
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Inventory_Log_Edge source:{self.source} target:{self.target} inv_id:{self.inv_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "source": self.source,
            "target": self.target,
            "inv_id": self.inv_id,
            "label": self.label,
            "animated": self.animated,
            "marker_end": self.marker_end,
            "timestamp_entered": self.timestamp_entered,
            "timestamp_modified": self.timestamp_modified,
            "timestamp_fetched": datetime.datetime.now(datetime.timezone.utc)
        }

    def get_id(self):
        """Get Row Id"""
        return (self.source, self.target)

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "(source, target)"
