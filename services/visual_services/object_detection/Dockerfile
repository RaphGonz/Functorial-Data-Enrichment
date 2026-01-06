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

# Code commun Raffinerie (serveur FastAPI générique)
RUN mkdir -p /app/services
COPY ./services/docker_api_server.py /app/services/docker_api_server.py
COPY ./services/mapping.py /app/services/mapping.py

# Scripts spécifiques object_detection
COPY ./services/visual_services/object_detection/run_object_detection.py /app/run_object_detection.py
COPY ./services/visual_services/object_detection/api_server.py /app/api_server.py

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
