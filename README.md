#  Promptify

> A Glorified AI Prompt Refinement Engine 
<img width="1920" height="1080" alt="Promptify Dashboard" src="https://github.com/user-attachments/assets/0366eb1e-f459-4a6f-bcaf-d791f2515748" />

---

### 🛠️ Tech Stack & Badges

[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Redis](https://img.shields.io/badge/Redis-Upstash-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://upstash.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Frontend-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)
[![Render](https://img.shields.io/badge/Render-Backend-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)

---

### Core Features

* **Asynchronous Prompt Refinement:** Uses dual-provider endpoints via **Groq** and **Google Gemini** to deliver low-latency optimized outputs.
* **Hybrid User Authentication:** Custom email/password accounts with securely salted password hashing and Google OAuth 2.0.
* **Intelligent Query Caching:** In-memory **Redis** caching to reduce redundant LLM calls and API overhead.
* **Sliding-Window Rate Limiting:** Tier-based usage quotas (Free and Premium) enforced by local sliding-window storage with progressive cooldowns.
* **Telemetry and Monitoring:** Integrated Prometheus metrics capturing latencies, session counts, and LLM call telemetry, with Grafana dashboards.

---

###  Directory Structure

```
├── backend/            # FastAPI backend server
│   ├── app/
│   │   ├── api/        # Auth and prompt enhancement API routers
│   │   ├── core/       # Configurations, logging, and database setup
│   │   ├── models/     # Pydantic validation schemas and document models
│   │   └── services/   # LLM integrations, sanitization, and rate-limiting
│   ├── main.py         # Entry point for backend
│   └── requirements.txt
├── frontend/           # React single-page application (TypeScript + Vite)
│   ├── src/
│   │   ├── components/ # Core UI elements, panels, and backgrounds
│   │   ├── contexts/   # User session and Auth state Context
│   │   ├── pages/      # Views: Limits page, Login page, Callback page
│   │   └── services/   # Fetch API integration
│   ├── index.html
│   └── vercel.json     # Client-side rewrites mapping for Vercel
```

---

###  Getting Started

#### Prerequisites
* Node.js (v18+)
* Python (v3.11+)
* A running MongoDB instance (Local or Atlas)
* A Redis instance (Local or Upstash)

#### 1. Setup Local Environment Files
Copy `.env.example` to `.env` in the root directory:
```bash
cp .env.example .env
```
Fill in your Groq, Gemini, and Google OAuth credentials.

#### 2. Run the Backend
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py
```
The API will start on `http://localhost:8000`.

#### 3. Run the Frontend
```bash
cd frontend
npm install
npm run dev
```
The client dashboard will open on `http://localhost:5173`.

---

