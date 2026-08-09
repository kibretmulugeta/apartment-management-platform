# Production Deployment Guide — Apartment Rental & Property Management Platform

This document outlines the step-by-step production deployment instructions for the **Apartment Rental & Property Management Platform** using **Vercel** (Frontend) and **Render / Railway** (FastAPI Backend, PostgreSQL, Redis, Celery Worker).

---

## 1. Monorepo Structure Verification

Ensure your GitHub repository (`apartment-management-platform`) maintains the following clean structure:

```text
apartment-management-platform/
│
├── frontend/                  # Next.js App Router (JavaScript / .jsx / Tailwind CSS)
│   ├── app/
│   ├── components/
│   ├── public/
│   ├── package.json
│   ├── jsconfig.json
│   └── vercel.json            # Vercel Deployment Blueprint
│
├── backend/                   # FastAPI Backend & Celery Worker
│   ├── app/
│   ├── migrations/            # Alembic Migrations
│   ├── seed.py                # Production Seed Script
│   ├── requirements.txt
│   └── Dockerfile
│
├── render.yaml                # Render Infrastructure-as-Code Blueprint
├── docker-compose.yml         # Local Docker Orchestration
├── .env.example               # Production Environment Template
└── README.md
```

---

## 2. Backend & Worker Infrastructure Deployment (Render)

### Option A: Automatic Blueprint Deployment (Recommended)
1. Push your monorepo code to GitHub (`git push origin main`).
2. Log into [Render Dashboard](https://dashboard.render.com).
3. Click **New +** -> **Blueprints**.
4. Connect your GitHub repository `apartment-management-platform`.
5. Render will automatically detect `render.yaml` and provision:
   - **PostgreSQL 15 Managed Database** (`apparent-postgres`)
   - **Redis Instance** (`apparent-redis`)
   - **FastAPI Web Service** (`apparent-backend`)
   - **Celery Worker** (`apparent-worker`)

### Option B: Manual Service Setup (Render / Railway)

#### Web Service (FastAPI)
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  ```ini
  ENVIRONMENT=production
  DEBUG=false
  DATABASE_URL=postgresql://<user>:<pass>@<host>/<dbname>
  REDIS_URL=redis://<host>:<port>/0
  JWT_SECRET=<secure_production_secret_32_bytes_min>
  JWT_REFRESH_SECRET=<secure_refresh_secret_32_bytes_min>
  STRIPE_SECRET_KEY=sk_live_...
  BREVO_API_KEY=<your_brevo_api_key>
  EMAIL_PROVIDER=brevo
  ```

#### Background Worker (Celery)
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `celery -A app.workers.celery_app worker --loglevel=info`
- **Environment Variables**: *(Matches Web Service)*

---

## 3. Frontend Deployment (Vercel)

1. Log into [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **Add New...** -> **Project**.
3. Import your GitHub repository `apartment-management-platform`.
4. Configure Project Settings:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: Click `Edit` and select `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
5. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL`: `https://<your-render-backend-url>/api/v1`
6. Click **Deploy**.

---

## 4. Post-Deployment Automated Initialization Scripts

Once the backend service has finished deploying and connected to the live PostgreSQL instance, execute the following database initialization commands to create all tables and populate initial production entities:

### Command Execution (Render Shell or Remote Terminal)

```bash
# Navigate to backend directory
cd backend

# 1. Run Alembic Database Migrations
alembic upgrade head

# 2. Run Production Seed Script (creates default Org, Admin, Landlord, Tenant, Maintenance accounts, properties, units, and general ledger journal entries)
python seed.py
```

### Production Demo Test Accounts (Post-Seed)
- **Platform Admin**: `admin@platform.com` / `AdminPass123!`
- **Landlord / Owner**: `landlord@apexpm.com` / `LandlordPass123!`
- **Property Manager**: `manager@apexpm.com` / `ManagerPass123!`
- **Resident Tenant**: `tenant@apexpm.com` / `TenantPass123!`
- **Maintenance Tech**: `tech@apexpm.com` / `TechPass123!`
