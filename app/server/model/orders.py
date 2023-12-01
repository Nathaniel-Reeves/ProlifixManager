from __future__ import annotations
from typing import List, Literal, get_args, Optional

from sqlalchemy import Integer, Enum, ForeignKey, Column, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON, ENUM

from .base import Base

import datetime
import enum

ExpirationTypes = Literal["Best_By", "Exp"]

class Sales_Orders(Base):
    __tablename__ = 'Sales_Orders'
    __table_args__ = {'schema': 'Orders'}
    
    # Primary Key
    prefix: Mapped[str] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(primary_key=True)
    sec_number: Mapped[int] = mapped_column(primary_key=True)
    suffix: Mapped[str] = mapped_column(primary_key=True)
    
    # Relationships
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    sales_orders_payments: Mapped[List["Sales_Orders_Payments"]] = relationship()
    sale_order_detail: Mapped[List["Sale_Order_Detail"]] = relationship()
    
    # Table Columns
    client_po_num: Mapped[str] = mapped_column(default=None)
    order_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    target_completion_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    completion_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    billed_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    closed_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    down_payment_actual: Mapped[float] = mapped_column(default=None)
    theoretical_po_amount: Mapped[float] = mapped_column(default=None)
    total_paid: Mapped[float] = mapped_column(default=None)
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Common Methods
    def __repr__(self):
        return f'<Sales_Order SO#{self.prefix}{self.year}~{self.month}~{self.sec_number}{self.suffix}>'
    
    def to_dict(self):
        return {
            'prefix': self.prefix,
            'year': self.year,
            'month': self.month,
            'sec_number': self.sec_number,
            'suffix': self.suffix,
            'organization_id': self.organization_id,
            'client_po_num': self.client_po_num,
            'order_date': self.order_date,
            'target_completion_date': self.target_completion_date,
            'completion_date': self.completion_date,
            'date_entered': self.date_entered,
            'billed_date': self.billed_date,
            'closed_date': self.closed_date,
            'down_payment_actual': self.down_payment_actual,
            'theoretical_po_amount': self.theoretical_po_amount,
            'total_paid': self.total_paid,
            'doc': self.doc
        }
    
    def get_id(self):
        return str(self.prefix) + str(self.year) + str(self.month) + str(self.sec_number)
    
    def get_id_name(self):
        return (
            "prefix",
            "year",
            "month",
            "sec_number",
            "suffix"
        )

class Sale_Order_Detail(Base):
    __tablename__ = 'Sale_Order_Detail'
    __table_args__ = {'schema': 'Orders'}
    
    # Primary Key
    so_detail_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    prefix: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    sec_number: Mapped[int] = mapped_column(nullable=False)
    suffix: Mapped[str] = mapped_column(nullable=False)
    fk_constraint = ForeignKeyConstraint( 
                    [
                        prefix, 
                        year, 
                        month, 
                        sec_number,
                        suffix
                    ], 
                    [
                        "Orders.Sales_Orders.prefix", 
                        "Orders.Sales_Orders.year", 
                        "Orders.Sales_Orders.month", 
                        "Orders.Sales_Orders.sec_number",
                        "Orders.Sales_Orders.suffix"
                    ], 
                    name="Sales_Order_Number_fk"
                )
    __table_args__ = (fk_constraint, {
        'schema': 'Orders'
    })
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    lot_numbers: Mapped[List["Lot_Numbers"]] = relationship()
    
    # Table Columns
    unit_order_qty: Mapped[int] = mapped_column(default=None)
    kilos_order_qty: Mapped[float] = mapped_column(default=None)
    special_instructions: Mapped[str] = mapped_column(default=None)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    bit_price_per_unit: Mapped[float] = mapped_column(default=None)
    final_ship_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Common Methods
    def __repr__(self):
        return f'<Sales_Order_Detail SO#{self.prefix}{self.year}~{self.month}~{self.sec_number} Product_id:{self.product_id} Qty:{self.unit_order_qty}{self.kilos_order_qty}{self.suffix}>'
    
    def to_dict(self):
        return {
            'prefix': self.prefix,
            'year': self.year,
            'month': self.month,
            'sec_number': self.sec_number,
            'suffix': self.suffix,
            'product_id': self.product_id,
            'unit_order_qty': self.unit_order_qty,
            'kilos_order_qty': self.kilos_order_qty,
            'special_instructions': self.special_instructions,
            'date_entered': self.date_entered,
            'bit_price_per_unit': self.bit_price_per_unit,
            'final_ship_date': self.final_ship_date,
            'doc': self.doc
        }
    
    def get_id(self):
        return self.so_detail_id
    
    def get_id_name(self):
        return "so_detail_id"
    
