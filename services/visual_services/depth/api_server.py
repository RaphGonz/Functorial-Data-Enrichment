from services.docker_api_server import create_service_app

def build_depth_command(req):
    cmd = [
        "python3", "run.py",
        "--encoder", req.encoder or "vits",
        "--img-path", req.image_path,
        "--outdir", req.outdir,
    ]
    return cmd

app = create_service_app(build_depth_command)
