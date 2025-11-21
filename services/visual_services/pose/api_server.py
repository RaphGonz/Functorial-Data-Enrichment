# services/visual_services/pose/api_server.py

import os
from services.docker_api_server import create_service_app

def build_pose_command(req) -> list[str]:
    """
    Construit la commande bash à exécuter pour générer une image de squelette
    uniquement, à partir de YOLOv8 pose.

    - source: req.input_path
    - sortie: req.outdir/pose_skeleton.png
    """
    input_path = req.input_path
    outdir = req.outdir

    # Laisser docker_api_server gérer la création des dossiers si c’est déjà le cas,
    # sinon tu peux garder cette ligne :
    os.makedirs(outdir, exist_ok=True)

    output_path = os.path.join(outdir, "pose_skeleton.png")

    cmd = [
        "python3",
        "/app/pose/pose_skeleton_only.py",
        "--input",
        input_path,
        "--output",
        output_path,
        "--model",
        "yolov8n-pose.pt",
    ]

    return cmd

app = create_service_app("pose", build_pose_command)