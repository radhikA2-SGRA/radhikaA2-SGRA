# Opportunity Finder

> **Low Marks ≠ Low Potential. Every Student Deserves a Path.**

A production-oriented full-stack foundation for Indian students to discover education, scholarship, college, career, alternative pathway, sports, and talent opportunities. Demo records are explicitly marked `is_demo=true` and must be verified before production use.

## Stack
- React + Vite + TypeScript
- FastAPI + SQLAlchemy + JWT
- PostgreSQL in production (SQLite is convenient for local development)
- Explainable, rule-based recommendations ready for future ML/LLM adapters

## Structure
- `frontend/` responsive student-facing SPA
- `backend/app/` API, models, authentication, recommendation service
- `database/` PostgreSQL schema and seed notes
- `docs/` architecture and API notes

## Run locally
### Backend
```bash
cd backend
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173`. API docs are at `http://localhost:8000/docs`.

### PostgreSQL
Set `DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/opportunity_finder` in `backend/.env`; tables are created on startup for this foundation. For production, use Alembic migrations and a managed database. A schema reference is in `database/schema.sql`.

### First admin
For development only, set `ADMIN_EMAIL` and `ADMIN_PASSWORD` in `.env`, then run:
```bash
python -m app.seed_admin
```
Never use demo credentials in production.

## Test the product
1. Register from **Get Started**; passwords are hashed with bcrypt.
2. Log in and complete profile fields from the dashboard.
3. Browse demo scholarships and colleges; each demo record is labeled.
4. Use **Assessment** to submit the seeded questions and receive transparent category results.
5. Generate a roadmap from the dashboard; recommendations include reasons and missing requirements.

## Safety and privacy
The API uses JWT bearer authentication, role checks, validation, CORS configuration, and no sensitive student fields in public opportunity responses. This starter intentionally avoids inventing official scholarship or college facts: seed records say `DEMO — verify before relying`. Add verified source URLs and `last_verified_date` before launch.

See `docs/architecture.md` and `docs/api.md` for extension points. Future modules (admin CRUD, notifications, saved opportunities, verified data import, multilingual UI, and ML ranking) can be added behind the same service boundaries.
