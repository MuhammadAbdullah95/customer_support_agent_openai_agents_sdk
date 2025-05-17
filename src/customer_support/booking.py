import os
from agents.tool import function_tool
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
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

# Function to get room availability from the 'rooms' table
@function_tool
def reserve_room(cnic: str, name: str, contact: str, room_id: int):
    """
    Reserver room for the customer,
    Reserve a room if available. Returns a message about the result.
    Handles all relevant constraint violations and errors.
    Args:
        cnic (str): CNIC of the customer.
        name (str): Name of the customer.
        contact (str): Contact number of the customer.
        room_id (int): Room no. to be reserved.
    """
    try:
        with Session(engine) as db:
            # Step 1: Check if room exists
            room_check = db.execute(
                text("SELECT status FROM rooms WHERE id = :room_id"),
                {"room_id": room_id}
            ).fetchone()

            if not room_check:
                return f"Room ID {room_id} does not exist."

            room_status = room_check[0]

            # Step 2: Check if the room is already reserved
            if room_status != "Available":
                return f"Room ID {room_id} is currently '{room_status}'. Cannot reserve."

            # Step 3: Insert booking into user_booking
            db.execute(
                text("""
                    INSERT INTO user_booking (CNIC, name, contact, room_id)
                    VALUES (:cnic, :name, :contact, :room_id)
                """),
                {"cnic": cnic, "name": name, "contact": contact, "room_id": room_id}
            )

            # Step 4: Update the room status to 'Reserved'
            db.execute(
                text("""
                    UPDATE rooms
                    SET status = 'Reserved'
                    WHERE id = :room_id
                """),
                {"room_id": room_id}
            )

            db.commit()
            return f"✅ Room ID {room_id} has been successfully reserved for {name}."

    except IntegrityError as e:
        db.rollback()

        # Handle unique CNIC or FK violation
        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            return f"❌ A booking already exists for CNIC '{cnic}'."
        elif isinstance(e.orig, psycopg2.errors.ForeignKeyViolation):
            return f"❌ Invalid room_id {room_id}. No such room exists."
        elif isinstance(e.orig, psycopg2.errors.CheckViolation):
            return f"❌ Room status or data violates a check constraint."
        else:
            return f"❌ Integrity error: {str(e.orig)}"

    except SQLAlchemyError as e:
        db.rollback()
        return f"❌ Database error: {str(e)}"

    except Exception as e:
        db.rollback()
        return f"❌ Unexpected error: {str(e)}"
    



if __name__ == "__main__":
    msg = reserve_room(
        cnic="35202-1234567-8",
        name="Ali Khan",
        contact="03001234567",
        room_id=2
    )
    print(msg)


