# Flask To-Do Web Application (Active / Inactive tabs)

This is a ready-to-run Flask To-Do web application implementing the SRS provided by the user (register/login, task CRUD, and **Active/Inactive** filters on the dashboard).

## Features
- User registration and login (passwords hashed)
- Create / Read / Update / Delete tasks
- Task attributes: title, description, due date, priority, category, reminder (optional)
- Active / Inactive tabs on dashboard (Active = incomplete, Inactive = completed)
- SQLite database using Flask-SQLAlchemy
- Flask-WTF forms with validation
- Bootstrap 5 (via CDN) for responsive UI

## Setup (Linux / WSL / macOS)
1. Create and activate a virtualenv (recommended):
```bash
python -m venv venv
source venv/bin/activate
```
2. Install requirements:
```bash
pip install -r requirements.txt
```
3. Initialize database and run:
```bash
python app.py
```
4. Open `http://127.0.0.1:5000` in your browser.

## Files
- `app.py` - main Flask application
- `models.py` - SQLAlchemy models (User, Task)
- `forms.py` - Flask-WTF forms for auth and tasks
- `templates/` - HTML templates (Bootstrap 5)
- `static/` - static folder (empty; Bootstrap via CDN)
- `README.md` - this file

## Notes
- For demo purposes SECRET_KEY is stored in `app.py`. Change it for production.
- To switch DB to MySQL/Postgres, update the SQLALCHEMY_DATABASE_URI in `app.py`.
