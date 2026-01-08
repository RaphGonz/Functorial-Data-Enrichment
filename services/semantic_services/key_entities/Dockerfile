FROM raffinerie-semantic-base

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only this enrichment (code + prompt files)
COPY ./services/semantic_services/key_entities/ /app/semantic_services/key_entities/

WORKDIR /app/semantic_services/key_entities

EXPOSE 8080
CMD ["python3", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]