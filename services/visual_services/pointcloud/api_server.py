from services.docker_api_server import create_service_app


def build_unik3d_command(req):
    # Config ViT-S (petit modèle)
    config_file = "configs/eval/vits.json"

    cmd = [
        "python3", "scripts/infer.py",
        "--input", req.input_path,
        "--output", req.outdir,
        "--config-file", config_file,
        "--save-ply",
    ]

    # Paramètres optionnels passés via req.extra
    if req.extra:
        camera_path = req.extra.get("camera_path")
        if camera_path:
            cmd.extend(["--camera-path", camera_path])

        resolution_level = req.extra.get("resolution_level")
        if resolution_level is not None:
            cmd.extend(["--resolution-level", str(resolution_level)])

    return cmd


app = create_service_app("pointcloud", build_unik3d_command)
