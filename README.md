# 🚀 EngineeringOS AI — Enterprise Autonomous Engineering Intelligence Platform

[![Build Status](https://github.com/Prudhvi-2412/EngineerMind-AI/actions/workflows/deploy.yml/badge.svg)](https://github.com/Prudhvi-2412/EngineerMind-AI/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Next.js: 14](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)
[![LangGraph](https://img.shields.io/badge/AI-LangGraph_OpenAI-purple.svg)](https://langchain.com)
[![Kubernetes Ready](https://img.shields.io/badge/Kubernetes-Ready-blue.svg)](https://kubernetes.io)

**EngineeringOS AI** is an enterprise-grade, autonomous engineering intelligence and telemetry platform. It unifies data across **GitHub, Jira, Slack, Prometheus, and Grafana** into a real-time **Neo4j Knowledge Graph** and executes **LangGraph AI Agents** to predict PR risks, sprint delays, incident root causes, and developer burnout before outages occur.

---

## 🌟 Key Features

- 🤖 **LangGraph AI Agents:**
  - **PR Risk Agent:** Calculates PR blast radius, database risks, and suggests expert reviewers.
  - **Architecture Review Agent:** Detects service coupling, circular dependencies, God classes, and SOLID violations.
  - **Sprint Prediction Agent:** Predicts sprint delay probability and burndown velocity using Jira webhooks.
  - **Incident Prediction Agent:** Correlates Prometheus telemetry, Grafana alerts, and log anomaly stack traces for outage prevention.
  - **Developer Insight Agent:** Computes code ownership matrices, bus factor risks, domain expertise tags, and burnout indicators.
  - **Grounded Engineering RAG Chat Assistant:** Answers system queries with zero hallucinations, backed by explicit database & graph citations.

- 📊 **Unified Dashboards & Analytics:**
  - **Executive Engineering Health Dashboard:** Composite health score card (`88.5 / 100`), DORA metrics, cloud cost trends, and top contributors.
  - **Analytics Module:** Time-series charts for Velocity, Deployment Frequency, MTTR, Lead Time for Changes, Bug Trends, and downloadable **CSV & PDF Reports**.

- 📢 **Multi-Channel Notification Service:**
  - Parallel dispatch across **Slack (Block Kit)**, **Email (SMTP)**, **GitHub PR Comments**, and **Microsoft Teams (Adaptive Cards)** with exponential backoff retries (`tenacity`).

- ⚡ **Production Infrastructure:**
  - **Observability Stack:** Prometheus metrics (`/metrics`), Grafana dashboards, OpenTelemetry distributed tracing, and Grafana Loki structured JSON logging.
  - **Deployment Ready:** Multi-stage Dockerfiles, Docker Compose, Nginx Reverse Proxy, and complete production Kubernetes manifests with HPA auto-scaling.

---

## 🏗️ Technology Stack

- **Backend:** FastAPI, Python 3.11, Pydantic V2, SQLAlchemy, AsyncPG, Celery, Redis.
- **Frontend:** Next.js 14 App Router, TypeScript, TailwindCSS, Lucide Icons, React Query.
- **AI / Graph:** LangGraph, LangChain, OpenAI (`gpt-4o`), Neo4j Knowledge Graph (Cypher).
- **Observability:** Prometheus, Grafana, OpenTelemetry, Grafana Loki, Structlog JSON.
- **Infrastructure:** Docker, Docker Compose, Nginx, Kubernetes (K8s), Helm, GitHub Actions.

---

## ⚡ Quickstart (Local Docker Compose)

```bash
# 1. Clone the repository
git clone https://github.com/Prudhvi-2412/EngineerMind-AI.git
cd EngineerMind-AI

# 2. Start the entire platform via Docker Compose
docker-compose up -d --build

# 3. Access Services:
# - Frontend Dashboard: http://localhost
# - Backend API Docs:   http://localhost/api/v1/docs
# - Grafana Dashboards: http://localhost:3000 (admin/admin)
# - Prometheus Metrics: http://localhost:9090
```

---

## ☸️ Kubernetes Production Deployment

```bash
# Apply all Kubernetes manifests
kubectl apply -f k8s/

# Verify Deployment Rollout
kubectl rollout status deployment/backend -n engineering-os
kubectl rollout status deployment/frontend -n engineering-os
```

---

## 📖 Documentation Directory

- 📐 [Architecture Documentation](docs/ARCHITECTURE.md)
- 🔌 [API Reference & Swagger Docs](docs/API_DOCUMENTATION.md)
- 🚀 [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- 💻 [Developer Setup Guide](docs/DEVELOPER_GUIDE.md)
- 📋 [Production Launch Checklist](docs/PRODUCTION_CHECKLIST.md)

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for details.
