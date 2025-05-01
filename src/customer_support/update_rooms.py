import os
from agents.tool import function_tool
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Get environment variables
db_host = os.getenv("HOST")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")

# Ensure all required environment variables are present
if not all([db_host, db_user, db_pass, db_name]):
    raise ValueError("Missing one or more required environment variables. Please check your .env file.")

# Construct the database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"

# Print credentials (for debugging — remove in production)
print(f"Database user: {db_user!r}")
print(f"Database name: {db_name!r}")

# Create SQLAlchemy engine and session factory
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for ORM models
Base = declarative_base()

# Dependency for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()







@function_tool
def update_user_room(cnic: str, new_room_id: int):
    """
    Updates a user's reserved room to a new room if it's available.
    Also updates the room status accordingly.
    Args:
        cnic (str): CNIC of the user.
        new_room_id (int): New room ID
    """
    try:
        with Session(engine) as db:
            # Step 1: Check if the user exists and get their current room
            booking = db.execute(
                text("SELECT room_id FROM user_booking WHERE CNIC = :cnic"),
                {"cnic": cnic}
            ).fetchone()

            if not booking:
                return f"❌ No booking found for CNIC '{cnic}'."

            old_room_id = booking[0]

            if old_room_id == new_room_id:
                return f"⚠️ You are already booked in room {new_room_id}."

            # Step 2: Check if new room exists and is available
            new_room = db.execute(
                text("SELECT status FROM rooms WHERE id = :room_id"),
                {"room_id": new_room_id}
            ).fetchone()

            if not new_room:
                return f"❌ New Room ID {new_room_id} does not exist."

            if new_room[0] != "Available":
                return f"❌ New Room ID {new_room_id} is currently '{new_room[0]}'. Cannot switch."

            # Step 3: Update booking
            db.execute(
                text("UPDATE user_booking SET room_id = :new_room_id WHERE CNIC = :cnic"),
                {"new_room_id": new_room_id, "cnic": cnic}
            )

            # Step 4: Update new room to 'Reserved'
            db.execute(
                text("UPDATE rooms SET status = 'Reserved' WHERE id = :room_id"),
                {"room_id": new_room_id}
            )

            # Step 5: Set old room back to 'Available'
            db.execute(
                text("UPDATE rooms SET status = 'Available' WHERE id = :room_id"),
                {"room_id": old_room_id}
            )

            db.commit()
            return f"✅ Room updated successfully. You have been moved from room {old_room_id} to room {new_room_id}."

    except IntegrityError as e:
        db.rollback()
        return f"❌ Integrity error: {str(e.orig)}"

    except SQLAlchemyError as e:
        db.rollback()
        return f"❌ Database error: {str(e)}"

    except Exception as e:
        db.rollback()
        return f"❌ Unexpected error: {str(e)}"
