from __future__ import annotations
import datetime

from sqlalchemy import Enum, ForeignKey, Column, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON

from .base import Base

class Product_Master(Base):
    """Product Master ORM Model"""
    __tablename__ = 'Product_Master'
    __table_args__ = {'schema': 'Products'}

    # Table Columns
    product_id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    product_name: Mapped[str] = mapped_column()
    current_product: Mapped[bool] = mapped_column()
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    spec_revise_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    TimeUnits = ("Years", "Months", "Days")
    exp_unit: Mapped[int] = mapped_column(Enum(
        *TimeUnits,
        name="TimeUnits",
        create_constraint=True,
        validate_strings=True,
        ))
    ExpirationTypes = ("Best_By", "Exp")
    exp_type: Mapped[int] = mapped_column(Enum(
        *ExpirationTypes,
        name="ExpirationTypes",
        create_constraint=True,
        validate_strings=True,
        ))
    exp_time_frame: Mapped[int] = mapped_column()
    exp_use_oldest_ingredient: Mapped[bool] = mapped_column(default=False)
    default_formula_id: Mapped[int] = mapped_column(ForeignKey('Formula_Master.formula_id'))
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
    default_formula_version: Mapped[int] = mapped_column(default=1)
    num_formula_versions: Mapped[int] = mapped_column(default=1)
    default_manufacturing_version: Mapped[int] = mapped_column(default=1)
    num_manufacturing_versions: Mapped[int] = mapped_column(default=1)

    doc = Column(MutableDict.as_mutable(JSON))

    # Relationships
    # formulas: Mapped[List["Formula_Master"]] = relationship()
    # lot_numbers: Mapped[List["Lot_Numbers"]] = relationship()
    # items: Mapped[List["Item_id"]] = relationship()

    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Product_Master id:{self.product_id} org_id:{self.organization_id} {self.product_name}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            'product_id': self.product_id,
            'organization_id': self.organization_id,
            'product_name': self.product_name,
            'current_product': self.current_product,
            'date_entered': self.date_entered,
            'exp_unit': self.exp_unit,
            'exp_type': self.exp_type,
            'exp_time_frame': self.exp_time_frame,
            'exp_use_oldest_ingredient': self.exp_use_oldest_ingredient,
            'default_formula_id': self.default_formula_id,
            'certified_fda': self.certified_fda,
            'certified_gmp': self.certified_gmp,
            'certified_made_with_organic': self.certified_made_with_organic,
            'certified_wildcrafted': self.certified_wildcrafted,
            'certified_usda_organic': self.certified_usda_organic,
            'certified_halal': self.certified_halal,
            'certified_kosher': self.certified_kosher,
            'certified_gluten_free': self.certified_gluten_free,
            'certified_national_sanitation_foundation': self.certified_national_sanitation_foundation,
            'certified_us_pharmacopeia': self.certified_us_pharmacopeia,
            'certified_non_gmo': self.certified_non_gmo,
            'certified_vegan': self.certified_vegan,
            'doc': self.doc,
            'default_formula_version': self.default_formula_version,
            'num_formula_versions': self.num_formula_versions,
            'default_manufacturing_version': self.default_manufacturing_version,
            'num_manufacturing_versions': self.num_manufacturing_versions
        }

    def get_id(self):
        """Get Row Id"""
        return self.product_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "product_id"

class Manufacturing_Process(Base):
    """Manufacturing Process ORM Model"""
    __tablename__ = 'Manufacturing_Process'
    __table_args__ = {'schema': 'Products'}

    # Table Columns
    process_spec_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    date_modified: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    current_default_process: Mapped[bool] = mapped_column(default=True)
    process_order: Mapped[int] = mapped_column(default=1)
    special_instruction: Mapped[str] = mapped_column(default=None)
    manufacturing_process_id: Mapped[int] = mapped_column()
    process_bid_cost: Mapped[float] = mapped_column(default=None)
    manufacturing_process_version: Mapped[int] = mapped_column(default=None)
    position: Mapped[str] = mapped_column(default=None)
    type: Mapped[str] = mapped_column(default=None)

    # Relationships

    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Manufacturing_Process id:{self.process_spec_id} product_id:{self.product_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            'process_spec_id': self.process_spec_id,
            'product_id': self.product_id,
            'date_entered': self.date_entered,
            'date_modified': self.date_modified,
            'current_default_process': self.current_default_process,
            'process_order': self.process_order,
            'special_instruction': self.special_instruction,
            'manufacturing_process_id': self.manufacturing_process_id,
            'process_bid_cost': self.process_bid_cost,
            'manufacturing_process_version': self.manufacturing_process_version,
            'position': self.position,
            'type': self.type
        }

    def get_id(self):
        """Get Row Id"""
        return self.process_spec_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "process_spec_id"

