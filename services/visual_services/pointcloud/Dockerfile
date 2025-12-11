# Image de service UniK3D, basée sur l’image GPU commune

#C'est un dockerfile brut et non pas dérivé et léger comme les autres
# la raison est qu'on risque d'avoir des conflits de dépendances
# et que Unik 3D est trop capricieux avec son environnement
#ça build et ça fontionne correctement comme ça

FROM raffinerie-gpu-base:latest

WORKDIR /app

# Cloner le repo UniK3D depuis GitHub
RUN git clone https://github.com/lpiccinelli-eth/UniK3D.git /app/pointcloud

WORKDIR /app/pointcloud

# Installer les dépendances sans réinstaller torch / torchvision déjà présentes dans l'image de base
RUN python3 -m pip install --no-cache-dir -r requirements.txt 

# Ajouter UniK3D au PYTHONPATH, car ce repo n’est PAS un package Python installable
#permet d’importer des modules depuis /app/pointcloud
#pour l'étape suivante
ENV PYTHONPATH="/app/pointcloud:${PYTHONPATH}"

COPY ./services/visual_services/pointcloud/api_server.py /app/pointcloud/api_server.py

EXPOSE 8080

CMD ["python3", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]

