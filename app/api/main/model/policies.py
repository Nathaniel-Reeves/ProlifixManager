from __future__ import annotations
from typing import List

from sqlalchemy import Enum, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON

from .base import Base

import datetime

# CREATE TABLE `Policies`.`Regulations` (
#   `regulation_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `unique_regulation` varchar(255) NOT NULL DEFAULT CONCAT(`regulation_date`, '-', `title`, '-', `section`) UNIQUE,
#   `title` varchar(8) NOT NULL,
#   `chapter` varchar(8) DEFAULT NULL,
#   `subchapter` varchar(8) DEFAULT NULL,
#   `part` varchar(8) DEFAULT NULL,
#   `subpart` varchar(8) DEFAULT NULL,
#   `regulation_date` varchar(16) NOT NULL,
#   `section` varchar(8) NOT NULL,
#   `timestamp_entered` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
#   `timestamp_modified` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
#   PRIMARY KEY (`regulation_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

class Regulations(Base):
    """Regulations ORM Model"""
    __tablename__ = 'Regulations'
    __table_args__ = {'schema': 'Policies'}

    # Primary Key
    regulation_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships

    # Table Columns
    unique_regulation: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    chapter: Mapped[str] = mapped_column(default=None)
    subchapter: Mapped[str] = mapped_column(default=None)
    part: Mapped[str] = mapped_column(default=None)
    subpart: Mapped[str] = mapped_column(default=None)
    regulation_date: Mapped[str] = mapped_column()
    section: Mapped[str] = mapped_column()
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Regulation id:{self.regulation_id} title:{self.title} section:{self.section}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "regulation_id": self.regulation_id,
            "unique_regulation": self.unique_regulation,
            "title": self.title,
            "chapter": self.chapter,
            "subchapter": self.subchapter,
            "part": self.part,
            "subpart": self.subpart,
            "regulation_date": self.regulation_date,
            "section": self.section,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }

    def get_id(self):
        """Get Row Id"""
        return self.regulation_id

    def get_id_name(self):
        """Get Row Id and Name"""
        return 'regulation_id'

# CREATE TABLE `Policies`.`Documents` (
#   `document_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `title` varchar(255) NOT NULL,
#   `subtitle` varchar(255) DEFAULT NULL,
#   `description` varchar(255) DEFAULT NULL,
#   `abv` varchar(8) DEFAULT NULL,
#   `revision` int(10) unsigned DEFAULT 1,
#   `timestamp_entered` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
#   `timestamp_modified` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
#   PRIMARY KEY (`document_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

class Documents(Base):
    """Documents ORM Model"""
    __tablename__ = 'Documents'
    __table_args__ = {'schema': 'Policies'}

    # Primary Key
    document_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships

    # Table Columns
    title: Mapped[str] = mapped_column()
    subtitle: Mapped[str] = mapped_column(default=None)
    description: Mapped[str] = mapped_column(default=None)
    abv: Mapped[str] = mapped_column(default=None)
    revision: Mapped[int] = mapped_column(default=1)
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Document id:{self.document_id} title:{self.title}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "document_id": self.document_id,
            "title": self.title,
            "subtitle": self.subtitle,
            "description": self.description,
            "abv": self.abv,
            "revision": self.revision,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }

    def get_id(self):
        """Get Row Id"""
        return self.document_id

    def get_id_name(self):
        """Get Row Id and Name"""
        return 'document_id'

# CREATE TABLE `Policies`.`Chapters` (
#   `chapter_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `document_id` int(10) unsigned NOT NULL,
#   `title` varchar(255) NOT NULL,
#   `subtitle` varchar(255) DEFAULT NULL,
#   `description` varchar(255) DEFAULT NULL,
#   `revision` int(10) unsigned DEFAULT 1,
#   `timestamp_entered` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
#   `timestamp_modified` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
#   PRIMARY KEY (`chapter_id`),
#   KEY `document_id` (`document_id`),
#   CONSTRAINT `Chapters_ibfk_1` FOREIGN KEY (`document_id`) REFERENCES `Documents` (`document_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

class Chapters(Base):
    """Chapters ORM Model"""
    __tablename__ = 'Chapters'
    __table_args__ = {'schema': 'Policies'}

    # Primary Key
    chapter_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    document_id: Mapped[int] = mapped_column(ForeignKey('Policies.Documents.document_id'))

    # Table Columns
    title: Mapped[str] = mapped_column()
    subtitle: Mapped[str] = mapped_column(default=None)
    description: Mapped[str] = mapped_column(default=None)
    revision: Mapped[int] = mapped_column(default=1)
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Chapter id:{self.chapter_id} title:{self.title}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "chapter_id": self.chapter_id,
            "document_id": self.document_id,
            "title": self.title,
            "subtitle": self.subtitle,
            "description": self.description,
            "revision": self.revision,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }

    def get_id(self):
        """Get Row Id"""
        return self.chapter_id

    def get_id_name(self):
        """Get Row Id and Name"""
        return 'chapter_id'

