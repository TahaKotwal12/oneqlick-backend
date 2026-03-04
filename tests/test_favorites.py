"""
Tests for the Favorites feature:
- GET /api/v1/favorites
- POST /api/v1/favorites/{restaurant_id}
- DELETE /api/v1/favorites/{restaurant_id}
- GET /api/v1/favorites/check/{restaurant_id}
"""
import pytest
import uuid
from unittest.mock import patch


class TestFavoritesEndpoints:
    """Test the favorites API endpoints."""

    FAKE_RESTAURANT_ID = str(uuid.uuid4())

    def test_get_favorites_unauthenticated(self, client):
        """Unauthenticated request should return 401."""
        resp = client.get("/api/v1/favorites")
        assert resp.status_code == 401

    def test_get_favorites_empty(self, client, auth_headers):
        """New user should have empty favorites list."""
        resp = client.get("/api/v1/favorites", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["total_count"] == 0
        assert data["favorites"] == []

    def test_check_favorite_not_favorited(self, client, auth_headers):
        """check endpoint should return is_favorite=False for unknown restaurant."""
        resp = client.get(
            f"/api/v1/favorites/check/{self.FAKE_RESTAURANT_ID}",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["data"]["is_favorite"] is False

    def test_add_favorite(self, client, auth_headers):
        """POST should add a restaurant to favorites (even if restaurant doesn't exist)."""
        resp = client.post(
            f"/api/v1/favorites/{self.FAKE_RESTAURANT_ID}",
            headers=auth_headers,
        )
        # Either 201 (created) or 200 (already exists, idempotent)
        assert resp.status_code in (200, 201)

    def test_add_favorite_idempotent(self, client, auth_headers):
        """Adding the same restaurant twice should not raise an error."""
        rid = str(uuid.uuid4())
        resp1 = client.post(f"/api/v1/favorites/{rid}", headers=auth_headers)
        resp2 = client.post(f"/api/v1/favorites/{rid}", headers=auth_headers)
        assert resp1.status_code in (200, 201)
        assert resp2.status_code in (200, 201)  # idempotent

    def test_remove_favorite(self, client, auth_headers):
        """DELETE should remove the favorite."""
        rid = str(uuid.uuid4())
        client.post(f"/api/v1/favorites/{rid}", headers=auth_headers)
        resp = client.delete(f"/api/v1/favorites/{rid}", headers=auth_headers)
        assert resp.status_code == 200

    def test_remove_nonexistent_favorite(self, client, auth_headers):
        """DELETE on a non-favorited restaurant should return 404."""
        resp = client.delete(
            f"/api/v1/favorites/{uuid.uuid4()}",
            headers=auth_headers,
        )
        assert resp.status_code == 404

    def test_check_after_add(self, client, auth_headers):
        """After adding a favorite, check should return is_favorite=True."""
        rid = str(uuid.uuid4())
        client.post(f"/api/v1/favorites/{rid}", headers=auth_headers)
        resp = client.get(f"/api/v1/favorites/check/{rid}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["data"]["is_favorite"] is True

    def test_check_after_remove(self, client, auth_headers):
        """After removing a favorite, check should return is_favorite=False."""
        rid = str(uuid.uuid4())
        client.post(f"/api/v1/favorites/{rid}", headers=auth_headers)
        client.delete(f"/api/v1/favorites/{rid}", headers=auth_headers)
        resp = client.get(f"/api/v1/favorites/check/{rid}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["data"]["is_favorite"] is False

    def test_get_favorites_pagination(self, client, auth_headers):
        """Pagination params should be respected."""
        resp = client.get(
            "/api/v1/favorites?page=1&page_size=5",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "page" in data
        assert "page_size" in data
        assert "has_more" in data
