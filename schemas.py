from pydantic import BaseModel, ConfigDict, Field, EmailStr
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

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRoleUpdate(BaseModel):
    role: str = Field(pattern="^(admin|user)$")

class UserStatusUpdate(BaseModel):
    is_active: bool
