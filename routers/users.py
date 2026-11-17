from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import UserDB
from schemas import UserResponse, UserRoleUpdate, UserStatusUpdate
from routers.auth import get_current_user, require_admin

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: UserDB = Depends(get_current_user)
):
    return current_user

@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_admin)
):
    return db.query(UserDB).all()

@router.patch("/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_admin)
):
    user = db.query(UserDB).filter(
        UserDB.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.id == current_user.id and role_data.role != "admin":
        raise HTTPException(
            status_code=400,
            detail="You cannot remove your own admin role"
        )

    if user.role == "admin" and role_data.role != "admin" and user.is_active:
        active_admin_count = db.query(UserDB).filter(
            UserDB.role == "admin",
            UserDB.is_active.is_(True)
    ).count()

        if active_admin_count <= 1:
            raise HTTPException(
                status_code=400,
                detail="Cannot demote the last active admin"
            )

    user.role = role_data.role

    db.commit()
    db.refresh(user)

    return user

@router.patch("/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    status_data: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_admin)
):
    user = db.query(UserDB).filter(
        UserDB.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.id == current_user.id and not status_data.is_active:
        raise HTTPException(
            status_code=400,
            detail="You cannot deactivate your own account"
        )

    if user.role == "admin" and user.is_active and not status_data.is_active:
        active_admin_count = db.query(UserDB).filter(
            UserDB.role == "admin",
            UserDB.is_active.is_(True)
    ).count()

        if active_admin_count <= 1:
            raise HTTPException(
                status_code=400,
                detail="Cannot deactivate the last active admin"
            )

    user.is_active = status_data.is_active

    db.commit()
    db.refresh(user)

    return user