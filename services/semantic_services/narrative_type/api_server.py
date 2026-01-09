# services/visual_services/pose/api_server.py

import os
from services.docker_api_server import create_service_app

def build_narrative_type_command(req) -> list[str]:
    """
    - source: req.input_path
    - sortie: req.outdir/narrative_type.json
    """
    input_path = req.input_path
    outdir = req.outdir


    os.makedirs(outdir, exist_ok=True)


    cmd = [
        "python3",
        "/app/semantic_services/narrative_type/run.py",
        "--input",
        input_path,
        "--output",
        outdir
    ]

    return cmd

app = create_service_app("narrative_type", build_narrative_type_command)