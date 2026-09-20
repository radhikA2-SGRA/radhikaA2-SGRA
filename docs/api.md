# API quick reference

All routes are prefixed with `/api`.

- `POST /auth/register` — create a student account
- `POST /auth/login` — return a JWT
- `GET /student/profile` and `PUT /student/profile` — authenticated profile
- `GET /scholarships`, `GET /colleges` — verified/demo opportunity records
- `GET /assessment/questions` — seeded questions
- `POST /assessment/submit` — authenticated transparent score result
- `POST /roadmap/generate` — authenticated starter roadmap
- `GET /health` — service health

Interactive OpenAPI documentation is available at `/docs` when FastAPI is running.
