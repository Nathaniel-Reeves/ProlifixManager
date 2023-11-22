from __future__ import annotations
from typing import List, Literal, get_args

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy import Integer, Enum, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import Column
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON

import datetime
import enum

from connector import Base

ExpirationTypes = Literal["Best_By", "Exp"]

class Sales_Orders(Base):
    __tablename__ = 'Sales_Orders'
    __table_args__ = {'schema': 'Orders'}
    
    # Table Columns
    prefix: Mapped[str] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(primary_key=True)
    sec_number: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
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
    
    # Relationships
    sales_orders_payments: Mapped[List["Sales_Orders_Payments"]] = relationship()
    sale_order_detail: Mapped[List["Sale_Order_Detail"]] = relationship()
    
    def __init__(self, prefix, year, month, sec_number, organization_id, client_po_num, order_date, target_completion_date, completion_date, date_entered, billed_date, closed_date, down_payment_actual, theoretical_po_amount, total_paid, doc):
        self.prefix = prefix
        self.year = year
        self.month = month
        self.sec_number = sec_number
        self.organization_id = organization_id
        self.client_po_num = client_po_num
        self.order_date = order_date
        self.target_completion_date = target_completion_date
        self.completion_date = completion_date
        self.date_entered = date_entered
        self.billed_date = billed_date
        self.closed_date = closed_date
        self.down_payment_actual = down_payment_actual
        self.theoretical_po_amount = theoretical_po_amount
        self.total_paid = total_paid
        self.doc = doc
    
    def __repr__(self):
        return f'<Sales_Order SO#{self.prefix}{self.year}~{self.month}~{self.sec_number}>'

