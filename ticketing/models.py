"""Data Models."""
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from . import db

class Customer(db.Model):
    """Data model for Customer Records"""
    __tablename__ = 'customers'
    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True
        )
    firstname = Column(
        String(50), 
        nullable=False
        )
    lastname = Column(
        String(50), 
        nullable=False
        )
    address = Column(
        String(250), 
        nullable=True
        )
    phone = Column(
        String(50), 
        nullable=False
        )
    email = Column(
        String(50), 
        nullable=True
        )

    def __repr__(self) -> str:
        return f'<Customer {self.first_name!r} {self.last_name!r}>'


class Ticket(db.Model):
    """Data model for Ticket records"""

    __tablename__ = 'tickets'
    id = Column(
        Integer, 
        autoincrement=True, 
        primary_key=True
        )
    customer_id = Column(
        Integer, 
        ForeignKey('customer.id'), 
        nullable = False
        )
    tickettype = Column(
        String(50), 
        nullable=False
        )
    ticketdescription = Column(
        String(250), 
        nullable=False
        )
    ticketstatus = Column(
        String(50), 
        nullable=False
        )
    created = Column(
        DateTime, 
        nullable=False
        )
    promised = Column(
        DateTime, 
        nullable=True
        )
    completed = Column(
        DateTime, 
        nullable=True
        )
    bDone = Column(
        Boolean, 
        nullable=False
        )
    bNotified = Column(
        Boolean, 
        nullable=False
        )
    bRetrieved = Column(
        Boolean, 
        nullable=False
        )
    labor_cost = Column(
        Float, 
        nullable=True
        )
    parts_cost = Column(
        Float, 
        nullable=True
        )
    other_cost = Column(
        Float, 
        nullable=True
        )
    notes = Column(
        Text, 
        nullable=True
        )

    customer = relationship('Customer', backref=backref('customers', lazy=True))
    
    def __repr__(self):
        return f'<Ticket {self.id!r}>'


class User(db.Model):
    """Data model for User records"""

    __tablename__ = 'users'
    id = Column(
        Integer, 
        autoincrement=True, 
        primary_key=True
        )
    username = Column(
        String(50), 
        nullable=False, 
        unique=True
        )
    password = Column(
        String(50), 
        nullable=False
        )
    first_name = Column(
        String(50), 
        nullable=False
        )
    last_name = Column(
        String(50), 
        nullable=False
        )
    address = Column(
        String(250), 
        nullable=True
        )
    phone = Column(
        String(50), 
        nullable=False
        )
    email = Column(
        String(50), 
        nullable=True
        )
    clearance = Column(
        Integer, 
        nullable=False
        )

    def __repr__(self) -> str:
        return f'<User {self.username!r}>'
