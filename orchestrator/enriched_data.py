from pydantic import BaseModel
from typing import List, Optional, Dict, Literal


# --- SEMANTIC ---------------------------------------------------------------

class Translation(BaseModel):
    available: Optional[bool]
    languages: Optional[List[str]]

class KeyEntities(BaseModel):
    persons: Optional[List[str]]
    objects: Optional[List[str]]
    locations: Optional[List[str]]

class Semantic(BaseModel):
    language: Optional[str]
    translation: Optional[Translation]
    summary: Optional[str]
    topic_classification: Optional[List[str]]
    key_entities: Optional[KeyEntities]
    emotions: Optional[List[str]]
    sentiment_score: Optional[List[float]]
    keywords: Optional[List[str]]
    narrative_type: Optional[str]
    style: Optional[str]


# --- VISUAL -----------------------------------------------------------------

class DepthNormalMap(BaseModel):
    path: Optional[str]
    confidence: Optional[float]
    method: Optional[str]

class PoseDetection(BaseModel):
    skeleton_path: Optional[str]
    detected: Optional[bool]

class SizeEstimation(BaseModel):
    relative_scale: Optional[float]
    absolute_size_m: Optional[float]
    confidence: Optional[float]

class MaterialEstimation(BaseModel): #en rajouter ça me parait pas assez
    metal: Optional[float]
    peinture: Optional[float]
    verre: Optional[float]
    tissu: Optional[float]
    peau: Optional[float]
    plastique: Optional[float]

class ObjectDetection(BaseModel):
    id: str
    label: str
    bbox: List[int]
    size_estimation: Optional[SizeEstimation]
    material_estimation: Optional[MaterialEstimation]

class Focal(BaseModel):
    estimated_mm: Optional[float]
    confidence: Optional[float]
    method: Optional[str]

class VanishingPoint(BaseModel):
    x: float
    y: float
    confidence: float

class Light(BaseModel):
    id: str
    position: List[float]
    orientation: List[float]
    color: List[int]
    intensity: float
    confidence: float
    method: str

class Visual(BaseModel):
    depth_map: Optional[DepthNormalMap]
    normal_map: Optional[DepthNormalMap]
    pose_detection: Optional[PoseDetection]
    object_detection: Optional[List[ObjectDetection]]
    focal: Optional[Focal]
    vanishing_points: Optional[List[VanishingPoint]]
    lights: Optional[List[Light]]
    dominant_colors: Optional[List[str]]
    pointcloud_3d: Optional[DepthNormalMap]


# --- LINKS ------------------------------------------------------------------

class Links(BaseModel):
    related_texts: Optional[List[str]]
    related_images: Optional[List[str]]
    generated_from: Optional[str]


# --- METADATA ---------------------------------------------------------------

class Metadata(BaseModel):
    creation_date: Optional[str]
    author: Optional[str]
    confidence_scores: Optional[Dict[str, float]]
    processing_history: Optional[List[Dict[str, str]]]


# --- ROOT MODEL -------------------------------------------------------------

class EnrichedData(BaseModel):
    id: str
    type: Literal["image", "text", "mixed", "image / text"]
    source_file: str

    semantic: Optional[Semantic]
    visual: Optional[Visual]
    links: Optional[Links]
    metadata: Optional[Metadata]
