from __future__ import annotations
from typing import List, Optional

from sqlalchemy import Integer, Enum, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON, ENUM

from .base import Base

import datetime

class Equipment(Base):
    __tablename__ = 'Equipment'
    __table_args__ = {'schema': 'Manufacturing'}
    
    # Primary Key
    equipment_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    process_id: Mapped[int] = mapped_column(ForeignKey('Manufacturing.Processes.process_id'))
    
    # Table Columns
    equipment_sn: Mapped[str] = mapped_column()
    StatusTypes = ("Working Order", "Broken", "Removed")
    status: Mapped[int] = mapped_column(Enum(
        *StatusTypes,
        name="StatusTypes",
        create_constraint=True,
        validate_strings=True,
        ))
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    date_modified: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Common Methods
    def __repr__(self):
        return f'<Equipment id:{self.equipment_id} equipment_sn:{self.process_id}>'
    
    def to_dict(self):
        return {
            "equipment_id": self.equipment_id,
            "process_id": self.process_id,
            "equipment_sn": self.equipment_sn,
            "status": self.status,
            "date_entered": self.date_entered,
            "date_modified": self.date_modified,
            "doc": self.doc
        }
        
    def get_id(self):
        return self.equipment_id
    
    def get_id_name(self):
        return "equipment_id"

class Processes(Base):
    __tablename__ = 'Processes'
    __table_args__ = {'schema': 'Manufacturing'}
    
    # Primary Key
    process_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    equipment: Mapped[List["Equipment"]] = relationship()
    
    # Table Columns
    process_name: Mapped[str] = mapped_column()
    process_sop: Mapped[str] = mapped_column()
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    date_modified: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Common Methods        
    def __repr__(self):
        return f'<Processes id:{self.process_id} process_name:{self.process_name}>'
    
    def to_dict(self):
        return {
            "process_id": self.process_id,
            "process_name": self.process_name,
            "process_sop": self.process_sop,
            "date_entered": self.date_entered,
            "date_modified": self.date_modified,
            "doc": self.doc
        }
        
    def get_id(self):
        return self.process_id
    
    def get_id_name(self):
        return "process_id"
