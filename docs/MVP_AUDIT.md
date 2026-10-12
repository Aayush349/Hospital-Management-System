# MediConnect HMS — Demo → MVP Audit

**Date:** 10 Oct 2026  
**Author:** Junior developer walkthrough (code + live start)  
**Goal:** Map frontend/backend flows, record every blocker, then fix them in later sessions.

This file is the working backlog. Do **not** treat the app as production-ready until the P0 and P1 items below are closed.

---

## 1. What I started and what happened

### Frontend (works as a static demo)

```bash
cd d:\HMS\mediconnect3
python -m http.server 5173
```

- `http://localhost:5173` → **HTTP 200** (login UI loads).
- `http://localhost:5173/api/health` → **HTTP 404** (Python static server does not proxy `/api`).

The live UI is `index.html` + Babel-in-browser (React UMD from `/vendor`). Source of truth for a pitch is the **inlined script inside `index.html`**, not the `src/*.jsx` files unless you rebuild.

### Backend (does not start on this machine)

```bash
cd d:\HMS\mediconnect3\server
npm install
node server.js
```

| Step | Result |
|------|--------|
| `npm install` | **Failed.** `better-sqlite3` has no prebuild for Node **v22.14.0** on Windows, then `node-gyp rebuild` failed: VS2019 Build Tools is present but **missing the C++ toolset**. |
| `node server.js` | **Failed.** `Cannot find module 'express'` (install rolled back; no usable `node_modules`). |
| `http://localhost:5000/api/health` | **Unable to connect** |

Until native SQLite compiles (or we swap to a pure-JS DB), the Node API cannot run. The frontend silently falls back to **localStorage mock data**.

---

## 2. How the project is actually wired

```
Browser  →  python http.server :5173  →  index.html (Babel compiles JSX in the browser)
                │
                └── fetch('/api/...')   ✗ no reverse proxy to :5000

Intended (not working here):
Browser  →  /api/*  →  Express :5000  →  SQLite mediconnect.db
                └── also writes fake Firebase config / optional Firestore
```

**Three copies of the frontend exist and can drift:**

| Copy | Path | Used at runtime? |
|------|------|------------------|
| Modular sources | `src/**/*.jsx` | Only if you rebuild |
| Compiled bundle | `src/appBundle.jsx` | Built by `build_bundle.py` |
| Inlined app | `index.html` `<script type="text/babel">` | **Yes — this is what the browser runs** |

Python helpers (`build_bundle.py`, `rebuild_index.py`, `embed_bundle.py`, `fix_*.py`) exist because keeping those copies in sync is already a known pain.

---

## 3. Frontend flows (what the UI thinks it does)

### 3.1 Auth (gate for everything)

**Screen:** `LoginPage.jsx`

Roles: `patient` | `doctor` | `admin` | `receptionist`

| Flow | UI steps | Intended API | Actual today |
|------|----------|--------------|--------------|
| Login | Identifier + password + role radio | `POST /api/auth/login` | Endpoint **does not exist**. Falls back to `localStorage` users from `mockData.js`. |
| Sign up | Name, email, phone, password, 4-digit PIN (patient/doctor only) | `POST /api/auth/signup` | Endpoint **does not exist**. User is stored only in `localStorage`. Doctor stays `pending`. |
| Forgot password | Fake OTP on screen + PIN + new password | `POST /api/auth/forgot-password` | Endpoint **does not exist**. OTP is generated in the browser and shown in the UI. |
| Session | `sessionStorage.mediconnect_session` | None | Logout clears session. No JWT, cookies, or server session. |
| Quick Access buttons | Fill demo email/password | — | **Does not switch the role radio.** If you stay on Doctor and click Patient credentials, login fails because role is sent with the request. |

Demo accounts (from `src/data/mockData.js` `INITIAL_USERS`):

