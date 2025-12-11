# docker/Dockerfile
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances système communes
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip \
    git wget \
    ninja-build \
    libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Pip à jour
RUN python3 -m pip install --upgrade pip

# PyTorch + torchvision compatibles CUDA 12.1
RUN python3 -m pip install --no-cache-dir \
    "torch==2.3.0+cu121" \
    "torchvision==0.18.0+cu121" \
    --index-url https://download.pytorch.org/whl/cu121

# FastAPI + Uvicorn communs aux services
RUN python3 -m pip install --no-cache-dir fastapi uvicorn

# Code commun Raffinerie
COPY ./services/docker_api_server.py /app/services/docker_api_server.py
COPY ./services/mapping.py /app/services/mapping.py

ENV PYTHONPATH=/app
