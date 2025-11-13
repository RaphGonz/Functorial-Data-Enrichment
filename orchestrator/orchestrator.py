import os
import json
import asyncio
from typing import List
from enriched_data import EnrichedData
from services.registry import get_service


class Orchestrator:
    """
    Structure :
    /dataset/raw/*.png|*.txt
    /dataset/processed/<id>/<op>/
        (artefacts écrits par le service)
    /dataset/processed/manifest.json
    """

    def __init__(self, raw_dir: str, processed_dir: str, operations: List[str]):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.operations = operations

    async def _run_op(self, op: str, source_path: str, outdir: str):
        """
        Appelle un service et retourne un fragment EnrichedData déjà instancié.
        Le service écrit ses fichiers binaires dans outdir et retourne uniquement
        du JSON partiel correspondant au schéma EnrichedData.
        """
        service = get_service(op)
        partial_json = await service.arun(source_path, outdir)
        return EnrichedData(**partial_json)

    async def _process_one(self, source_path: str) -> EnrichedData:
        """
        Crée le dossier processed/<id>/, appelle tous les services en parallèle,
        fusionne les fragments EnrichedData en un seul EnrichedData complet.
        """
        basename = os.path.basename(source_path)
        name, ext = os.path.splitext(basename)

        item_dir = os.path.join(self.processed_dir, name)
        os.makedirs(item_dir, exist_ok=True)

        type_guess = "image" if ext.lower() in [".png", ".jpg", ".jpeg"] else "text"

        enriched = EnrichedData(
            id=name,
            type=type_guess,
            source_file=os.path.relpath(source_path, self.processed_dir),
            semantic=None,
            visual=None,
            links=None,
            metadata=None
        )

        tasks = []
        for op in self.operations:
            op_dir = os.path.join(item_dir, op)
            os.makedirs(op_dir, exist_ok=True)
            tasks.append(self._run_op(op, source_path, op_dir))

        results = await asyncio.gather(*tasks)

        for frag in results:
            if frag.semantic:
                enriched.semantic = frag.semantic
            if frag.visual:
                enriched.visual = frag.visual
            if frag.links:
                enriched.links = frag.links
            if frag.metadata:
                enriched.metadata = frag.metadata

        return enriched

    async def run(self):
        """
        Parcourt tous les fichiers de /raw, traite chacun en parallèle,
        produit un manifest.json avec la liste complète des EnrichedData.
        """
        files = [
            os.path.join(self.raw_dir, f)
            for f in os.listdir(self.raw_dir)
            if os.path.isfile(os.path.join(self.raw_dir, f))
        ]

        results = await asyncio.gather(*[self._process_one(p) for p in files])

        manifest_path = os.path.join(self.processed_dir, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump([r.dict() for r in results], f, indent=2)
