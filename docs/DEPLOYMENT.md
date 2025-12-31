# ChainSense AI - Deployment Guide

## Prerequisites

### Required Tools

- Docker Desktop 4.x+
- Kubernetes 1.28+ (or Docker Desktop Kubernetes)
- kubectl CLI
- Helm 3.x (optional)
- Git

### Cloud Provider Requirements (Production)

For production deployments, you'll need:
- Kubernetes cluster (GKE, EKS, AKS, or self-managed)
- Container registry (GHCR, ECR, GCR, ACR)
- PostgreSQL 15+ (managed or self-hosted)
- Redis 7+ (managed or self-hosted)
- Domain name with DNS management
- TLS certificates (Let's Encrypt or purchased)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/tanvir-eece-cse/ChainSense-AI.git
cd ChainSense-AI
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit with your local settings
# Use default values for development
```

### 3. Start with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ML Service**: http://localhost:8001
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)

### 5. Initialize Database

```bash
# Run migrations (if needed)
docker-compose exec backend alembic upgrade head

# Seed sample data (optional)
docker-compose exec backend python -m app.scripts.seed_data
```

## Kubernetes Deployment

### 1. Prepare Kubernetes Cluster

```bash
# Verify kubectl connection
kubectl cluster-info
kubectl get nodes

# Create namespace
kubectl apply -f k8s/namespace.yaml
```

### 2. Configure Secrets

**Option A: Using kubectl (Development)**

```bash
# Create secrets from .env file
kubectl create secret generic chainsense-secrets \
  --from-literal=SECRET_KEY='your-secret-key' \
  --from-literal=POSTGRES_USER='chainsense' \
  --from-literal=POSTGRES_PASSWORD='secure-password' \
  --from-literal=POSTGRES_DB='chainsense_db' \
  --from-literal=REDIS_PASSWORD='redis-password' \
  --from-literal=DATABASE_URL='postgresql+asyncpg://chainsense:secure-password@postgres:5432/chainsense_db' \
  --from-literal=REDIS_URL='redis://:redis-password@redis:6379/0' \
  -n chainsense-ai
```

**Option B: Using External Secrets Operator (Production)**

```yaml
# external-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: chainsense-secrets
  namespace: chainsense-ai
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: chainsense-secrets
  data:
    - secretKey: SECRET_KEY
      remoteRef:
        key: chainsense/secrets
        property: secret_key
```

### 3. Create Container Registry Secret

```bash
# For GitHub Container Registry
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=your-github-username \
  --docker-password=your-github-token \
  -n chainsense-ai
```

### 4. Deploy Components

```bash
# Deploy in order
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/database.yaml

# Wait for database to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n chainsense-ai --timeout=120s

# Deploy services
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/ml-service-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployments
kubectl get pods -n chainsense-ai
kubectl get services -n chainsense-ai
```

### 5. Configure Ingress

**With NGINX Ingress Controller:**

```bash
# Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

# Get external IP
kubectl get svc -n ingress-nginx
```

**With TLS (cert-manager):**

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: tanvir@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

### 6. Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n chainsense-ai

# Check services
kubectl get svc -n chainsense-ai

# Check ingress
kubectl get ingress -n chainsense-ai

# View logs
kubectl logs -f deployment/backend -n chainsense-ai

# Port forward for local testing
kubectl port-forward svc/backend 8000:8000 -n chainsense-ai
```

## CI/CD Pipeline Setup

### GitHub Actions Configuration

1. **Create GitHub Secrets:**

Navigate to: Repository → Settings → Secrets and variables → Actions

Required secrets:
- `KUBE_CONFIG` - Base64 encoded kubeconfig file
- `API_URL` - Production API URL

```bash
# Generate KUBE_CONFIG
cat ~/.kube/config | base64 -w 0
```

2. **Enable GitHub Actions:**

The workflows are already configured in `.github/workflows/`:
- `ci-cd.yml` - Main CI/CD pipeline
- `security.yml` - Security scanning

3. **Configure Branch Protection:**

Settings → Branches → Add rule:
- Require status checks before merging
- Require branches to be up to date
- Status checks: `backend`, `frontend`, `ml-service`, `security`

### Manual Deployment

```bash
# Build and push images
docker build -t ghcr.io/tanvir-eece-cse/chainsense-ai-backend:latest ./backend
docker push ghcr.io/tanvir-eece-cse/chainsense-ai-backend:latest

docker build -t ghcr.io/tanvir-eece-cse/chainsense-ai-frontend:latest ./frontend
docker push ghcr.io/tanvir-eece-cse/chainsense-ai-frontend:latest

docker build -t ghcr.io/tanvir-eece-cse/chainsense-ai-ml:latest ./ml-service
docker push ghcr.io/tanvir-eece-cse/chainsense-ai-ml:latest

# Update deployments
kubectl rollout restart deployment/backend -n chainsense-ai
kubectl rollout restart deployment/frontend -n chainsense-ai
kubectl rollout restart deployment/ml-service -n chainsense-ai
```

## Production Checklist

### Security

- [ ] Change all default passwords
- [ ] Enable TLS/HTTPS
- [ ] Configure network policies
- [ ] Set up secret management
- [ ] Enable audit logging
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Run security scans

### Performance

- [ ] Configure HPA thresholds
- [ ] Set resource limits
- [ ] Enable caching
- [ ] Configure connection pooling
- [ ] Set up CDN for frontend

### Monitoring

- [ ] Deploy Prometheus
- [ ] Configure Grafana dashboards
- [ ] Set up alerting
- [ ] Configure log aggregation
- [ ] Enable tracing (optional)

### Backup & Recovery

- [ ] Configure database backups
- [ ] Test recovery procedures
- [ ] Document runbooks
- [ ] Set up disaster recovery

## Troubleshooting

### Common Issues

**Pod CrashLoopBackOff:**
```bash
kubectl describe pod <pod-name> -n chainsense-ai
kubectl logs <pod-name> -n chainsense-ai --previous
```

**Database Connection Issues:**
```bash
# Check database pod
kubectl logs postgres-0 -n chainsense-ai

# Test connection
kubectl exec -it backend-xxx -n chainsense-ai -- python -c "from app.core.database import engine; print(engine)"
```

**Image Pull Errors:**
```bash
# Verify secret
kubectl get secret ghcr-secret -n chainsense-ai -o yaml

# Check image name
kubectl describe pod <pod-name> -n chainsense-ai | grep Image
```

### Useful Commands

```bash
# Get pod shell
kubectl exec -it <pod-name> -n chainsense-ai -- /bin/sh

# Port forward
kubectl port-forward svc/backend 8000:8000 -n chainsense-ai

# Scale deployment
kubectl scale deployment backend --replicas=5 -n chainsense-ai

# View HPA status
kubectl get hpa -n chainsense-ai

# Delete and recreate
kubectl delete -f k8s/ && kubectl apply -f k8s/
```

## Support

- **Documentation**: https://github.com/tanvir-eece-cse/ChainSense-AI/docs
- **Issues**: https://github.com/tanvir-eece-cse/ChainSense-AI/issues
- **Author**: Md. Tanvir Hossain
