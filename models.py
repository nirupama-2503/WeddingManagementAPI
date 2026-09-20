

from database import Base, engine, get_db
from sqlalchemy import Column, Integer, String, Float

class GuestDB(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    rsvp = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

class EventDB(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

class VendorDB(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index =True)
    vendor_name = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    status = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)


class ExpenseDB(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    purpose = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(String, nullable=False)
    status = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)