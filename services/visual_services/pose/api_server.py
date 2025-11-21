import os
from docker_api_server import create_service_app

def build_pose_command(req):
    # S'assurer que le dossier de sortie existe
    os.makedirs(req.outdir, exist_ok=True)

    # Nom du fichier de sortie : même nom + suffixe _pose.jpg
    img_name = os.path.basename(req.input_path)
    stem, _ = os.path.splitext(img_name)
    out_image_path = os.path.join(req.outdir, f"{stem}_pose.jpg")

    # Config + checkpoint MMPose (top-down COCO HRNet)
    mmpose_config = (
        "configs/body_2d_keypoint/topdown_heatmap/coco/"
        "td-hm_hrnet-w48_8xb32-210e_coco-256x192.py"
    )
    mmpose_checkpoint = (
        "checkpoints/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth"
    )

    cmd = [
        "python3", "demo/image_demo.py",
        req.input_path,          # image d'entrée
        mmpose_config,
        mmpose_checkpoint,
        "--out-file", out_image_path,
        "--device", "cuda:0",
        # Optionnel :
        # "--device", "cuda:0",
        # "--draw-heatmap",
    ]
    return cmd

app = create_service_app("pose", build_pose_command)
