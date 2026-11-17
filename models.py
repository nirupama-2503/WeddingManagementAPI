

from database import Base, engine, get_db
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship


guest_events = Table(
    "guest_events",
    Base.metadata,
    Column("guest_id", ForeignKey("guests.id"), primary_key=True),
    Column("event_id", ForeignKey("events.id"), primary_key=True)
)


class GuestDB(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    rsvp = Column(String, nullable=False)
    events = relationship("EventDB",secondary=guest_events,back_populates="guests")

class EventDB(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    expenses = relationship("ExpenseDB",back_populates="event",cascade="all, delete-orphan")
    guests = relationship("GuestDB",secondary=guest_events,back_populates="events")
    vendor_assignments = relationship("VendorEventDB",back_populates="event",cascade="all, delete-orphan")

class VendorDB(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index =True)
    vendor_name = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    event_assignments = relationship("VendorEventDB",back_populates="vendor",cascade="all, delete-orphan")


class ExpenseDB(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    purpose = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(String, nullable=False)
    status = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    event = relationship("EventDB", back_populates="expenses")



class VendorEventDB(Base):
    __tablename__ = "vendor_events"

    __table_args__ = (UniqueConstraint("vendor_id","event_id",name="uq_vendor_event"),)
    id = Column(Integer, primary_key=True, index=True)

    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    cost = Column(Float, nullable=False)

    vendor = relationship("VendorDB", back_populates="event_assignments")
    event = relationship("EventDB", back_populates="vendor_assignments")


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

Base.metadata.create_all(bind=engine)