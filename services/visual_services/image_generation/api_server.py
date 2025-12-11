import os
from services.docker_api_server import create_service_app


def build_image_generation_command(req) -> list[str]:
    
    input_path = req.input_path
    outdir = req.outdir  # == <item_dir>/image_generation
    os.makedirs(outdir, exist_ok=True)

    cmd = [
        "python3",
        "/app/run_image.py",
        "--input-path",
        input_path,
        "--outdir",
        outdir,
    ]
    return cmd


app = create_service_app("image_generation", build_image_generation_command)
