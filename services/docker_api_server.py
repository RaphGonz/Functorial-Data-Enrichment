from typing import Optional
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
        extra: Optional[dict] = None

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
    # UTILITAIRE DE NORMALISATION DES FICHIERS
    # ---------------------------------------------------------
    def normalize_output_files(service_name: str, outdir: str) -> None:
        """
        Assure que le(s) fichier(s) de sortie aient le nom attendu par SERVICE_MAPPING.
        Par ex., si SERVICE_MAPPING[service]["files"] = ["map.png"], on renomme
        le premier fichier compatible trouvé dans outdir en 'map.png' si besoin.
        """
        spec = SERVICE_MAPPING.get(service_name)
        if not spec:
            return

        loader_type = spec["json_loader"]
        files = spec["files"]

        # On ne traite ici que le cas simple: 1 fichier, type binary_path
        if loader_type != "binary_path" or len(files) != 1:
            return

        desired_name = files[0]
        desired_path = os.path.join(outdir, desired_name)

        # Si le fichier avec le bon nom existe déjà, on ne fait rien
        if os.path.exists(desired_path):
            return

        # Sinon, on cherche un candidat dans le dossier de sortie
        ext = os.path.splitext(desired_name)[1].lower()
        candidates = []

        if not os.path.isdir(outdir):
            return

        for f in os.listdir(outdir):
            full = os.path.join(outdir, f)
            if not os.path.isfile(full):
                continue
            if ext:
                if f.lower().endswith(ext):
                    candidates.append(full)
            else:
                candidates.append(full)

        if not candidates:
            return

        # On prend le premier candidat (ou trié si tu veux plus de déterminisme)
        src = sorted(candidates)[0]
        os.rename(src, desired_path)

    
    def build_output_dict(service_name, outdir):
        """
        Construit un dict simple basé sur SERVICE_MAPPING,
        sans structure de fragment EnrichedData.
        """
        spec = SERVICE_MAPPING.get(service_name)
        if not spec:
            return {"error": f"Unknown service '{service_name}'"}

        loader_type = spec["json_loader"]
        files = spec["files"]
        enriched_path = spec["enriched_path"]      # ex: ["visual", "depth_map"]
        method = spec["method"]

        # Charger les données
        if len(files) == 1:
            file_path = os.path.join(outdir, files[0])
            value = load_output(loader_type, file_path)
        else:
            # fusionne proprement les fragments retournés par load_output()
            merged = {}
            for f in files:
                fp = os.path.join(outdir, f)
                part = load_output(loader_type, fp)
                if isinstance(part, dict):
                    merged.update(part)
            value = merged
        
        # Ajouter "method" si binary_path
        if loader_type == "binary_path":
            value = {
                "path": value,
                "confidence": None,
                "method": method
            }

        # Construction d'un simple dict json basé sur enriched_path
        # Ex: ["visual", "depth_map"] → {"visual": {"depth_map": value}}
        root_key = enriched_path[0]
        sub_key = enriched_path[1]

        return {
            root_key: {
            sub_key: value
            }
        }

    # ---------------------------------------------------------
    # ENDPOINT /run
    # ---------------------------------------------------------
    @app.post("/run")
    def run_service(req: RunRequest):
        # exécute le module python/cli/dialog interne
        cmd = command_builder(req)

        # Si le command_builder renvoie une str → on utilise un shell (pour &&, etc.)
        # Si c'est une liste → comportement historique (pose, depth, etc.)
        use_shell = isinstance(cmd, str)

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=use_shell,
        )
        
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        
        # Normalise les noms de fichiers produits dans outdir
        normalize_output_files(name, req.outdir)

        # construit le JSON partiel attendu par l’orchestrateur
        fragment = build_output_dict(name, req.outdir)
        return fragment

    return app
