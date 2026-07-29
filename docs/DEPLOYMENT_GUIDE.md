# Production Deployment Guide: EngineeringOS AI

This guide details deployment options for **Local Docker Compose**, **Production Kubernetes (EKS / GKE / AKS)**, and **CI/CD Automation**.

---

## 1. Local Development (Docker Compose)

### Prerequisites
- Docker Engine `v24+` & Docker Compose `v2+`

### Step 1: Environment Configuration
Create a `.env` file in the project root:
```env
POSTGRES_SERVER=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=engineering_os_auth
REDIS_HOST=redis
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123
JWT_SECRET_KEY=your_secure_jwt_secret
OPENAI_API_KEY=sk-proj-your-openai-api-key
```

### Step 2: Build & Launch Services
```bash
docker-compose up -d --build
```

---

## 2. Production Kubernetes Deployment

### Step 1: Configure Kubernetes Secrets
Generate base64 encoded secrets or edit `k8s/01-configmaps-secrets.yaml` with production credentials:
```yaml
stringData:
  POSTGRES_PASSWORD: "YOUR_PROD_POSTGRES_PASSWORD"
  NEO4J_PASSWORD: "YOUR_PROD_NEO4J_PASSWORD"
  JWT_SECRET_KEY: "YOUR_PROD_JWT_SECRET"
  OPENAI_API_KEY: "sk-proj-your-actual-key"
```

### Step 2: Apply Manifests
```bash
kubectl apply -f k8s/
```

### Step 3: Verify Status & Ingress
```bash
kubectl get pods -n engineering-os
kubectl get ingress -n engineering-os
```

---

## 3. Monitoring & Grafana Dashboard Setup

1. Open Grafana at `http://localhost:3000` (or `http://grafana.engineeringos.company.com`).
2. Login with credentials `admin` / `admin`.
3. Add Prometheus datasource pointing to `http://prometheus:9090`.
4. Add Loki datasource pointing to `http://loki:3100`.
