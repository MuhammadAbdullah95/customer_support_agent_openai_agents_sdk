import os
from agents.tool import function_tool
import os
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
def cancel_booking(cnic: str):
    """
    Cancels the booking for a user identified by CNIC.
    Frees the reserved room and deletes the user_booking entry.
    Args:
        cnic (str): CNIC of the user.
    """
    try:
        with Session(engine) as db:
            # Step 1: Check if booking exists
            booking = db.execute(
                text("SELECT room_id FROM user_booking WHERE CNIC = :cnic"),
                {"cnic": cnic}
            ).fetchone()

            if not booking:
                return f"❌ No booking found for CNIC '{cnic}'."

            room_id = booking[0]

            # Step 2: Delete the booking
            db.execute(
                text("DELETE FROM user_booking WHERE CNIC = :cnic"),
                {"cnic": cnic}
            )

            # Step 3: Update room status to 'Available'
            db.execute(
                text("UPDATE rooms SET status = 'Available' WHERE id = :room_id"),
                {"room_id": room_id}
            )

            db.commit()
            return f"✅ Booking for CNIC '{cnic}' has been cancelled. Room {room_id} is now available."

    except IntegrityError as e:
        db.rollback()
        return f"❌ Integrity error during cancellation: {str(e.orig)}"

    except SQLAlchemyError as e:
        db.rollback()
        return f"❌ Database error during cancellation: {str(e)}"

    except Exception as e:
        db.rollback()
        return f"❌ Unexpected error: {str(e)}"
