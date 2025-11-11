import requests
from services.base_service import BaseService

class ExternalService(BaseService):
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def run(self, image_path: str):
        
        payload = {"image_path": image_path}
        r = requests.post(self.url, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()
        
        #return {f"{self.name}": f"L'image {image_path} est une photo de chat"}