class Formula_Master(Base):
    """Formula Master ORM Model"""
    __tablename__ = 'Formula_Master'
    __table_args__ = {'schema': 'Products'}

    # Table Columns
    formula_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    formulation_version: Mapped[int] = mapped_column(default=1)
    notes: Mapped[str] = mapped_column(default=None)
    total_grams_per_unit: Mapped[float] = mapped_column()
    total_capsules_per_unit: Mapped[float] = mapped_column()
    total_milliliters_per_unit: Mapped[float] = mapped_column()
    min_grams_per_unit: Mapped[float] = mapped_column()
    max_grams_per_unit: Mapped[float] = mapped_column()
    min_mg_per_capsule: Mapped[float] = mapped_column()
    max_mg_per_capsule: Mapped[float] = mapped_column()
    min_milliliters_per_unit: Mapped[float] = mapped_column()
    max_milliliters_per_unit: Mapped[float] = mapped_column()
    total_mg_per_capsule: Mapped[float] = mapped_column()
    mg_empty_capsule: Mapped[float] = mapped_column()
    CapsuleSizes = ("1","2","0","00")
    capsule_size: Mapped[int] = mapped_column(Enum(
        *CapsuleSizes,
        name="CapsuleSizes",
        create_constraint=True,
        validate_strings=True,
        ))
    capsule_weight: Mapped[float] = mapped_column()

    # Relationships

    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Formula_Master id:{self.formula_id} product_id:{self.product_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            'formula_id': self.formula_id,
            'product_id': self.product_id,
            'date_entered': self.date_entered,
            'formulation_version': self.formulation_version,
            'notes': self.notes,
            'total_grams_per_unit': self.total_grams_per_unit,
            'total_capsules_per_unit': self.total_capsules_per_unit,
            'total_milliliters_per_unit': self.total_milliliters_per_unit,
            'min_grams_per_unit': self.min_grams_per_unit,
            'max_grams_per_unit': self.max_grams_per_unit,
            'min_mg_per_capsule': self.min_mg_per_capsule,
            'max_mg_per_capsule': self.max_mg_per_capsule,
            'min_milliliters_per_unit': self.min_milliliters_per_unit,
            'max_milliliters_per_unit': self.max_milliliters_per_unit,
            'total_mg_per_capsule': self.total_mg_per_capsule,
            'mg_empty_capsule': self.mg_empty_capsule,
            'capsule_size': self.capsule_size,
            'capsule_weight': self.capsule_weight
        }

    def get_id(self):
        """Get Row Id"""
        return self.formula_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "formula_id"

class Formula_Detail(Base):
    """Formula Detail ORM Model"""
    __tablename__ = 'Formula_Detail'
    __table_args__ = {'schema': 'Products'}

    # Table Columns
    formula_ingredient_id: Mapped[int] = mapped_column(primary_key=True)
    formula_id: Mapped[int] = mapped_column(ForeignKey('Products.Formula_Master.formula_id'))
    percent: Mapped[float] = mapped_column()
    mg_per_capsule: Mapped[float] = mapped_column()
    ml_per_unit: Mapped[float] = mapped_column()
    grams_per_unit: Mapped[float] = mapped_column()
    notes: Mapped[str] = mapped_column(default=None)
    specific_brand_required: Mapped[bool] = mapped_column(default=False)
    specific_ingredient_required: Mapped[bool] = mapped_column(default=False)

    # Relationships

    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Formula_Detail id:{self.formula_ingredient_id} formula_id:{self.formula_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            'formula_ingredient_id': self.formula_ingredient_id,
            'formula_id': self.formula_id,
            'percent': self.percent,
            'mg_per_capsule': self.mg_per_capsule,
            'ml_per_unit': self.ml_per_unit,
            'grams_per_unit': self.grams_per_unit,
            'notes': self.notes,
            'specific_brand_required': self.specific_brand_required,
            'specific_ingredient_required': self.specific_ingredient_required
        }

    def get_id(self):
        """Get Row Id"""
        return self.formula_ingredient_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "formula_ingredient_id"

class Ingredient_Brands_Join(Base):
    """Ingredient Brands Join ORM Model"""
    __tablename__ = 'Ingredient_Brands_Join'
    __table_args__ = {'schema': 'Products'}

    # Table Columns
    _id: Mapped[int] = mapped_column(primary_key=True)
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Products.Formula_Detail.formula_ingredient_id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    priority: Mapped[int] = mapped_column()

    # Relationships

    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Ingredient_Brands_Join id:{self._id} formula_ingredient_id:{self.formula_ingredient_id} brand_id:{self.brand_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            '_id': self._id,
            'formula_ingredient_id': self.formula_ingredient_id,
            'brand_id': self.brand_id,
            'priority': self.priority
        }

    def get_id(self):
        """Get Row Id"""
        return self._id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "_id"

