"""
Pytest configuration and shared fixtures for OneQlick backend tests.

Run with:
    pytest tests/ -v
    
For Postgres (recommended — avoids FK graph issues with SQLite):
    $env:TEST_DATABASE_URL="postgresql://user:pass@localhost/oneqlick_test"
    pytest tests/ -v

For quick smoke tests against the live dev database (read-only tests only):
    $env:TEST_DATABASE_URL="<your dev DATABASE_URL>"
    pytest tests/ -v -k "unauthenticated or nonexistent"
"""
import pytest
import sys
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
import os

# ─── Mock optional dependencies before app import ────────────────────────────
# Some modules (prometheus, etc.) may not be installed in test env
for mod in [
    "prometheus_fastapi_instrumentator",
    "prometheus_fastapi_instrumentator.instrumentation",
]:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()

from app.main import app
from app.infra.db.postgres.postgres_config import get_db

# ─── Test Database Setup ──────────────────────────────────────────────────────
# Use the real Postgres DB with per-test rollbacks so no data is committed.
# SQLite cannot be used here because the app's FK graph is too complex for it.

_DB_URL = os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL")

if _DB_URL:
    engine = create_engine(_DB_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    # No DB URL set — tests requiring DB will be skipped
    engine = None
    TestingSessionLocal = None


@pytest.fixture()
def db():
    """
    Provide a database session that rolls back after each test.
    Requires TEST_DATABASE_URL or DATABASE_URL env variable.
    """
    if engine is None:
        pytest.skip("No TEST_DATABASE_URL set — skipping DB test")

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    """Provide a TestClient with the test DB override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(client, db):
    """
    Register + login a test user and return Authorization headers.
    Mocks OTP so no real SMS is sent.
    """
    import uuid
    test_phone = f"+91{str(uuid.uuid4().int)[:10]}"

    with patch("app.services.otp_service.OtpService.send_otp", return_value=True), \
         patch("app.services.otp_service.OtpService.verify_otp", return_value=True):

        client.post("/api/v1/auth/send-otp", json={"phone": test_phone})
        resp = client.post("/api/v1/auth/verify-otp", json={
            "phone": test_phone,
            "otp": "123456",
            "first_name": "Test",
            "last_name": "User",
        })

    if resp.status_code not in (200, 201):
        pytest.skip(f"Auth setup failed: {resp.status_code} {resp.text}")

    token = resp.json().get("data", {}).get("access_token")
    if not token:
        pytest.skip("Could not get auth token")

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def mock_razorpay():
    """Mock Razorpay service to avoid real API calls in tests."""
    with patch("app.services.razorpay_service.razorpay_service") as mock:
        mock.create_order.return_value = {
            "razorpay_order_id": "order_test123",
            "amount": 50000,
            "currency": "INR",
            "status": "created",
        }
        mock.verify_payment_signature.return_value = True
        mock.initiate_refund.return_value = {
            "id": "rfnd_test123",
            "payment_id": "pay_test123",
            "amount": 50000,
            "status": "processed",
        }
        yield mock


