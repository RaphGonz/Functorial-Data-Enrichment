from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

def create_service_app(name,command_builder):
    """
    Crée une API FastAPI standardisée pour un service dockerisé.
    command_builder(req: BaseModel) -> list[str] retourne la commande à exécuter.
    """
    app = FastAPI(title=name)

    class RunRequest(BaseModel):
        input_path: str            # fichier d’entrée générique
        outdir: str = "output"  # répertoire de sortie
        extra: dict | None = None  # paramètres libres optionnels

    @app.post("/run")
    def run_service(req: RunRequest):
        cmd = command_builder(req)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        return {"stdout": result.stdout.strip()}

    return app
