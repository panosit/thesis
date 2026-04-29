# Thesis (Django App)

This project is a Django web application.

## Prerequisites

Choose one setup method:

### Option A: Run locally (without Docker)
- Python 3.10+
- pip

### Option B: Run with Docker
- Docker
- Docker Compose (v2+)

---

## 1) Run locally (without Docker)

### Step 1: Clone the repository
```bash
git clone <your-repo-url>
cd thesis
```

### Step 2: (Recommended) Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Apply database migrations
```bash
python manage.py migrate
```

### Step 5: (Optional) Create an admin user
```bash
python manage.py createsuperuser
```

### Step 6: Start the development server
```bash
python manage.py runserver
```

### Step 7: Open the app
- Main site: http://localhost:8000
- Admin: http://localhost:8000/admin

---

## 2) Run with Docker Compose

### Step 1: Build and start containers
```bash
docker compose up --build
```

### Step 2: Run migrations (in another terminal)
```bash
docker compose exec web python manage.py migrate
```

### Step 3: (Optional) Create an admin user
```bash
docker compose exec web python manage.py createsuperuser
```

### Step 4: Open the app
- Main site: http://localhost:8000
- Admin: http://localhost:8000/admin

### Step 5: Stop containers
```bash
docker compose down
```

---

## Useful commands

### Collect static files
Local:
```bash
python manage.py collectstatic --noinput
```

Docker:
```bash
docker compose exec web python manage.py collectstatic --noinput
```

### Run tests
Local:
```bash
python manage.py test
```

Docker:
```bash
docker compose exec web python manage.py test
```

---

## Notes
- The included `Dockerfile` runs the app using Gunicorn on port `8000`.
- `docker-compose.yaml` maps port `8000` and mounts the project directory for easier development.
- If port `8000` is already in use, stop the conflicting process or change the port mapping in `docker-compose.yaml`.
