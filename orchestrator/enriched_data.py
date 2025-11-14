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
    language: Optional[str] = None
    translation: Optional[Translation] = None
    summary: Optional[str] = None
    topic_classification: Optional[List[str]] = None
    key_entities: Optional[KeyEntities] = None
    emotions: Optional[List[str]] = None
    sentiment_score: Optional[List[float]] = None
    keywords: Optional[List[str]] = None
    narrative_type: Optional[str] = None
    style: Optional[str] = None


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
    depth_map: Optional[DepthNormalMap] = None
    normal_map: Optional[DepthNormalMap] = None
    pose_detection: Optional[PoseDetection] = None
    object_detection: Optional[List[ObjectDetection]] = None
    focal: Optional[Focal] = None
    vanishing_points: Optional[List[VanishingPoint]] = None
    lights: Optional[List[Light]] = None
    dominant_colors: Optional[List[str]] = None
    pointcloud_3d: Optional[DepthNormalMap] = None


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

    semantic: Optional[Semantic] = None
    visual: Optional[Visual] = None
    links: Optional[Links] = None
    metadata: Optional[Metadata] = None
