from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sysnet_cites_core_engine.repository import PostgreSQLRepository

app = FastAPI(title="CITES-X Core Portal")
templates = Jinja2Templates(directory="packages/cites-portal-core/sysnet_cites_portal/templates")

# DB Setup (using the standard TEST_DB_URL for this phase)
DB_URL = "postgresql+asyncpg://docker:docker@localhost:25432/docker"
engine = create_async_engine(DB_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {
        "title": "CITES-X | Paperless CITES",
        "request": request
    })

@app.get("/permits/{permit_id}")
async def view_permit(request: Request, permit_id: str):
    async with async_session() as session:
        repo = PostgreSQLRepository(session)
        permit = await repo.get_permit(permit_id)
        
        if not permit:
            raise HTTPException(status_code=404, detail="Permit not found")
            
        movements = await repo.get_movements(permit_id)
        
        return templates.TemplateResponse(request, "permit_detail.html", {
            "title": f"Permit {permit_id}",
            "request": request,
            "permit": permit,
            "movements": movements
        })
