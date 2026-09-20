# Architecture

The application is split into a Vite SPA and a FastAPI REST API. The frontend owns presentation and navigation; it stores only the short-lived JWT and never receives password hashes. The API validates input with Pydantic, hashes passwords with bcrypt, and reads/writes through SQLAlchemy.

## Extension boundaries
- `Opportunity` is a common verified-data shape for scholarships and colleges. Add normalized eligibility/course tables as import requirements grow.
- Recommendation logic belongs in `backend/app/recommendation/`; the current API returns transparent demo reasons. A future ML adapter should return reasons and confidence, never an unexplained eligibility verdict.
- Add Alembic for controlled migrations before production deployment.
- Add admin dependencies that require `user.role == 'admin'`, then expose CRUD and verification logs.

## Privacy
Student profile and assessment endpoints require a bearer token. Public opportunity listing intentionally excludes private student data. Configure strict production CORS and rotate JWT secrets.
