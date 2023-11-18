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

class Sales_Orders(Base):
    __tablename__ = 'Sales_Orders'
    __table_args__ = {'schema': 'Orders'}
    
    # TODO: Add table columns

class Sales_Order_Detail(Base):
    __tablename__ = 'Sales_Order_Detail'
    __table_args__ = {'schema': 'Sales_Orders'}
    
    # TODO: Add table columns
    
class Sales_Order_Payments(Base):
    __tablename__ = 'Sales_Order_Payments'
    __table_args__ = {'schema': 'Sales_Orders'}
    
    # TODO: Add table columns
    
class Lot_Numbers(Base):
    __tablename__ = 'Lot_Numbers'
    __table_args__ = {'schema': 'Sales_Orders'}
    
    # TODO: Add table columns
    
class Purchase_Orders(Base):
    __tablename__ = 'Purchase_Orders'
    __table_args__ = {'schema': 'Orders'}
    
    # TODO: Add table columns

class Purchase_Order_Detail(Base):
    __tablename__ = 'Purchase_Order_Detail'
    __table_args__ = {'schema': 'Purchase_Orders'}
    
    # TODO: Add table columns
    
    