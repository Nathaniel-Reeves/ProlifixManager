from __future__ import annotations
from typing import List, Literal, get_args, Optional

from sqlalchemy import Integer, Enum, ForeignKey, Column
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON, ENUM

import datetime
import enum

class Base(DeclarativeBase):
    pass

RiskLevels = Literal["UNKNOWN", "No_Risk", "Low_Risk", "Medium_Risk", "High_Risk"]

class Organizations(Base):
    __tablename__ = 'Organizations'
    __table_args__ = {'schema': 'Organizations'}
    
    # Primary Key
    organization_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    # 1 to M
    organization_names: Mapped[List["Organization_Names"]] = relationship()
    people: Mapped[Optional["People"]] = relationship()
    facilities: Mapped[Optional["Facilities"]] = relationship()

    # Table Columns
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    website_url: Mapped[str] = mapped_column(default=None)
    vetted: Mapped[bool] = mapped_column()
    date_vetted: Mapped[datetime.datetime] = mapped_column()
    risk_level: Mapped[RiskLevels] = mapped_column(Enum(
        *get_args(RiskLevels),
        name="RiskLevels",
        create_constraint=True,
        validate_strings=True,
    ))
    supplier: Mapped[bool] = mapped_column(default=False)
    client: Mapped[bool] = mapped_column(default=False)
    lab: Mapped[bool] = mapped_column(default=False)
    courier: Mapped[bool] = mapped_column(default=False)
    other: Mapped[bool] = mapped_column(default=False)
    
    doc = Column(MutableDict.as_mutable(JSON))

    def __init__(self, organization_id, website_url, vetted, date_vetted, date_entered, risk_level, supplier, client, lab, courier, other, doc):
        self.organization_id = organization_id
        self.website_url = website_url
        self.vetted = vetted
        self.date_vetted = date_vetted
        self.date_entered = date_entered
        self.risk_level = risk_level
        self.supplier = supplier
        self.client = client
        self.lab = lab
        self.courier = courier
        self.other = other
        self.doc = doc
        

    def __repr__(self):
        return f'<Organization {self.organization_id, self.website_url}>'
    
    def to_dict(self):
        return {
            'organization_id': self.organization_id,
            'website_url': self.website_url,
            'vetted': self.vetted,
            'date_vetted': self.date_vetted,
            'date_entered': self.date_entered,
            'risk_level': self.risk_level,
            'supplier': self.supplier,
            'client': self.client,
            'lab': self.lab,
            'courier': self.courier,
            'other': self.other,
            'doc': self.doc
        }
    
    def get_id(self):
        return self.organization_id

class Organization_Names(Base):
    __tablename__ = 'Organization_Names'
    __table_args__ = {'schema': 'Organizations'}
    
    # Primary Key
    name_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    # M to 1
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    
    # Table Columns
    organization_name: Mapped[str] = mapped_column(default=None)
    organization_initial: Mapped[str] = mapped_column(default=None)
    primary_name: Mapped[bool] = mapped_column(default=False)
    
    def __init__(self, name_id, organization_id, organization_name, organization_initial, primary_name):
        self.name_id = name_id
        self.organization_id = organization_id
        self.organization_name = organization_name
        self.organization_initial = organization_initial
        self.primary_name = primary_name
    
    def __repr__(self):
        return f'<Organization_Name {self.name_id}, {self.organization_id}, {self.organization_name}>'
    
    def to_dict(self):
        return {
            'name_id': self.name_id,
            'organization_id': self.organization_id,
            'organization_name': self.organization_name,
            'organization_initial': self.organization_initial,
            'primary_name': self.primary_name
        }
    
    def get_id(self):
        return self.name_id

