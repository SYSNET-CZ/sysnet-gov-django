from fastapi import FastAPI, Request, HTTPException, Depends
from sysnet_cites_core_engine.epix.translator import EpixTranslator
from sysnet_cites_core_engine.repository import PostgreSQLRepository
from sysnet_cites_core_engine.auth import require_role, Role
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

app = FastAPI(title="CITES-X EPIX Gateway")

# Gateway typically uses MTLS or System Bearer tokens for Inter-Gov communication
DB_URL = "postgresql+asyncpg://docker:docker@localhost:25432/docker"
engine = create_async_engine(DB_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@app.get("/epix/v1/verify/{permit_number}")
async def verify_permit_epix(permit_number: str):
    """
    Public Gov-to-Gov endpoint for permit verification.
    Returns eCITES XML format.
    """
    async with async_session() as session:
        repo = PostgreSQLRepository(session)
        permit = await repo.get_permit(permit_number)
        
        if not permit:
            raise HTTPException(status_code=404, detail="Permit not found in international registry")
            
        # Transform to standard XML
        xml_output = EpixTranslator.to_xml(permit)
        
        from fastapi import Response
        return Response(content=xml_output, media_type="application/xml")

@app.post("/epix/v1/validate-incoming")
async def validate_incoming(request: Request):
    """
    Endpoint for our Customs to validate a foreign permit provided as XML.
    """
    # Logic to receive and verify foreign XML
    return {"status": "implementing", "info": "UN/CEFACT Validation Logic"}
