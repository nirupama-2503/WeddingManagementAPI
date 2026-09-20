from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import EventDB
from schemas import Event, EventResponse

router = APIRouter(
        prefix="/events",
    tags=["Events"]
)

@router.post("/", status_code=201, response_model=EventResponse)
def create_event(event: Event, db: Session = Depends(get_db)):
    event_db=EventDB(
        event_name=event.event_name,
        date=event.date,
        time=event.time,
        venue=event.venue,
        description=event.description,
        status=event.status
    )
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db

@router.get("/",status_code=200,response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    events = db.query(EventDB).all()
    return events

@router.get("/{event_id}", status_code=200, response_model=EventResponse)
def get_single_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )
    return event

@router.put("/{event_id}", status_code=200, response_model=EventResponse)
def update_event(event_id: int, event: Event, db: Session = Depends(get_db)):
    event_db = db.query(EventDB).filter(EventDB.id==event_id).first()
    if event_db is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )
    event_db.event_name = event.event_name
    event_db.date = event.date
    event_db.time = event.time
    event_db.venue = event.venue
    event_db.description = event.description
    event_db.status = event.status
    db.commit()
    db.refresh(event_db)
    return event_db

@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event_db = db.query(EventDB).filter(EventDB.id == event_id).first()
    if event_db is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )
    db.delete(event_db)
    db.commit()