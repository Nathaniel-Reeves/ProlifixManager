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

class Components(Base):
    __tablename__ = 'Inventory'
    __table_args__ = {'schema': 'Inventory'}
    
    # TODO: add columns to this table

class Component_Names(Base):
    __tablename__ = 'Component_Names'
    __table_args__ = {'schema': 'Inventory'}
    
    # TODO: add columns to this table

class Item_id(Base):
    __tablename__ = 'Item_id'
    __table_args__ = {'schema': 'Inventory'}
    
    # TODO: add columns to this table
    
class Inventory(Base):
    __tablename__ = 'Inventory'
    __table_args__ = {'schema': 'Inventory'}
    
    # TODO: add columns to this table
    
class Inventory_Log(Base):
    __tablename__ = 'Inventory_Log'
    __table_args__ = {'schema': 'Inventory'}
    
    # TODO: add columns to this table

