from pydantic import BaseModel, ConfigDict, Field
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

class VendorEventCreate(BaseModel):
    vendor_id: int
    event_id: int
    cost: float = Field(ge=0)

class VendorEventCostUpdate(BaseModel):
    cost: float = Field(ge=0)

class VendorAssignmentResponse(BaseModel):
    message: str
    assignment_id: int
    vendor_id: int
    event_id: int
    cost: float

class EventVendorResponse(BaseModel):
    vendor_id: int
    vendor_name: str
    service_type: str
    cost: float


class Expense(BaseModel):
    purpose: str
    amount: float = Field(gt=0, description="Amount must be greater than zero")
    category: str
    date: str
    status: str
    event_id: int = Field(gt=0, description="Event ID must be greater than zero")

class ExpenseResponse(Expense):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ExpensetotalResponse(BaseModel):
    total_expenses: float


class EventStatusUpdate(BaseModel):
    status : str