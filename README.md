# Apparent Management — SaaS Property Management & Apartment Rental Platform

Production-ready multi-tenant apartment rental and property management platform built with Next.js (JavaScript/JSX), FastAPI, PostgreSQL, Redis, Celery, and Tailwind CSS.

## Features
- **Multi-tenant Architecture**: Enterprise organization isolation.
- **Immutable Double-Entry Financial Ledger**: General ledger accounts with atomic balance updates.
- **Multi-Role Portals**: Landlord/Property Manager, Tenant, Maintenance Staff, and Platform Admin.
- **Rental Application & Leasing Lifecycle**: Electronic application submission, approval workflow, digital signatures, lease generation.
- **Stripe Payments & Webhooks**: Tokenized rent payments with idempotent webhook logging.
- **Maintenance Work Orders**: Maintenance ticketing, priority dispatch, cost recording, completion evidence.
- **Background Workers & Reminders**: Celery background tasks for rent reminders and lease expiration alerts.

## Quick Start (Docker)

```bash
# 1. Clone the repository
# 2. Copy environment variables
cp .env.example .env

# 3. Spin up services (Frontend, Backend API, PostgreSQL, Redis, Celery Worker)
docker-compose up --build
```

Access the platform at:
- **Public Website & Discovery**: http://localhost:3000
- **Landlord Portal**: http://localhost:3000/portal/landlord
- **Tenant Portal**: http://localhost:3000/portal/tenant
- **Maintenance Portal**: http://localhost:3000/portal/maintenance
- **Admin Portal**: http://localhost:3000/admin
- **FastAPI OpenAPI Docs**: http://localhost:8000/docs

## Seed Accounts (Development)
- **Admin**: `admin@platform.com` / `AdminPass123!`
- **Landlord**: `landlord@apexpm.com` / `LandlordPass123!`
- **Property Manager**: `manager@apexpm.com` / `ManagerPass123!`
- **Tenant**: `tenant@apexpm.com` / `TenantPass123!`
- **Maintenance Tech**: `tech@apexpm.com` / `TechPass123!`
