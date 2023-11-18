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

class Formula_Master(Base):
    __tablename__ = 'Formula_Master'
    __table_args__ = {'schema': 'Formulas'}
    
    #TODO: add columns to this table

class Formula_Detail(Base):
    __tablename__ = 'Formula_Detail'
    __table_args__ = {'schema': 'Formulas'}
    
    #TODO: add columns to this table

class Client_Spec_Group(Base);
    __tablename__ = 'Client_Spec_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    #TODO: add columns to this table

class Primary_Group(Base);
    __tablename__ = 'Primary_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    #TODO: add columns to this table

class Secondary_Group(Base);
    __tablename__ = 'Secondary_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    #TODO: add columns to this table

class Tertiary_Group(Base);
    __tablename__ = 'Tertiary_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    #TODO: add columns to this table

class Quaternary_Group(Base);
    __tablename__ = 'Quaternary_Group'
    __table_args__ = {'schema': 'Formulas'}
    
    #TODO: add columns to this table