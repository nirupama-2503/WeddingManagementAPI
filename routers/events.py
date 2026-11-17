from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import EventDB, UserDB
from schemas import Event, EventResponse, EventStatusUpdate, ExpenseResponse
from routers.auth import get_current_user, require_admin

router = APIRouter(
        prefix="/events",
    tags=["Events"]
)

@router.post("/", status_code=201, response_model=EventResponse)
def create_event(
    event: Event,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
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
def get_events(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(EventDB)

    if status:
        query = query.filter(EventDB.status == status)

    return query.all()

@router.get("/{event_id}", status_code=200, response_model=EventResponse)
def get_single_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )
    return event

@router.get("/{event_id}/expenses", status_code=200, response_model=list[ExpenseResponse])
def get_event_expenses(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EventDB).filter(EventDB.id==event_id).first()
    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event.expenses

@router.get("/{event_id}/guests")
def get_event_guests(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = db.query(EventDB).filter(EventDB.id == event_id).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event.guests


@router.put("/{event_id}", status_code=200, response_model=EventResponse)
def update_event(
    event_id: int,
    event: Event,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
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
def delete_event(
    event_id: int,
    current_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db)
):
    event_db = db.query(EventDB).filter(EventDB.id == event_id).first()
    if event_db is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )
    db.delete(event_db)
    db.commit()


@router.patch("/{event_id}", status_code=200, response_model=EventResponse)
def update_event_status(
    event_id: int,
    status_update: EventStatusUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event_db = db.query(EventDB).filter(EventDB.id == event_id).first()
    if event_db is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )
    event_db.status = status_update.status
    db.commit()
    db.refresh(event_db)
    return event_db




