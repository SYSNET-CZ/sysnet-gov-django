from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sysnet_cites_portal.main import app as core_app

app = FastAPI(title="CITES-X Slovenský portál (Evidencia držby)")
templates = Jinja2Templates(directory="packages/cites-portal-sk/sysnet_cites_portal_sk/templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "sk_index.html", {
        "title": "CITES-X | Evidencia držby (SR)",
        "request": request
    })

# Mount core app for common services
app.mount("/core", core_app)
