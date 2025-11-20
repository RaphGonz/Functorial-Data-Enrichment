from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from orchestrator.orchestrator import Orchestrator
from services.service_spec import ServiceSpec

# Instanciation de l'application FastAPI
app = FastAPI(
    title="Raffinerie Data API",
    version="1.0",
    description="API de la Raffinerie de données (image + texte)"
)

# ---- AJOUT ----

class OrchestratorRequest(BaseModel):
    raw_dir: str
    processed_dir: str
    service_specs: List[ServiceSpec]

@app.post("/test-orchestrator")
async def test_orchestrator_image_only(req: OrchestratorRequest):
    orch = Orchestrator(
        raw_dir=req.raw_dir,
        processed_dir=req.processed_dir,
        service_specs=req.service_specs  # Vous pouvez ajouter des spécifications de service si nécessaire
    )
    await orch.run()
    return {"status": "ok", "processed_dir": req.processed_dir}


# ---- FIN AJOUT ----

@app.get("/")
def root():
    return {"message": "Raffinerie API en ligne"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

#pour lancer : python -m uvicorn main:app --reload