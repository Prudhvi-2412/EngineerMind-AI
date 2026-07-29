from datetime import datetime
from app.application.collectors.jira_collector import JiraCollector
from app.application.collectors.slack_collector import SlackCollector
from app.application.collectors.prometheus_collector import PrometheusCollector
from app.application.collectors.grafana_collector import GrafanaCollector


def test_jira_collector_normalization():
    payload = {
        "webhookEvent": "jira:issue_created",
        "timestamp": 1700000000000,
        "issue": {
            "key": "ENG-402",
            "fields": {
                "summary": "Fix Redis memory leak in Celery worker",
                "status": {"name": "In Progress"},
                "priority": {"name": "High"},
                "assignee": {"emailAddress": "engineer@company.com"},
                "project": {"key": "ENG"}
            }
        }
    }

    event = JiraCollector.normalize(payload, delivery_id="delivery-jira-123")

    assert event.source == "jira"
    assert event.event_category == "issue"
    assert event.event_action == "issue.issue_created"
    assert event.normalized_payload["issue_key"] == "ENG-402"
    assert event.normalized_payload["assignee_email"] == "engineer@company.com"


def test_slack_collector_normalization():
    payload = {
        "team_id": "T12345",
        "event": {
            "type": "message",
            "client_msg_id": "msg-999",
            "user": "U98765",
            "text": "Incident resolved on payment-service",
            "ts": "1700000000.000100"
        }
    }

    event = SlackCollector.normalize(payload, delivery_id="delivery-slack-999")

    assert event.source == "slack"
    assert event.event_category == "communication"
    assert event.event_action == "chat.message"
    assert event.normalized_payload["user_id"] == "U98765"


def test_prometheus_collector_normalization():
    payload = {
        "status": "firing",
        "receiver": "webhook-adapter",
        "alerts": [
            {
                "labels": {"alertname": "HighMemoryUsage", "severity": "critical", "service": "auth-service"},
                "annotations": {"summary": "RAM usage exceeded 90%"},
                "startsAt": "2026-07-29T10:00:00Z"
            }
        ]
    }

    event = PrometheusCollector.normalize(payload, delivery_id="prom-100")

    assert event.source == "prometheus"
    assert event.event_category == "alert"
    assert event.event_action == "alert.firing"
    assert event.normalized_payload["alerts"][0]["alert_name"] == "HighMemoryUsage"
    assert event.normalized_payload["alerts"][0]["severity"] == "critical"


def test_grafana_collector_normalization():
    payload = {
        "state": "alerting",
        "ruleId": 42,
        "ruleName": "Latency Spike",
        "message": "P99 latency > 500ms"
    }

    event = GrafanaCollector.normalize(payload, delivery_id="grafana-42")

    assert event.source == "grafana"
    assert event.event_category == "alert"
    assert event.event_action == "alert.alerting"
    assert event.normalized_payload["rule_name"] == "Latency Spike"