class Ingredients_Join(Base):
    """Ingredients Join ORM Model"""
    __tablename__ = 'Ingredients_Join'
    __table_args__ = {'schema': 'Products'}

    # Table Columns
    _id: Mapped[int] = mapped_column(primary_key=True)
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Products.Formula_Detail.formula_ingredient_id'))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
    priority: Mapped[int] = mapped_column()

    # Relationships

    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Ingredients_Join id:{self._id} formula_ingredient_id:{self.formula_ingredient_id} ingredient_id:{self.ingredient_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            '_id': self._id,
            'formula_ingredient_id': self.formula_ingredient_id,
            'ingredient_id': self.ingredient_id,
            'priority': self.priority
        }

    def get_id(self):
        """Get Row Id"""
        return self._id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "_id"

class Process_Components(Base):
    """Process Components ORM Model"""
    __tablename__ = 'Process_Components'
    __table_args__ = {'schema': 'Products'}

    # Table Columns
    process_component_id: Mapped[int] = mapped_column(primary_key=True)
    process_spec_id: Mapped[int] = mapped_column(ForeignKey('Products.Manufacturing_Process.process_spec_id'))
    specific_component_required: Mapped[bool] = mapped_column(default=False)
    specific_brand_required: Mapped[bool] = mapped_column(default=False)
    qty_per_unit: Mapped[float] = mapped_column()

    # Relationships

    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Process_Components id:{self.process_component_id} process_spec_id:{self.process_spec_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            'process_component_id': self.process_component_id,
            'process_spec_id': self.process_spec_id,
            'specific_component_required': self.specific_component_required,
            'specific_brand_required': self.specific_brand_required,
            'qty_per_unit': self.qty_per_unit
        }

    def get_id(self):
        """Get Row Id"""
        return self.process_component_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "process_component_id"

class Components_Join(Base):
    """Components Join ORM Model"""
    __tablename__ = 'Components_Join'
    __table_args__ = {'schema': 'Products'}

    # Table Columns
    _id: Mapped[int] = mapped_column(primary_key=True)
    process_component_id: Mapped[int] = mapped_column(ForeignKey('Products.Process_Components.process_component_id'))
    component_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))
    priority: Mapped[int] = mapped_column()

    # Relationships

    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Components_Join id:{self._id} process_component_id:{self.process_component_id} component_id:{self.component_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            '_id': self._id,
            'process_component_id': self.process_component_id,
            'component_id': self.component_id,
            'priority': self.priority
        }

    def get_id(self):
        """Get Row Id"""
        return self._id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "_id"

class Component_Brands_Join(Base):
    """Component Brands Join ORM Model"""
    __tablename__ = 'Component_Brands_Join'
    __table_args__ = {'schema': 'Products'}

    # Table Columns
    _id: Mapped[int] = mapped_column(primary_key=True)
    process_component_id: Mapped[int] = mapped_column(ForeignKey('Products.Process_Components.process_component_id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    priority: Mapped[int] = mapped_column()

    # Relationships

    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Component_Brands_Join id:{self._id} process_component_id:{self.process_component_id} brand_id:{self.brand_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            '_id': self._id,
            'process_component_id': self.process_component_id,
            'brand_id': self.brand_id,
            'priority': self.priority
        }

    def get_id(self):
        """Get Row Id"""
        return self._id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "_id"

class Manufacturing_Process_Edges(Base):
    """Manufacturing Process Edges ORM Model"""
    __tablename__ = 'Manufacturing_Process_Edges'

    # Primary Key
    source: Mapped[int] = mapped_column(primary_key=True)
    target: Mapped[int] = mapped_column(primary_key=True)

    __table_args__ = (ForeignKeyConstraint([source, target],
                                           [Manufacturing_Process.process_spec_id, Manufacturing_Process.process_spec_id]),
                      {'schema': 'Products'})

    # Relationships
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))

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

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Manufacturing_Process_Edge source:{self.source} target:{self.target} product_id:{self.product_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "id": f"{self.source}-{self.target}",
            "source": self.source,
            "target": self.target,
            "product_id": self.product_id,
            "label": self.label,
            "animated": self.animated,
            "marker_end": self.marker_end
        }

    def get_id(self):
        """Get Row Id"""
        return (self.source, self.target)

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "(source, target)"