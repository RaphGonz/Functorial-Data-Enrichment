FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# -------------------------------------------------------------
# System deps
# -------------------------------------------------------------
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    git \
    wget \
    libgl1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------
# Pip upgrade (CRITICAL)
# -------------------------------------------------------------
RUN pip install --upgrade pip

# -------------------------------------------------------------
# Global pip constraints (CRITICAL)
# -------------------------------------------------------------
RUN echo "numpy<2" > /tmp/constraints.txt

# -------------------------------------------------------------
# NumPy pinned FIRST (CRITICAL)
# -------------------------------------------------------------
RUN pip install --no-cache-dir \
    --constraint /tmp/constraints.txt \
    "numpy<2"

# -------------------------------------------------------------
# Torch 2.1.2 + cu118 (COMPATIBLE basicsr / Real-ESRGAN)
# -------------------------------------------------------------
RUN pip install --no-cache-dir \
    --constraint /tmp/constraints.txt \
    torch==2.1.2+cu118 \
    torchvision==0.16.2+cu118 \
    --index-url https://download.pytorch.org/whl/cu118

# -------------------------------------------------------------
# Diffusers + HF
# -------------------------------------------------------------
RUN pip install --no-cache-dir \
    --constraint /tmp/constraints.txt \
    diffusers==0.30.2 \
    "transformers<4.37" \
    accelerate \
    huggingface_hub \
    safetensors \
    pillow \
    opencv-python \
    einops \
    timm \
    fastapi \
    "uvicorn[standard]"

WORKDIR /app

# ------------------------------
# SD-1.5-PRUNED single-file
# ------------------------------
RUN mkdir -p /app/models/sd15

# -------------------------------------------------------------
# Real-ESRGAN (INSTALL AS PACKAGE)
# -------------------------------------------------------------
RUN pip install --no-cache-dir \
    --constraint /tmp/constraints.txt \
    realesrgan

# -------------------------------------------------------------
# Copy service code
# -------------------------------------------------------------
RUN mkdir -p /app/services

COPY ./services/docker_api_server.py /app/services/docker_api_server.py
COPY ./services/mapping.py          /app/services/mapping.py

COPY ./services/visual_services/image_generation/run_image.py  /app/run_image.py
COPY ./services/visual_services/image_generation/api_server.py /app/api_server.py

# -------------------------------------------------------------
# PYTHONPATH (FIXED)
# -------------------------------------------------------------
ENV PYTHONPATH=/app

# -------------------------------------------------------------
# Entry point
# -------------------------------------------------------------
EXPOSE 8080
CMD ["python3", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
