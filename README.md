# 🏨 Ainnovate Hotel AI Booking System

An intelligent, multi-agent hotel booking assistant powered by Python, FastAPI,Chainlit, PostgreSQL, and Openai AI Agents SDK. This system allows users to check room availability, reserve, update, or cancel bookings, and ask hotel-related FAQs through a natural language chatbot interface.

---

## ✨ Features

- ✅ **Room Availability Checker Agent**  
  Checks real-time room availability and specific room statuses.

- ✅ **Booking Agent**  
  Handles room reservations, updates existing bookings, and processes cancellations.

- ✅ **FAQs Retrieval Agent**  
  Answers customer questions related to hotel services, policies, amenities, and offers.

- ✅ **Main Triager Agent**  
  The central AI agent that professionally interacts with the user and delegates tasks to the appropriate sub-agent.

- ✅ **PostgreSQL Backend**  
  Persistent storage of room information and user bookings with constraint management.

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **FastAPI** (or Flask)
- **Chainlit** (for UI)
- **PostgreSQL**
- **SQLAlchemy** (ORM)
- **LangChain / OpenAI Agents SDK** (for agent orchestration)
- **.env for secrets**
- Optional: **Chainlit / Streamlit UI**

---

## 🧠 Agents Overview

### 🔹 1. `main_triager_agent`
- Understands user intent
- Routes requests to the right sub-agent:
  - `booking_agent`
  - `rooms_availability_checker_agent`
  - `FAQs_retreival`

### 🔹 2. `booking_agent`
- Collects required booking data:
  - `Name`, `CNIC`, `Contact`, `Room ID`
- Validates availability before booking
- Can:
  - Book new rooms
  - Cancel bookings
  - Update reserved rooms

### 🔹 3. `rooms_availability_checker_agent`
- Lists all available rooms
- Can check the status of a specific room (available/reserved)

### 🔹 4. `FAQs_retreival`
- Answers questions like:
  - "What’s the check-in time?"
  - "Do you provide airport pickup?"

---

## 🗃️ Database Schema

### `rooms` Table
```sql
room_id SERIAL PRIMARY KEY
room_number VARCHAR(10)
room_type VARCHAR(20)
price NUMERIC
status VARCHAR(10) CHECK (status IN ('available', 'reserved'))
```

### `user_booking` Table
```sql
id SERIAL PRIMARY KEY
CNIC VARCHAR(15) NOT NULL UNIQUE
name VARCHAR(20) NOT NULL
contact VARCHAR(20) NOT NULL
room_id INTEGER REFERENCES rooms(room_id)
```

---

## 🚀 How It Works

1. User interacts with the **main triager agent** via a chat interface.
2. Based on user intent:
   - It forwards the request to one of the specialized agents.
3. The chosen agent:
   - Collects required inputs
   - Uses database tools (e.g., `reserve_room`, `cancel_booking`)
   - Returns the response to the main agent
4. Main agent summarizes and returns results to the user.

---

## 🧪 Example Use Cases

- **User**: “I want to book room 4.”  
  **Agent**: “Sure! Please provide your name, CNIC, and contact.”  
  *(Passes data to `booking_agent`, which checks status and reserves.)*

- **User**: “Cancel my reservation.”  
  **Agent**: “Please share your CNIC to proceed.”  
  *(Uses `cancel_booking` tool.)*

- **User**: “Is room 3 available?”  
  *(Main agent delegates to `rooms_availability_checker_agent`.)*

- **User**: “Do you offer breakfast?”  
  *(Handled by `FAQs_retreival`.)*

---

## 📦 Running the Project

1. Clone the repo:

```bash
git clone https://github.com/MuhammadAbdullah95/customer_support_agent_openai_agents_sdk.git
cd customer_support_agent_openai_agents_sdk
```

2. Set up your `.env` file:

```
GOOGLE_API_KEY=your_api_key
HUGGINGFACEHUB_API_TOKEN=your_api_token
PINECONE_API_KEY=your_api_key
PINECONE_ENV=your_env
OPENAI_API_KEY=your_api_key
DB_USER=postgres
DB_PASS=yourpassword
DB_NAME=hotel_management_system
HOST=localhost
```

3. Set up PostgreSQL tables using `psql` or a DB GUI.

4. Install dependencies:

```bash
uv sync
```

5. Run the app:

```bash
uv run chainlit run main.py
```

---

## 📈 Future Improvements

- Add payment gateway integration
- Admin dashboard for managing bookings
- NLP improvements using RAG (Retrieval-Augmented Generation)
- Logging and analytics

---

## 👨‍💻 Author

Built with ❤️ by **Muhammad Abdullah** at [Ainnovate Solutions](#)

