from __future__ import annotations
from typing import List, Literal, get_args, Optional

from sqlalchemy import Integer, Enum, ForeignKey, Column
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON, ENUM

import datetime
import enum

class Base(DeclarativeBase):
    pass

class Formula_Master(Base):
    __tablename__ = 'Formula_Master'
    __table_args__ = {'schema': 'Formulas'}
    
    # Table Columns
    formula_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S'))
    formulation_version: Mapped[int] = mapped_column(default=None)
    notes: Mapped[str] = mapped_column(default=None)
    capsule_size: Mapped[str] = mapped_column(default=None)
    empty_capsule_mg: Mapped[float] = mapped_column(default=0.0)
    total_grams_per_unit: Mapped[float] = mapped_column(default=0.0)
    total_capsules_per_unit: Mapped[float] = mapped_column(default=0.0)
    total_milliliters_per_unit: Mapped[float] = mapped_column(default=0.0)
    fill_min: Mapped[float] = mapped_column(default=0.0)
    fill_max: Mapped[float] = mapped_column(default=0.0)
    label_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
    
    # Relationships
    formula_detail: Mapped[List["Formula_Detail"]] = relationship()
    
    # Formula Versioning
    __mapper_args__ = {"version_id_col": formulation_version}
    
    def __init__(self, formula_id, product_id, date_entered, formulation_version, notes, capsule_size, empty_capsule_mg, total_grams_per_unit, total_capsules_per_unit, total_milliliters_per_unit, fill_min, fill_max, label_id):
        self.formula_id = formula_id
        self.product_id = product_id
        self.date_entered = date_entered
        self.formulation_version = formulation_version
        self.notes = notes
        self.capsule_size = capsule_size
        self.empty_capsule_mg = empty_capsule_mg
        self.total_grams_per_unit = total_grams_per_unit
        self.total_capsules_per_unit = total_capsules_per_unit
        self.total_milliliters_per_unit = total_milliliters_per_unit
        self.fill_min = fill_min
        self.fill_max = fill_max
        self.label_id = label_id
    
    def __repr__(self):
        return f'<Formula_Master formula_id:{self.formula_id} product_id:{self.product_id} version:{self.formulation_version} date_entered:{self.date_entered}>'
    

class Formula_Detail(Base):
    __tablename__ = 'Formula_Detail'
    __table_args__ = {'schema': 'Formulas'}
    
    # Table Columns
    formula_detail_id: Mapped[int] = mapped_column(primary_key=True)
    formula_id: Mapped[int] = mapped_column(ForeignKey('Formulas.Formula_Master.formula_id'))
    percent: Mapped[float] = mapped_column(default=0.0)
    mg_per_capsule: Mapped[float] = mapped_column(default=0.0)
    ml_per_unit: Mapped[float] = mapped_column(default=0.0)
    grams_per_unit: Mapped[float] = mapped_column(default=0.0)
    organic_specs: Mapped[bool] = mapped_column(default=False)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
    notes: Mapped[str] = mapped_column(default=None)
    brand_specific: Mapped[bool] = mapped_column(default=False)
    organic_specific: Mapped[bool] = mapped_column(default=False)
    
    # Relationships
    client_spec_group: Mapped[List["Client_Spec_Group"]] = relationship()
    primary_group: Mapped[List["Primary_Group"]] = relationship()
    secondary_group: Mapped[List["Secondary_Group"]] = relationship()
    tertiary_group: Mapped[List["Tertiary_Group"]] = relationship()
    quaternary_group: Mapped[List["Quaternary_Group"]] = relationship()
    
    def __init__(self, formula_detail_id, formula_id, percent, mg_per_capsule, ml_per_unit, grams_per_unit, organic_specs, ingredient_id, notes, brand_specific, organic_specific):
        self.formula_detail_id = formula_detail_id
        self.formula_id = formula_id
        self.percent = percent
        self.mg_per_capsule = mg_per_capsule
        self.ml_per_unit = ml_per_unit
        self.grams_per_unit = grams_per_unit
        self.organic_specs = organic_specs
        self.ingredient_id = ingredient_id
        self.notes = notes
        self.brand_specific = brand_specific
        self.organic_specific = organic_specific
        
    def __repr__(self):
        return f'<id:{self.formula_detail_id} formula_id:{self.formula_id} percent:{self.percent}>'

