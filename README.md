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
      "needs_fields": ["visual.base_text"]
    }
  ]
}
