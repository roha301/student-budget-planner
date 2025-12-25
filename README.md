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
- Obtain an API token (DRF Token auth): POST username/password to `/api/auth/token/` to receive a token for Authorization: Token <key>
- Implement OpenAI utilities and build responsive frontend.
