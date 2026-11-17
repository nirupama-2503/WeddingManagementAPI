
from getpass import getpass

from database import SessionLocal
from models import UserDB
from security import hash_password


db = SessionLocal()

try:
    existing_admin = db.query(UserDB).filter(
        UserDB.role == "admin"
    ).first()

    if existing_admin:
        print("An admin account already exists.")
        raise SystemExit

    username = input("Enter admin username: ").strip()
    email = input("Enter admin email: ").strip()
    password = getpass("Enter admin password: ")
    confirm_password = getpass("Confirm admin password: ")

    if not username or not email:
        print("Username and email are required.")
        raise SystemExit

    if len(password) < 8 or len(password) > 128:
        print("Password must be between 8 and 128 characters.")
        raise SystemExit

    if password != confirm_password:
        print("Passwords do not match.")
        raise SystemExit

    existing_user = db.query(UserDB).filter(
        (UserDB.username == username) |
        (UserDB.email == email)
    ).first()

    if existing_user:
        print("Username or email already exists.")
        raise SystemExit

    admin = UserDB(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role="admin",
        is_active=True
    )

    db.add(admin)
    db.commit()

    print("Admin account created successfully!")

except Exception:
    db.rollback()
    raise

finally:
    db.close()
