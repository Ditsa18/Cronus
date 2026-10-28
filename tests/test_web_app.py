"""Integration tests for FastAPI Web Dashboard and REST API."""

import pytest
from fastapi.testclient import TestClient
from src.web_app import app, state


@pytest.fixture
def client():
    """Create a FastAPI test client fixture."""
    return TestClient(app)


def test_serve_index(client):
    """Verify that the frontend HTML index is served successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Cronus Bank" in response.text
    assert "Fraud Screening Ops" in response.text


def test_get_kpis(client):
    """Verify KPI endpoint returns valid summary metrics."""
    response = client.get("/api/kpis")
    assert response.status_code == 200
    data = response.json()
    assert "total_transactions" in data
    assert "suspicious_transactions" in data
    assert "suspicious_percentage" in data
    assert data["total_transactions"] > 0


def test_get_charts(client):
    """Verify chart series endpoint returns data for all 4 visualizations."""
    response = client.get("/api/charts")
    assert response.status_code == 200
    data = response.json()
    assert "hourly" in data
    assert "types" in data
    assert "channels" in data
    assert "combinations" in data
    assert len(data["hourly"]["labels"]) > 0


def test_get_suspicious_transactions(client):
    """Verify suspicious review queue pagination and filtering."""
    response = client.get("/api/transactions/suspicious?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "records" in data
    assert len(data["records"]) <= 10
    if len(data["records"]) > 0:
        first = data["records"][0]
        assert "Transaction_ID" in first
        assert "Suspicion_Score" in first


def test_get_account_risk(client):
    """Verify top account risk ranking endpoint."""
    response = client.get("/api/accounts/risk?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "top_accounts" in data
    assert len(data["top_accounts"]) <= 5


def test_get_business_questions(client):
    """Verify questions endpoint returns answers for Q1 through Q10."""
    response = client.get("/api/questions")
    assert response.status_code == 200
    data = response.json()
    assert "Q1" in data
    assert "Q10" in data


def test_update_screening_config(client):
    """Verify dynamic re-screening via POST /api/screen."""
    payload = {
        "amount_method": "p99",
        "custom_amount_threshold": 60000.0,
        "late_night_start": 23,
        "late_night_end": 5,
        "freq_threshold": 6,
        "suspicion_threshold": 2
    }
    response = client.post("/api/screen", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "kpis" in data


def test_generate_fresh_data(client):
    """Verify generating fresh transactions dynamically."""
    response = client.post("/api/generate?n=500&seed=999")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["kpis"]["total_transactions"] == 500


def test_export_suspicious_csv(client):
    """Verify exporting the review queue as a CSV stream."""
    response = client.get("/api/export/suspicious")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "Transaction_ID" in response.text
