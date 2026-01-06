# services/visual_services/mesh_3d/run_mesh_3d.py
import argparse
import json
import os
import shutil
import subprocess
from typing import Any, Dict, List, Optional

from PIL import Image

# Nouveau : script TripoSR
TRIPOSR_RUN_PATH = "/app/run.py"

# Dossier du modèle offline
TRIPOSR_MODEL_DIR = "/app/local_triposr_model"

TRIPOSR_IMAGE_SIZE = 512  # taille carrée cible


def preprocess_crop_for_triposr(src_path: str, dst_path: str) -> None:
    """
    Charge un crop (PNG avec alpha possible), le met sur un fond blanc
    dans un canvas carré 512x512, centré, puis sauvegarde en RGB.
    """
    img = Image.open(src_path).convert("RGBA")
    w, h = img.size

    # Redimensionne l'image pour qu'elle rentre dans un carré 512x512
    scale = min(TRIPOSR_IMAGE_SIZE / w, TRIPOSR_IMAGE_SIZE / h)
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))
    img_resized = img.resize((new_w, new_h), Image.LANCZOS)

    # Canvas blanc carré
    canvas = Image.new("RGBA", (TRIPOSR_IMAGE_SIZE, TRIPOSR_IMAGE_SIZE), (255, 255, 255, 255))

    # Centre l'objet dans le canvas
    offset_x = (TRIPOSR_IMAGE_SIZE - new_w) // 2
    offset_y = (TRIPOSR_IMAGE_SIZE - new_h) // 2
    canvas.paste(img_resized, (offset_x, offset_y), img_resized)

    # Convertit en RGB (plus d'alpha) et sauvegarde
    canvas_rgb = canvas.convert("RGB")
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    canvas_rgb.save(dst_path)


def generate_mesh_for_object(crop_path: str, tmp_dir: str) -> str:
    """
    Lance TripoSR sur une image croppée et renvoie le chemin du .obj généré.
    Les sorties brutes sont placées dans tmp_dir/.
    """
    # Crée le dossier temporaire + le sous-dossier "0" attendu par TripoSR
    os.makedirs(tmp_dir, exist_ok=True)
    os.makedirs(os.path.join(tmp_dir, "0"), exist_ok=True)

    # Image préprocessée pour TripoSR (512x512, fond blanc, centrée)
    preprocessed_path = os.path.join(tmp_dir, "input_triposr.png")
    preprocess_crop_for_triposr(crop_path, preprocessed_path)

    cmd: List[str] = [
        "python3",
        TRIPOSR_RUN_PATH,

        # TripoSR attend simplement l'image en argument
        preprocessed_path,

        # Sortie dans le dossier temporaire
        "--output-dir", tmp_dir,

        # Modèle offline
        "--pretrained-model-name-or-path", TRIPOSR_MODEL_DIR,

        # Optionnel : garder la vitesse
        "--mc-resolution", "256"
    ]

    subprocess.run(cmd, check=True)

    # TripoSR écrit ici :
    # tmp_dir/<index>/mesh.obj, donc typiquement tmp_dir/0/mesh.obj
    for root, _dirs, files in os.walk(tmp_dir):
        for fname in files:
            if fname.lower().endswith(".obj"):
                return os.path.join(root, fname)

    raise FileNotFoundError(f"Aucun fichier .obj généré par TripoSR dans {tmp_dir}")


def load_objects(objects_json_path: str) -> List[Dict[str, Any]]:
    if not os.path.isfile(objects_json_path):
        return []
    with open(objects_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{objects_json_path} ne contient pas une liste JSON d'objets")
    return data


def save_objects(objects_json_path: str, objects: List[Dict[str, Any]]) -> None:
    # Création du dossier si besoin
    dir_name = os.path.dirname(objects_json_path)
    if dir_name and not os.path.isdir(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    with open(objects_json_path, "w", encoding="utf-8") as f:
        json.dump(objects, f, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outdir",
        type=str,
        required=True,
        help="Dossier de sortie du service mesh_3d, ex: /shared/output/<id>/mesh_3d",
    )
    args = parser.parse_args()

    

    # outdir = /shared/output/<id>/mesh_3d (fourni par l'orchestrateur)
    outdir = os.path.normpath(args.outdir)
    os.makedirs(outdir, exist_ok=True)

    # base_dir = /shared/output/<id>
    base_dir = os.path.dirname(outdir)

    # Dossier et fichier d'object_detection existants
    object_detection_dir = os.path.join(base_dir, "object_detection")
    objects_json_path = os.path.join(object_detection_dir, "objects.json")

    objects = load_objects(objects_json_path)
    if not objects:
        # Rien à faire si l'on n'a pas d'objets à enrichir
        return

    # Tous les .obj sont rangés dans /shared/output/<id>/object_detection/
    mesh_root_dir = object_detection_dir
    os.makedirs(mesh_root_dir, exist_ok=True)

    # Dossier temporaire pour les générations
    tmp_root_dir = os.path.join(outdir, "tmp")
    os.makedirs(tmp_root_dir, exist_ok=True)

    for idx, obj in enumerate(objects):
        seg: Optional[Dict[str, Any]] = obj.get("segmentation") or {}
        crop_path = seg.get("cropped_image_path")

        if not crop_path:
            continue

        crop_path_fs = crop_path
        if not os.path.isabs(crop_path_fs):
            crop_path_fs = crop_path

        if not os.path.isfile(crop_path_fs):
            continue

        obj_id = obj.get("id") or f"obj_{idx:03d}"

        final_mesh_name = f"{obj_id}_mesh.obj"
        final_mesh_path = os.path.join(mesh_root_dir, final_mesh_name)

        existing_mesh = obj.get("mesh_3d")
        if (
            isinstance(existing_mesh, dict)
            and isinstance(existing_mesh.get("path"), str)
            and os.path.isfile(existing_mesh.get("path"))
        ):
            continue

        tmp_dir = os.path.join(tmp_root_dir, obj_id)

        generated_mesh_path = generate_mesh_for_object(
            crop_path=crop_path_fs,
            tmp_dir=tmp_dir,
        )

        if os.path.isfile(final_mesh_path):
            os.remove(final_mesh_path)
        shutil.move(generated_mesh_path, final_mesh_path)

        final_mesh_path_norm = final_mesh_path.replace("\\", "/")

        obj["mesh_3d"] = {
            "path": final_mesh_path_norm,
            "method": "tripoSR",
            "confidence": None,
        }

    save_objects(objects_json_path, objects)

    objects_json_dest = os.path.join(outdir, "objects.json")
    save_objects(objects_json_dest, objects)

    # Nettoyage : on supprime le scratch /tmp du service mesh_3d
    tmp_root_dir = os.path.join(outdir, "tmp")
    shutil.rmtree(tmp_root_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
