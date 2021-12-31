from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, Float, Text
from sqlalchemy.orm import mapper
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DECIMAL, Boolean, DateTime
from ticketing.database import Base

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, autoincrement=True, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    address = Column(String(250), nullable=True)
    phone = Column(String(50), nullable=False)
    email = Column(String(50), nullable=True)

    def __init__(self, first_name, last_name, address, phone, email) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.email = email

    def __repr__(self) -> str:
        return f'<Customer {self.first_name!r} {self.last_name!r}>'

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, autoincrement=True, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable = False)
    ticket_type = Column(String(50), nullable=False)
    ticket_description = Column(String(250), nullable=False)
    ticket_status = Column(String(50), nullable=False)
    created = Column(DateTime, nullable=False)
    promised = Column(DateTime, nullable=True)
    completed = Column(DateTime, nullable=True)
    bDone = Column(Boolean, nullable=False)
    bNotified = Column(Boolean, nullable=False)
    bRetrieved = Column(Boolean, nullable=False)
    labor_cost = Column(Float, nullable=True)
    parts_cost = Column(Float, nullable=True)
    other_cost = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

    def __init__(self, customer_id, ticket_type, ticket_description, 
    ticket_status, created, promised, completed, bDone, bNotified, bRetrieved,
    labor_cost, parts_cost, other_cost, notes):

        self.customer_id = customer_id
        self.ticket_type = ticket_type
        self.ticket_description = ticket_description
        self.ticket_status = ticket_status
        self.created = created
        self.promised = promised
        self.completed = completed
        self.bDone = bDone
        self.bNotified = bNotified
        self.bRetrieved = bRetrieved
        self.labor_cost = labor_cost
        self.parts_cost = parts_cost
        self.other_cost = other_cost
        self.notes = notes
    
    def __repr__(self):
        return f'<Ticket {self.id!r}>'