class People(Base):
    __tablename__ = 'People'
    __table_args__ = {'schema': 'Organizations'}
    
    # Primary Key
    person_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    # M to 1
    organization_id: Mapped[int] = mapped_column(
            ForeignKey('Organizations.Organizations.organization_id')
        )

    # 1 to 1
    # user_id: Mapped[int] = mapped_column(ForeignKey('Organization.Users.user_id'))
    
    # Table Columns
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
    
    def to_dict(self):
        return {
            'person_id': self.person_id,
            'organization_id': self.organization_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'job_description': self.job_description,
            'department': self.department,
            'phone_number_primary': self.phone_number_primary,
            'phone_number_secondary': self.phone_number_secondary,
            'email_address_primary': self.email_address_primary,
            'email_address_secondary': self.email_address_secondary,
            'birthday': self.birthday,
            'is_employee': self.is_employee,
            'contract_date': self.contract_date,
            'termination_date': self.termination_date,
            'clock_number': self.clock_number
        }
    
    def getName(self):
        return f'{self.first_name} {self.last_name}'


ColorThemes = Literal["Light", "Dark"]

class Users(Base):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'Organizations'}
    
    # Primary Key
    user_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    # 1 to 1
    person_id: Mapped[int] = mapped_column(ForeignKey('People.People.person_id'))
    
    # Table Columns
    username: Mapped[str] = mapped_column(default=None)
    encrypted_password: Mapped[str] = mapped_column(default=None)
    profile_picture: Mapped[str] = mapped_column(default=None)
    color_theme: Mapped[ColorThemes] = mapped_column(Enum(
            *get_args(ColorThemes),
            name="ColorThemes",
            create_constraint=True,
            validate_strings=True,
        ))
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    def __init__(self, user_id, username, encrypted_password, profile_picture, color_theme):
        self.user_id = user_id
        self.username = username
        self.encrypted_password = encrypted_password
        self.profile_picture = profile_picture
        self.color_theme = color_theme
    
    def __repr__(self):
        return f'<User {self.user_id}, {self.username}>'

BuildingTypes = Literal["Head_Office", "Office", "Distribution_Warehouse", "Manufacture_Facility", "Storefront"]

TimeUnits = Literal["Unknown", "Days", "Weeks", "Months"]

class Facilities(Base):
    __tablename__ = 'Facilities'
    __table_args__ = {'schema': 'Organizations'}
    
    # Primary Key
    facility_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    # M to 1
    organization_id: Mapped[int] = mapped_column(
            ForeignKey('Organizations.Organizations.organization_id')
        )
    
    # Table Columns
    building_type: Mapped[BuildingTypes] = mapped_column(Enum(
        *get_args(BuildingTypes),
        name="BuildingTypes",
        create_constraint=True,
        validate_strings=True,
    ))
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
    ship_time_units: Mapped[TimeUnits] = mapped_column(Enum(
        *get_args(TimeUnits),
        name="TimeUnits",
        create_constraint=True,
        validate_strings=True,
    ))
    ship_time_in_days: Mapped[int] = mapped_column()
    notes: Mapped[str] = mapped_column()
    
    def __init__(self, facility_id, organization_id, building_type, building_name, street_1_number, street_1_type, street_1_direction, street_1_name, street_2_number, street_2_type, street_2_direction, address_type, address_type_identifier, local_municipality, city_town, governing_district, postal_area, country, ship_time, ship_time_units, ship_in_days, notes):
        self.facility_id = facility_id
        self.organization_id = organization_id
        self.building_type = building_type
        self.building_name = building_name
        self.street_1_number = street_1_number
        self.street_1_type = street_1_type
        self.street_1_direction = street_1_direction
        self.street_1_name = street_1_name
        self.street_2_number = street_2_number
        self.street_2_type = street_2_type
        self.street_2_direction = street_2_direction
        self.address_type = address_type
        self.address_type_identifier = address_type_identifier
        self.local_municipality = local_municipality
        self.city_town = city_town
        self.governing_district = governing_district
        self.postal_area = postal_area
        self.country = country
        self.ship_time = ship_time
        self.ship_time_units = ship_time_units
        self.ship_time_in_days = ship_in_days
        self.notes = notes
        
    def __repr__(self):
        return f'<Facility {self.facility_id}, {self.building_name}, {self.country}, {self.governing_district}, {self.city_town}>'
