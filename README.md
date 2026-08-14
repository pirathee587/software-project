# 🌍 TravelHub — Full-Stack Travel Management Platform

<div align="center">

![TravelHub](https://img.shields.io/badge/TravelHub-v1.0.0-blue?style=for-the-badge)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.5.11-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white)
![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Java](https://img.shields.io/badge/Java-21-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

**A comprehensive travel booking and management platform connecting tourists, travel agencies, hotel owners, and administrators.**

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [API Overview](#-api-overview)
- [User Roles](#-user-roles)
- [Database Entities](#-database-entities)
- [Running Tests](#-running-tests)

---

## 🌐 Project Overview

TravelHub is a multi-role, full-stack travel management platform that enables:

- 🧳 **Tourists** to discover, book, and review travel packages, hotels, and vehicles
- 🏢 **Travel Agencies** to create and manage tour packages, bookings, drivers, and vehicles
- 🏨 **Hotel Owners** to manage hotel listings, rooms, amenities, and view analytics
- 🛡️ **Administrators** to oversee all platform activity, users, agents, payments, and notifications
- 🤖 **AI Chatbot** powered by LangChain + Groq to assist users with travel recommendations

---

## 🏗️ Architecture

The platform follows a **3-tier microservice-style architecture**:

```
+--------------------------------------------------+
|            React Frontend  (Port 5173)           |
|         TypeScript + Vite + TailwindCSS          |
+--------------------+-----------------------------+
                     |  REST API (Axios)
          +----------+----------+
          |                     |
+---------v----------+ +--------v-----------+
|  Spring Boot API   | |  Python Chatbot    |
|    (Port 8080)     | |  Service (Port 8000)|
|  JWT + Security    | |  LangChain + Groq  |
+---------+----------+ +--------+-----------+
          |                     |
+---------v---------------------v-----------+
|          PostgreSQL  (via Supabase)        |
|        Supabase Storage  (Images)          |
+--------------------------------------------+
```

---

## ✨ Features

### 👤 Tourist Portal
- Browse and search tour packages and hotels
- Book travel packages with full itinerary details
- Hotel room booking with preference selection
- Vehicle / transport booking
- Secure online payments via **PayHere**
- Refund request management
- Write and manage reviews with image uploads
- AI-powered chatbot for travel assistance
- Document upload and verification
- Real-time notifications

### 🏢 Travel Agency Portal
- Create, update, and manage tour packages with itineraries and images
- Manage vehicle fleet and driver assignments
- View and handle booking requests
- Agent analytics dashboard with charts
- Notification management
- Profile and settings management

### 🏨 Hotel Owner Portal
- Add and manage hotel listings with amenities
- Room management (add, edit, delete rooms)
- View booking history and analytics
- Dashboard with occupancy metrics

### 🛡️ Admin Portal
- Full platform oversight and user management
- Agent approval and account management
- Payment and refund management
- Broadcast notifications to all users
- Hotel and package moderation
- Analytics and reporting dashboards

### 🤖 AI Chatbot Service
- RAG (Retrieval-Augmented Generation) using ChromaDB vector store
- Real-time data sync with backend via scheduled jobs
- Powered by **Groq LLM** + **LangChain**
- Sentence-transformer embeddings for semantic search

---

## 🛠️ Tech Stack

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| React | 18.3 | UI Framework |
| TypeScript | 6.0 | Type Safety |
| Vite | 5.4 | Build Tool & Dev Server |
| TailwindCSS | 3.4 | Utility-First Styling |
| Radix UI | Latest | Accessible UI Primitives |
| React Router DOM | 6.30 | Client-side Routing |
| React Hook Form | 7.61 | Form Management |
| Zod | 3.25 | Schema Validation |
| TanStack Query | 5.83 | Server State Management |
| Axios | 1.6 | HTTP Client |
| Framer Motion | 12.42 | Animations |
| Recharts | 2.15 | Data Visualization |
| Supabase JS | 2.108 | Storage & Auth |

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Spring Boot | 3.5.11 | REST API Framework |
| Java | 21 | Programming Language |
| Spring Security | Latest | Authentication & Authorization |
| Spring Data JPA | Latest | ORM / Database Access |
| PostgreSQL | Latest | Primary Database |
| Flyway | Latest | Database Migrations |
| JWT (jjwt) | 0.12.6 | Token-based Authentication |
| Lombok | 1.18.46 | Boilerplate Reduction |
| OpenPDF | 2.0.3 | PDF Generation |
| Spring Mail | Latest | Email Notifications |
| TestNG + Mockito | 7.9 | Unit Testing |

### Chatbot Service
| Technology | Version | Purpose |
|---|---|---|
| FastAPI | 0.111 | REST API Framework |
| Python | 3.10+ | Programming Language |
| LangChain | 0.2.6 | LLM Orchestration |
| LangChain-Groq | 0.1.6 | Groq LLM Integration |
| ChromaDB | 0.5.0 | Vector Store |
| Sentence-Transformers | 3.0 | Text Embeddings |
| Uvicorn | 0.29 | ASGI Server |

### Infrastructure & External Services
| Service | Purpose |
|---|---|
| Supabase | PostgreSQL hosting + File Storage |
| Groq | LLM API for AI chatbot |
| PayHere | Payment gateway integration |
| Gmail SMTP | Transactional email notifications |

---

## 📁 Project Structure

```
travelhub/
|
+-- frontend/                           # React + Vite + TypeScript
|   +-- src/
|   |   +-- auth/                       # Login, register, auth guards
|   |   +-- components/                 # Shared/reusable UI components
|   |   +-- context/                    # React context providers
|   |   +-- features/
|   |   |   +-- admin/                  # Admin dashboard & pages
|   |   |   +-- agency/                 # Travel agency pages
|   |   |   +-- hotelOwner/             # Hotel owner pages
|   |   |   +-- tourist/                # Tourist-facing pages
|   |   +-- hooks/                      # Custom React hooks
|   |   +-- routes/                     # Route configuration
|   |   +-- services/                   # API service layer (Axios)
|   |   +-- styles/                     # Global CSS styles
|   |   +-- utils/                      # Utility/helper functions
|   +-- .env.example
|   +-- package.json
|   +-- vite.config.js
|
+-- backend/                            # Spring Boot REST API
|   +-- src/main/java/com/travelhub/backend/
|   |   +-- config/                     # Spring Beans & configuration
|   |   +-- controller/                 # 41 REST API controllers
|   |   +-- dto/                        # Data Transfer Objects
|   |   +-- entity/                     # 22 JPA entity classes
|   |   +-- enums/                      # Enum definitions
|   |   +-- event/                      # Spring application events
|   |   +-- listener/                   # Event listeners
|   |   +-- repository/                 # Spring Data JPA repositories
|   |   +-- security/                   # JWT filter & Spring Security
|   |   +-- service/                    # Business logic layer
|   |   +-- util/                       # Helper utilities
|   +-- .env.example
|   +-- pom.xml
|
+-- chatbot-service/                    # Python AI chatbot microservice
    +-- main.py                         # FastAPI app + LangChain RAG pipeline
    +-- data_sync.py                    # Syncs backend data to vector store
    +-- chroma_data/                    # ChromaDB persistent vector storage
    +-- requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Java JDK | 21 | [adoptium.net](https://adoptium.net/) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org/) |
| Python | 3.10+ | [python.org](https://www.python.org/) |
| Supabase Account | — | [supabase.com](https://supabase.com/) |
| Groq API Key | — | [console.groq.com](https://console.groq.com/) |

---

### 1️⃣ Backend Setup

```bash
# Navigate to backend
cd backend

# Copy and fill in environment variables
cp .env.example .env

# Run with the bundled Maven wrapper
./mvnw spring-boot:run

# Windows PowerShell
.\mvnw.cmd spring-boot:run
```

> API will be available at **http://localhost:8080**

---

### 2️⃣ Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install all npm dependencies
npm install

# Copy and fill in environment variables
cp .env.example .env

# Start the Vite development server
npm run dev
```

> App will be available at **http://localhost:5173**

---

### 3️⃣ Chatbot Service Setup

```bash
# Navigate to chatbot service
cd chatbot-service

# Create and activate a Python virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
# Add: GROQ_API_KEY=your_key
# Add: BACKEND_URL=http://localhost:8080

# Start the FastAPI server
uvicorn main:app --reload --port 8000
```

> Chatbot API will be available at **http://localhost:8000**

---

## 🔐 Environment Variables

### `backend/.env`

| Variable | Description |
|----------|-------------|
| `DB_URL` | Supabase PostgreSQL JDBC connection string |
| `DB_USERNAME` | Database username (e.g. `postgres.<project-ref>`) |
| `DB_PASSWORD` | Database password |
| `GMAIL_APP_PASSWORD` | Gmail App Password for SMTP email sending |
| `SUPABASE_KEY` | Supabase anonymous / service role API key |
| `PAYHERE_SECRET` | PayHere merchant secret for payment verification |

### `frontend/.env`

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend base URL (default: `http://localhost:8080`) |
| `VITE_SUPABASE_URL` | Supabase project URL |
| `VITE_SUPABASE_KEY` | Supabase anonymous key |

### `chatbot-service/.env`

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key for LLM access |
| `BACKEND_URL` | Backend API base URL |

---

## 📡 API Overview

The backend exposes **41 REST controllers**:

| Controller | Purpose |
|-----------|---------|
| `AuthController` | Login, register, JWT refresh |
| `UserController` | User profile management |
| `BookingController` | Create, view, cancel bookings |
| `PackageController` | Browse tour packages |
| `HotelController` | Browse hotels |
| `RoomController` | Room availability & booking |
| `ReviewController` | Submit and view reviews |
| `PaymentController` | PayHere payment processing |
| `RefundController` | Refund request management |
| `ChatbotController` | AI chatbot proxy |
| `RecommendationController` | AI-based recommendations |
| `AgentPackageController` | Agency package management |
| `AgentBookingController` | Agency booking handling |
| `AgentVehicleController` | Vehicle & driver management |
| `OwnerHotelController` | Hotel owner management |
| `AdminDashboardController` | Admin analytics |
| `AdminUserController` | Admin user management |
| `AdminPaymentController` | Admin payment oversight |
| `AdminNotificationController` | Broadcast notifications |
| `DocumentController` | Document upload & verification |

> All secured endpoints require **`Authorization: Bearer <JWT>`** header.

---

## 👥 User Roles

| Role | Description | Portal |
|------|-------------|--------|
| `TOURIST` | End-user who books travel | Tourist portal |
| `AGENT` | Travel agency representative | Agency portal |
| `HOTEL_OWNER` | Hotel property owner | Hotel owner portal |
| `ADMIN` | Platform administrator | Admin portal (full access) |

---

## 🗄️ Database Entities

| Entity | Description |
|--------|-------------|
| `User` | Platform users (all roles) |
| `Agent` | Travel agency profiles |
| `AgentSettings` | Agency configuration |
| `Hotel` | Hotel property listings |
| `Room` | Individual hotel rooms |
| `Amenity` | Hotel amenities |
| `Package` | Tour packages |
| `PackageItinerary` | Day-by-day tour itinerary |
| `PackageImage` | Package gallery images |
| `Booking` | Travel bookings |
| `BookingHotelPreference` | Hotel preferences per booking |
| `Vehicle` | Agency vehicle records |
| `Driver` | Agency driver records |
| `VehicleOwner` | Vehicle ownership mapping |
| `Payment` | Payment transactions |
| `RefundRequest` | Refund requests |
| `Review` | User-submitted reviews |
| `ReviewImage` | Review photo attachments |
| `Notification` | System notifications |
| `UserNotification` | Per-user notification state |
| `Document` | Uploaded verification documents |
| `EmailLog` | Email delivery audit log |

---

## 🧪 Running Tests

```bash
# Backend unit tests (TestNG + Mockito)
cd backend
./mvnw test

# Frontend ESLint check
cd frontend
npm run lint
```

---

## 📝 License

This project was developed as a software engineering capstone project.  
All rights reserved © TravelHub Team.

---

<div align="center">
  <strong>Built with ❤️ by the TravelHub Team</strong>
</div>
