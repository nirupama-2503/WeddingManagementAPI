from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import GuestDB, EventDB, UserDB
from schemas import Guest, GuestResponse
from routers.auth import get_current_user, require_admin

router = APIRouter(
    prefix="/guest",
    tags=["Guests"]
)

@router.get("/", response_model=list[GuestResponse])
def get_guests(db: Session = Depends(get_db)):
    guests = db.query(GuestDB).all()
    return guests

@router.post("/", status_code=201, response_model=GuestResponse)
def create_guest(
    guest: Guest,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    guest_db = GuestDB(
        name=guest.name,
        age=guest.age,
        rsvp=guest.rsvp
    )
    db.add(guest_db)
    db.commit()
    db.refresh(guest_db)
    return guest_db

@router.post("/{guest_id}/events/{event_id}")
def add_guest_to_event(
    guest_id: int,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    guest = db.query(GuestDB).filter(GuestDB.id == guest_id).first()
    event = db.query(EventDB).filter(EventDB.id == event_id).first()

    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event in guest.events:
        raise HTTPException(
        status_code=400,
        detail="Guest is already registered for this event"
        )

    guest.events.append(event)

    db.commit()

    return {"message": "Guest added to event successfully"}

@router.get("/{guest_id}", response_model=GuestResponse)
def get_single_guest(guest_id: int, db: Session = Depends(get_db)):
    guest = db.query(GuestDB).filter(GuestDB.id == guest_id).first()
    if guest is None:
        raise HTTPException(
            status_code=404,
            detail="Guest not found"
        )
    return guest

@router.get("/{guest_id}/events")
def get_guest_events(guest_id: int,db: Session = Depends(get_db)):
    guest = db.query(GuestDB).filter(GuestDB.id == guest_id).first()

    if not guest:
        raise HTTPException(
            status_code=404,
            detail="Guest not found"
        )

    return guest.events

@router.put("/{guest_id}", response_model=GuestResponse)
def update_guest(
    guest_id: int,
    guest: Guest,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    guest_db = db.query(GuestDB).filter(GuestDB.id == guest_id).first()
    if guest_db is None:
        raise HTTPException(
            status_code=404,
            detail="Guest not found"
        )
    guest_db.name = guest.name
    guest_db.age = guest.age
    guest_db.rsvp = guest.rsvp
    db.commit()
    db.refresh(guest_db)
    return guest_db

@router.delete("/{guest_id}", status_code=204)
def delete_guest(
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_admin)
):
    guest_db = db.query(GuestDB).filter(GuestDB.id == guest_id).first()
    if guest_db is None:
        raise HTTPException(
            status_code=404,
            detail="Guest not found"
        )
    db.delete(guest_db)
    db.commit()