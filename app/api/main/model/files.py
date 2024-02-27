from __future__ import annotations
from typing import List, Optional

from sqlalchemy import Integer, Enum, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON, ENUM

from .base import Base

import datetime

class Files(Base):
    __tablename__ = 'Files'
    __table_args__ = {'schema': 'Files'}
    
    # Primary Key
    file_hash: Mapped[str] = mapped_column(primary_key=True)
    
    # Relationships
    
    # Table Columns
    file_name: Mapped[str] = mapped_column()
    file_type: Mapped[str] = mapped_column()
    file_pointer: Mapped[str] = mapped_column()
    id_code: Mapped[str] = mapped_column()
    pg: Mapped[str] = mapped_column()
    
    # Common Methods
    def __repr__(self):
        return f'<File Record hash:{self.file_hash}'
    
    def to_dict(self):
        return {
            "file_hash": self.file_hash,
            "file_name": self.file_name,
            "file_type": self.file_type,
            "file_pointer": self.file_pointer,
            "id_code": self.id_code,
            "pg": self.pg
        }
    
    def get_id(self):
        return self.file_hash
    
    def get_id_name(self):
        return "file_hash"