# ==============================================================================
# AIPE Framework - Tests - API Healthcheck Integration Tests
# ==============================================================================
# Automates integration tests for GET /health endpoint.
# Ensures API returns HTTP 200 and expected JSON payload structure.
# ==============================================================================

from fastapi.testclient import TestClient

from src.core.config import settings
from src.main import app

# Initialize FastAPI TestClient (simulates HTTP requests without network overhead)
client = TestClient(app)


def test_health_check() -> None:
    """Validate GET /health endpoint behavior and schema contract compliance."""
    # 1. Issue HTTP GET request to /health endpoint
    response = client.get("/health")

    # 2. Validate HTTP 200 OK status code
    assert response.status_code == 200

    # 3. Parse JSON response payload
    data = response.json()

    # 4. Assert response payload matches settings values
    assert data["status"] == settings.HEALTH_STATUS
    assert data["environment"] == settings.ENVIRONMENT
    assert data["version"] == settings.VERSION
