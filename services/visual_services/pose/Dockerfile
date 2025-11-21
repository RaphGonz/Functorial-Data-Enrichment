FROM raffinerie-gpu-base

WORKDIR /app/pose

# Dépendances Python spécifiques MMPose
RUN python3 -m pip install --no-cache-dir cython xtcocotools openmim

# Installer chumpy SANS build isolation pour éviter le bug "No module named 'pip'"
RUN python3 -m pip install --no-cache-dir --no-build-isolation "chumpy==0.70"

# mmengine / mmcv / mmdet via mim (a besoin de torch déjà présent dans l'image de base)
RUN mim install mmengine "mmcv>=2.0.0" "mmdet>=3.1.0"

# Cloner MMPose
RUN git clone https://github.com/open-mmlab/mmpose.git repo

WORKDIR /app/pose/repo

# Installer MMPose (build + editable)
RUN python3 -m pip install --no-cache-dir -r requirements/build.txt && \
    python3 -m pip install --no-cache-dir -e .

# Checkpoint HRNet
RUN mkdir -p checkpoints && \
    wget -O checkpoints/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth \
    "https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth"

# API spécifique pose
COPY ./services/visual_services/pose/api_server.py /app/pose/repo/api_server.py

EXPOSE 8080
ENV PYTHONPATH="/app/pose/repo:/app"

CMD ["python3", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
