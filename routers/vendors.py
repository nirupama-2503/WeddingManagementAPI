from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import VendorDB
from schemas import Vendor, VendorResponse

router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"]
)

@router.post("/", status_code=201, response_model=VendorResponse)
def create_vendor(vendor: Vendor, db: Session = Depends(get_db)):
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

@router.get("/", status_code=200, response_model=list[VendorResponse])
def get_vendors(service_type: str | None = None, db: Session = Depends(get_db)):
    query = db.query(VendorDB)

    if service_type:
        query = query.filter(VendorDB.service_type == service_type)

    vendors = query.all()
    return vendors      

@router.get("/{vendor_id}", status_code=200, response_model=VendorResponse)
def get_single_vendor(vendor_id: int, db: Session = Depends(get_db)):   
    vendor = db.query(VendorDB).filter(VendorDB.id == vendor_id).first()
    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )
    return vendor

@router.put("/{vendor_id}", status_code=200, response_model=VendorResponse)
def update_vendor(vendor_id: int, vendor: Vendor, db: Session = Depends(get_db)):
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
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):   
    vendor_db = db.query(VendorDB).filter(VendorDB.id == vendor_id).first()
    if vendor_db is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )
    
    db.delete(vendor_db)
    db.commit()
