from __future__ import annotations
from typing import List, Literal, get_args, Optional

from sqlalchemy import Integer, Enum, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON, ENUM

from .base import Base

import datetime
import enum

class Formula_Master(Base):
    __tablename__ = 'Formula_Master'
    __table_args__ = {'schema': 'Formulas'}
    
    # Primary Key
    formula_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    label_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
    
    # Table Columns
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
    
    # Formula Versioning
    __mapper_args__ = {"version_id_col": formulation_version}
    
    # Common Methods
    def __repr__(self):
        return f'<Formula_Master formula_id:{self.formula_id} product_id:{self.product_id} version:{self.formulation_version} date_entered:{self.date_entered}>'
    
    def to_dict(self):
        return {
            "formula_id": self.formula_id,
            "product_id": self.product_id,
            "label_id": self.label_id,
            "formulation_version": self.formulation_version,
            "date_entered": self.date_entered,
            "notes": self.notes,
            "capsule_size": self.capsule_size,
            "empty_capsule_mg": self.empty_capsule_mg,
            "total_grams_per_unit": self.total_grams_per_unit,
            "total_capsules_per_unit": self.total_capsules_per_unit,
            "total_milliliters_per_unit": self.total_milliliters_per_unit,
            "fill_min": self.fill_min,
            "fill_max": self.fill_max
        }
    
    def get_id(self):
        return self.formula_id
    
    def get_id_name(self):
        return "formula_id"

class Formula_Detail(Base):
    __tablename__ = 'Formula_Detail'
    __table_args__ = {'schema': 'Formulas'}
    
    # Primary Key
    formula_detail_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    formula_id: Mapped[int] = mapped_column(ForeignKey('Formulas.Formula_Master.formula_id'))
    client_spec_group: Mapped[List["Client_Spec_Group"]] = relationship()
    primary_group: Mapped[List["Primary_Group"]] = relationship()
    secondary_group: Mapped[List["Secondary_Group"]] = relationship()
    tertiary_group: Mapped[List["Tertiary_Group"]] = relationship()
    quaternary_group: Mapped[List["Quaternary_Group"]] = relationship()
    
    # Table Columns
    percent: Mapped[float] = mapped_column(default=0.0)
    mg_per_capsule: Mapped[float] = mapped_column(default=0.0)
    ml_per_unit: Mapped[float] = mapped_column(default=0.0)
    grams_per_unit: Mapped[float] = mapped_column(default=0.0)
    organic_specs: Mapped[bool] = mapped_column(default=False)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
    notes: Mapped[str] = mapped_column(default=None)
    brand_specific: Mapped[bool] = mapped_column(default=False)
    organic_specific: Mapped[bool] = mapped_column(default=False)

    # Common Methods
    def __repr__(self):
        return f'<id:{self.formula_detail_id} formula_id:{self.formula_id} percent:{self.percent}>'
    
    def to_dict(self):
        return {
            "formula_detail_id": self.formula_detail_id,
            "formula_id": self.formula_id,
            "percent": self.percent,
            "mg_per_capsule": self.mg_per_capsule,
            "ml_per_unit": self.ml_per_unit,
            "grams_per_unit": self.grams_per_unit,
            "organic_specs": self.organic_specs,
            "ingredient_id": self.ingredient_id,
            "notes": self.notes,
            "brand_specific": self.brand_specific,
            "organic_specific": self.organic_specific
        }
    
    def get_id(self):
        return self.formula_detail_id
    
    def get_id_name(self):
        return "formula_detail_id"

OrganicSpecTypes = Literal['organic', 'non_organic', 'cut_and_sifted', 'organic_or_wildcrafted', 'wildcrafted', 'any']

