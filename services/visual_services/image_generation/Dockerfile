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

RUN pip install --upgrade pip

# -------------------------------------------------------------
# Torch 2.2.0 + cu118 (compatible Flux + CUDA 11.8)
# -------------------------------------------------------------
RUN pip install --no-cache-dir \
    torch==2.2.0+cu118 \
    torchvision==0.17.0+cu118 \
    --index-url https://download.pytorch.org/whl/cu118

# -------------------------------------------------------------
# Diffusers + HF (open models compatible)
# -------------------------------------------------------------
RUN pip install --no-cache-dir \
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
    
RUN pip install --no-cache-dir "numpy<2" --force-reinstall

WORKDIR /app

# ------------------------------
# SD-1.5-PRUNED single-file
# ------------------------------
RUN mkdir -p /models/sd15
        
# -------------------------------------------------------------
# SwinIR – clone repo + pretrained model
# -------------------------------------------------------------
RUN git clone https://github.com/JingyunLiang/SwinIR.git /app/SwinIR && \
    mkdir -p /models/swinir


# -------------------------------------------------------------
# Copy service code
# -------------------------------------------------------------
RUN mkdir -p /app/services

COPY ./services/docker_api_server.py /app/services/docker_api_server.py
COPY ./services/mapping.py          /app/services/mapping.py

COPY ./services/visual_services/image_generation/run_image.py  /app/run_image.py
COPY ./services/visual_services/image_generation/api_server.py /app/api_server.py

ENV PYTHONPATH=/app

# -------------------------------------------------------------
# Entry point
# -------------------------------------------------------------
EXPOSE 8080
CMD ["python3", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
