# Japanese Learning Platform (Sem VII Python Project)

Django web app for learning Japanese across JLPT levels N5–N1: video lessons, quizzes, flashcards, listening exercises, reference books, and progress tracking.

## Requirements

- Python 3.12+
- SQLite (local) or PostgreSQL (production on Render)
- AWS S3 (optional; recommended for media uploads on Render)

## Local development

```powershell
cd myDjango
python -m venv ..\.venv
..\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

Create a superuser for admin access:

```powershell
python manage.py createsuperuser
```

## Environment variables

Copy `.env.example` to `.env` and adjust as needed:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key (required in production) |
| `DEBUG` | `True` for local dev, `False` on Render |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `DATABASE_URL` | PostgreSQL URL (Render sets this automatically) |
| `USE_S3` | `True` to store uploads on S3 |
| `AWS_*` | S3 credentials and bucket name |
| `CSRF_TRUSTED_ORIGINS` | e.g. `https://your-app.onrender.com` |

## Deploy to Render

1. Push this repo to GitHub.
2. In the Render dashboard, create a **Blueprint** from `render.yaml`, or create a Web Service manually:
   - **Root directory:** `myDjango`
   - **Build command:** `./build.sh`
   - **Start command:** `gunicorn myDjango.wsgi:application --bind 0.0.0.0:$PORT`
3. Link the PostgreSQL database (included in the blueprint).
4. Set environment variables:
   - `ALLOWED_HOSTS` → your Render hostname (e.g. `your-app.onrender.com`)
   - `CSRF_TRUSTED_ORIGINS` → `https://your-app.onrender.com`
   - For uploads: `USE_S3=True` plus AWS credentials
5. After deploy, run once in the Render shell:

   ```bash
   python manage.py createsuperuser
   ```

Health check endpoint: `/health/`

## Project structure

```
myDjango/
├── manage.py
├── requirements.txt
├── build.sh
├── japan/              # Main app (views, models, URLs)
├── myDjango/           # Project settings
├── Templates/          # HTML templates
└── media/              # Local uploads (when USE_S3=False)
```
