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
    date_entered: Mapped[datetime.datetime] = mapped_column(default=None)
    spec_revise_date: Mapped[datetime.datetime] = mapped_column(default=None)
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
    num_product_variants: Mapped[int] = mapped_column()

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
            'num_manufacturing_versions': self.num_manufacturing_versions,
            'num_product_variants': self.num_product_variants
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

    timeUnits = ('Seconds', 'Minutes', 'Hours', 'Days')

    # Table Columns
    process_spec_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    date_entered: Mapped[datetime.datetime] = mapped_column(default=None)
    date_modified: Mapped[datetime.datetime] = mapped_column(default=None)
    current_default_process: Mapped[bool] = mapped_column(default=True)
    process_order: Mapped[int] = mapped_column(default=1)
    special_instruction: Mapped[str] = mapped_column(default=None)
    manufacturing_process_version: Mapped[int] = mapped_column(default=None)
    custom_setup_time: Mapped[float] = mapped_column(default=None)
    custom_setup_time_units: Mapped[int] = mapped_column(Enum(
        *timeUnits,
        name="timeUnits1",
        create_constraint=True,
        validate_strings=True,
    ))
    custom_setup_num_employees: Mapped[int] = mapped_column(default=None)
    custom_setup_time_use_default: Mapped[bool] = mapped_column(default=True)
    custom_cleaning_time: Mapped[float] = mapped_column(default=None)
    custom_cleaning_time_units: Mapped[int] = mapped_column(Enum(
        *timeUnits,
        name="timeUnits2",
        create_constraint=True,
        validate_strings=True,
    ))
    custom_cleaning_num_employees: Mapped[int] = mapped_column(default=None)
    custom_cleaning_time_use_default: Mapped[bool] = mapped_column(default=True)
    position: Mapped[str] = mapped_column(default=None)
    type: Mapped[str] = mapped_column(default=None)
    qty_per_box: Mapped[int] = mapped_column(default=None)
    box_weight_in_lbs: Mapped[float] = mapped_column(default=None)
    box_sticker_required: Mapped[bool] = mapped_column(default=False)
    percent_loss: Mapped[float] = mapped_column(default=0)
    target_process_rate: Mapped[float] = mapped_column(default=None)
    targetProcessRateUnit = ('Products', 'Barrels', 'Kilos', 'Liters', 'Capsules', 'Ingredients', 'Batches')
    target_process_rate_unit: Mapped[int] = mapped_column(Enum(
        *targetProcessRateUnit,
        name="targetProcessRateUnit",
        create_constraint=True,
        validate_strings=True,
    ))
    target_process_rate_per: Mapped[float] = mapped_column(default=None)
    target_process_rate_per_unit: Mapped[int] = mapped_column(Enum(
        *timeUnits,
        name="timeUnits3",
        create_constraint=True,
        validate_strings=True,
    ))
    target_process_num_employees: Mapped[int] = mapped_column(default=None)
    primary_process: Mapped[bool] = mapped_column(default=False)
    max_pallet_layers: Mapped[int] = mapped_column()
    boxes_per_layer: Mapped[int] = mapped_column()
    bid_notes: Mapped[str] = mapped_column(default=None)
    custom_ave_percent_loss: Mapped[float] = mapped_column(default=None)
    use_default_ave_percent_loss: Mapped[bool] = mapped_column(default=True)

    # Relationships
    manufacturing_process_id: Mapped[int] = mapped_column(ForeignKey('Manufacturing.Processes.process_id'))
    variant_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Variant.variant_id'))
    box_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'))

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
            'manufacturing_process_version': self.manufacturing_process_version,
            'custom_setup_time': self.custom_setup_time,
            'custom_setup_time_units': self.custom_setup_time_units,
            'custom_setup_num_employees': self.custom_setup_num_employees,
            'custom_setup_time_use_default': self.custom_setup_time_use_default,
            'custom_cleaning_time': self.custom_cleaning_time,
            'custom_cleaning_time_units': self.custom_cleaning_time_units,
            'custom_cleaning_num_employees': self.custom_cleaning_num_employees,
            'custom_cleaning_time_use_default': self.custom_cleaning_time_use_default,
            'position': self.position,
            'type': self.type,
            'variant_id': self.variant_id,
            'qty_per_box': self.qty_per_box,
            'box_weight_in_lbs': self.box_weight_in_lbs,
            'box_sticker_required': self.box_sticker_required,
            'percent_loss': self.percent_loss,
            'target_process_rate': self.target_process_rate,
            'target_process_rate_unit': self.target_process_rate_unit,
            'target_process_rate_per': self.target_process_rate_per,
            'target_process_rate_per_unit': self.target_process_rate_per_unit,
            'target_process_num_employees': self.target_process_num_employees,
            'primary_process': self.primary_process,
            'max_pallet_layers': self.max_pallet_layers,
            'boxes_per_layer': self.boxes_per_layer,
            'box_id': self.box_id,
            'bid_notes': self.bid_notes,
            'custom_ave_percent_loss': self.custom_ave_percent_loss,
            'use_default_ave_percent_loss': self.use_default_ave_percent_loss
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
    date_entered: Mapped[datetime.datetime] = mapped_column(default=None)
    formulation_version: Mapped[int] = mapped_column(default=1)
    notes: Mapped[str] = mapped_column(default=None)

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
            'notes': self.notes
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
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Products.Formula_Detail.formula_ingredient_id'), nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'), nullable=False)
    priority: Mapped[int] = mapped_column(nullable=False)

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
    formula_ingredient_id: Mapped[int] = mapped_column(ForeignKey('Products.Formula_Detail.formula_ingredient_id'), nullable=False)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'), nullable=False)
    priority: Mapped[int] = mapped_column(nullable=False)

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
    process_component_id: Mapped[int] = mapped_column(ForeignKey('Products.Process_Components.process_component_id'), nullable=False)
    component_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'), nullable=False)
    priority: Mapped[int] = mapped_column(nullable=False)

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
    process_component_id: Mapped[int] = mapped_column(ForeignKey('Products.Process_Components.process_component_id'), nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'), nullable=False)
    priority: Mapped[int] = mapped_column(nullable=False)

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
    id: Mapped[int] =  mapped_column(primary_key=True)

    __table_args__ = {'schema': 'Products'}

    # Relationships
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    source: Mapped[int] = mapped_column(ForeignKey('Products.Manufacturing_Process.process_spec_id'))
    target: Mapped[int] = mapped_column(ForeignKey('Products.Manufacturing_Process.process_spec_id'))

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
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "product_id": self.product_id,
            "label": self.label,
            "animated": self.animated,
            "marker_end": self.marker_end
        }

    def get_id(self):
        """Get Row Id"""
        return self.id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "id"

