from __future__ import annotations
from typing import List

from .handle_exclude import handle_exclude

# Composite Primary Keys were initially part of the ORM Models, however due to the complexity,
# They were replaced with single primary keys.  This module has leftover notes from the initial
# implementation for reference in case Composite Primary Keys are needed in the future.

from sqlalchemy import Enum, ForeignKey, Column # , ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.mysql import JSON

from .base import Base

import datetime

class Sales_Orders(Base):
    """Sales Orders ORM Model"""
    __tablename__ = 'Sales_Orders'
    __table_args__ = {'schema': 'Orders'}

    # Primary Key  (Old Composite Key)
    # prefix: Mapped[str] = mapped_column(primary_key=True)
    # year: Mapped[int] = mapped_column(primary_key=True)
    # month: Mapped[int] = mapped_column(primary_key=True)
    # sec_number: Mapped[int] = mapped_column(primary_key=True)
    # suffix: Mapped[str] = mapped_column(primary_key=True)

    # New Primary Key
    so_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    sales_orders_payments: Mapped[List["Sales_Orders_Payments"]] = relationship()
    sale_order_detail: Mapped[List["Sale_Order_Detail"]] = relationship()

    # Table Columns
    prefix: Mapped[str] = mapped_column(default=None)
    year: Mapped[int] = mapped_column(default=None)
    month: Mapped[int] = mapped_column(default=None)
    sec_number: Mapped[int] = mapped_column(default=None)
    suffix: Mapped[str] = mapped_column(default=None)
    client_po_num: Mapped[str] = mapped_column(default=None)
    order_date: Mapped[datetime.datetime] = mapped_column(default=None)
    target_completion_date: Mapped[datetime.datetime] = mapped_column(default=None)
    completion_date: Mapped[datetime.datetime] = mapped_column(default=None)
    billed_date: Mapped[datetime.datetime] = mapped_column(default=None)
    closed_date: Mapped[datetime.datetime] = mapped_column(default=None)
    down_payment_actual: Mapped[float] = mapped_column(default=None)
    theoretical_po_amount: Mapped[float] = mapped_column(default=None)
    total_paid: Mapped[float] = mapped_column(default=None)
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()
    lot_num_assigned: Mapped[bool] = mapped_column(default=False)

    doc = Column(MutableDict.as_mutable(JSON))

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Sales_Order SO#{self.prefix}{self.year}~{self.month}~{self.sec_number}{self.suffix}>'

    def to_dict(self, exclude=[]):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        out = {
            'so_id': self.so_id,
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
            'billed_date': self.billed_date,
            'closed_date': self.closed_date,
            'down_payment_actual': self.down_payment_actual,
            'theoretical_po_amount': self.theoretical_po_amount,
            'total_paid': self.total_paid,
            'doc': self.doc,
            'lot_num_assigned': self.lot_num_assigned,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }
        return handle_exclude(out, exclude)

    def get_id(self):
        """Get Row Id"""
        # return str(self.prefix) + str(self.year) + str(self.month) + str(self.sec_number)
        return self.so_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        # return (
        #     "prefix",
        #     "year",
        #     "month",
        #     "sec_number",
        #     "suffix"
        # )
        return "so_id"

class Sale_Order_Detail(Base):
    """Sale Order Detail ORM Model"""
    __tablename__ = 'Sale_Order_Detail'
    __table_args__ = {'schema': 'Orders'}

    # Primary Key
    so_detail_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships

    # Old Composite Foreign Key (Notes)
    # prefix: Mapped[str] = mapped_column(nullable=False)
    # year: Mapped[int] = mapped_column(nullable=False)
    # month: Mapped[int] = mapped_column(nullable=False)
    # sec_number: Mapped[int] = mapped_column(nullable=False)
    # suffix: Mapped[str] = mapped_column(nullable=False)
    # fk_constraint = ForeignKeyConstraint(
    #                 [
    #                     prefix,
    #                     year,
    #                     month,
    #                     sec_number,
    #                     suffix
    #                 ],
    #                 [
    #                     "Orders.Sales_Orders.prefix",
    #                     "Orders.Sales_Orders.year",
    #                     "Orders.Sales_Orders.month",
    #                     "Orders.Sales_Orders.sec_number",
    #                     "Orders.Sales_Orders.suffix"
    #                 ],
    #                 name="Sales_Order_Number_fk"
    #             )
    # __table_args__ = (fk_constraint, {
    #     'schema': 'Orders'
    # })

    so_id: Mapped[int] = mapped_column(ForeignKey('Orders.Sales_Orders.so_id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Master.product_id'))
    variant_id: Mapped[int] = mapped_column(ForeignKey('Products.Product_Variants.variant_id'))
    formula_id: Mapped[int] = mapped_column(ForeignKey('Products.Formulas.formula_id'))

    # Table Columns
    unit_order_qty: Mapped[int] = mapped_column(default=None)
    kilos_order_qty: Mapped[float] = mapped_column(default=None)
    special_instructions: Mapped[str] = mapped_column(default=None)
    bid_price_per_unit: Mapped[float] = mapped_column(default=None)
    final_ship_date: Mapped[datetime.datetime] = mapped_column(default=None)
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()
    lot_num_assigned: Mapped[bool] = mapped_column(default=False)
    percent_overage: Mapped[float] = mapped_column(default=None)

    doc = Column(MutableDict.as_mutable(JSON))

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Sales_Order_Detail SO#{self.prefix}{self.year}~{self.month}~{self.sec_number} Product_id:{self.product_id} Qty:{self.unit_order_qty}{self.kilos_order_qty}{self.suffix}>'

    def to_dict(self, exclude=[]):
        """Converts Data to Dictionary representation

        Parameters:
            exclude (List): Columns to exclude from the output

        Returns:
            Dict: Columns as Keys
        """
        out = {
            'so_detail_id': self.so_detail_id,
            'so_id': self.so_id,
            'variant_id': self.variant_id,
            'formula_id': self.formula_id,
            'product_id': self.product_id,
            'unit_order_qty': self.unit_order_qty,
            'kilos_order_qty': self.kilos_order_qty,
            'special_instructions': self.special_instructions,
            'bid_price_per_unit': self.bid_price_per_unit,
            'final_ship_date': self.final_ship_date,
            'doc': self.doc,
            'lot_num_assigned': self.lot_num_assigned,
            'percent_overage': self.percent_overage,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }
        return handle_exclude(out, exclude)



    def get_id(self):
        """Get Row Id"""
        return self.so_detail_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "so_detail_id"

