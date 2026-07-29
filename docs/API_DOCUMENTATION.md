# API Reference Documentation: EngineeringOS AI

Interactive Swagger API UI available at `/api/v1/docs` when running the application.

---

## 1. Authentication & OAuth Endpoints (`/api/v1/auth`, `/api/v1/oauth`)

| Method | Endpoint | Description | Request Body / Query |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login` | Email/Password JWT Authentication | `UserLogin` |
| `POST` | `/api/v1/auth/refresh` | Refresh JWT Token | `TokenRefreshRequest` |
| `GET` | `/api/v1/oauth/github/login` | Initiate GitHub OAuth PKCE flow | Query `code_challenge` |
| `GET` | `/api/v1/oauth/github/callback` | Exchange OAuth code for JWT token | Query `code`, `state` |

---

## 2. Event Collector & Webhook Endpoints (`/api/v1/collector`, `/api/v1/github`)

| Method | Endpoint | Description | Headers |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/github/webhook` | GitHub Push, PR, Issue Webhooks | `X-Hub-Signature-256` |
| `POST` | `/api/v1/collector/events` | Generic Event Ingestion Endpoint | Bearer JWT |

---

## 3. LangGraph AI Agents Endpoints (`/api/v1/agents`)

| Method | Endpoint | Description | Payload |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/agents/pr-risk` | PR Risk & Blast Radius AI Assessment | `AnalyzePRRiskRequest` |
| `POST` | `/api/v1/agents/architecture-review` | Architecture Code Smell & Coupling Review | `AnalyzeArchitectureRequest` |
| `POST` | `/api/v1/agents/sprint-prediction` | Jira Sprint Success Probability | `PredictSprintRequest` |
| `POST` | `/api/v1/agents/incident-prediction` | Telemetry Root Cause & Outage Prediction | `PredictIncidentRequest` |
| `POST` | `/api/v1/agents/developer-insights` | Code Ownership & Burnout Assessment | `AnalyzeDeveloperInsightRequest` |

---

## 4. Grounded Chat, Notifications & Analytics (`/api/v1/chat`, `/notifications`, `/analytics`)

| Method | Endpoint | Description | Response / Export |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/chat/message` | Grounded AI RAG Chat Assistant | `ChatMessageResponse` |
| `POST` | `/api/v1/notifications/send` | Multi-Channel Risk Alert Dispatch | `SendAlertNotificationResponse` |
| `GET` | `/api/v1/analytics/trends` | Time-Series Metrics Dataset | `AnalyticsTimeSeriesResponse` |
| `GET` | `/api/v1/analytics/export/csv` | Download Analytics CSV File | `text/csv` attachment |
| `GET` | `/api/v1/analytics/export/pdf` | Download Executive Analytics PDF Report | `application/pdf` attachment |

---

## 5. Observability & Health Checks (`/healthz`, `/health/readiness`, `/metrics`)

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/healthz` | Kubernetes Container Liveness Probe | Public |
| `GET` | `/health/readiness` | Deep PostgreSQL, Neo4j & Redis Health | Public |
| `GET` | `/metrics` | Prometheus Metrics Scrape Endpoint | Public / Internal |
