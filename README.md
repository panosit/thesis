# Thesis (Django App)

This project is a Django web application.

## Prerequisites

Choose one setup method:

### Option A: Run locally (without Docker)
- Python 3.14+
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

### Step 4: Configure environment variables
Copy `.env.example` into your deployment environment and set:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`

For local development, you can run with the defaults or set `DJANGO_DEBUG=True`.

### Step 5: Apply database migrations
```bash
python manage.py migrate
```

### Step 6: (Optional) Create an admin user
```bash
python manage.py createsuperuser
```

### Step 7: Start the development server
```bash
python manage.py runserver
```

### Step 8: Open the app
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

---

## 3) Run with Kubernetes

These manifests are intended for local Kubernetes tools such as Docker Desktop Kubernetes, Minikube, or Kind.

### Quick local start with Colima
```bash
chmod +x scripts/run-k8s-local.sh
./scripts/run-k8s-local.sh
```

The script starts Colima with Kubernetes, builds the image, deploys the app, waits for rollout, creates a local admin user, and starts port-forwarding.

Default local credentials:

- Username: `admin`
- Password: `admin12345`

You can override them:
```bash
ADMIN_USERNAME=myadmin ADMIN_PASSWORD='change-me' ./scripts/run-k8s-local.sh
```

### Step 1: Build the image
```bash
docker build -t thesis:latest .
```

If you use Minikube, build inside Minikube's Docker environment:
```bash
eval $(minikube docker-env)
docker build -t thesis:latest .
```

### Step 2: Set a real secret key
Edit `k8s/secret.yaml` and replace `replace-this-with-a-strong-secret-key`.

### Step 3: Deploy
```bash
kubectl apply -k k8s
```

The pod runs database migrations in an init container before starting Gunicorn.
SQLite data and uploaded media are stored in the `thesis-data` persistent volume claim.

### Step 4: Open the app locally
```bash
kubectl port-forward service/thesis-web 8000:8000
```

Then open:

- Main site: http://localhost:8000
- Admin: http://localhost:8000/admin

### Useful Kubernetes commands
```bash
kubectl get pods
kubectl logs deployment/thesis-web
kubectl describe pod -l app=thesis-web
kubectl delete -k k8s
```
