FROM raffinerie-semantic-base

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only this enrichment (code + prompt files)
COPY ./services/semantic_services/translations/ /app/semantic_services/translations/

WORKDIR /app/semantic_services/translations

EXPOSE 8080
CMD ["python3", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]