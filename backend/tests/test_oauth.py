import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.services.oauth_service import OAuthService
from app.models.user import User, Role
from app.core.security import decode_token

# Ensure database tables exist for tests
Base.metadata.create_all(bind=engine)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_google_oauth_authorization_url():
    """Verify Google OAuth authorization URL structure and state encoding."""
    url = OAuthService.get_authorization_url("google", role="LANDLORD")
    assert "https://accounts.google.com/o/oauth2/v2/auth" in url
    assert "client_id=" in url
    assert "response_type=code" in url
    assert "scope=openid" in url
    assert "state=google%3ALANDLORD" in url or "state=google:LANDLORD" in url

def test_google_oauth_mock_login_and_provisioning():
    """Verify OAuth code processing, user creation, role assignment, and JWT token creation."""
    db = SessionLocal()
    try:
        mock_code = "mock_test_google_123"
        state = "google:LANDLORD"
        
        user, access_token, refresh_token = OAuthService.process_oauth_login(
            provider="google",
            code=mock_code,
            db=db,
            default_role="TENANT",
            state=state
        )

        assert user is not None
        assert user.id is not None
        assert user.email == f"user_{mock_code[:6]}@google.com"
        assert user.is_active is True
        assert user.is_verified is True

        # Check role assignment from state (LANDLORD)
        role_names = [r.name for r in user.roles]
        assert "LANDLORD" in role_names

        # Check organization assignment
        assert user.current_org_id is not None

        # Check JWT access token validity
        payload = decode_token(access_token)
        assert payload.get("sub") == user.id
        assert payload.get("type") == "access"

        # Re-authenticate existing user to ensure idempotency
        user_again, token_again, _ = OAuthService.process_oauth_login(
            provider="google",
            code=mock_code,
            db=db,
            default_role="TENANT",
            state=state
        )
        assert user_again.id == user.id

        print(f"\n[OAuth Test] Successfully authenticated user: {user.email} (ID: {user.id}, Role: {role_names})")
    finally:
        db.close()

def test_google_oauth_api_endpoints():
    """Test OAuth authorization URL endpoint and callback API endpoint via FastAPI TestClient."""
    # Test GET OAuth URL endpoint
    resp = client.get("/api/v1/auth/oauth/google/url?role=LANDLORD")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "authorization_url" in data["data"]
    assert "https://accounts.google.com/o/oauth2/v2/auth" in data["data"]["authorization_url"]

    # Test GET OAuth Callback endpoint
    cb_resp = client.get("/api/v1/auth/oauth/google/callback?code=mock_api_test_123&state=google:TENANT")
    assert cb_resp.status_code == 200
    cb_data = cb_resp.json()
    assert cb_data["success"] is True
    assert "access_token" in cb_data["data"]
    assert "refresh_token" in cb_data["data"]
    assert cb_data["data"]["user"]["email"] == "user_mock_a@google.com"

if __name__ == "__main__":
    test_google_oauth_authorization_url()
    test_google_oauth_mock_login_and_provisioning()
    test_google_oauth_api_endpoints()
    print("\n[SUCCESS] ALL OAUTH TESTS PASSED!")
