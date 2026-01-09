# services/visual_services/pose/api_server.py

import os
from services.docker_api_server import create_service_app

def build_topic_classification_command(req) -> list[str]:
    """
    - source: req.input_path
    - sortie: req.outdir/topic_classification.json
    """
    input_path = req.input_path
    outdir = req.outdir


    os.makedirs(outdir, exist_ok=True)


    cmd = [
        "python3",
        "/app/semantic_services/topic_classification/run.py",
        "--input",
        input_path,
        "--output",
        outdir
    ]

    return cmd

app = create_service_app("topic_classification", build_topic_classification_command)