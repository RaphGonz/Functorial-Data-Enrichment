# MMPose - Dockerfile basé sur l'officiel + endpoint FastAPI

ARG PYTORCH="1.8.1"
ARG CUDA="10.2"
ARG CUDNN="7"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

ENV DEBIAN_FRONTEND=noninteractive
ENV TORCH_CUDA_ARCH_LIST="6.0 6.1 7.0+PTX"
ENV TORCH_NVCC_FLAGS="-Xfatbin -compress-all"
ENV CMAKE_PREFIX_PATH="$(dirname $(which conda))/../"

WORKDIR /app

# Fix GPG keys + dépendances système
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub && \
    apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub && \
    apt-get update && apt-get install -y \
        git ninja-build \
        libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-glx \
        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# xtcocotools + MMEngine + MMCV (comme Dockerfile officiel)
# xtcocotools + MMEngine + MMCV + MMDetection
RUN pip install --no-cache-dir cython xtcocotools openmim && \
    mim install mmengine "mmcv>=2.0.0" "mmdet>=3.1.0"

# Cloner MMPose
RUN conda clean --all
RUN git clone https://github.com/open-mmlab/mmpose.git /mmpose
WORKDIR /mmpose
RUN git checkout main
ENV FORCE_CUDA="1"

# Installer MMPose (comme Dockerfile officiel)
RUN pip install --no-cache-dir -r requirements/build.txt && \
    pip install --no-cache-dir -e .

# Checkpoint HRNet pour la démo top-down
RUN mkdir -p checkpoints && \
    wget -O checkpoints/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth \
    "https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth"

# FastAPI + Uvicorn
RUN pip install --no-cache-dir fastapi uvicorn

# Wrappers API
COPY ./services/docker_api_server.py /mmpose/docker_api_server.py
COPY ./services/mapping.py /mmpose/services/mapping.py
COPY ./services/visual_services/pose/api_server.py /mmpose/api_server.py

EXPOSE 8080
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/mmpose"

CMD ["python", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
