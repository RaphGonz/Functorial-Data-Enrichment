import os
import yaml
from string import Template
from services.external_service import ExternalService

CONFIG_PATH = "./config/services.yml"


def load_service_config(path=CONFIG_PATH):
    """Charge services.yml et remplace les variables d'environnement (${VAR})."""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
        substituted = Template(raw).substitute(os.environ)
    return yaml.safe_load(substituted)


SERVICE_CONFIG = load_service_config()

service_registry = {
    name: ExternalService(name, conf["url"])
    for name, conf in SERVICE_CONFIG.get("services", {}).items()
}


def get_service(name: str):
    service = service_registry.get(name)
    if service:
        return service
    raise ValueError(f"Service '{name}' non trouvé ou désactivé")