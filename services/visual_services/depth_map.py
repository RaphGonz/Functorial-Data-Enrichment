from services.base_service import BaseService

class DepthMapService(BaseService):
    name = "depth_map"

    def run(self, image_path: str):
        # Simulation. Dans la réalité, ici tu appelleras ton repo Docker
        # ou un script Python externe.
        return {"depth_map": f"depth map pour{image_path}"}