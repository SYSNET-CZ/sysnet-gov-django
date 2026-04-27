
import pytest
from unittest.mock import patch, MagicMock
from api.dependencies import get_request_identity
from sysnet_auth import AuthenticatedUser

@pytest.mark.asyncio
async def test_get_identity_no_token():
    # Simulace requestu bez Authorization headeru
    request = MagicMock()
    request.headers = {}
    
    identity = await get_request_identity(request)
    assert identity is None

@pytest.mark.asyncio
async def test_get_identity_valid_token():
    # Simulace requestu s validním tokenem
    request = MagicMock()
    request.headers = {"Authorization": "Bearer valid_token"}
    
    user_mock = AuthenticatedUser(
        sub="test-user-id",
        name="Test User",
        email="test@sysnet.cz",
        preferred_username="testuser",
        roles=["admin"]
    )
    
    # Mockujeme přímo volání auth_lib v dependencies
    with patch("api.dependencies.verify_token", return_value=user_mock):
        identity = await get_request_identity(request)
        assert identity is not None
        assert identity.sub == "test-user-id"

def test_whoami_anonymous(auth_client):
    response = auth_client.get("/whoami")
    assert response.status_code == 200
    assert response.json() == {"identity": None}

def test_whoami_authenticated(auth_client):
    user_data = {
        "sub": "user-123",
        "name": "Arnost Testovaci",
        "email": "arnost@sysnet.cz"
    }
    
    # Mockujeme verify_token pro FastAPI endpoint
    with patch("api.dependencies.verify_token", return_value=AuthenticatedUser(**user_data, preferred_username="arnost", roles=[])):
        response = auth_client.get("/whoami", headers={"Authorization": "Bearer fake_token"})
        assert response.status_code == 200
        assert response.json()["identity"]["sub"] == "user-123"
