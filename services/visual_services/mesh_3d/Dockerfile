FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# -------------------------------------------------------------
# 1. System dependencies
# -------------------------------------------------------------
RUN apt update && apt install -y \
    git \
    wget \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    cmake && \
    rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------
# 2. Working directory
# -------------------------------------------------------------
WORKDIR /app

# -------------------------------------------------------------
# 3. Clone TripoSR repo
# -------------------------------------------------------------
RUN git clone https://github.com/VAST-AI-Research/TripoSR.git /app
RUN rm -rf /app/examples /app/assets_demo || true

# -------------------------------------------------------------
# 4. CUDA environment
# -------------------------------------------------------------
ENV PATH="/usr/local/cuda-11.8/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda-11.8/lib64:${LD_LIBRARY_PATH}"
ENV CUDA_HOME=/usr/local/cuda

# -------------------------------------------------------------
# 5. Install PyTorch cu118
# -------------------------------------------------------------
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
        torch==2.0.1 \
        torchvision \
        torchaudio \
        --index-url https://download.pytorch.org/whl/cu118

# -------------------------------------------------------------
# 6. TripoSR dependencies
# -------------------------------------------------------------
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir onnxruntime

# torchmcubes recompilé proprement pour sm_75 (GTX 1660 Ti)
RUN pip uninstall -y torchmcubes || true && \
    TORCH_CUDA_ARCH_LIST="7.5" pip install --no-cache-dir \
        git+https://github.com/tatsy/torchmcubes.git

# -------------------------------------------------------------
# 7. Download pretrained model files directly from HuggingFace
# -------------------------------------------------------------
RUN mkdir -p /app/local_triposr_model

# config.yaml
RUN wget -O /app/local_triposr_model/config.yaml \
    https://huggingface.co/stabilityai/TripoSR/resolve/main/config.yaml

# model.ckpt
RUN wget -O /app/local_triposr_model/model.ckpt \
    https://huggingface.co/stabilityai/TripoSR/resolve/main/model.ckpt

# -------------------------------------------------------------
# 8. FastAPI + Uvicorn + pipeline services
# -------------------------------------------------------------
RUN python3 -m pip install --no-cache-dir fastapi "uvicorn[standard]"

RUN mkdir -p /app/services

COPY ./services/docker_api_server.py /app/services/docker_api_server.py
COPY ./services/mapping.py /app/services/mapping.py

COPY ./services/visual_services/mesh_3d/run_mesh_3d.py /app/run_mesh_3d.py
COPY ./services/visual_services/mesh_3d/api_server.py /app/api_server.py

ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["python3", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
