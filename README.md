# Raphinerie
Pour ajouter un enrichissement :
Trouver un repo git convenable
IA => Dockerfile imitant ceux qui existent déjà
api_server.py en fonction du repo
Modifier enriched_data.py et mapping en fonction de ce que fournis la techno
ajouter dans docker-compose (copier ce qui est déjà fait)
ajouter dans .env
ajouter dans services.all_services_specs.py
ajouter dans config.service.yml

Dans le cas où les docker ne trouvent pas docker-gpu-base
run cette commande
docker build -f docker/Dockerfile -t raffinerie-gpu-base .

puis

docker build -f services/X/Y/Dockerfile -t raffinerie-Y .

Et ensuite

docker compose up -d --no-build

Pour lancer l'appli

basic appel test

Poids à télécharger
depth : https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_vits.pth?download=true
object detection : https://dl.fbaipublicfiles.com/detectron2/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl

et le renommer mask_rcnn_R_50_FPN_3x.pkl

pointcloud : https://huggingface.co/lpiccinelli/unik3d-vitl/resolve/main/config.json
              https://huggingface.co/lpiccinelli/unik3d-vitl/resolve/main/model.safetensors
              https://huggingface.co/lpiccinelli/unik3d-vitl/resolve/main/pytorch_model.bin
et tout mettre dans le dossier models (c'est très relou comme fonctionnement)

image_generation : https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt à mettre dans models/sd-15
                    https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/003_realSR_BSRGAN_DFOWMFC_s64w8_SwinIR-L_x4_GAN.pth
à renommer real_4x.pth et mettre dans models/swinIR

pose : https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n-pose.pt

mesh_3d : https://huggingface.co/stabilityai/TripoSR/resolve/main/model.ckpt



{
  "raw_dir": "/shared/input",
  "processed_dir": "/shared/output",
  "service_specs": [
    {
      "name": "depth",
      "fills": [
        "visual.depth_map"
      ],
      "needs_image": true
    },
    {
      "name": "pose",
      "fills": [
        "visual.pose_detection"
      ],
      "needs_image": true
    },
    {
      "name": "pointcloud",
      "fills": [
        "visual.pointcloud_3d"
      ],
      "needs_image": true
    },
    {
      "name": "object_detection",
      "fills": [
        "visual.object_detection"
      ],
      "needs_image": true
    },
    {
      "name": "mesh_3d",
      "fills": [
        "visual.object_detection.mesh_3d"
      ],
      "needs_fields": ["visual.object_detection"]
    },
    {
      "name": "image_generation",
      "fills": [
        "visual.base_image"
      ],
      "needs_fields": ["semantic.base_text"]
    }
  ]
}
