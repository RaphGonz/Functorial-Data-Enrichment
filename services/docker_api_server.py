from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os
import json

from services.mapping import SERVICE_MAPPING


def create_service_app(name, command_builder):
    """
    API FastAPI pour un service dockerisé.
    Ce serveur :
    - exécute une commande locale (subprocess)
    - regarde le dossier de sortie outdir
    - récupère les fichiers définis par SERVICE_MAPPING[name]
    - construit un fragment EnrichedData partiel
    - renvoie ce fragment au lieu du stdout brut
    """
    app = FastAPI(title=name)

    # ---------------------------------------------------------
    # MODEL DE LA REQUÊTE
    # ---------------------------------------------------------
    class RunRequest(BaseModel):
        input_path: str
        outdir: str = "output"
        extra: dict | None = None

    # ---------------------------------------------------------
    # LOADER UTILITAIRES
    # ---------------------------------------------------------
    def load_text(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()

    def load_json(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # loader générique selon mapping.json_loader
    def load_output(loader_type, file_path):
        if loader_type == "text":
            return load_text(file_path)
        if loader_type == "json":
            return load_json(file_path)
        if loader_type == "binary_path":
            return file_path.replace("\\", "/")
        if loader_type == "pose":
            # cas spécial : pose_detection
            return {
                "skeleton_path": file_path.replace("\\", "/"),
                "detected": True
            }
        return None

    # ---------------------------------------------------------
    # CONSTRUCTION DU FRAGMENT ENRICHEDDATA
    # ---------------------------------------------------------
    def build_fragment(service_name, outdir):
        """
        Traduit le dossier de sortie en fragment EnrichedData.
        """
        spec = SERVICE_MAPPING.get(service_name)
        if not spec:
            return {"error": f"Unknown service '{service_name}'"}

        loader_type = spec["json_loader"]
        files = spec["files"]
        enriched_path = spec["enriched_path"]
        method = spec["method"]

        # récupération des données depuis les fichiers
        if len(files) == 1:
            file_path = os.path.join(outdir, files[0])
            value = load_output(loader_type, file_path)
        else:
            # multi-fichiers possibles (rare)
            value = {}
            for f in files:
                fp = os.path.join(outdir, f)
                value[f] = load_output(loader_type, fp)

        # si le champ doit contenir method
        if loader_type == "binary_path":
            value = {
                "path": value,
                "confidence": None,
                "method": method
            }

        # injection dans structure imbriquée
        root = {}
        cursor = root

        for key in enriched_path[:-1]:
            cursor[key] = {}
            cursor = cursor[key]

        cursor[enriched_path[-1]] = value
        return root

    # ---------------------------------------------------------
    # ENDPOINT /run
    # ---------------------------------------------------------
    @app.post("/run")
    def run_service(req: RunRequest):
        # exécute le module python/cli/dialog interne
        cmd = command_builder(req)
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return {"error": result.stderr.strip()}

        # construit le JSON partiel attendu par l’orchestrateur
        fragment = build_fragment(name, req.outdir)
        return fragment

    return app
