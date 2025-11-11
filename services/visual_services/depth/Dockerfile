# Depth-Anything-V2 Small - Dockerfile with FastAPI endpoint

FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# --- System dependencies ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip git wget && \
    rm -rf /var/lib/apt/lists/*

# --- Clone official repository ---
RUN git clone https://github.com/DepthAnything/Depth-Anything-V2.git /app/repo

WORKDIR /app/repo

# --- Install repo dependencies ---
RUN pip install --no-cache-dir -r requirements.txt

# --- Add FastAPI + Uvicorn for serving HTTP ---
RUN pip install fastapi uvicorn

# --- Download model weights (Small version) ---
RUN mkdir -p checkpoints && \
    wget -O checkpoints/depth_anything_v2_vits.pth \
    "https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_vits.pth?download=true"

# --- Copy the API wrapper ---
COPY ./api_server.py /app/repo/api_server.py

EXPOSE 8080
ENV PYTHONUNBUFFERED=1

# --- Launch the FastAPI server ---
CMD ["python3", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
