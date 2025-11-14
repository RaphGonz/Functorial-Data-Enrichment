from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from routes.base_router import RaffinerieRouter

from orchestrator.orchestrator import Orchestrator

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
    operations: list[str]

@app.post("/test-orchestrator")
async def test_orchestrator(req: OrchestratorRequest):
    orch = Orchestrator(
        raw_dir=req.raw_dir,
        processed_dir=req.processed_dir,
        operations=req.operations
    )
    await orch.run()
    return {"status": "ok", "processed_dir": req.processed_dir}
# ---- FIN AJOUT ----

# Création du routeur principal
api_router = RaffinerieRouter()

# Enregistrement du routeur sous le préfixe /api/v1
app.include_router(api_router.get_router(), prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Raffinerie API en ligne"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

#pour lancer : python -m uvicorn main:app --reload