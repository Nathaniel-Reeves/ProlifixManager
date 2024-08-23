from __future__ import annotations
from typing import List

from sqlalchemy import Enum, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON

from .base import Base

import datetime

class Equipment(Base):
    """Equipment ORM Model"""
    __tablename__ = 'Equipment'
    __table_args__ = {'schema': 'Manufacturing'}

    # Primary Key
    equipment_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    process_id: Mapped[int] = mapped_column(ForeignKey('Manufacturing.Processes.process_id'))

    # Table Columns
    equipment_sn: Mapped[str] = mapped_column()
    StatusTypes = ("Working_Order", "Broken", "Removed")
    status: Mapped[int] = mapped_column(Enum(
        *StatusTypes,
        name="StatusTypes",
        create_constraint=True,
        validate_strings=True,
        ))
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    equipment_history = Column(MutableDict.as_mutable(JSON))

    equipment_name: Mapped[str] = mapped_column(default=None)

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Equipment id:{self.equipment_id} equipment_sn:{self.process_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "equipment_id": self.equipment_id,
            "process_id": self.process_id,
            "equipment_sn": self.equipment_sn,
            "status": self.status,
            "equipment_history": self.equipment_history,
            "equipment_name": self.equipment_name,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }

    def get_id(self):
        """Get Row Id"""
        return self.equipment_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "equipment_id"

class Processes(Base):
    """Processes ORM Model"""
    __tablename__ = 'Processes'
    __table_args__ = {'schema': 'Manufacturing'}

    # Primary Key
    process_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    equipment: Mapped[List["Equipment"]] = relationship()

    timeUnits = ('Seconds', 'Minutes', 'Hours', 'Days')

    # Table Columns
    process_name: Mapped[str] = mapped_column()
    process_sop: Mapped[str] = mapped_column()
    rework_process: Mapped[bool] = mapped_column(default=False)
    min_personnel: Mapped[int] = mapped_column(default=0)
    max_personnel: Mapped[int] = mapped_column(default=0)
    bpr_page_template: Mapped[str] = mapped_column()
    bpr_data_template = Column(JSON, default={})
    component_filters = Column(JSON, default=[])
    requires_product_variant: Mapped[bool] = mapped_column(default=False)
    requires_components: Mapped[bool] = mapped_column(default=False)
    requires_box_specs: Mapped[bool] = mapped_column(default=False)
    requires_samples: Mapped[bool] = mapped_column(default=False)
    requires_retention: Mapped[bool] = mapped_column(default=False)
    top_handle: Mapped[bool] = mapped_column(default=True)
    bottom_handle: Mapped[bool] = mapped_column(default=False)
    left_handle: Mapped[bool] = mapped_column(default=False)
    right_handle: Mapped[bool] = mapped_column(default=False)
    ave_percent_loss: Mapped[float] = mapped_column()
    setup_time: Mapped[float] = mapped_column(default=None)
    setup_time_units: Mapped[int] = mapped_column(Enum(
        *timeUnits,
        name="timeUnits1",
        create_constraint=True,
        validate_strings=True,
    ))
    setup_num_employees: Mapped[int] = mapped_column(default=None)
    cleaning_time: Mapped[float] = mapped_column(default=None)
    cleaning_time_units: Mapped[int] = mapped_column(Enum(
        *timeUnits,
        name="timeUnits2",
        create_constraint=True,
        validate_strings=True,
    ))
    cleaning_num_employees: Mapped[int] = mapped_column(default=None)
    process_sop_link: Mapped[str] = mapped_column()
    equipment_specific: Mapped[bool] = mapped_column(default=False)
    VariantTypes = ("powder", "liquid", "capsule")
    product_variant_type: Mapped[int] = mapped_column(Enum(
        *VariantTypes,
        name="VariantTypes",
        create_constraint=True,
        validate_strings=True
    ))
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Processes id:{self.process_id} process_name:{self.process_name}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "process_id": self.process_id,
            "process_name": self.process_name,
            "process_sop": self.process_sop,
            "rework_process": self.rework_process,
            "min_personnel": self.min_personnel,
            "max_personnel": self.max_personnel,
            "bpr_page_template": self.bpr_page_template,
            "bpr_data_template": self.bpr_data_template,
            "requires_samples": self.requires_samples,
            "requires_retention": self.requires_retention,
            "requires_product_variant": self.requires_product_variant,
            "requires_components": self.requires_components,
            "requires_box_specs": self.requires_box_specs,
            "top_handle": self.top_handle,
            "bottom_handle": self.bottom_handle,
            "left_handle": self.left_handle,
            "right_handle": self.right_handle,
            "ave_percent_loss": self.ave_percent_loss,
            "setup_time": self.setup_time,
            "setup_time_units": self.setup_time_units,
            "setup_num_employees": self.setup_num_employees,
            "cleaning_time": self.cleaning_time,
            "cleaning_time_units": self.cleaning_time_units,
            "cleaning_num_employees": self.cleaning_num_employees,
            "process_sop_link": self.process_sop_link,
            "equipment_specific": self.equipment_specific,
            "product_variant_type": self.product_variant_type,
            "component_filters": self.component_filters,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }

    def get_id(self):
        """Get Row Id"""
        return self.process_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "process_id"
