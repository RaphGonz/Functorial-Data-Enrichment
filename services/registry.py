from services.external_service import ExternalService
from config.config import SERVICE_CONFIG

service_registry = {
    name: ExternalService(name,conf["url"]) for name,conf in SERVICE_CONFIG.items()
}

def get_service(name: str):
    service = service_registry.get(name)
    if service and service.enabled:
        return service
    raise ValueError(f"Service '{name}' non trouvé ou désactivé")
