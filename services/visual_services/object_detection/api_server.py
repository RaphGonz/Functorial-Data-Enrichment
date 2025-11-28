# services/visual_services/object_detection/api_server.py

import os
from services.docker_api_server import create_service_app


def build_object_detection_command(req) -> list[str]:
    """
    Construit la commande bash à exécuter pour générer le JSON des objets détectés.

    - source : req.input_path
    - sortie : req.outdir/objects.json
    """
    input_path = req.input_path
    outdir = req.outdir

    os.makedirs(outdir, exist_ok=True)

    cmd = [
        "python3",
        "/app/run_object_detection.py",
        "--input",
        input_path,
        "--outdir",
        outdir,
    ]

    return cmd


app = create_service_app("object_detection", build_object_detection_command)