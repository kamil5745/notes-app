# NoteFlow

NoteFlow is a Django REST Framework project for notes with categories, tags, file attachments, likes, view counters, and server-rendered Django pages.

## Stack

- Backend: Django 6.0.2, Django REST Framework 3.16.1
- DB: SQLite (`db.sqlite3`)
- Auth: Django auth/session for web pages, DRF permissions for API access; JWT is Missing / Not found
- Server: Gunicorn in Docker, nginx reverse proxy in Docker Compose
- Frontend: Django templates plus static vanilla JavaScript and CSS

## Project structure

```text
.
|-- config/
|   |-- settings.py
|   |-- urls.py
|   |-- wsgi.py
|   `-- asgi.py
|-- document/
|   |-- api/
|   |   |-- pagination.py
|   |   |-- permissions.py
|   |   |-- serializers.py
|   |   |-- urls.py
|   |   `-- views.py
|   |-- migrations/
|   |-- static/
|   |-- templates/
|   |-- forms.py
|   |-- models.py
|   |-- urls.py
|   `-- views.py
|-- docs/
|   `-- api.md
|-- nginx/
|   `-- nginx.conf
|-- Dockerfile
|-- docker-compose.yml
|-- manage.py
|-- README.md
`-- requirements.txt
```

## Local setup without Docker

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py runserver
```

Default local URLs:

- Web pages: `http://127.0.0.1:8000/notes/`
- API: `http://127.0.0.1:8000/api/`
- Admin: `http://127.0.0.1:8000/admin/`

Verified local behavior:

- `python manage.py check`: passes
- `python manage.py runserver`: starts on `http://127.0.0.1:8000/`
- `GET /`: returns `404`
- `GET /notes/`: returns `200`
- `GET /api/note/?page=1` without authentication: returns `403`
- `GET /notes/register/`: works
- `GET /notes/login/`: works

## Docker setup

`docker-compose.yml` exists.

```bash
docker compose up --build
```

Docker Compose runs migrations, collects static files, starts Gunicorn on the `web` service, and starts nginx.

URLs from the current compose file:

- Django web service: `http://127.0.0.1:8000/`
- nginx: `http://127.0.0.1/`

## Environment variables

`config/settings.py` currently does not read environment variables with `os.environ` or `os.getenv`.

Real settings currently defined in code:

- `SECRET_KEY`: hard-coded in `config/settings.py`
- `DEBUG`: `True`
- `ALLOWED_HOSTS`: `['*']`
- `DATABASES`: SQLite, `BASE_DIR / 'db.sqlite3'`
- `STATIC_URL`: `/static/`
- `STATIC_ROOT`: `BASE_DIR / 'static'`
- `MEDIA_URL`: `/media/`
- `MEDIA_ROOT`: `BASE_DIR / 'media'`
- `CORS_ALLOW_ALL_ORIGINS`: `True`

`docker-compose.yml` sets `DEBUG=1`, but `settings.py` does not currently consume it.

## API documentation

See [docs/api.md](docs/api.md).

## Demo checklist

- login works: `/notes/login/` works
- token received: Missing / Not found, JWT endpoints are not registered
- notes list opens: `/notes/` returns `200`; `GET /api/note/?page=1` requires authentication and returns `403` without login
- note creation works: `/notes/create/` posts to `POST /api/note/`
- note detail opens: `/notes/{slug}/` and `GET /api/note/{id}/`
- like works: `GET /api/note/{id}/like/` and `POST /api/note/{id}/like/`
- category works, if categories exist: `GET /api/category/`
