import os
from agents.tool import function_tool
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
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
def get_rooms_availability():
    """
    Fetches all room availability records from the 'rooms' table.
    Returns:
        list[dict]: List of dictionaries, each representing a row.
    """
    try:
        with Session(engine) as db:
            stmt = text("SELECT * FROM rooms WHERE status = 'Available'")
            result = db.execute(stmt)
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]  # Convert each row to a dict
    except Exception as e:
        print(f"Error in get_rooms_availability: {e}")
        return []
    
@function_tool
def check_room_status(room_id: int):
    """
    Check the availability status of a specific room by its ID.
    Returns 'Available', 'Reserved', or a user-friendly message if the room doesn't exist.
    Args: 
        room_id (int): ID of the room to check.
    Returns:
        str: Status of the room.
    """
    try:
        with Session(engine) as db:
            result = db.execute(
                text("SELECT status FROM rooms WHERE id = :room_id"),
                {"room_id": room_id}
            ).fetchone()

            if result is None:
                return f"❌ Room ID {room_id} does not exist."

            status = result[0]
            return f"✅ Room {room_id} is currently: {status}."

    except SQLAlchemyError as e:
        return f"❌ Database error while checking room status: {str(e)}"

    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# Run the function when the script is executed directly
if __name__ == "__main__":
    availability = get_rooms_availability()
    print("Room Availability:")
    for room in availability:
        print(room)

