# MediConnect — Hospital Management System (HMS)

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20Tailwind%20CSS-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![AI](https://img.shields.io/badge/AI-OpenRouter%20LLM-purple)](https://openrouter.ai)

MediConnect is a comprehensive, full-stack Hospital Management Web Platform designed with an intuitive user experience inspired by Apollo 24|7 and Practo. It features four role-based portals connected to a modular FastAPI backend with SQLite persistence and OpenRouter AI chat support.

---

## 🚀 Quick Setup & Run

### 1. Prerequisites
- **Python 3.10+** installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/Aayush349/Hospital-Management-System.git
cd Hospital-Management-System
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables
Copy the sample environment file and provide your OpenRouter API key:
```bash
cp .env.example .env
```
Open `.env` and insert your OpenRouter API key:
```ini
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 5. Launch the Application
Run the root launcher:
```bash
python start.py
```
This automatically initializes the SQLite database schema, applies initial seed records, and serves the application:
- 🌐 **Web Application**: [http://localhost:8000](http://localhost:8000)
- 📖 **Interactive Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📑 **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 👥 Default Demo Credentials

| Role | Username / Identifier | Password | Key Features |
|---|---|---|---|
| **Patient** | `tushar.tawar` | `patient123` | Book Appointments, View EHR, Order Home Lab Tests, AI Chatbot |
| **Doctor** | `dr.ananya` | `doctor123` | Real-time OPD Queue, Patient History Dossier, Digital Prescriptions |
| **Receptionist** | `receptionist` | `desk123` | Desk Check-In, Token Allocation, Doctor Availability Roster |
| **Admin** | `admin` | `admin@hms` | Real-time Analytics, Manage Doctors & Departments CRUD |

---

## 🏗️ Project Architecture

```
mediconnect3/
├── backend/
│   ├── main.py                    # FastAPI app entry point & static file hosting
│   ├── config.py                  # Environment config & OpenRouter setup
│   ├── db/                        # Database connection, DDL schema & seed data
│   ├── models/                    # Pydantic schemas (auth, appointments, doctors, etc.)
│   ├── services/                  # Business logic layer (CRUD operations, AI engine)
│   ├── routers/                   # REST API routes (FastAPI APIRouters)
│   ├── database.py                # Backward-compatibility facade
│   └── requirements.txt
├── src/                           # Frontend Source of Truth (Modular React JSX)
│   ├── components/                # Reusable UI (Navbar, Modals, AI Assistant)
│   ├── portals/                   # Role portals (Patient, Doctor, Receptionist, Admin)
│   ├── api/                       # API integration & service wrappers
│   └── data/                      # Baseline data & schemas
├── frontend/                      # Compiled production assets & offline vendor bundle
│   ├── index.html                 # Bundled Single Page Application (SPA)
│   └── vendor/                    # Offline React & Babel vendor assets
├── scripts/                       # Bundler & build automation tools
│   ├── build_bundle.py            # Compiles modular JSX into appBundle.jsx
│   └── rebuild_index.py           # Syncs appBundle into index.html
├── docs/                          # Project reports & audit documents
├── start.py                       # Unified root application runner
└── .env.example                   # Environment configuration template
```

---

## 🛠️ Rebuilding the Frontend Bundle
When making updates to modular source files in `src/`, compile and refresh the bundle with:
```bash
python scripts/build_bundle.py
python scripts/rebuild_index.py
```

---

## 📄 License
This project is open-source and available for educational and university demonstration purposes.
