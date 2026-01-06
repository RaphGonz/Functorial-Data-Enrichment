FROM raffinerie-gpu-base

WORKDIR /app/depth

# Cloner Depth-Anything-V2
RUN git clone https://github.com/DepthAnything/Depth-Anything-V2.git repo

WORKDIR /app/depth/repo

# Install requirements du repo DepthAnything
RUN python3 -m pip install --no-cache-dir -r requirements.txt

#fais un directory checkpoints pour y mettre le model
RUN mkdir -p checkpoints

# Copier l'API spécifique depth
# (docker_api_server.py et mapping.py sont déjà dans /app/services via l'image de base)
COPY ./services/visual_services/depth/api_server.py /app/depth/repo/api_server.py

EXPOSE 8080
WORKDIR /app/depth/repo
CMD ["python3", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
