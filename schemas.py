from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

class Guest(BaseModel):
    name: str
    age: int
    rsvp: str

class GuestResponse(Guest):
    id: int
    name: str
    age: int
    rsvp: str

    model_config = ConfigDict(from_attributes=True)


class Event(BaseModel):
    event_name: str
    date: str
    time: str
    venue: str
    description: str
    status: str

class EventResponse(Event):
    id: int
    
    model_config = ConfigDict(from_attributes=True)



class Vendor(BaseModel):
    vendor_name: str
    service_type: str
    contact_info: str
    cost: float
    status: str

class VendorResponse(Vendor):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Expense(BaseModel):
    purpose: str
    amount: float   
    category: str
    date: str
    status: str

class ExpenseResponse(Expense):
    id: int

    model_config = ConfigDict(from_attributes=True)
