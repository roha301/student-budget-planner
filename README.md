# Student Expense & Budget Planner (AI-powered)

Django-based webapp for students to track expenses, plan budgets, and get AI-powered advice (categorization, forecasting, suggestions) using OpenAI.

Features
- Django + Django REST Framework backend
- Oracle (PL/SQL) schema and sample stored procedures
- OpenAI integration for categorization and budgeting suggestions
- Dark emerald green glassmorphism UI (starter template)
- Docker + docker-compose (including optional Oracle XE service)

Quick start
1. Create a Python virtual environment and install dependencies:
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt

2. Configure environment variables (example in `.env`):
   DJANGO_SECRET_KEY=your-secret
   ORACLE_USER=...
   ORACLE_PASSWORD=...
   ORACLE_HOST=oracle
   ORACLE_PORT=1521
   ORACLE_SID=XE
   OPENAI_API_KEY=sk-...

3. Run Docker Compose to start an optional Oracle XE instance (if you want):
   docker-compose up -d

4. Run migrations and start server:
   python manage.py migrate
   python manage.py runserver

Notes
- Oracle requires Oracle Instant Client for `cx_Oracle`. On Windows, install the Instant Client and add it to your PATH; on Linux use the Oracle Instant Client packages or the `gvenzl/oracle-xe` Docker image.
- This scaffold includes sample PL/SQL scripts in `db/plsql/` and a helper at `scripts/db_setup.py` to run them via `cx_Oracle`.

Database setup (example)
1. Create `.env` from `.env.example` and set credentials.
2. If using Docker Compose, start Oracle: `docker-compose up -d`.
3. Run: `python scripts/db_setup.py` to execute PL/SQL scripts and load demo data.

Next steps
- Run migrations: `python manage.py migrate`
- Create a superuser: `python manage.py createsuperuser`
- Obtain an API token (DRF Token auth): POST username/password to `/api/auth/token/` to receive a token for `Authorization: Token <key>`

AI Endpoints (authenticated)
- POST `/api/ai/suggest-budget/` -> { months_of_history: 3 }
- POST `/api/ai/forecast/` -> { months: 3 }
- POST `/api/ai/query/` -> { query: 'How much did I spend on food?' }

GitLab integration
1. Create a project on GitLab (or use your existing project ID `77321095`).
2. Add repository remote and push the branch `complete/finish-all` when ready:
   - git remote add origin git@gitlab.com:<your-namespace>/<repo>.git
   - git branch -M main
   - git push -u origin main
   - git push origin complete/finish-all
3. In GitLab, add CI/CD variables (Settings → CI / CD → Variables):
   - OPENAI_API_KEY (masked)
   - OPENAI_MODEL (optional)
   - TEST_SQLITE = True
   - If publishing Docker images: CI_REGISTRY, CI_REGISTRY_IMAGE will be set by GitLab automatically

Local testing tips
- To run tests using sqlite (avoiding Oracle dependency) set `TEST_SQLITE=True` env var before running tests or in CI.
- Example: `TEST_SQLITE=True python manage.py test`

Dev tips
- Use `localStorage` key `token` to store API token for the demo dashboard (see `static/js/dashboard.js`).
- Configure `OPENAI_API_KEY` and optional `OPENAI_MODEL` in `.env` to enable AI features.