| Role | Email | Password | PIN |
|------|-------|----------|-----|
| Patient | `tushar.tawar@example.com` | `patient123` | `1234` |
| Doctor | `dr.ananya@mediconnect.in` | `doctor123` | `4321` |
| Admin | `admin@mediconnect.in` | `admin@hms` | `9999` |
| Receptionist | `receptionist@mediconnect.in` | `desk123` | `7777` |

**Identity mismatch:** login user id is `usr-1` named **Tushar Tawar**. Backend seed patient is `patient-1` named **Aarav Sharma**. Mock patient profile is `pat-101`. Isolation logic mixes all three.

### 3.2 Patient portal

Tabs: Home → Find doctors → Book → Health records → Home sample tracker → Profile → Share EHR.

| Flow | What happens | Gap vs real MVP |
|------|----------------|-----------------|
| Search doctors | Filter `doctors` already loaded in App state | Search is client-side only. |
| Book appointment | `BookingModal` 4-step stepper → `apiService.bookAppointment` | Date chips are **hardcoded Sep 2026** (`2026-09-17` …), not “today”. Payload uses `timeSlot` / `doctorSpecialty`; backend expects `time` / `specialty`. `patientId` defaults to `pat-101` while backend uses `patient-1`. |
| View appointments | Filtered in `App.jsx` by `patientId` **or name** | Logged-in user is `usr-1`. Seed APTs use `pat-101` / `patient-1`. Name match may save the demo; any new signup will see an **empty list**. |
| Profile edit | `PUT /api/patients/current` | Backend always updates **only** `patient-1`. New patients never get a `patients` row. |
| Lab packages | `GET /api/lab/packages` | Backend returns hardcoded JSON (OK for MVP). |
| Home sample | `POST /api/lab/home-sample` | Always stored as `patient-1` on backend. “Simulate next stage” is a demo button, not a real lab workflow. |
| Share records | Create token + password in localStorage | **No backend table.** Link only works in the same browser. |
| AI assistant | Keyword `detectIntent` + canned replies | Not LLM. Chat history can POST to `/api/chat/message` if server is up. |

### 3.3 Doctor portal

Sub-tabs: OPD queue, availability/slots, manage receptionist.

| Flow | Gap |
|------|-----|
| Resolve current doctor | Matches `authUser.id` (`usr-2`) to `doctors.id` (`doc-1`) — **IDs never match**. Falls back to name contains `"ananya"` or `doctors[0]`. Second doctor (`Dr. Rajan Mehta`) can land on the wrong queue. |
| Queue statuses | UI uses Waiting / In-Consultation / Completed. Backend seed uses `Upcoming` / `Completed`. Filter mismatch. |
| Write prescription | `POST /api/prescriptions` | If backend is up, appointment is marked Completed. Payload `patientName` is not stored in SQL. |
| Slot manager | `PUT /api/doctors/:id` | Works if IDs line up. |
| Create receptionist | `registerUser` | No users table. Stored in localStorage only. |

### 3.4 Receptionist portal

| Flow | Gap |
|------|-----|
| Assigned doctor | `authUser.assignedDoctorId` (`doc-1`) | Walk-in booking sends `timeSlot`, not `time`. |
| Booked-slot check | Uses `a.timeSlot` | Backend appointments have `time`, so **double-booking is not detected** when API is live. |

### 3.5 Admin portal

| Flow | Gap |
|------|-----|
| KPI cards | `GET /api/admin/stats` | Mix of real counts + **hardcoded** `bedOccupancy: 73`, `patientSatisfaction: 4.8`, `avgWaitTime: 12`, `onlineConsultations: 45`. Charts in `ReportsAnalytics` ignore live appointments and use **fake weekly arrays**. |
| Add doctor / department | POST endpoints exist | No auth. Duplicate department ids crash SQLite (`PRIMARY KEY`). |
| Verify pending doctor | `verifyDoctorUser` | **localStorage only.** Backend never stores pending doctors. |
| Export PDF | `alert("Simulated...")` | Not implemented. |
| Role switcher / RoleModal | Still in the app after login | Lets a logged-in **patient** open Admin/Doctor views. Demo leftover, not MVP-safe. |

