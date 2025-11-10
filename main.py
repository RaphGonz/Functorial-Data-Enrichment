from fastapi import FastAPI
from pydantic import BaseModel
from routes.base_router import RaffinerieRouter

# Instanciation de l'application FastAPI
app = FastAPI(
    title="Raffinerie Data API",
    version="1.0",
    description="API de la Raffinerie de données (image + texte)"
)

# Création du routeur principal
api_router = RaffinerieRouter()

# Enregistrement du routeur sous le préfixe /api/v1
app.include_router(api_router.get_router(), prefix="/api/v1")

class InferenceRequest(BaseModel):
    image_path: str

@app.post("/run")
def run_model(req: InferenceRequest):
    # Exemple : appel du modèle local
    result = {"message": f"Traitement sur {req.image_path}"}
    return result

@app.get("/")
def root():
    return {"message": "Raffinerie API en ligne"}

#pour lancer : python -m uvicorn main:app --reload