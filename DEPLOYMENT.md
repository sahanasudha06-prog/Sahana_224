# Deploy to Vercel

Vercel detects this Django project from `manage.py` and uses
`gym_project.wsgi.application`. It also runs `collectstatic` and serves files
from `STATIC_ROOT`.

## 1. Import the GitHub repository

In Vercel, create a project and import
[Sahana_224](https://github.com/sahanasudha06-prog/Sahana_224). The Django
files, including `manage.py` and `requirements.txt`, are at the repository
root, so leave **Root Directory** set to `./`.

## 2. Configure environment variables

Add these in the Vercel project settings for each environment you deploy:

- `DJANGO_SECRET_KEY`: a new, private Django secret. Generate one locally with:
  `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `DATABASE_URL`: the connection URL for a managed PostgreSQL database. Vercel
  serverless filesystems are ephemeral, so the local SQLite database is only a
  development fallback and must not be used for production data.

Vercel deployment hostnames are allowed automatically. If you use a custom
domain, add its hostname to `ALLOWED_HOSTS` and its HTTPS origin to
`CSRF_TRUSTED_ORIGINS`. Both variables accept comma-separated values.

## 3. Deploy and migrate

Deploy from the Vercel dashboard. Before using the app, run the Django
migrations against the production database once:

```powershell
$env:DATABASE_URL = "your-production-database-url"
$env:DJANGO_SECRET_KEY = "your-django-secret"
python manage.py migrate
```

Keep the database URL and secret private; do not commit them to the repository.