class Sales_Orders_Payments(Base):
    """Sales Orders Payments ORM Model"""
    __tablename__ = 'Sales_Order_Payments'
    __table_args__ = {'schema': 'Orders'}

    # Primay Key
    payment_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    so_id: Mapped[int] = mapped_column(ForeignKey('Orders.Sales_Orders.so_id'))

    # Table Columns
    payment_amount: Mapped[float] = mapped_column(default=None)
    PaymentTypes = ("down_payment", "other", "final_payment")
    payment_type: Mapped[int] = mapped_column(Enum(
        *PaymentTypes,
        name="PaymentTypes",
        create_constraint=True,
        validate_strings=True,
    ))
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    doc = Column(MutableDict.as_mutable(JSON))

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Sales_Order_Payments SO#{self.prefix}{self.year}~{self.month}~{self.sec_number} Type:{self.payment_type} Amount:{self.payment_amount}{self.suffix}>'

    def to_dict(self, exclude=[]):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        out = {
            'payment_id': self.payment_id,
            'so_id': self.so_id,
            'payment_type': self.payment_type,
            'payment_amount': self.payment_amount,
            'doc': self.doc,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }
        return handle_exclude(out, exclude)

    def get_id(self):
        """Get Row Id"""
        return self.payment_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "payment_id"

class Lot_And_Batch_Numbers(Base):
    """Lot And Batch Numbers ORM Model"""
    __tablename__ = 'Lot_And_Batch_Numbers'
    __table_args__ = {'schema': 'Orders'}

    # Primary Key
    lot_num_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    so_detail_id: Mapped[int] = mapped_column(ForeignKey('Orders.Sale_Order_Detail.so_detail_id'))

    # Table Columns
    prefix: Mapped[str] = mapped_column(default=None)
    year: Mapped[int] = mapped_column(default=None)
    month: Mapped[int] = mapped_column(default=None)
    sec_number: Mapped[int] = mapped_column(default=None)
    suffix: Mapped[str] = mapped_column(default=None)
    target_unit_yield: Mapped[int] = mapped_column(default=None)
    actual_unit_yield: Mapped[int] = mapped_column(default=None)
    retentions: Mapped[int] = mapped_column(default=None)
    total_shippable_product: Mapped[int] = mapped_column(default=None)
    batch_printed: Mapped[bool] = mapped_column(default=False)
    bpr_printed: Mapped[bool] = mapped_column(default=False)
    exp_date: Mapped[datetime.datetime] = mapped_column(default=None)
    ExpirationTypes = ("Best_By", "Exp")
    exp_type: Mapped[int] = mapped_column(Enum(
        *ExpirationTypes,
        name="ExpirationTypes",
        create_constraint=True,
        validate_strings=True,
    ))
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()
    batch_record: Mapped[bool] = mapped_column(default=False)
    total_batch_size: Mapped[float] = mapped_column(default=None)
    production_record: Mapped[bool] = mapped_column(default=False)
    allocated_batch_size: Mapped[float] = mapped_column(default=None)
    allocated_from_lot_num_id: Mapped[int] = mapped_column(ForeignKey('Orders.Lot_And_Batch_Numbers.lot_num_id'), default=None)

    doc = Column(MutableDict.as_mutable(JSON))

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Lot_And_Batch_Numbers Lot#:{self.prefix} {self.year}{self.month}{self.sec_number} {self.suffix} Product_id:{self.product_id} >'

    def to_dict(self, exclude=[]):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        out = {
            'lot_num_id': self.lot_num_id,
            'prefix': self.prefix,
            'year': self.year,
            'month': self.month,
            'sec_number': self.sec_number,
            'suffix': self.suffix,
            'target_unit_yield': self.target_unit_yield,
            'actual_unit_yield': self.actual_unit_yield,
            'retentions': self.retentions,
            'total_shippable_product': self.total_shippable_product,
            'batch_printed': self.batch_printed,
            'bpr_printed': self.bpr_printed,
            'exp_date': self.exp_date,
            'exp_type': self.exp_type,
            'doc': self.doc,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }
        return handle_exclude(out, exclude)

    def get_id(self):
        """Get Row Id"""
        return self.lot_num_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "lot_num_id"

