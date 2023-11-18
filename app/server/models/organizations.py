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

class RiskLevels(enum.Enum):
    UNKNOWN = 'UNKNOWN'
    No_Risk = 'No_Risk'
    Low_Risk = 'Low_Risk'
    Medium_Risk = 'Medium_Risk'
    High_Risk = 'High_Risk'

class Organizations(Base):
    __tablename__ = 'Organizations'
    __table_args__ = {'schema': 'Organizations'}

    # Table Columns
    organization_id: Mapped[int] = mapped_column(primary_key=True)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    website_url: Mapped[str] = mapped_column(default=None)
    vetted: Mapped[bool] = mapped_column()
    date_vetted: Mapped[datetime.datetime] = mapped_column()
    supplier: Mapped[bool] = mapped_column(default=False)
    client: Mapped[bool] = mapped_column(default=False)
    lab: Mapped[bool] = mapped_column(default=False)
    courier: Mapped[bool] = mapped_column(default=False)
    other: Mapped[bool] = mapped_column(default=False)
    
    doc = Column(MutableDict.as_mutable(JSON))
    risk_level = Column(Enum(RiskLevels))
    
    # Relationships
    organization_names: Mapped[List["Organization_Names"]] = relationship()
    people: Mapped[List["People"]] = relationship()
    facilities: Mapped[List["Facilities"]] = relationship()
    

    def __init__(self, organization_id, website_url):
        self.organization_id = organization_id
        self.website_url = website_url

    def __repr__(self):
        return f'<Organization {self.organization_id, self.website_url}>'

class Organization_Names(Base):
    __tablename__ = 'Organization_Names'
    __table_args__ = {'schema': 'Organizations'}
    
    # Table Columns
    name_id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    organization_name: Mapped[str] = mapped_column(default=None)
    organization_initial: Mapped[str] = mapped_column(default=None)
    primary_name: Mapped[bool] = mapped_column(default=False)
    
    # Relationships

    
    def __init__(self, name_id, organization_id, organization_name, organization_initial, primary_name):
        self.name_id = name_id
        self.organization_id = organization_id
        self.organization_name = organization_name
        self.organization_initial = organization_initial
        self.primary_name = primary_name
    
    def __repr__(self):
        return f'<Organization_Name {self.name_id}, {self.organization_id}, {self.organization_name}>'

    
class People(Base):
    __tablename__ = 'People'
    __table_args__ = {'schema': 'Organizations'}
    
    # Table Columns
    person_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(default=None)
    last_name: Mapped[str] = mapped_column(default=None)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    job_description: Mapped[str] = mapped_column(default=None)
    department: Mapped[str] = mapped_column(default=None)
    phone_number_primary: Mapped[str] = mapped_column(default=None)
    phone_number_secondary: Mapped[str] = mapped_column(default=None)
    email_address_primary: Mapped[str] = mapped_column(default=None)
    email_address_secondary: Mapped[str] = mapped_column(default=None)
    birthday: Mapped[datetime.datetime] = mapped_column()
    is_employee: Mapped[bool] = mapped_column(default=False)
    contract_date: Mapped[datetime.datetime] = mapped_column()
    termination_date: Mapped[datetime.datetime] = mapped_column()
    clock_number: Mapped[str] = mapped_column(default=None)
    
    # Relationships
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    users: Mapped[List["Users"]] = relationship()
    
    def __init__(self, person_id, organization_id, first_name, last_name, job_description, department, phone_number_primary, phone_number_secondary, email_primary, email_address_secondary, birthday, is_employee, contract_date, termination_date, clock_number):
        self.person_id = person_id
        self.organization_id = organization_id
        self.first_name = first_name
        self.last_name = last_name
        self.job_description = job_description
        self.department = department
        self.phone_number_primary = phone_number_primary
        self.phone_number_secondary = phone_number_secondary
        self.email_address_primary = email_primary
        self.email_address_secondary = email_address_secondary
        self.birthday = birthday
        self.is_employee = is_employee
        self.contract_date = contract_date
        self.termination_date = termination_date
        self.clock_number = clock_number

    def __repr__(self):
        return f'<Person {self.person_id}, {self.first_name}, {self.last_name}>'
    
    def getName(self):
        return f'{self.first_name} {self.last_name}'

class ColorThemes(enum.Enum):
    LIGHT = 'Light'
    DARK = 'Dark'

class Users(Base):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'Organizations'}
    
    # Table Columns
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(default=None)
    encrypted_password: Mapped[str] = mapped_column(default=None)
    profile_picture: Mapped[str] = mapped_column(default=None)
    
    doc = Column(MutableDict.as_mutable(JSON))
    color_theme = Column(Enum(ColorThemes))
    
    # Relationships
    person_id: Mapped[int] = mapped_column(ForeignKey('Organizations.People.person_id'))
    
    def __init__(self, user_id, username, encrypted_password, profile_picture, color_theme):
        self.user_id = user_id
        self.username = username
        self.encrypted_password = encrypted_password
        self.profile_picture = profile_picture
        self.color_theme = color_theme
    
    def __repr__(self):
        return f'<User {self.user_id}, {self.username}>'

class BuildingTypes(enum.Enum):
    Head_Office = "Head_Office"
    Office = "Office"
    Distribution_Warehouse = "Distribution_Warehouse"
    Manufacture_Facility = "Manufacture_Facility"
    Storefront = "Storefront"

class TimeUnits(enum.Enum):
    Unknown = "Unknown"
    Days = "Days"
    Weeks = "Weeks"
    Months = "Months"

class Facilities(Base):
    __tablename__ = 'Facilities'
    __table_args__ = {'schema': 'Organizations'}
    
    # Table Columns
    facility_id: Mapped[int] = mapped_column(primary_key=True)
    building_name: Mapped[str] = mapped_column()
    street_1_number: Mapped[int] = mapped_column()
    street_1_number_suffix: Mapped[str] = mapped_column()
    street_1_name: Mapped[str] = mapped_column()
    street_1_type: Mapped[str] = mapped_column()
    street_1_direction: Mapped[str] = mapped_column()
    street_2_number: Mapped[int] = mapped_column()
    street_2_number_suffix: Mapped[str] = mapped_column()
    street_2_name: Mapped[str] = mapped_column()
    street_2_type: Mapped[str] = mapped_column()
    street_2_direction: Mapped[str] = mapped_column()
    address_type: Mapped[str] = mapped_column()
    address_type_identifier: Mapped[str] = mapped_column()
    local_municipality: Mapped[str] = mapped_column()
    city_town: Mapped[str] = mapped_column()
    governing_district: Mapped[str] = mapped_column()
    postal_area: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    ship_time: Mapped[int] = mapped_column()
    ship_time_in_days: Mapped[int] = mapped_column()
    notes: Mapped[str] = mapped_column()
    
    building_type = Column(Enum(BuildingTypes))
    ship_time_units = Column(Enum(TimeUnits))
    
    # Relationships
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
