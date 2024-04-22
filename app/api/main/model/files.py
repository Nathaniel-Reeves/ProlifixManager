from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Files(Base):
    """Files ORM Model"""
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
    ref_count: Mapped[int] = mapped_column()

    # Common Methods
    def __repr__(self):
        return f'<File Record hash:{self.file_hash}'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "file_hash": self.file_hash,
            "file_name": self.file_name,
            "file_type": self.file_type,
            "file_pointer": self.file_pointer,
            "id_code": self.id_code,
            "pg": self.pg,
            "ref_count": self.ref_count
        }

    def get_id(self):
        """Get Row Id"""
        return self.file_hash

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "file_hash"