# class OrganicSpecTypes(enum.Enum):
#     organic = 'organic'
#     non_organic = 'non_organic'
#     any = 'any'
    
OrganicSpecTypes = Literal['organic', 'non_organic', 'any']

class Client_Spec_Group(Base):
    __tablename__ = 'Client_Spec_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    # Table Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Formulas.Formula_Detail.formula_detail_id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    organic_spec: Mapped[OrganicSpecTypes] = mapped_column(Enum(
        *get_args(OrganicSpecTypes),
        name="OrganicSpecTypes",
        create_constraint=True,
        validate_strings=True,
        )
    )
    
    # Relationships
    
    def __init__(self, id, formula_ingredient_id, brand_id, organic_spec):
        self.id = id
        self.formula_ingredient_id = formula_ingredient_id
        self.brand_id = brand_id
        self.organic_spec = organic_spec
        
    def __repr__(self):
        return f'<id:{self.id} ing_id:{self.formula_ingredient_id} brand:{self.brand_id} organic_spec:{self.organic_spec}>'

class Primary_Group(Base):
    __tablename__ = 'Primary_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    # Table Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Formulas.Formula_Detail.formula_detail_id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    organic_spec: Mapped[OrganicSpecTypes] = mapped_column(Enum(
        *get_args(OrganicSpecTypes),
        name="OrganicSpecTypes",
        create_constraint=True,
        validate_strings=True,
        )
    )
    
    # Relationships
    
    def __init__(self, id, formula_ingredient_id, brand_id, organic_spec):
        self.id = id
        self.formula_ingredient_id = formula_ingredient_id
        self.brand_id = brand_id
        self.organic_spec = organic_spec
        
    def __repr__(self):
        return f'<id:{self.id} ing_id:{self.formula_ingredient_id} brand:{self.brand_id} organic_spec:{self.organic_spec}>'

class Secondary_Group(Base):
    __tablename__ = 'Secondary_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    # Table Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Formulas.Formula_Detail.formula_detail_id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    organic_spec: Mapped[OrganicSpecTypes] = mapped_column(Enum(
        *get_args(OrganicSpecTypes),
        name="OrganicSpecTypes",
        create_constraint=True,
        validate_strings=True,
        )
    )
    
    # Relationships
    
    def __init__(self, id, formula_ingredient_id, brand_id, organic_spec):
        self.id = id
        self.formula_ingredient_id = formula_ingredient_id
        self.brand_id = brand_id
        self.organic_spec = organic_spec
        
    def __repr__(self):
        return f'<id:{self.id} ing_id:{self.formula_ingredient_id} brand:{self.brand_id} organic_spec:{self.organic_spec}>'

class Tertiary_Group(Base):
    __tablename__ = 'Tertiary_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    # Table Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Formulas.Formula_Detail.formula_detail_id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    organic_spec: Mapped[OrganicSpecTypes] = mapped_column(Enum(
        *get_args(OrganicSpecTypes),
        name="OrganicSpecTypes",
        create_constraint=True,
        validate_strings=True,
        )
    )
    
    # Relationships
    
    def __init__(self, id, formula_ingredient_id, brand_id, organic_spec):
        self.id = id
        self.formula_ingredient_id = formula_ingredient_id
        self.brand_id = brand_id
        self.organic_spec = organic_spec
        
    def __repr__(self):
        return f'<id:{self.id} ing_id:{self.formula_ingredient_id} brand:{self.brand_id} organic_spec:{self.organic_spec}>'

class Quaternary_Group(Base):
    __tablename__ = 'Quaternary_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    # Table Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Formulas.Formula_Detail.formula_detail_id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    organic_spec: Mapped[OrganicSpecTypes] = mapped_column(Enum(
        *get_args(OrganicSpecTypes),
        name="OrganicSpecTypes",
        create_constraint=True,
        validate_strings=True,
        )
    )
    
    # Relationships
    
    def __init__(self, id, formula_ingredient_id, brand_id, organic_spec):
        self.id = id
        self.formula_ingredient_id = formula_ingredient_id
        self.brand_id = brand_id
        self.organic_spec = organic_spec
        
    def __repr__(self):
        return f'<id:{self.id} ing_id:{self.formula_ingredient_id} brand:{self.brand_id} organic_spec:{self.organic_spec}>'