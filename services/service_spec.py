
from pydantic import BaseModel
from typing import List


class ServiceSpec(BaseModel):
    name: str
    fills: List[str]
    needs_image: bool = False
    needs_text: bool = False
    needs_json: bool = False
    needs_fields: List[str] = []
