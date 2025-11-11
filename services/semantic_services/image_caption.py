from services.base_service import BaseService

class ImageCaptionService(BaseService):
    name = "image_caption"

    def run(self, image_path: str):
        # Simulation. Dans la réalité, ici tu appelleras ton repo Docker
        # ou un script Python externe.
        return {"caption": f"L'image {image_path} est une photo de chat"}