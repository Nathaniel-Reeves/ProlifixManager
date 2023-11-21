from __future__ import annotations
from typing import Any, List, Literal, get_args

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

ProductTypes = Literal["Powder", "Capsule", "Liquid", "Other"]

TimeUnits = Literal["Years", "Months", "Days"]

ExpirationTypes = Literal["Best_By", "Exp"]

class Product_Master(Base):
    __tablename__ = 'Product_Master'
    __table_args__ = {'schema': 'Products'}
    
    # Table Columns
    product_id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.organization_id'))
    product_name: Mapped[str] = mapped_column()
    type: Mapped[ProductTypes] = mapped_column(Enum(
        *get_args(ProductTypes),
        name="ProductTypes",
        create_constraint=True,
        validate_strings=True,
        ))
    current_product: Mapped[bool] = mapped_column()
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    spec_issue_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    spec_revise_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    exp_unit: Mapped[TimeUnits] = mapped_column(Enum(
        *get_args(TimeUnits),
        name="TimeUnits",
        create_constraint=True,
        validate_strings=True,
        ))
    exp_type: Mapped[ExpirationTypes] = mapped_column(Enum(
        *get_args(ExpirationTypes),
        name="ExpirationTypes",
        create_constraint=True,
        validate_strings=True,
        ))
    exp_time_frame: Mapped[int] = mapped_column()
    exp_use_oldest_ingredient: Mapped[bool] = mapped_column(default=False)
    default_formula_id: Mapped[int] = mapped_column(ForeignKey('Formula_Master.formula_id'))
    certified_usda_organic: Mapped[bool] = mapped_column(default=False)
    certified_halal: Mapped[bool] = mapped_column(default=False)
    certified_kosher: Mapped[bool] = mapped_column(default=False)
    certified_gluten_free: Mapped[bool] = mapped_column(default=False)
    certified_national_sanitation_foundation: Mapped[bool] = mapped_column(default=False)
    certified_us_pharmacopeia: Mapped[bool] = mapped_column(default=False)
    certified_non_gmo: Mapped[bool] = mapped_column(default=False)
    certified_vegan: Mapped[bool] = mapped_column(default=False)
    
    doc = Column(MutableDict.as_mutable(JSON))

    # Relationships
    components: Mapped[List["ProductComponents"]] = relationship()
    # formulas: Mapped[List["Formula_Master"]] = relationship()
    # lot_numbers: Mapped[List["Lot_Numbers"]] = relationship()
    # items: Mapped[List["Item_id"]] = relationship()
    
class ProductComponents(Base):
    __tablename__ = 'Components'
    __table_args__ = {'schema': 'Products'}
    
    # Table Columns
    component_id: Mapped[int] = mapped_column(primary_key=True)
    material_qty_per_unit: Mapped[float] = mapped_column(default=0.0)
    current_default_component: Mapped[bool] = mapped_column(default=False)
    component_list_version: Mapped[int] = mapped_column(default=0)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Relationships
    materials_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    
    def __init__(self, component_id, material_qty_per_unit, current_default_component, component_list_version, date_entered):
        self.component_id = component_id
        self.material_qty_per_unit = material_qty_per_unit
        self.current_default_component = current_default_component
        self.component_list_version = component_list_version
        self.date_entered = date_entered
    
    def __repr__(self):
        return f'<Components id:{self.component_id} date_entered:{self.date_entered}>'

class Manufacturing_Process(Base):
    __tablename__ = 'Manufacturing_Process'
    __table_args__ = {'schema': 'Manufacturing'}
    
    # Table Columns
    process_spec_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    date_modified: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    
    doc = Column(MutableDict.as_mutable(JSON))

    # Relationships
    
    def __init__(self, process_spec_id, product_id, date_entered, date_modified, doc):
        self.process_spec_id = process_spec_id
        self.product_id = product_id
        self.date_entered = date_entered
        self.date_modified = date_modified
        self.doc = doc
        
    def __repr__(self):
        return f'<Manufacturing_Process id:{self.process_spec_id} product_id:{self.product_id}>'