class Product_Variant(Base):
    """Product Variant ORM Model"""
    __tablename__ = 'Product_Variant'
    __table_args__ = {'schema': 'Products'}

    # Table Columns
    variant_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    variant_title: Mapped[str] = mapped_column()
    VariantTypes = ("powder", "liquid", "capsule")
    variant_type: Mapped[int] = mapped_column(Enum(
        *VariantTypes,
        name="VariantTypes",
        create_constraint=True,
        validate_strings=True
    ))
    date_entered: Mapped[datetime.datetime] = mapped_column(default=None)
    date_modified: Mapped[datetime.datetime] = mapped_column(default=None)
    primary_variant: Mapped[bool] = mapped_column(default=False)
    discontinued: Mapped[bool] = mapped_column(default=False)
    discontinued_reason: Mapped[str] = mapped_column(default=None)
    notes: Mapped[str] = mapped_column(default=None)
    total_grams_per_unit: Mapped[float] = mapped_column(default=None)
    total_capsules_per_unit: Mapped[float] = mapped_column(default=None)
    total_mg_per_capsule: Mapped[float] = mapped_column(default=None)
    mg_empty_capsule: Mapped[float] = mapped_column(default=None)
    CapsuleSizes = ("1","2","0","00")
    capsule_size: Mapped[int] = mapped_column(Enum(
        *CapsuleSizes,
        name="CapsuleSizes",
        create_constraint=True,
        validate_strings=True,
        default=None
        ))
    total_milliliters_per_unit: Mapped[float] = mapped_column(default=None)
    min_grams_per_unit: Mapped[float] = mapped_column(default=None)
    max_grams_per_unit: Mapped[float] = mapped_column(default=None)
    min_mg_per_capsule: Mapped[float] = mapped_column(default=None)
    max_mg_per_capsule: Mapped[float] = mapped_column(default=None)
    min_milliliters_per_unit: Mapped[float] = mapped_column(default=None)
    max_milliliters_per_unit: Mapped[float] = mapped_column(default=None)
    variant_title_suffix: Mapped[str] = mapped_column()

    # Relationships

    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Product_Variant id:{self.variant_id} product_id:{self.product_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            'variant_id': self.variant_id,
            'product_id': self.product_id,
            'variant_title': self.variant_title,
            'variant_type': self.variant_type,
            'date_entered': self.date_entered,
            'date_modified': self.date_modified,
            'primary_variant': self.primary_variant,
            'discontinued': self.discontinued,
            'discontinued_reason': self.discontinued_reason,
            'notes': self.notes,
            'total_grams_per_unit': self.total_grams_per_unit,
            'total_capsules_per_unit': self.total_capsules_per_unit,
            'total_mg_per_capsule': self.total_mg_per_capsule,
            'mg_empty_capsule': self.mg_empty_capsule,
            'capsule_size': self.capsule_size,
            'total_milliliters_per_unit': self.total_milliliters_per_unit,
            'min_grams_per_unit': self.min_grams_per_unit,
            'max_grams_per_unit': self.max_grams_per_unit,
            'min_mg_per_capsule': self.min_mg_per_capsule,
            'max_mg_per_capsule': self.max_mg_per_capsule,
            'min_milliliters_per_unit': self.min_milliliters_per_unit,
            'max_milliliters_per_unit': self.max_milliliters_per_unit,
            'variant_title_suffix': self.variant_title_suffix
        }

    def get_id(self):
        """Get Row Id"""
        return self.variant_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "variant_id"