### 3.6 Shared EHR (pan-India link)

URL: `?share=TOKEN` or `#share=TOKEN` → `DoctorSharedEhrView` **bypasses login**.

Unlock, revoke, access limits, and logs are **localStorage only**. Another device/browser cannot open the record.

---

## 4. Backend flows (what `server/server.js` actually exposes)

SQLite file: `server/mediconnect.db` (created on first successful start).

### Tables

`departments`, `doctors`, `patients`, `appointments`, `prescriptions`, `lab_reports`, `sample_orders`, `chat_messages`

**Missing tables the frontend already calls:** `users`, `share_links`, receptionist assignment, payments, notifications.

### Implemented routes

| Method | Path | Notes |
|--------|------|--------|
| GET | `/api/health` | OK |
| GET/POST | `/api/departments` | POST: `name.toLowerCase()` throws if `name` missing |
| GET | `/api/doctors`, `/api/doctors/:id` | |
| POST/PUT | `/api/doctors`, `/api/doctors/:id` | |
| GET/PUT | `/api/patients/current` | **Hardcoded `patient-1`** |
| GET/POST | `/api/appointments` | ID `APT-` + random 4 digits — **collision possible** |
| PATCH | `/api/appointments/:id/status` | No 404 if id missing |
| GET/POST | `/api/prescriptions` | Not filtered by patient/doctor |
| GET | `/api/lab/reports`, `/api/lab/packages` | Packages not in DB |
| GET/POST | `/api/lab/home-sample` | Always `patient-1` |
| PATCH | `/api/lab/orders/:id/status` | |
| GET | `/api/admin/stats` | Partial fake KPIs |
| GET/POST/DELETE | `/api/chat/history`, `/api/chat/message` | Storage only |

### Frontend calls that **have no backend route**

- `GET /api/users`
- `POST /api/auth/signup`
- `POST /api/auth/login`
- `POST /api/auth/forgot-password`
- share-link CRUD

`apiFetch` treats any non-OK response as `null` and **silently falls back to mock data**, so the UI looks “fine” while the API is missing.

### Seed data problems

- Seed patient: `patient-1` / **Aarav Sharma** vs UI **Tushar Tawar** / `pat-101` / `usr-1`.
- Seed appointments: `2025-08-10`, `2025-08-22`, `2025-09-15` — all in the past relative to **Oct 2026**.
- `doctor_count` on departments is static seed numbers, not `COUNT(doctors)`.

---

## 5. End-to-end map (MVP critical path)

```
[Login] ──✗── no /auth/* ──► localStorage users
   │
   ├─ Patient books OPD
   │     payload timeSlot/specialty/patientId=pat-101
   │     ──✗── column/field mismatch ──► SQLite appointment incomplete or empty queue
   │
   ├─ Doctor opens queue
   │     auth usr-2 vs doctor doc-1 ──✗── wrong/empty queue
   │     writes Rx ──► prescriptions table (if server up)
   │     patient records ──✗── isolation by wrong ids
   │
   ├─ Receptionist walk-in
   │     ──✗── same booking payload mismatch
   │
   ├─ Admin KPIs
   │     ──⚠── live counts mixed with fake charts
   │
   └─ Share EHR / Firebase / AI
         ──✗── local only / demo Firebase key / keyword bot
```

---

## 6. Issue list (fix these)

Severity: **P0** = MVP cannot work without it · **P1** = core flow broken · **P2** = quality / security · **P3** = polish.

### P0 — Cannot even run a real stack

| ID | Issue | Where |
|----|--------|--------|
| P0-1 | `better-sqlite3` does not install on Node 22 + this Windows VS setup | `server/package.json` |
| P0-2 | Backend `node_modules` missing; `express` not installed | `server/` |
| P0-3 | Frontend `BASE_URL = '/api'` but static server is `:5173` and API is `:5000` — **no proxy** | `src/api/apiService.js` |
| P0-4 | Auth APIs the login page depends on do not exist | `server.js` vs `apiService.js` |
| P0-5 | No `users` table; passwords live in `localStorage` as plaintext | mock + LoginPage |