class Purchase_Orders(Base):
    """Purchase Orders ORM Model"""
    __tablename__ = 'Purchase_Orders'
    __table_args__ = {'schema': 'Orders'}

    # Primary Key
    po_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    organization_id: Mapped[int] = mapped_column(ForeignKey('Organizations.Organizations.organization_id'))
    purchase_order_details: Mapped[List["Purchase_Order_Detail"]] = relationship()

    # Table Columns
    prefix: Mapped[str] = mapped_column(default=None)
    year: Mapped[int] = mapped_column(default=None)
    month: Mapped[int] = mapped_column(default=None)
    sec_number: Mapped[int] = mapped_column(default=None)
    suffix: Mapped[str] = mapped_column(default=None)
    supplier_so_num: Mapped[str] = mapped_column(default=None)
    order_date: Mapped[datetime.datetime] = mapped_column(default=None)
    eta_date: Mapped[datetime.datetime] = mapped_column(default=None)
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    doc = Column(MutableDict.as_mutable(JSON))

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Purchase_Orders PO#:{self.prefix} {self.year}{self.month}{self.sec_number} >'

    def to_dict(self, exclude=[]):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        out = {
            'po_id': self.po_id,
            'prefix': self.prefix,
            'year': self.year,
            'month': self.month,
            'sec_number': self.sec_number,
            'organization_id': self.organization_id,
            'supplier_so_num': self.supplier_so_num,
            'order_date': self.order_date,
            'eta_date': self.eta_date,
            'doc': self.doc,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }
        return handle_exclude(out, exclude)

    def get_id(self):
        """Get Row Id"""
        return self.po_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return 'po_id'

class Purchase_Order_Detail(Base):
    """Purchase Order Detail ORM Model"""
    __tablename__ = 'Purchase_Order_Detail'
    __table_args__ = {'schema': 'Orders'}

    # Primary Key
    po_detail_id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    po_id: Mapped[int] = mapped_column(ForeignKey('Orders.Purchase_Orders.po_id'))
    component_id: Mapped[int] = mapped_column(ForeignKey('Inventory.Components.component_id'), nullable=False)

    # Table Columns
    unit_order_qty: Mapped[int] = mapped_column(default=None)
    kilos_order_qty: Mapped[float] = mapped_column(default=None)
    special_instructions: Mapped[str] = mapped_column(default=None)
    bid_price_per_unit: Mapped[float] = mapped_column(default=None)
    bid_price_per_kilo: Mapped[float] = mapped_column(default=None)
    timestamp_entered: Mapped[datetime.datetime] = mapped_column()
    timestamp_modified: Mapped[datetime.datetime] = mapped_column()

    doc = Column(MutableDict.as_mutable(JSON))

    # Common Methods
    def __repr__(self):
        """Return a string representation of Object"""
        return f'<Purchase_Order_Detail PO#:{self.prefix} {self.year}{self.month}{self.sec_number} >'

    def to_dict(self, exclude=[]):
        """Converts Data to Dictionary representation

        Returns:
            Dict: Columns as Keys
        """
        out = {
            'po_detail_id': self.po_detail_id,
            'po_id': self.po_id,
            'component_id': self.component_id,
            'unit_order_qty': self.unit_order_qty,
            'kilos_order_qty': self.kilos_order_qty,
            'special_instructions': self.special_instructions,
            'bid_price_per_unit': self.bid_price_per_unit,
            'bid_price_per_kilo': self.bid_price_per_kilo,
            'doc': self.doc,
            "timestamp_entered": (self.timestamp_entered - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_modified": (self.timestamp_modified - datetime.timedelta(hours=6)).isoformat(),
            "timestamp_fetched": datetime.datetime.now().isoformat()
        }
        return handle_exclude(out, exclude)

    def get_id(self):
        """Get Row Id"""
        return self.po_detail_id

    def get_id_name(self):
        """Get Primary ID Column Name"""
        return "po_detail_id"
