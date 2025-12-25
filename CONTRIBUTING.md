# Contributing

Thanks for wanting to contribute! A short guide to help contributors get started.

## How to contribute

1. Fork the repository and create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-change main
   ```
2. Create a clean, focused commit for each logical change. Keep commit messages descriptive.
3. Run tests and linters locally before opening a PR:
   ```bash
   python -m venv .venv
   . .venv/bin/activate    # or .\.venv\Scripts\activate on Windows
   pip install -r requirements.txt
   TEST_SQLITE=True python manage.py test
   black . && isort . && flake8 --exclude .venv
   ```
4. Open a Pull Request with a short description and link related issues.

## Code style
- The project uses `black` and `isort` — please run them before creating a PR.
- Keep lines reasonably short (wrap long strings where appropriate).

## Reporting bugs
- Create an issue with a clear description, reproduction steps, and logs/tracebacks if available.

## Questions
If you want help or guidance, open an issue and tag @roha301 and I’ll help triage it.