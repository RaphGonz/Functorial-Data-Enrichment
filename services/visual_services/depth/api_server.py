from docker_api_server import create_service_app

def build_depth_command(req):

    encoder = None

    if req.extra and "encoder" in req.extra:    
        encoder = req.extra["encoder"]

    cmd = [
        "python3", "run.py",
        "--encoder", encoder or "vits",
        "--img-path", req.input_path,
        "--outdir", req.outdir,
        "--pred-only"
    ]
    return cmd

app = create_service_app("depth",build_depth_command)
