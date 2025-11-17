from ast import Dict
import os
import json
import asyncio
from typing import Any, List, Optional

from pydantic import BaseModel
from orchestrator.enriched_data import EnrichedData
from services.registry import get_service

def merge_dicts(a, b):
    for key, val in b.items():
        if key in a and isinstance(a[key], dict) and isinstance(val, dict):
            merge_dicts(a[key], val)
        else:
            a[key] = val
    return a

class ManifestData(BaseModel):
    image_path: Optional[str] = None
    description: Optional[str] = None
    else_data: Dict[str, Any] = {}


class Orchestrator:
    """
    Structure :
    /dataset/raw/*.png|*.txt
    /dataset/processed/<id>/<op>/
        (artefacts écrits par le service)
    /dataset/processed/manifest.json
    """

    def __init__(self, raw_dir: str, processed_dir: str, visual_operations: List[str], semantic_operations: List[str]):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.visual_operations = visual_operations
        self.semantic_operations = semantic_operations

    async def _run_op(self, op: str, source_path: str, outdir: str):
        """
        Appelle un service et retourne un fragment EnrichedData déjà instancié.
        Le service écrit ses fichiers binaires dans outdir et retourne uniquement
        du JSON partiel correspondant au schéma EnrichedData.
        """
        service = get_service(op)
        partial_json = await service.arun(source_path, outdir)
        return partial_json

    async def process(self, source_path: str, operations) -> EnrichedData:
        """
        Crée le dossier processed/<id>/, appelle tous les services en parallèle,
        fusionne les fragments EnrichedData en un seul EnrichedData complet.
        """
        basename = os.path.basename(source_path)
        name, ext = os.path.splitext(basename)

        item_dir = os.path.join(self.processed_dir, name)
        os.makedirs(item_dir, exist_ok=True)

        merged = {} #le futur EnrichedData

        tasks = [] #liste des json partiels à fusionner
        for op in operations:
            op_dir = os.path.join(item_dir, op)
            os.makedirs(op_dir, exist_ok=True)
            tasks.append(self._run_op(op, source_path, op_dir))

        results = await asyncio.gather(*tasks)

        for frag in results:
            if isinstance(frag, dict):
                merge_dicts(merged, frag)

        merged["id"] = name
        merged["source_file"] = os.path.relpath(source_path, self.processed_dir)

        return EnrichedData(**merged)
    
    
    async def run(self,pipeline_type:str):
        files = [
            os.path.join(self.raw_dir, f)
            for f in os.listdir(self.raw_dir)
            if os.path.isfile(os.path.join(self.raw_dir, f))
        ]

        manifest_file = None
        image_files = []

        for path in files:
            if path.endswith("manifest.json"):
                manifest_file = path
            else:
                image_files.append(path)
        
        manifest_item_list = []
        if manifest_file:
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest_json = json.load(f)

            for item in manifest_json:
                manifest_item_list.append(
                    ManifestData(
                        image_path=item.get("image_path"),
                        description=item.get("description"),
                        else_data=item.get("else") or {}
                    )
                )
        
        if pipeline_type=="image_text":
            img_result = await asyncio.gather(*[self.process(img,self.visual_operations) for img in image_files])
            manifest_result = await asyncio.gather(*[self.process(md,self.semantic_operations) for md in manifest_item_list])
        
        if pipeline_type=="image_only":
            img_result = await asyncio.gather(*[self.process(img,self.visual_operations) for img in image_files])
            manifest_result = []

        input_data_list = img_result + manifest_result

        manifest_path = os.path.join(self.processed_dir, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump([md.model_dump() for md in input_data_list], f, indent=2)