import requests
import aiohttp
from services.base_service import BaseService

#transforms a service call into an external HTTP request to the service URL

class ExternalService(BaseService):
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def run(self, input_path: str, outdir: str = "output", extra: dict | None = None):
        payload = {
            "input_path": input_path,
            "outdir": outdir,
            "extra": extra,
        }
        r = requests.post(self.url, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()
    
    async def arun(self, input_path: str, outdir: str = "output", extra: dict | None = None):
        payload = {
            "input_path": input_path,
            "outdir": outdir,
            "extra": extra,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload, timeout=300) as r:
                r.raise_for_status()
                return await r.json()