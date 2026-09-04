# Ledger — Daily Expense Tracker (Django)

A wallet-style expense tracker: top up a balance, log daily expenses, and
watch the balance go down. Multi-user (each person has their own login and
their own wallet). Built as a mobile-first Progressive Web App (PWA), so it
can be "installed" to a phone's home screen straight from the browser — no
app store needed.

## What's inside

- `expense_tracker/` — Django project settings and root URLs
- `wallet/` — the app: `Transaction` model, views, forms, templates
- `static/` — mobile-first CSS, PWA `manifest.json`, `service-worker.js`, icons
- Built-in Django auth (login/signup/logout) so each user's data is private

## How the balance works

Every entry is a `Transaction` with a `type` of `income` (money added to the
wallet) or `expense`. The dashboard sums them:

```
balance = sum(income amounts) - sum(expense amounts)
```

Add money once (e.g. a monthly top-up or salary), then log expenses as they
happen — each one instantly subtracts from the balance.

## Running it locally

```bash
python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # optional, for the /admin/ panel
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`, click **Create an account**, then start
adding money and expenses.

## Using it on your phone (PWA install)

The site is installable like an app once it's reachable from your phone —
either running on your computer and opened over your home Wi-Fi, or deployed
to the internet (see below, recommended for daily use since your phone needs
to reach the server anytime you want to log an expense).

**Android (Chrome):** open the site → tap the **⋮** menu → **Add to Home
screen** / **Install app**.

**iPhone (Safari):** open the site → tap the **Share** icon → **Add to Home
Screen**.

Once installed, it opens full-screen with its own icon, no browser address
bar — it behaves like a native app, and the service worker caches the app
shell so it opens instantly even on a flaky connection.

## Deploying so your phone can reach it anytime

Running on your laptop only works while your phone is on the same Wi-Fi and
your laptop is on. For real daily use, deploy it to a small always-on host:

1. **Pick a host** — Railway, Render, Fly.io, or a small VPS (DigitalOcean,
   Hetzner) all work well for a single Django app.
2. **Set environment-based settings for production** (see below) — don't
   deploy with `DEBUG = True` or the default `SECRET_KEY`.
3. **Use PostgreSQL instead of SQLite** once more than one process/instance
   might write to the database — most hosts above provide this as an add-on.
4. **Serve static files** with `whitenoise` (already in `requirements.txt`) —
   add it to `MIDDLEWARE` and run `python manage.py collectstatic`.
5. **HTTPS is required** for the PWA install prompt and service worker to
   work on a real domain (Chrome/Safari won't install over plain HTTP except
   on `localhost`). Most hosts above give you HTTPS automatically.

Minimal production checklist in `settings.py`:

```python
import os

DEBUG = False
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
ALLOWED_HOSTS = ["yourdomain.com"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # add, right after SecurityMiddleware
    # ...rest unchanged
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
    "default": dj_database_url.config(default=os.environ["DATABASE_URL"])
    # pip install dj-database-url for this helper
}
```

Run with `gunicorn expense_tracker.wsgi:application` instead of
`runserver` in production.

## Extending it

- **Categories** — add a `category` field to `Transaction` and a filter on
  the dashboard.
- **Monthly reset / budgets** — add a `Budget` model per month and compare
  against `spent_today`/`spent_this_month` aggregates (the dashboard view
  already shows the aggregation pattern to copy).
- **Charts** — the dashboard view already computes totals; a small chart
  library (e.g. Chart.js via CDN) can plot spend-by-day from the same data.
- **REST API** — if you later want a native mobile app too, add Django REST
  Framework alongside this; the `Transaction` model doesn't need to change.
