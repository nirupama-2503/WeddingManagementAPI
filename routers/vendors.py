from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import VendorDB, EventDB, VendorEventDB, UserDB
from schemas import Vendor, VendorAssignmentResponse, VendorResponse, VendorEventCreate, VendorEventCostUpdate, EventVendorResponse
from routers.auth import get_current_user, require_admin
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"]
)

@router.post("/", status_code=201, response_model=VendorResponse)
def create_vendor(
    vendor: Vendor,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    vendor_db = VendorDB(
        vendor_name=vendor.vendor_name,
        service_type=vendor.service_type,
        contact_info=vendor.contact_info,
        cost=vendor.cost,
        status=vendor.status
    )

    db.add(vendor_db)
    db.commit()
    db.refresh(vendor_db)
    return vendor_db

@router.post("/assign-event")
def assign_vendor_to_event(
    data: VendorEventCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    vendor = db.query(VendorDB).filter(
        VendorDB.id == data.vendor_id
    ).first()

    if not vendor:
        logger.warning(
            "Vendor not found: vendor_id=%s",
            data.vendor_id
        )
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    event = db.query(EventDB).filter(
        EventDB.id == data.event_id
    ).first()

    if not event:
        logger.warning(
            "Event not found: event_id=%s",
            data.event_id
        )
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    existing = db.query(VendorEventDB).filter(
        VendorEventDB.vendor_id == data.vendor_id,
        VendorEventDB.event_id == data.event_id
    ).first()

    if existing:
        logger.warning(
            "Vendor already assigned: vendor_id=%s, event_id=%s",
            data.vendor_id,
            data.event_id
        )
        raise HTTPException(
            status_code=400,
            detail="Vendor is already assigned to this event"
        )

    assignment = VendorEventDB(
        vendor_id=data.vendor_id,
        event_id=data.event_id,
        cost=data.cost
    )

    db.add(assignment)

    try:
        db.commit()
        db.refresh(assignment)

    except IntegrityError:
        db.rollback()
        logger.warning(
            "Duplicate vendor assignment detected: vendor_id=%s, event_id=%s",
            data.vendor_id,
            data.event_id
        )
        raise HTTPException(
            status_code=409,
            detail="Vendor is already assigned to this event"
        )

    logger.info(
        "Vendor assigned successfully: assignment_id=%s, vendor_id=%s, event_id=%s, user_id=%s",
        assignment.id,
        assignment.vendor_id,
        assignment.event_id,
        current_user.id
    )

    return {
        "message": "Vendor assigned successfully",
        "assignment_id": assignment.id,
        "vendor_id": assignment.vendor_id,
        "event_id": assignment.event_id,
        "cost": assignment.cost
    }


@router.get("/", status_code=200, response_model=list[VendorResponse])
def get_vendors(service_type: str | None = None, db: Session = Depends(get_db)):
    query = db.query(VendorDB)

    if service_type:
        query = query.filter(VendorDB.service_type == service_type)

    vendors = query.all()
    return vendors

@router.get("/{vendor_id}", status_code=200, response_model=VendorResponse)
def get_single_vendor(
    vendor_id: int,
    db: Session = Depends(get_db)
    ):
    vendor = db.query(VendorDB).filter(VendorDB.id == vendor_id).first()
    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )
    return vendor

@router.get("/events/{event_id}/vendors", response_model=list[EventVendorResponse])

def get_event_vendors(
    event_id: int,
    db: Session = Depends(get_db),
):
    try:
        event = db.query(EventDB).filter(EventDB.id == event_id).first()

        if not event:
            logger.warning("Event not found: event_id=%s", event_id)
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        assignments = (
            db.query(VendorEventDB)
            .filter(VendorEventDB.event_id == event_id)
            .all()
        )

        result = [
            {
                "vendor_id": assignment.vendor.id,
                "vendor_name": assignment.vendor.vendor_name,
                "service_type": assignment.vendor.service_type,
                "cost": assignment.cost
            }
            for assignment in assignments
        ]

        logger.info(
            "Retrieved %s vendors for event_id=%s",
            len(result),
            event_id
        )

        return result

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Failed to retrieve vendors for event_id=%s",
            event_id
        )
        raise




@router.put("/assignments/{assignment_id}/cost",response_model=VendorAssignmentResponse)
def update_vendor_cost(
    assignment_id: int,
    data: VendorEventCostUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    assignment = db.query(VendorEventDB).filter(
        VendorEventDB.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Vendor assignment not found"
        )

    assignment.cost = data.cost

    db.commit()
    db.refresh(assignment)

    return {
        "message": "Vendor cost updated successfully",
        "assignment_id": assignment.id,
        "vendor_id": assignment.vendor_id,
        "event_id": assignment.event_id,
        "cost": assignment.cost
    }


@router.put("/{vendor_id}", status_code=200, response_model=VendorResponse)
def update_vendor(
    vendor_id: int,
    vendor: Vendor,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    vendor_db = db.query(VendorDB).filter(VendorDB.id == vendor_id).first()
    if vendor_db is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )
    vendor_db.vendor_name = vendor.vendor_name
    vendor_db.service_type = vendor.service_type
    vendor_db.contact_info = vendor.contact_info
    vendor_db.cost = vendor.cost
    vendor_db.status = vendor.status

    db.commit()
    db.refresh(vendor_db)
    return vendor_db

@router.delete("/{vendor_id}", status_code=204)
def delete_vendor(
    vendor_id: int,
    current_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db)
):
    vendor_db = db.query(VendorDB).filter(VendorDB.id == vendor_id).first()
    if vendor_db is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    db.delete(vendor_db)
    db.commit()

@router.delete("/assignments/{assignment_id}")
def delete_vendor_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_admin)
):
    assignment = db.query(VendorEventDB).filter(
        VendorEventDB.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Vendor assignment not found"
        )

    db.delete(assignment)
    db.commit()

    return {
        "message": "Vendor assignment deleted successfully"
    }
