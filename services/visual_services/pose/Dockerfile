FROM raffinerie-gpu-base

WORKDIR /app/pose

# Pose estimation simple avec YOLOv8 pose
RUN python3 -m pip install --no-cache-dir "ultralytics==8.3.0" opencv-python pillow

# Copier l'API FastAPI + le script appelé par la commande
COPY ./services/visual_services/pose/api_server.py /app/pose/api_server.py
COPY ./services/visual_services/pose/pose_skeleton_only.py /app/pose/pose_skeleton_only.py

EXPOSE 8080
ENV PYTHONPATH="/app:/app/pose"

CMD ["python3", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
