import os
import json
import asyncio
from typing import Dict, Any, List, Optional

from pydantic import BaseModel
from orchestrator.enriched_data import EnrichedData
from services.registry import get_service
from services.service_spec import ServiceSpec


def merge_dicts(a: Dict, b: Dict):
    for k, v in b.items():
        if k in a and isinstance(a[k], dict) and isinstance(v, dict):
            merge_dicts(a[k], v)
        else:
            a[k] = v
    return a


class State(BaseModel):
    id: str
    item_dir: str
    image_path: Optional[str] = None
    text: Optional[str] = None
    enriched: Dict[str, Any] = {}
    fields_ready: Dict[str, bool] = {}



class Orchestrator:

    def __init__(self, raw_dir: str, processed_dir: str, service_specs: List[ServiceSpec]):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.service_specs = service_specs

    # ---------------------------------------------------------
    def _load_raw(self) -> List[State]:
        states = []
        manifest_path = None
        for filename in os.listdir(self.raw_dir):
            fpath = os.path.join(self.raw_dir, filename)
            if not os.path.isfile(fpath):
                continue

            name, ext = os.path.splitext(filename)
            

            if filename == "manifest.json":
                manifest_path = fpath
                continue

            if ext.lower() in [".png", ".jpg", ".jpeg", ".bmp"]:
                item_dir = os.path.join(self.processed_dir, name)
                os.makedirs(item_dir, exist_ok=True)
                states.append(
                    State(
                        id=name,
                        item_dir=item_dir,
                        image_path=fpath,
                        enriched={},
                        fields_ready={}
                    )
                )
            elif ext.lower() in [".txt"]:
                with open(fpath, "r", encoding="utf-8") as f:
                    txt = f.read().strip()
                item_dir = os.path.join(self.processed_dir, name)
                os.makedirs(item_dir, exist_ok=True)
                states.append(
                    State(
                        id=name,
                        item_dir=item_dir,
                        text=txt,
                        enriched={},
                        fields_ready={"semantic.summary": False}
                    )
                )
        if manifest_path:
            # chargement du manifest pour compléter/ajouter des States 
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)

            # dictionnaire temporaire pour retrouver les States par image_path
            state_by_path = {s.image_path: s for s in states if s.image_path}

            for item in manifest:
                img = item.get("image_path")
                desc = item.get("description")
                extra = {k:v for k,v in item.items() if k not in ["image_path","description"]}

                if img in state_by_path:
                    st = state_by_path[img]
                    if desc:
                        st.text = desc
                    merge_dicts(st.enriched, extra)
                else:
                # si image absente du dossier brut mais présente dans le manifest
                    mid = os.path.splitext(os.path.basename(img or "item"))[0]
                    idir = os.path.join(self.processed_dir, mid)
                    os.makedirs(idir, exist_ok=True)

                    st = State(
                        id=mid,
                        item_dir=idir,
                        image_path=img,
                        text=desc,
                        enriched=extra,
                        fields_ready={}
                            )
                    states.append(st)

        return states

    # ---------------------------------------------------------
    def _ensure_file(self, state: State) -> str:
        if state.image_path:
            return state.image_path

        temp_json = os.path.join(state.item_dir, "tmp.json")

        data = {
            "text": state.text,
            **state.enriched
            }

        with open(temp_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return temp_json

    # ---------------------------------------------------------
    def _inputs_available(self, state: State, spec: ServiceSpec) -> bool:
        if spec.needs_image and not state.image_path:
            return False

        if spec.needs_text and not state.text:
            return False

        if spec.needs_json and not isinstance(state.enriched, dict):
            return False

        for fld in spec.needs_fields:
            if not state.fields_ready.get(fld, False):
                return False

        return True

    # ---------------------------------------------------------
    def _already_filled(self, state: State, spec: ServiceSpec) -> bool:
        for fld in spec.fills:
            if state.fields_ready.get(fld) is True:
                continue
            return False
        return True

    # ---------------------------------------------------------
    async def _run_service(self, state: State, spec: ServiceSpec):
        service = get_service(spec.name)

        source = self._ensure_file(state)
        outdir = os.path.join(state.item_dir, spec.name)
        os.makedirs(outdir, exist_ok=True)

        result = await service.arun(source, outdir)

        merge_dicts(state.enriched, result)

        for fld in spec.fills:
            state.fields_ready[fld] = True

    # ---------------------------------------------------------
    async def run(self):

        print("\n========== ORCHESTRATOR RUN START ==========\n")
        print(f"RAW DIR: {self.raw_dir}")
        print(f"PROCESSED DIR: {self.processed_dir}")
        print(f"SERVICE SPECS: {[s.name for s in self.service_specs]}\n")

        states = self._load_raw()

        print("---- STATES LOADED ----")
        for s in states:
            print(f"State: id={s.id}")
            print(f"  image_path = {s.image_path}")
            print(f"  text       = {s.text}")
            print(f"  item_dir   = {s.item_dir}")
            print(f"  enriched   = {s.enriched}")
            print(f"  fields_ready = {s.fields_ready}")
        print("------------------------\n")
        iteration = 0
        while True: #très dangereux, mais je ne sais pas comment faire autrement pour l'instant, ptet ajouter un compteur max d'itérations
            
            iteration += 1
            print(f"\n---- ITERATION {iteration} ----")
            
            progress = False

            for state in states:
                print(f"\nChecking state '{state.id}'")
                for spec in self.service_specs:
                    print(f"  -> trying service '{spec.name}'")
                    if not self._inputs_available(state, spec):
                        print("     [skip] inputs not available")
                        continue

                    if self._already_filled(state, spec):
                        print(f"     [skip] already filled: {spec.fills}")
                        continue
                    
                    print(f"     [RUN] executing service '{spec.name}'")
                    print(f"     using source: {self._ensure_file(state)}")

                    await self._run_service(state, spec)

                    print(f"     [OK] service '{spec.name}' finished")
                    print(f"     updated enriched: {state.enriched}")
                    print(f"     updated fields_ready: {state.fields_ready}")
                    progress = True

            if not progress:
                print("\nNo more progress. Stopping loop.\n")
                break

        
        print("\n---- FINAL ENRICHMENT ----")
        manifest = []
        for st in states:
            print(f"Assembling enriched data for '{st.id}' ...")
            enriched = EnrichedData(
                id=st.id,
                source_file=st.image_path or st.id,
                text=st.text,
                **st.enriched
            )
            manifest.append(enriched.model_dump())

        out_manifest = os.path.join(self.processed_dir, "manifest.json")
        print(f"\nWriting final manifest to: {out_manifest}")
        with open(out_manifest, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        print("\n========== ORCHESTRATOR RUN END ==========\n")
