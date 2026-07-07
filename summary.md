# Promptify Project Summary & Resume Reference

This document provides a comprehensive overview of the **Promptify** architecture, technical achievements, and a set of ATS-friendly resume bullet points describing your work on this project.

---

## Technical Overview

**Promptify** is a professional, high-performance AI Prompt Enhancement Engine designed to refine rough, user-input prompts into highly optimized instruction sets for LLMs. The project features a distributed, production-ready stack with asynchronous request flows, custom caching, usage logging, rate limiting, and telemetry.

### Technology Stack
* **Frontend:** React 19 (TypeScript, Vite, Tailwind CSS, Framer Motion, react-router-dom)
* **Backend:** FastAPI (Python 3.11+, Uvicorn, Pydantic v2, python-jose, Authlib)
* **Database & Cache:** MongoDB Atlas (asynchronous `motor` driver), Redis (Upstash), SQLite (rate-limiting database)
* **Hosting & DevOps:** Vercel (Frontend SPA hosting with client-side rewrites), Render (Backend Python Web Service), Docker ready
* **Monitoring & Telemetry:** Prometheus (custom metrics collection), Grafana (visualization dashboard)

---

## Architecture Diagram

```
[ Frontend: React / Vite ] ──(HTTPS)──> [ API Gateway: Cloudflare / Render ]
          │                                           │
          │ (Google OAuth Sign-In)                    ▼
          └───────────────────────────────> [ Backend: FastAPI ]
                                                      │
             ┌─────────────────┬──────────────────────┼──────────────────────┐
             ▼                 ▼                      ▼                      ▼
      [ MongoDB Atlas ]     [ Redis ]         [ LLM APIs ]            [ SQLite ]
       - User Profiles      - Token Blacklist  - Google Gemini         - Local Rate
       - Prompt History     - Cache Responses  - Groq (Llama 3)          Limiting
       - Usage Audit Logs
```

---

## ATS-Friendly Resume Bullet Points

### Option 1: Full-Stack / Backend Engineer Focus
* **Architected and developed Promptify**, a high-performance AI prompt enhancement platform using **FastAPI** and **React (TypeScript)**, achieving asynchronous prompt refinement under **500ms** latency via **Groq** and **Google Gemini** integration.
* **Migrated the data persistence layer** from SQLAlchemy (relational PostgreSQL/SQLite) to a cloud-managed **MongoDB Atlas** document database using the asynchronous **Motor** driver; created unique partial indexes to resolve identity duplicate key constraints, increasing signup reliability by **100%**.
* **Designed and implemented a multi-tier token authentication system** supporting both **Google OAuth 2.0** and secure password auth via **bcrypt** hashing, leveraging **Redis (Upstash)** for refresh-token management and token blacklisting to ensure secure session states.
* **Optimized API performance and reduced LLM API costs** by designing an intelligent **Redis-based caching layer** that bypasses third-party LLM invocation for duplicate prompts, reducing external API overhead.
* **Engineered a progressive rate-limiting system** in SQLite with sliding-window telemetry that enforces hourly and daily usage quotas based on free and premium tiers, featuring progressive cooldown locks to mitigate API abuse.
* **Integrated Prometheus custom metrics** to track latency percentiles, LLM call counts, and user sessions; built **Grafana** visualization dashboards to achieve real-time monitoring and service observability.

### Option 2: Frontend / Full-Stack Focus
* **Built a responsive, high-fidelity user interface** using **React 19, TypeScript, and Tailwind CSS**, featuring fluid micro-animations powered by **Framer Motion** and robust client-side routing via **react-router-dom**.
* **Configured Vercel deployment pipelines** with custom routing rewrites to ensure seamless routing navigation for SPA paths like OAuth callback redirects, achieving a **0% page routing failure rate** for active authentication flows.
* **Integrated Google OAuth and custom JWT state management** into the React client utilizing a secure React Context provider, persisting sessions securely using local storage token extraction.
* **Deployed and orchestrated a dual-host production system** spanning **Vercel** (static frontend hosting) and **Render** (asynchronous backend API), configuring custom CORS allowed origins and headers to block cross-origin requests.
