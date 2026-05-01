#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-thesis:latest}"
LOCAL_PORT="${LOCAL_PORT:-8000}"
SERVICE_PORT="${SERVICE_PORT:-8000}"
ADMIN_USERNAME="${ADMIN_USERNAME:-admin}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin12345}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@example.com}"

need() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

need colima
need docker
need kubectl

echo "Starting Colima with Kubernetes..."
colima start --kubernetes

echo "Building Docker image: ${IMAGE_NAME}"
env -u DOCKER_HOST docker build -t "${IMAGE_NAME}" .

echo "Applying Kubernetes manifests..."
kubectl apply -k k8s

echo "Waiting for deployment rollout..."
kubectl rollout status deployment/thesis-web --timeout=180s

echo "Creating/updating local admin user: ${ADMIN_USERNAME}"
kubectl exec deployment/thesis-web -- python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
user, _ = User.objects.get_or_create(username='${ADMIN_USERNAME}', defaults={'email': '${ADMIN_EMAIL}'})
user.email = '${ADMIN_EMAIL}'
user.is_staff = True
user.is_superuser = True
user.set_password('${ADMIN_PASSWORD}')
user.save()
print('Admin user ready: ${ADMIN_USERNAME}')
"

echo
echo "App is ready."
echo "URL: http://127.0.0.1:${LOCAL_PORT}/"
echo "Admin: http://127.0.0.1:${LOCAL_PORT}/admin/"
echo "Username: ${ADMIN_USERNAME}"
echo "Password: ${ADMIN_PASSWORD}"
echo
echo "Starting port-forward. Press Ctrl+C to stop it."
kubectl port-forward service/thesis-web "${LOCAL_PORT}:${SERVICE_PORT}"
