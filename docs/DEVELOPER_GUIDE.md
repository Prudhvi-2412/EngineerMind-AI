# Developer Onboarding & Development Guide: EngineeringOS AI

Welcome to the **EngineeringOS AI** codebase! This guide covers setup, code style, database migrations, and testing workflows.

---

## 1. Local Environment Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- PostgreSQL 16 & Neo4j 5 local or containerized

```bash
# Create Python Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Backend Dependencies
pip install -r requirements.txt

# Install Frontend Dependencies
cd frontend
npm install
```

---

## 2. Database Migrations (Alembic)

```bash
# Generate a new migration script
alembic revision --autogenerate -m "Add new telemetry model"

# Upgrade database schema to head
alembic upgrade head
```

---

## 3. Running Unit & Integration Tests

```bash
# Run pytest unit test suite with coverage
pytest tests/unit/ --cov=app

# Run specific agent test
pytest tests/unit/test_pr_risk_agent.py -v
```

---

## 4. Code Formatting & Linting

```bash
# Python Formatting & Linting
black app/ tests/
flake8 app/

# Frontend Formatting & Linting
cd frontend
npm run lint
```
