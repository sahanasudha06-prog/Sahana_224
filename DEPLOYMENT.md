# Deploy to Vercel

## Project configuration

The GitHub repository root contains `manage.py`, `requirements.txt`, and
`gym_project/`. Set the Vercel **Root Directory** to `./`. The root
`.python-version` file selects Python 3.12.

Vercel's [Django deployment support](https://vercel.com/docs/frameworks/full-stack/django)
detects `manage.py`, reads `gym_project.wsgi.application`, installs
`requirements.txt`, runs `collectstatic`, and serves files from `STATIC_ROOT`.
Leave the Build Command and Output Directory unset. No `vercel.json` is needed
for this project.

## Environment variables

Set these in Vercel under **Project Settings → Environment Variables** for
every environment you deploy (Production, Preview, and Development as needed):

- `DJANGO_SECRET_KEY`: a private Django signing key. Generate a new one locally:

  ```powershell
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

- `DATABASE_URL`: the connection string for a hosted PostgreSQL database,
  such as Neon or Supabase.

Keep `DJANGO_DEBUG` unset or set it to `false` in Vercel. When debugging is
disabled and `DJANGO_SECRET_KEY` is absent, Django settings intentionally stop
loading with `ImproperlyConfigured: Set DJANGO_SECRET_KEY when DEBUG is
disabled.` This can be surfaced by Vercel as `DJANGO_SETTINGS_FAILED`.
Confirm the key exists in the exact environment (Production or Preview) that
is building; changing Vercel environment variables requires a new deployment.

Vercel hostnames are allowed automatically. If you use a custom domain, add
its hostname to `ALLOWED_HOSTS` and its HTTPS origin to
`CSRF_TRUSTED_ORIGINS`. Both variables accept comma-separated values.
HTTPS redirects and secure session/CSRF cookies are enabled when debugging is
disabled. HSTS is intentionally not enabled; enable it only after confirming
HTTPS is enforced for every hostname.

## Database and migrations

Without `DATABASE_URL`, the project uses the local `db.sqlite3` file. SQLite
is suitable for local development but not persistent production data on
Vercel: serverless filesystems are ephemeral and are not shared reliably
between function instances. Use hosted PostgreSQL in production.

Back up the production database before schema changes. From a trusted local
PowerShell session, set the private production database URL and signing key,
then inspect and apply migrations deliberately:

```powershell
$env:DATABASE_URL = "<private production database URL>"
$env:DJANGO_SECRET_KEY = "<private Django secret>"
python manage.py showmigrations
python manage.py migrate --plan
python manage.py migrate
```

Do not run migrations as an automatic build step. Do not copy the local
SQLite database to Vercel or commit it to Git.

## Local checks on Windows

Run these commands from the repository root, where `manage.py` is located:

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DJANGO_DEBUG = "true"
python manage.py check
python manage.py runserver
```

The `venv` directory is ignored by Git. Never set `DJANGO_DEBUG=true` in
Vercel.

## Inspect a deployment

In Vercel, open the deployment and review **Build Logs** for Python 3.12,
dependency installation, Django detection, and successful static collection.
Review **Runtime Logs** for request-time exceptions. If settings discovery
fails, inspect the first exception and traceback before
`DJANGO_SETTINGS_FAILED`; redact secrets and database credentials before
sharing logs.