class Client_Spec_Group(Base):
    __tablename__ = 'Client_Spec_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Formulas.Formula_Detail.formula_detail_id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    
    # Table Columns
    organic_spec: Mapped[OrganicSpecTypes] = mapped_column(Enum(
        *get_args(OrganicSpecTypes),
        name="OrganicSpecTypes",
        create_constraint=True,
        validate_strings=True,
        )
    )
    
    # Common Methods    
    def __repr__(self):
        return f'<id:{self.id} ing_id:{self.formula_ingredient_id} brand:{self.brand_id} organic_spec:{self.organic_spec}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "formula_ingredient_id": self.formula_ingredient_id,
            "brand_id": self.brand_id,
            "organic_spec": self.organic_spec
        }

class Primary_Group(Base):
    __tablename__ = 'Primary_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Formulas.Formula_Detail.formula_detail_id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    
    # Table Columns
    organic_spec: Mapped[OrganicSpecTypes] = mapped_column(Enum(
        *get_args(OrganicSpecTypes),
        name="OrganicSpecTypes",
        create_constraint=True,
        validate_strings=True,
        )
    )
    
    # Common Methods
    def __repr__(self):
        return f'<Primary Formula Group id:{self.id} ing_id:{self.formula_ingredient_id} brand:{self.brand_id} organic_spec:{self.organic_spec}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "formula_ingredient_id": self.formula_ingredient_id,
            "brand_id": self.brand_id,
            "organic_spec": self.organic_spec
        }
    
    def get_id(self):
        return self.id
    
    def get_id_name(self):
        return "id"

class Secondary_Group(Base):
    __tablename__ = 'Secondary_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Formulas.Formula_Detail.formula_detail_id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    
    # Table Columns
    organic_spec: Mapped[OrganicSpecTypes] = mapped_column(Enum(
        *get_args(OrganicSpecTypes),
        name="OrganicSpecTypes",
        create_constraint=True,
        validate_strings=True,
        )
    )
    
    # Common Methods
    def __repr__(self):
        return f'<Secondary Formula Group id:{self.id} ing_id:{self.formula_ingredient_id} brand:{self.brand_id} organic_spec:{self.organic_spec}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "formula_ingredient_id": self.formula_ingredient_id,
            "brand_id": self.brand_id,
            "organic_spec": self.organic_spec
        }
    
    def get_id(self):
        return self.id
    
    def get_id_name(self):
        return "id"

class Tertiary_Group(Base):
    __tablename__ = 'Tertiary_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Formulas.Formula_Detail.formula_detail_id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    
    # Table Columns
    organic_spec: Mapped[OrganicSpecTypes] = mapped_column(Enum(
        *get_args(OrganicSpecTypes),
        name="OrganicSpecTypes",
        create_constraint=True,
        validate_strings=True,
        )
    )
    
    # Common Methods
    def __repr__(self):
        return f'<Tertiary Formula Group id:{self.id} ing_id:{self.formula_ingredient_id} brand:{self.brand_id} organic_spec:{self.organic_spec}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "formula_ingredient_id": self.formula_ingredient_id,
            "brand_id": self.brand_id,
            "organic_spec": self.organic_spec
        }
    
    def get_id(self):
        return self.id
    
    def get_id_name(self):
        return "id"

class Quaternary_Group(Base):
    __tablename__ = 'Quaternary_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Formulas.Formula_Detail.formula_detail_id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    
    # Table Columns
    organic_spec: Mapped[OrganicSpecTypes] = mapped_column(Enum(
        *get_args(OrganicSpecTypes),
        name="OrganicSpecTypes",
        create_constraint=True,
        validate_strings=True,
        )
    )
    
    # Common Methods
    def __repr__(self):
        return f'<Quarternary Formula Group id:{self.id} ing_id:{self.formula_ingredient_id} brand:{self.brand_id} organic_spec:{self.organic_spec}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "formula_ingredient_id": self.formula_ingredient_id,
            "brand_id": self.brand_id,
            "organic_spec": self.organic_spec
        }
    
    def get_id(self):
        return self.id
    
    def get_id_name(self):
        return "id"