class Sale_Order_Detail(Base):
    __tablename__ = 'Sales_Order_Detail'
    __table_args__ = {'schema': 'Orders'}
    
    # Primary Key
    so_detail_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships
    lot_numbers: Mapped[List["Lot_Numbers"]] = relationship()
    prefix: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    sec_number: Mapped[int] = mapped_column(nullable=False)
    fk_constraint = ForeignKeyConstraint( 
                    [
                        prefix, 
                        year, 
                        month, 
                        sec_number
                    ], 
                    [
                        "Orders.Sales_Orders.prefix", 
                        "Orders.Sales_Orders.year", 
                        "Orders.Sales_Orders.month", 
                        "Orders.Sales_Orders.sec_number"
                    ], 
                    name="Sales_Order_Number_fk"
                )
    __table_args__ = (fk_constraint, {
        'schema': 'Orders'
    })
    
    
    # Table Columns
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    unit_order_qty: Mapped[int] = mapped_column(default=None)
    kilos_order_qty: Mapped[float] = mapped_column(default=None)
    special_instructions: Mapped[str] = mapped_column(default=None)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    bit_price_per_unit: Mapped[float] = mapped_column(default=None)
    final_ship_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    
    def __init__(self, so_detail_id, prefix, year, month, sec_number, product_id, unit_order_qty, kilos_order_qty, special_instructions, date_entered, bit_price_per_unit, final_ship_date, doc):
        self.so_detail_id = so_detail_id
        self.prefix = prefix
        self.year = year
        self.month = month
        self.sec_number = sec_number
        self.product_id = product_id
        self.unit_order_qty = unit_order_qty
        self.kilos_order_qty = kilos_order_qty
        self.special_instructions = special_instructions
        self.date_entered = date_entered
        self.bit_price_per_unit = bit_price_per_unit
        self.final_ship_date = final_ship_date
        self.doc = doc
    
    def __repr__(self):
        return f'<Sales_Order_Detail SO#{self.prefix}{self.year}~{self.month}~{self.sec_number} Product_id:{self.product_id} Qty:{self.unit_order_qty}{self.kilos_order_qty}>'
    
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
    fk_constraint = ForeignKeyConstraint( 
                    [
                        prefix, 
                        year, 
                        month, 
                        sec_number
                    ], 
                    [
                        "Orders.Sales_Orders.prefix", 
                        "Orders.Sales_Orders.year", 
                        "Orders.Sales_Orders.month", 
                        "Orders.Sales_Orders.sec_number"
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
    
    def __init__(self, so_detail_id, prefix, year, month, sec_number, payment_amount, payment_type, date_entered, doc):
        self.so_detail_id = so_detail_id
        self.prefix = prefix
        self.year = year
        self.month = month
        self.sec_number = sec_number
        self.payment_amount = payment_amount
        self.payment_type = payment_type
        self.date_entered = date_entered
        self.doc = doc
        
    def __repr__(self):
        return f'<Sales_Order_Payments SO#{self.prefix}{self.year}~{self.month}~{self.sec_number} Type:{self.payment_type} Amount:{self.payment_amount}>'
    
class Lot_Numbers(Base):
    __tablename__ = 'Lot_Numbers'
    __table_args__ = {'schema': 'Orders'}
    
    # Table Columns
    prefix: Mapped[str] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(primary_key=True)
    sec_number: Mapped[int] = mapped_column(primary_key=True)
    suffix: Mapped[str] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    so_detail_id: Mapped[int] = mapped_column(ForeignKey('Orders.Sales_Order_Detail.so_detail_id'))
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
    
    def __init__(self, prefix, year, month, sec_number, suffix, product_id, so_detail_id, target_unit_yield, actual_unit_yield, retentions, total_shippable_product, batch_printed, bpr_printed, date_entered, exp_date, exp_type, doc):
        self.prefix = prefix
        self.year = year
        self.month = month
        self.sec_number = sec_number
        self.suffix = suffix
        self.product_id = product_id
        self.so_detail_id = so_detail_id
        self.target_unit_yield = target_unit_yield
        self.actual_unit_yield = actual_unit_yield
        self.retentions = retentions
        self.total_shippable_product = total_shippable_product
        self.batch_printed = batch_printed
        self.bpr_printed = bpr_printed
        self.date_entered = date_entered
        self.exp_date = exp_date
        self.exp_type = exp_type
        self.doc = doc
    
    def __repr__(self):
        return f'<Lot_Numbers Lot#:{self.prefix} {self.year}{self.month}{self.sec_number} {self.suffix} Product_id:{self.product_id} >'
    
class Purchase_Orders(Base):
    __tablename__ = 'Purchase_Orders'
    __table_args__ = {'schema': 'Orders'}
    
    # Table Columns
    prefix: Mapped[str] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(primary_key=True)
    sec_number: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    supplier_so_num: Mapped[str] = mapped_column(default=None)
    order_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    eta_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime)
    date_entered: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    doc = Column(MutableDict.as_mutable(JSON))
    
    # Relationships
    purchase_order_details: Mapped[List["Purchase_Order_Detail"]] = relationship()
    
    def __init__(self, prefix, year, month, sec_number, organization_id, supplier_so_num, order_date, eta_date, date_entered, doc):
        self.prefix = prefix
        self.year = year
        self.month = month
        self.sec_number = sec_number
        self.organization_id = organization_id
        self.supplier_so_num = supplier_so_num
        self.order_date = order_date
        self.eta_date = eta_date
        self.date_entered = date_entered
        self.doc = doc
    
    def __repr__(self):
        return f'<Purchase_Orders PO#:{self.prefix} {self.year}{self.month}{self.sec_number} >'

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
    
    def __init__(self, po_detail_id, prefix, year, month, sec_number, component_id, unit_order_qty, kilos_order_qty, special_instructions, datetime_entered, bid_price_per_unit, bid_price_per_kilo, doc):
        self.po_detail_id = po_detail_id
        self.prefix = prefix
        self.year = year
        self.month = month
        self.sec_number = sec_number
        self.component_id = component_id
        self.unit_order_qty = unit_order_qty
        self.kilos_order_qty = kilos_order_qty
        self.special_instructions = special_instructions
        self.datetime_entered = datetime_entered
        self.bid_price_per_unit = bid_price_per_unit
        self.bid_price_per_kilo = bid_price_per_kilo
        self.doc = doc
    
    def __repr__(self):
        return f'<Purchase_Order_Detail PO#:{self.prefix} {self.year}{self.month}{self.sec_number} >'
    
    
