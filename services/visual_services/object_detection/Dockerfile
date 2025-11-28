# Service Detectron2 : détection + segmentation d’instances

FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    build-essential \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*

# Detectron2 depuis GitHub (version 0.6 compatible torch 2.x / cu118)
RUN pip install --no-cache-dir \
    'git+https://github.com/facebookresearch/detectron2.git'\
    opencv-python-headless

# FastAPI + Uvicorn communs aux services
RUN pip install --no-cache-dir fastapi uvicorn

# Forcer NumPy 1.x pour être compatible avec les modules compilés
RUN pip install --no-cache-dir "numpy<2" --force-reinstall

# Pré-télécharger le checkpoint Mask R-CNN et le copier dans /app/models
RUN python -c "from detectron2 import model_zoo; from detectron2.utils.file_io import PathManager; import os, shutil; \
url = model_zoo.get_checkpoint_url('COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml'); \
local_path = PathManager.get_local_path(url); \
os.makedirs('/app/models', exist_ok=True); \
dst = '/app/models/mask_rcnn_R_50_FPN_3x.pkl'; \
shutil.copy2(local_path, dst); \
print('Saved weights to', dst)"

# Code commun Raffinerie (serveur FastAPI générique)
RUN mkdir -p /app/services
COPY ./services/docker_api_server.py /app/services/docker_api_server.py
COPY ./services/mapping.py /app/services/mapping.py

# Scripts spécifiques object_detection
COPY ./services/visual_services/object_detection/run_object_detection.py /app/run_object_detection.py
COPY ./services/visual_services/object_detection/api_server.py /app/api_server.py

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
