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

class Equipment(Base):
    __tablename__ = 'Equipment'
    __table_args__ = {'schema': 'Manufacturing'}
    
    # TODO: add columns to this table

class Processes(Base):
    __tablename__ = 'Processes'
    __table_args__ = {'schema': 'Manufacturing'}
    
    # TODO: add columns to this table
