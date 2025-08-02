# 📢 Case Study: AI-Powered Hotel Customer Support Assistant — by BlueOrbitAi

## 🔍 Overview

The **Ainnovate Hotel AI Booking System**, built by **BlueOrbitAi**, is a smart, multi-agent chatbot solution for **automating hotel customer support and booking operations**. This system lets users **check room availability**, **book or cancel reservations**, and ask **hotel-related FAQs** in natural language via a chat interface.

It leverages OpenAI's **Agents SDK**, **FastAPI**, and a robust **PostgreSQL database** to deliver real-time, reliable, and scalable AI-powered guest services.

---

## ⚠️ The Problem

* Hotels face high support costs due to repetitive guest queries.
* Manual booking processes are prone to errors.
* No 24/7 smart assistant for answering FAQs or modifying reservations.

---

## 💡 The Solution

The Ainnovate AI system provides a **central triager agent** that communicates with guests and delegates tasks to sub-agents. These include:

* A **room availability checker**
* A **booking and cancellation agent**
* An **FAQ retriever**

This modular design allows for accurate and timely support, reducing staff workload while enhancing guest experience.

---

## ✨ Key Features

| Feature                     | Description                                    |
| --------------------------- | ---------------------------------------------- |
| ✅ Room Availability Checker | Provides real-time room status info            |
| ✅ Booking Agent             | Books, updates, and cancels reservations       |
| ✅ FAQs Retrieval Agent      | Responds to hotel service and policy questions |
| ✅ Main Triager Agent        | Detects user intent and routes tasks           |
| ✅ PostgreSQL Database       | Stores room and user booking data securely     |

---

## ⚙️ Tech Stack

* **Python 3.11+** – Core language
* **FastAPI** – Backend framework
* **PostgreSQL** – Database for persistence
* **SQLAlchemy** – ORM layer
* **Chainlit** – Chat UI (development mode)
* **OpenAI Agents SDK** – Agent architecture and tool management
* **LangChain** – Optional orchestration layer

---

## 🧠 Agent Architecture

1. **Main Triager Agent**
   ├─ Analyzes user input and selects sub-agent

2. **Booking Agent**
   ├─ Handles:

   * New bookings (name, CNIC, contact, room ID)
   * Reservation updates
   * Booking cancellations

3. **Room Availability Checker**
   ├─ Lists available rooms and checks specific room statuses

4. **FAQs Retrieval Agent**
   ├─ Answers questions like "Do you offer breakfast?" or "What’s the checkout time?"

---

## 📂 Database Schema

**rooms**

* room\_id (PK)
* room\_number
* room\_type
* price
* status (available / reserved)

**user\_booking**

* id (PK)
* CNIC (unique)
* name
* contact
* room\_id (FK)

---

## 💬 Real-World Use Cases

| User Query              | System Behavior                                |
| ----------------------- | ---------------------------------------------- |
| "Book room 4"           | Requests user details, books via booking agent |
| "Cancel my reservation" | Asks for CNIC, cancels booking                 |
| "Is room 3 available?"  | Checks via availability agent                  |
| "Do you offer pickup?"  | Answered by FAQ agent                          |

---

## 📈 Results & Impact

* 💬 100% of basic queries answered by AI
* ⏱️ Average reply time: **\~2 seconds**
* ✉️ Reduced booking errors through validation + constraints
* ✨ Seamless experience for guests via natural language

---

## 🚀 Future Roadmap

* 💳 Payment gateway integration
* 📊 Admin dashboard for hotel management
* 🧠 RAG-powered answer refinement
* ✉️ Multilingual support and voice input
* 📉 Analytics and logging for usage tracking

---

## 👨‍💼 Author

**Muhammad Abdullah**
CTO at [BlueOrbitAi](https://www.blueorbitai.com)
Agent Developer | Backend Engineer | AI Architect

📨 **Contact:** [ma2404374@gmail.com](mailto:ma2404374@gmail.com)
🔗 **GitHub:** [MuhammadAbdullah95](https://github.com/MuhammadAbdullah95)
📁 **Project Repo:** [GitHub Link](https://github.com/MuhammadAbdullah95/customer_support_agent_openai_agents_sdk)

---