PaymentTypes = Literal["down_payment", "other", "final_payment"]
    
class Sales_Orders_Payments(Base):
    __tablename__ = 'Sales_Order_Payments'
    __table_args__ = {'schema': 'Orders'}
    
    # Primay Key
    payment_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    prefix: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    sec_number: Mapped[int] = mapped_column(nullable=False)
    suffix: Mapped[str] = mapped_column(nullable=False)
    fk_constraint = ForeignKeyConstraint( 
                    [
                        prefix, 
                        year, 
                        month, 
                        sec_number,
                        suffix
                    ], 
                    [
                        "Orders.Sales_Orders.prefix", 
                        "Orders.Sales_Orders.year", 
                        "Orders.Sales_Orders.month", 
                        "Orders.Sales_Orders.sec_number",
                        "Orders.Sales_Orders.suffix"
                    ], 
                    name="Sales_Order_Number_fk"
                )
    __table_args__ = (fk_constraint, {
        'schema': 'Orders'
    })
    
    # Table Columns
    payment_amount: Mapped[float] = mapped_column(default=None)
    payment_type: Mapped[PaymentTypes] = mapped_column(Enum(
        *get_args(PaymentTypes),
        name="PaymentTypes",
        create_constraint=True,
        validate_strings=True,
        ))
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Common Methods
    def __repr__(self):
        return f'<Sales_Order_Payments SO#{self.prefix}{self.year}~{self.month}~{self.sec_number} Type:{self.payment_type} Amount:{self.payment_amount}{self.suffix}>'
    
    def to_dict(self):
        return {
            'prefix': self.prefix,
            'year': self.year,
            'month': self.month,
            'sec_number': self.sec_number,
            'suffix': self.suffix,
            'payment_type': self.payment_type,
            'payment_amount': self.payment_amount,
            'date_entered': self.date_entered,
            'doc': self.doc
        }
    
    def get_id(self):
        return self.payment_id
    
    def get_id_name(self):
        return "payment_id"
    
class Lot_Numbers(Base):
    __tablename__ = 'Lot_Numbers'
    __table_args__ = {'schema': 'Orders'}
    
    # Primary Key
    prefix: Mapped[str] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(primary_key=True)
    sec_number: Mapped[int] = mapped_column(primary_key=True)
    suffix: Mapped[str] = mapped_column(primary_key=True)
    
    # Relationships
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    so_detail_id: Mapped[int] = mapped_column(ForeignKey('Orders.Sale_Order_Detail.so_detail_id'))
    
    # Table Columns
    target_unit_yield: Mapped[int] = mapped_column(default=None)
    actual_unit_yield: Mapped[int] = mapped_column(default=None)
    retentions: Mapped[int] = mapped_column(default=None)
    total_shippable_product: Mapped[int] = mapped_column(default=None)
    batch_printed: Mapped[bool] = mapped_column(default=False)
    bpr_printed: Mapped[bool] = mapped_column(default=False)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    exp_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    exp_type: Mapped[ExpirationTypes] = mapped_column(Enum(
        *get_args(ExpirationTypes),
        name="ExpirationTypes",
        create_constraint=True,
        validate_strings=True,
        ))
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Common Methods
    def __repr__(self):
        return f'<Lot_Numbers Lot#:{self.prefix} {self.year}{self.month}{self.sec_number} {self.suffix} Product_id:{self.product_id} >'
    
    def to_dict(self):
        return {
            'prefix': self.prefix,
            'year': self.year,
            'month': self.month,
            'sec_number': self.sec_number,
            'suffix': self.suffix,
            'product_id': self.product_id,
            'target_unit_yield': self.target_unit_yield,
            'actual_unit_yield': self.actual_unit_yield,
            'retentions': self.retentions,
            'total_shippable_product': self.total_shippable_product,
            'batch_printed': self.batch_printed,
            'bpr_printed': self.bpr_printed,
            'date_entered': self.date_entered,
            'exp_date': self.exp_date,
            'exp_type': self.exp_type,
            'doc': self.doc
        }
    
    def get_id(self):
        return str(self.prefix) + str(self.year) + str(self.month) + str(self.sec_number)
    
    def get_id_name(self):
        return (
            "prefix",
            "year",
            "month",
            "sec_number",
            "suffix"
        )