### P1 — Core product flows broken even if the server starts

| ID | Issue | Where |
|----|--------|--------|
| P1-1 | Patient IDs disagree: `patient-1` vs `pat-101` vs `usr-1` | seed, mockData, App isolation |
| P1-2 | Patient names disagree: Aarav Sharma vs Tushar Tawar vs README Aarav | seed / Login / README |
| P1-3 | Doctor user id `usr-2` ≠ doctor row `doc-1` | App.jsx, DoctorPortal.jsx |
| P1-4 | Booking payload: `timeSlot` / `doctorSpecialty` vs API `time` / `specialty` | BookingModal, ReceptionistPortal, server |
| P1-5 | Isolation uses `authSession.user.id` so new patients/doctors see **no records** | App.jsx |
| P1-6 | Doctor queue hardcoded `includes('ananya')` | App.jsx |
| P1-7 | Appointment statuses: UI Waiting/In-Consultation vs DB Upcoming | DoctorPortal, server |
| P1-8 | `GET /api/patients/current` always `patient-1` — no multi-patient | server.js |
| P1-9 | Home sample always `patient-1` | server.js |
| P1-10 | Share links / revoke / unlock not persisted in SQLite | apiService.js |
| P1-11 | `verifyDoctorUser` never hits the API | apiService.js |
| P1-12 | Role switcher still allows any logged-in user to open other portals | Navbar / RoleModal / App.jsx |
| P1-13 | Booking dates hardcoded to mid-September 2026, not calendar-relative | BookingModal.jsx |
| P1-14 | `checkServer()` caches `serverAvailable` for the whole page lifetime — if API starts later, UI never retries | apiService.js |
| P1-15 | Failed API (`!res.ok`) returns `null` → silent mock fallback (looks successful, data not saved) | apiFetch |
| P1-16 | Prescriptions/labs/appointments APIs return **all rows** (no patient/doctor filter) | server.js |
| P1-17 | `index.html` vs `src/` can drift; fixing `src/` does not change the running demo until rebuild | index.html, build scripts |

### P2 — Security, data integrity, crashes

| ID | Issue | Where |
|----|--------|--------|
| P2-1 | No auth middleware; CORS `*` | server.js |
| P2-2 | Passwords stored plaintext (localStorage + would-be DB) | mockData, registerUser |
| P2-3 | Share EHR page skips login (`?share=`) | App.jsx |
| P2-4 | Forgot-password OTP is shown on screen (simulated) | LoginPage.jsx |
| P2-5 | Firebase config is a **demo/fake** project id and API key | firebaseService.js |
| P2-6 | `POST /departments` crashes if `name` is missing | server.js |
| P2-7 | Duplicate department id / random APT/RX/HSL ids can collide (PK error unhandled) | server.js |
| P2-8 | PATCH appointment with unknown id returns `null` JSON | server.js |
| P2-9 | `App.jsx` uses `<Icons.ShieldCheck>` but **does not import Icons** (breaks if you run modular src instead of the bundle) | src/App.jsx |
| P2-10 | Signup success path never `setLoading(false)` | LoginPage.jsx |
| P2-11 | Quick Access buttons do not set `selectedRole` | LoginPage.jsx |
| P2-12 | Admin stats / analytics charts are mostly fake | ReportsAnalytics, admin stats |
| P2-13 | No input validation (email, phone, fee, dates) on API | server.js |
| P2-14 | Chat delete without `sessionId` does not clear all (and never 404s) | server.js |
| P2-15 | `uuid` package is deprecated (install warning) | package.json |

### P3 — Demo leftovers / MVP polish

