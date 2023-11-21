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

class StatusTypes(enum.Enum):
    Working_Order = "Working_Order"
    Broken = "Broken"
    Removed = "Removed"

class Equipment(Base):
    __tablename__ = 'Equipment'
    __table_args__ = {'schema': 'Manufacturing'}
    
    # Table Columns
    equipment_id: Mapped[int] = mapped_column(primary_key=True)
    process_id: Mapped[int] = mapped_column(ForeignKey('Manufacturing.Processes.process_id'))
    equipment_sn: Mapped[str] = mapped_column()
    status: Mapped[Enum(StatusTypes)] = mapped_column(default=StatusTypes.Working_Order)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    date_modified: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Relationships
    
    def __init__(self, equipment_id, process_id, equipment_sn, status, date_entered, date_modified, doc):
        self.equipment_id = equipment_id
        self.process_id = process_id
        self.equipment_sn = equipment_sn
        self.status = status
        self.date_entered = date_entered
        self.date_modified = date_modified
        self.doc = doc
        
    def __repr__(self):
        return f'<Equipment id:{self.equipment_id} equipment_sn:{self.process_id}>'

class Processes(Base):
    __tablename__ = 'Processes'
    __table_args__ = {'schema': 'Manufacturing'}
    
    # Table Columns
    process_id: Mapped[int] = mapped_column(primary_key=True)
    process_name: Mapped[str] = mapped_column()
    process_sop: Mapped[str] = mapped_column()
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    date_modified: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Relationships
    equipment: Mapped[List["Equipment"]] = relationship()
    
    def __init__(self, process_id, process_name, process_sop, date_entered, date_modified, doc):
        self.process_id = process_id
        self.process_name = process_name
        self.process_sop = process_sop
        self.date_entered = date_entered
        self.date_modified = date_modified
        self.doc = doc
        
    def __repr__(self):
        return f'<Processes id:{self.process_id} process_name:{self.process_name}>'
