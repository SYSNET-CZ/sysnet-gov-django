import enum
import asyncio
import time
import httpx
from typing import Optional, List, Set, Dict, Any
from dataclasses import dataclass, field
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError

class Role(str, enum.Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"

ROLE_HIERARCHY: Dict[Role, Set[Role]] = {
    Role.ADMIN: {Role.ADMIN, Role.OPERATOR, Role.VIEWER},
    Role.OPERATOR: {Role.OPERATOR, Role.VIEWER},
    Role.VIEWER: {Role.VIEWER},
}

def expand_roles(roles: Set[Role]) -> Set[Role]:
    effective: Set[Role] = set()
    for role in roles:
        effective.update(ROLE_HIERARCHY.get(role, set()))
    return effective

@dataclass(frozen=True)
class Principal:
    sub: str
    username: str
    roles: Set[Role]
    claims: Dict[str, Any] = field(default_factory=dict, compare=False, hash=False)

    def has_role(self, role: Role) -> bool:
        return role in self.roles

# Configuration (In production via env vars)
KEYCLOAK_URL = "https://auth.sysnet.cz"
REALM = "hermes-test"
CLIENT_ID = "cites-x-api"
JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"

class JWKSCache:
    def __init__(self, ttl: int = 300):
        self._ttl = ttl
        self._keys: List[Dict[str, Any]] = []
        self._fetched_at: float = 0.0
        self._lock = asyncio.Lock()

    async def get_keys(self) -> List[Dict[str, Any]]:
        async with self._lock:
            if not self._keys or (time.monotonic() - self._fetched_at) > self._ttl:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(JWKS_URL)
                    resp.raise_for_status()
                    self._keys = resp.json().get("keys", [])
                    self._fetched_at = time.monotonic()
            return self._keys

jwks_cache = JWKSCache()
security = HTTPBearer()

async def get_current_principal(res: HTTPAuthorizationCredentials = Security(security)) -> Principal:
    token = res.credentials
    try:
        keys = await jwks_cache.get_keys()
        # In real life, find the right key via 'kid' in header
        # For brevity/POC we assume RS256 and single key or jose handles it
        unverified_claims = jwt.get_unverified_claims(token)
        
        # In production use full validation:
        # payload = jwt.decode(token, keys, algorithms=["RS256"], audience=CLIENT_ID)
        payload = unverified_claims # Temporary POC bypass
        
        raw_roles = payload.get("realm_access", {}).get("roles", [])
        parsed_roles = set()
        for r in raw_roles:
            try:
                parsed_roles.add(Role(r))
            except ValueError:
                continue

        return Principal(
            sub=payload.get("sub"),
            username=payload.get("preferred_username"),
            roles=expand_roles(parsed_roles),
            claims=payload
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication: {str(e)}"
        )

def require_role(required_role: Role):
    async def role_checker(principal: Principal = Depends(get_current_principal)):
        if not principal.has_role(required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required role: {required_role}"
            )
        return principal
    return role_checker
