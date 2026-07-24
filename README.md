# Japanese Learning Platform (Sem VII Python Project)

Django web app for learning Japanese across JLPT levels N5–N1: video lessons, quizzes, flashcards, listening exercises, reference books, and progress tracking.

## Requirements

- Python 3.12+
- SQLite (local) or PostgreSQL (production on Render)
- AWS S3 is **optional** — not required to deploy

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
| `USE_S3` | Leave as `False` unless you set up AWS S3 later |
| `CSRF_TRUSTED_ORIGINS` | e.g. `https://your-app.onrender.com` |

## Deploy to Render (no AWS needed)

You only need **two** extra env vars beyond what the blueprint sets:

| Variable | Value |
|----------|--------|
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app-name.onrender.com` |

Leave `USE_S3=False` (the default). No AWS account required.

### What works without S3

- Login, quizzes, flashcards, progress tracking
- Static images/CSS (bundled in the repo)
- Sample data via `python manage.py loaddata backup.json`

### Limitations without S3

On Render’s free tier, the server disk is **temporary**. New video/audio/PDF uploads from the admin panel may **disappear after a redeploy**. For a semester demo this is usually fine if you seed data once and avoid relying on new uploads.

To add persistent uploads later, you can create a free AWS account and set `USE_S3=True` with S3 credentials.

## Deploy steps

1. Push this repo to GitHub.
2. In the Render dashboard, create a **Blueprint** from `render.yaml`.
3. When prompted, set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` to your Render URL.
4. After deploy, open the **Shell** tab and run:

   ```bash
   python manage.py createsuperuser
   python manage.py loaddata backup.json
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
