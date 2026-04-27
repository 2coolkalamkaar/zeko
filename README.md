# Python Kubernetes Starter

This project contains a starter Python Flask application configured for containerization and Kubernetes deployment.

## Files
- `app.py`: The main Flask application.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Instructions to build the Docker image.
- `k8s-deployment.yaml`: Kubernetes Deployment and Service manifests.
- `.dockerignore`: Files to exclude from the Docker build.

## How to use

### 1. Build the Docker Image
```bash
docker build -t your-username/python-app:latest .
```

### 2. Push to a Registry
```bash
docker push your-username/python-app:latest
```

### 3. Deploy to Kubernetes
Update the `image` field in `k8s-deployment.yaml` with your pushed image name, then run:
```bash
kubectl apply -f k8s-deployment.yaml
```

## Note on this Environment
This preview environment is primarily configured for Node.js. These Python files are provided for your use in external environments (Docker, K8s).
# zeko
