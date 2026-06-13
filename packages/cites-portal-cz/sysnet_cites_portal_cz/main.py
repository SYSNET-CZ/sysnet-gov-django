from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sysnet_cites_portal.main import app as core_app
from sysnet_cites_core_engine.repository import PostgreSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

app = FastAPI(title="CITES-X Český portál (GDS 4 / sysnet-gov-ui)")

# Templates lookup priority: CZ (GDS 4) -> Core (ECL)
templates = Jinja2Templates(directory=[
    "packages/cites-portal-cz/sysnet_cites_portal_cz/templates",
    "packages/cites-portal-core/sysnet_cites_portal/templates"
])

DB_URL = "postgresql+asyncpg://docker:docker@localhost:25432/docker"
engine = create_async_engine(DB_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "cz_index.html", {
        "title": "CITES-X | Registr CITES (ČR)",
        "request": request
    })

from .auth import get_current_principal, require_role, Role, Principal

from sysnet_cites_core_engine.audit.service import AuditLogger

@app.get("/permits/{permit_id}")
async def view_permit_cz(
    request: Request, 
    permit_id: str,
    principal: Principal = Depends(require_role(Role.VIEWER))
):
    async with async_session() as session:
        # Audit Logging Stage 8
        auditor = AuditLogger(session)
        await auditor.log(
            actor_id=principal.sub,
            action="ACCESS",
            target_id=permit_id,
            client_ip=request.client.host,
            payload={"portal": "cz", "username": principal.username}
        )

        repo = PostgreSQLRepository(session)
        permit = await repo.get_permit(permit_id)
        
        if not permit:
            raise HTTPException(status_code=404, detail="Permit not found")
            
        movements = await repo.get_movements(permit_id)
        
        # CZ specific context: check § 23 registration status
        is_registered = permit.extension_data.get("cz_registration_number") is not None
        
        return templates.TemplateResponse(request, "permit_detail_cz.html", {
            "title": f"Detail povolení {permit_id}",
            "request": request,
            "permit": permit,
            "movements": movements,
            "is_registered": is_registered,
            "legislation": "§ 23 zákona č. 100/2004 Sb."
        })

# Mount core paths if needed for static etc.
app.mount("/core", core_app)
