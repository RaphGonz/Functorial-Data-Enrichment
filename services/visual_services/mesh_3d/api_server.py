import os
from services.docker_api_server import create_service_app


def build_mesh_3d_command(req) -> list[str]:
    """
    Lance le script mesh_3d sur le dossier de l'item.

    - object_detection écrit dans: <item_dir>/object_detection/
    - ce service écrit dans      : <item_dir>/mesh_3d/
    - les fichiers .obj finaux sont rangés dans: <item_dir>/object_detection/
    """
    outdir = req.outdir  # == <item_dir>/mesh_3d
    os.makedirs(outdir, exist_ok=True)

    cmd = [
        "python3",
        "/app/run_mesh_3d.py",
        "--outdir",
        outdir,
    ]
    return cmd


app = create_service_app("mesh_3d", build_mesh_3d_command)
