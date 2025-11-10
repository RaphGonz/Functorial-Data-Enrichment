from services.visual_services.image_caption import ImageCaptionService
from services.visual_services.depth_map import DepthMapService

service_registry = {
    s.name: s for s in [
        ImageCaptionService(),
        DepthMapService(),
    ]
}

def get_service(name: str):
    service = service_registry.get(name)
    if service and service.enabled:
        return service
    raise ValueError(f"Service '{name}' non trouvé ou désactivé")