class Purchase_Orders(Base):
    __tablename__ = 'Purchase_Orders'
    __table_args__ = {'schema': 'Orders'}
    
    # Primary Key
    prefix: Mapped[str] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(primary_key=True)
    sec_number: Mapped[int] = mapped_column(primary_key=True)
    suffix: Mapped[str] = mapped_column(primary_key=True)
    
    # Relationships
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    purchase_order_details: Mapped[List["Purchase_Order_Detail"]] = relationship()
    
    # Table Columns
    supplier_so_num: Mapped[str] = mapped_column(default=None)
    order_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    eta_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    doc = Column(MutableDict.as_mutable(JSON))

    # Common Methods
    def __repr__(self):
        return f'<Purchase_Orders PO#:{self.prefix} {self.year}{self.month}{self.sec_number} >'
    
    def to_dict(self):
        return {
            'prefix': self.prefix,
            'year': self.year,
            'month': self.month,
            'sec_number': self.sec_number,
            'organization_id': self.organization_id,
            'supplier_so_num': self.supplier_so_num,
            'order_date': self.order_date,
            'eta_date': self.eta_date,
            'date_entered': self.date_entered,
            'doc': self.doc
        }
    
    def get_id(self):
        return str(self.prefix) + str(self.year) + str(self.month) + str(self.sec_number)
    
    def get_id_name(self):
        return (
            "prefix",
            "year",
            "month",
            "sec_number"
        )

class Purchase_Order_Detail(Base):
    __tablename__ = 'Purchase_Order_Detail'
    __table_args__ = {'schema': 'Orders'}
    
    # Primary Key
    po_detail_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    po_detail_id: Mapped[int] = mapped_column(primary_key=True)
    prefix: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    suffix: Mapped[str] = mapped_column(nullable=False)
    sec_number: Mapped[int] = mapped_column(nullable=False)
    fk_constraint = ForeignKeyConstraint( 
                    [
                        prefix, 
                        year, 
                        month, 
                        sec_number
                    ], 
                    [
                        "Orders.Purchase_Orders.prefix", 
                        "Orders.Purchase_Orders.year", 
                        "Orders.Purchase_Orders.month", 
                        "Orders.Purchase_Orders.sec_number"
                    ], 
                    name="Purchase_Order_Number_fk"
                )
    __table_args__ = (fk_constraint, {
        'schema': 'Orders'
    })
    component_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'), nullable=False)

    # Table Columns
    unit_order_qty: Mapped[int] = mapped_column(default=None)
    kilos_order_qty: Mapped[float] = mapped_column(default=None)
    special_instructions: Mapped[str] = mapped_column(default=None)
    datetime_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    bid_price_per_unit: Mapped[float] = mapped_column(default=None)
    bid_price_per_kilo: Mapped[float] = mapped_column(default=None)
    
    doc = Column(MutableDict.as_mutable(JSON))

    # Common Methods    
    def __repr__(self):
        return f'<Purchase_Order_Detail PO#:{self.prefix} {self.year}{self.month}{self.sec_number} >'
    
    def to_dict(self):
        return {
            'po_detail_id': self.po_detail_id,
            'prefix': self.prefix,
            'year': self.year,
            'month': self.month,
            'sec_number': self.sec_number,
            'component_id': self.component_id,
            'unit_order_qty': self.unit_order_qty,
            'kilos_order_qty': self.kilos_order_qty,
            'special_instructions': self.special_instructions,
            'datetime_entered': self.datetime_entered,
            'bid_price_per_unit': self.bid_price_per_unit,
            'bid_price_per_kilo': self.bid_price_per_kilo,
            'doc': self.doc
        }
    
    def get_id(self):
        return self.po_detail_id
    
    def get_id_name(self):
        return "po_detail_id"
    
    
