from pydantic import BaseModel
from typing import List, Optional, Dict


# --- SEMANTIC ---------------------------------------------------------------

class TranslationItem(BaseModel):
    language: str          # ex: "en", "fr", "de"
    text: str              # texte traduit dans cette langue

class KeyEntities(BaseModel):
    persons: Optional[List[str]]
    objects: Optional[List[str]]
    locations: Optional[List[str]]

class Semantic(BaseModel):
    description: Optional[str] = None
    language: Optional[str] = None
    translations: Optional[List[TranslationItem]] = None
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
    path: Optional[str]
    confidence: Optional[float]
    method: Optional[str]

class Segmentation(BaseModel):
    mask_path: Optional[str]
    cropped_image_path: Optional[str]
    confidence: Optional[float]
    method: Optional[str]

class Mesh3D(BaseModel):
    path: str                # ex: "path/to/obj_001.obj"
    method: str              # ex: "one2345"
    confidence: Optional[float] = None  # optionnel, peut rester None

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
    segmentation: Optional[Segmentation] = None
    mesh_3d: Optional[Mesh3D] = None
    size_estimation: Optional[SizeEstimation] = None
    material_estimation: Optional[MaterialEstimation] = None

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
    base_image: Optional[str] = None
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
    source_file: str
    # NEW: texte brut fourni par l’utilisateur (manifest.json ou .txt)
    text: Optional[str] = None

    semantic: Optional[Semantic] = None
    visual: Optional[Visual] = None
    links: Optional[Links] = None
    metadata: Optional[Metadata] = None
