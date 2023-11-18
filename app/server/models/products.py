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

class ProductTypes(enum.Enum):
    Powder = "Powder"
    Capsule = "Capsule"
    Liquid = "Liquid"
    Other = "Other"

class TimeUnits(enum.Enum):
    Years = "Years"
    Months = "Months"
    Days = "Days"
    
class ExpirationTypes(enum.Enum):
    Best_By = "Best_By"
    Exp = "Exp"

class Product_Master(Base):
    __tablename__ = 'Product_Master'
    __table_args__ = {'schema': 'Products'}
    
    # Table Columns
    product_id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.organization_id'))
    product_name: Mapped[str] = mapped_column()
    current_product: Mapped[bool] = mapped_column()
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    spec_issue_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    spec_revise_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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
    
    type = Column(Enum(ProductTypes))
    doc = Column(MutableDict.as_mutable(JSON))
    exp_unit = Column(Enum(TimeUnits))
    exp_type = Column(Enum(ExpirationTypes)) 

    # Relationships
    components: Mapped[List["Components"]] = relationship()
    formulas: Mapped[List["Formula_Master"]] = relationship()
    lot_numbers: Mapped[List["Lot_Numbers"]] = relationship()
    items: Mapped[List["Item_id"]] = relationship()
    
class Components(Base):
    __tablename__ = 'Components'
    __table_args__ = {'schema': 'Products'}
    
    # Table Columns
    component_id: Mapped[int] = mapped_column(primary_key=True)
    material_qty_per_unit: Mapped[float] = mapped_column(default=0.0, Nullable=False)
    current_default_component: Mapped[bool] = mapped_column(default=False)
    component_list_version: Mapped[int] = mapped_column(default=0)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Relationships
    materials_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
