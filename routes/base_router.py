from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Any

from services.registry import get_service

# ---- Schémas simples d'entrée et de sortie ----
class EnrichRequest(BaseModel):
    input_path: str
    outdir: str
    operations: List[str]

class EnrichResponse(BaseModel):
    status: str
    result: Any

# ---- Classe principale du routeur ----
class RaffinerieRouter:
    """Regroupe tous les points d'entrée de l'API Raffinerie."""

    def __init__(self):
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self):
        # Route principale /enrich
        @self.router.post("/enrich", response_model=EnrichResponse)
        def enrich_endpoint(req: EnrichRequest):
            # Simulation : à terme, appelera le service réel d’enrichissement
            result = {}
            for op in req.operations:
                service = get_service(op)
                result[op] = service.run(req.input_path,outdir=req.outdir)

            return {"status": "ok", "result": result}

        # Route de test /ping
        @self.router.get("/ping")
        def ping():
            return {"status": "alive"}

    def get_router(self):
        return self.router