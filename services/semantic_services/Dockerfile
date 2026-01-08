# Build a reusable base image for ALL semantic enrichments.
# No API, no EXPOSE, no CMD.
#name = semantic-gpu-base

FROM raffinerie-gpu-base

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Minimal deps for: FastAPI service + Ollama HTTP calls + strict JSON parsing/validation
RUN python3 -m pip install --no-cache-dir \
    "fastapi>=0.115,<1" \
    "uvicorn[standard]>=0.32,<1" \
    "pydantic>=2.7,<3" \
    "httpx>=0.27,<1" \
    "orjson>=3.10,<4" \
    "ollama"

# Optional: if you want shared helpers available to all enrichments at runtime
# Keep it minimal; this is still "no API".
# (docker_api_server.py and mapping.py already exist in /app/services from raffinerie-gpu-base)
COPY ./services/semantic_services/_shared /app/semantic_shared

ENV PYTHONPATH=/app