| ID | Issue | Where |
|----|--------|--------|
| P3-1 | README still says “mock service + role switcher, no login” | README.md |
| P3-2 | README patient UHID `MC-2026-8941` vs mock `MC-2026-9082` | README vs mockData |
| P3-3 | AI assistant is keyword matching, advertised as AI | AiAssistantModal.jsx |
| P3-4 | “Simulate next lab stage” is a presenter cheat | HomeSampleTracker |
| P3-5 | Export analytics PDF is `alert()` | ReportsAnalytics |
| P3-6 | Payments are labels only (UPI/Card/Pay at Clinic) — no transaction | BookingModal |
| P3-7 | Video consult is a type label, no WebRTC | BookingModal |
| P3-8 | Browser compiles JSX via Babel every load (slow, not an MVP deploy story) | index.html |
| P3-9 | Temp Chrome profiles (`temp_eval_profile`, etc.) pollute the repo | project root |
| P3-10 | Unsplash avatars need network; fail offline | mock doctors |
| P3-11 | Navbar fallback names still say Aarav / Ananya | Navbar.jsx |
| P3-12 | RoleModal toast still says Aarav Sharma | App.jsx |
| P3-13 | `engines.node >= 16` but better-sqlite3 9.x is painful on Node 22 | package.json |
| P3-14 | No `.env`, no `.gitignore` hygiene for `mediconnect.db` / `node_modules` | server/ |
| P3-15 | Doctor mock slots in `mockData.js` differ from backend seed for the same doctor | mock vs server.js |
| P3-16 | Receptionist generateSlots uses 12-hour strings that may not match doctor `availableSlots` | ReceptionistPortal |
| P3-17 | `getUsers()` 404s forever while server is “up”, then falls back — mixed cloud/local users | apiService |

---

## 7. Suggested MVP fix order (next sessions)

We should fix in this order so each step is testable:

1. **Make the stack boot**  
   Replace `better-sqlite3` with `sql.js` **or** pin Node 20 LTS **or** install VS “Desktop development with C++”. Add a tiny proxy so the browser’s `/api` hits `:5000` (Express can also `express.static` the frontend).

2. **Single identity model**  
   One patient id, one doctor id, one user id mapping (`users.doctor_id`, `users.patient_id`). Align seed + mock + login demos to the same names.

3. **Auth on the server**  
   `users` table, signup/login/reset, hashed passwords (even for MVP), session token. Remove silent mock fallback when we want “real MVP mode”.

4. **Align booking/prescription payloads**  
   Same field names (`time` vs `timeSlot`), statuses, and filters by logged-in id.

5. **Lock portals to the logged-in role**  
   Kill (or hide) the demo Role Switcher.

6. **Persist share links** (or cut the feature from MVP scope).

7. **Rebuild `index.html` from `src/` once** so we stop editing two apps.

8. **Strip Firebase/demo KPIs** or mark them clearly as “not in MVP”.

---

## 8. Out of scope for a first working MVP (cut or stub)

- Real payments / UPI  
- Real video consultation  
- Real Google Cloud Firestore  
- Real LLM assistant  
- PDF export  
- Multi-hospital / ABDM  
- True pan-India share without a backend  

Keep the UI, but do not claim they are live.

---

## 9. How to re-test after we start fixing

```bash
# Backend
cd server
npm install
npm start
curl http://localhost:5000/api/health

# Frontend (until we add a proxy)
cd ..
python -m http.server 5173
# Then login with demo users and book an appointment.
# Confirm the new row exists in SQLite, not only in localStorage.
```

**Definition of done for “working MVP”:**

- Backend starts without native-compile drama.  
- Login hits SQLite, not localStorage.  
- Patient books → doctor sees that appointment → doctor writes Rx → patient sees Rx.  
- Receptionist walk-in appears in that doctor’s queue.  
- Admin counts match those records.  
- A second browser/profile sees the same data.

---

*Runtime captured 10 Oct 2026: frontend 200 on :5173; backend not running; `/api/health` 404 from the static server; `npm install` failed on `better-sqlite3` / missing MSVC toolset.*