# CREATE TABLE `Policies`.`Chapter_Regulation_Join` (
#   `_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `regulation_id` int(10) unsigned,
#   `chapter_id` int(10) unsigned,
#   `timestamp_entered` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
#   `timestamp_modified` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
#   KEY `regulation_id` (`regulation_id`),
#   KEY `chapter_id` (`chapter_id`),
#   PRIMARY KEY (`_id`),
#   CONSTRAINT `Chapter_Regulation_Join_ibfk_1` FOREIGN KEY (`regulation_id`) REFERENCES `Regulations` (`regulation_id`),
#   CONSTRAINT `Chapter_Regulation_Join_ibfk_2` FOREIGN KEY (`chapter_id`) REFERENCES `Chapters` (`chapter_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

class Chapter_Regulation_Join(Base):
    """Chapter_Regulation_Join ORM Model"""
    __tablename__ = 'Chapter_Regulation_Join'
    __table_args__ = {'schema': 'Policies'}

    # Primary Key
    _id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    regulation_id: Mapped[int] = mapped_column(ForeignKey('Policies.Regulations.regulation_id'))
    chapter_id: Mapped[int] = mapped_column(ForeignKey('Policies.Chapters.chapter_id'))

    # Table Columns
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Chapter_Regulation_Join id:{self._id} regulation_id:{self.regulation_id} chapter_id:{self.chapter_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "_id": self._id,
            "regulation_id": self.regulation_id,
            "chapter_id": self.chapter_id,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }

    def get_id(self):
        """Get Row Id"""
        return self._id

    def get_id_name(self):
        """Get Row Id and Name"""
        return '_id'

# CREATE TABLE `Policies`.`Chapter_Sections` (
#   `section_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `chapter_id` int(10) unsigned NOT NULL,
#   `title` varchar(255) NOT NULL,
#   `subtitle` varchar(255) DEFAULT NULL,
#   `content` longtext DEFAULT NULL,
#   `timestamp_entered` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
#   `timestamp_modified` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
#   PRIMARY KEY (`section_id`),
#   KEY `chapter_id` (`chapter_id`),
#   CONSTRAINT `Chapter_Sections_ibfk_1` FOREIGN KEY (`chapter_id`) REFERENCES `Chapters` (`chapter_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

class Chapter_Sections(Base):
    """Chapter_Sections ORM Model"""
    __tablename__ = 'Chapter_Sections'
    __table_args__ = {'schema': 'Policies'}

    # Primary Key
    section_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    chapter_id: Mapped[int] = mapped_column(ForeignKey('Policies.Chapters.chapter_id'))

    # Table Columns
    title: Mapped[str] = mapped_column()
    subtitle: Mapped[str] = mapped_column(default=None)
    content: Mapped[str] = mapped_column(default=None)
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Chapter_Sections id:{self.section_id} title:{self.title}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "section_id": self.section_id,
            "chapter_id": self.chapter_id,
            "title": self.title,
            "subtitle": self.subtitle,
            "content": self.content,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }

    def get_id(self):
        """Get Row Id"""
        return self.section_id

    def get_id_name(self):
        """Get Row Id and Name"""
        return 'section_id'

# CREATE TABLE `Policies`.`Authors_Join` (
#   `author_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `user_id` int(10) unsigned NOT NULL,
#   `document_id` int(10) unsigned NOT NULL,
#   `chapter_id` int(10) unsigned NOT NULL,
#   `timestamp_entered` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
#   `timestamp_modified` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
#   PRIMARY KEY (`author_id`),
#   KEY `user_id` (`user_id`),
#   KEY `document_id` (`document_id`),
#   KEY `chapter_id` (`chapter_id`),
#   CONSTRAINT `Authors_Join_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Organizations`.`Users` (`user_id`),
#   CONSTRAINT `Authors_Join_ibfk_2` FOREIGN KEY (`chapter_id`) REFERENCES `Chapters` (`chapter_id`),
#   CONSTRAINT `Authors_Join_ibfk_3` FOREIGN KEY (`document_id`) REFERENCES `Documents` (`document_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

class Authors_Join(Base):
    """Authors_Join ORM Model"""
    __tablename__ = 'Authors_Join'
    __table_args__ = {'schema': 'Policies'}

    # Primary Key
    author_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    user_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Users.user_id'))
    document_id: Mapped[int] = mapped_column(ForeignKey('Policies.Documents.document_id'))
    chapter_id: Mapped[int] = mapped_column(ForeignKey('Policies.Chapters.chapter_id'))

    # Table Columns
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Author id:{self.author_id} user_id:{self.user_id} document_id:{self.document_id} chapter_id:{self.chapter_id}>'

    def to_dict(self):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        return {
            "author_id": self.author_id,
            "user_id": self.user_id,
            "document_id": self.document_id,
            "chapter_id": self.chapter_id,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }

    def get_id(self):
        """Get Row Id"""
        return self.author_id

    def get_id_name(self):
        """Get Row Id and Name"""
        return 'author_id'
