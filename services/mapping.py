#gives the mapping between service names and their file outputs and enriched data paths

SERVICE_MAPPING = {
    # -----------------------------
    # VISUAL
    # -----------------------------
    "base_image": {
        "files": ["base.png"],
        "json_loader": "binary_path",
        "enriched_path": ["visual", "base_image"],
        "method": "flux"
    },

    "depth": {
        "files": ["map.png"],
        "json_loader": "binary_path",
        "enriched_path": ["visual", "depth_map"],
        "method": "depth"
    },

    "normals": {
        "files": ["normal.png"],
        "json_loader": "binary_path",
        "enriched_path": ["visual", "normal_map"],
        "method": "normals"
    },

    "pose": {
        "files": ["pose.png"],
        "json_loader": "binary_path",
        "enriched_path": ["visual", "pose_detection"],
        "method": "pose"
    },

    "object_detection": {
        "files": ["objects.json"],
        "json_loader": "json",
        "enriched_path": ["visual", "object_detection"],
        "method": "detectron2"
    },

    "mesh_3d": {
        "files": ["objects.json"],
        "json_loader": "json",
        # On réécrit complètement visual.object_detection
        "enriched_path": ["visual", "object_detection"],
        "method": "tripoSR",
    },

    "focal": {
        "files": ["focal.json"],
        "json_loader": "json",
        "enriched_path": ["visual", "focal"],
        "method": "focal"
    },

    "vanishing_points": {
        "files": ["points.json"],
        "json_loader": "json",   # list of {x,y,confidence}
        "enriched_path": ["visual", "vanishing_points"],
        "method": None
    },

    "lights": {
        "files": ["lights.json"],
        "json_loader": "json",   # list of lights
        "enriched_path": ["visual", "lights"],
        "method": "lights"
    },

    "dominant_colors": {
        "files": ["colors.json"],
        "json_loader": "json",
        "enriched_path": ["visual", "dominant_colors"],
        "method": None
    },

    "pointcloud": {
        "files": ["cloud.ply"],
        "json_loader": "binary_path",
        "enriched_path": ["visual", "pointcloud_3d"],
        "method": "pointcloud"
    },

    # -----------------------------
    # SEMANTIC
    # -----------------------------
    "base_text": {
        "files": ["base_text.txt"],
        "json_loader": "text",
        "enriched_path": ["semantic", "base_text"],
        "method": "caption"
    },

    "language": {
        "files": ["language.txt"],
        "json_loader": "text",
        "enriched_path": ["semantic", "language"],
        "method": None
    },

    "translations": {
        "files": ["translations.json"],
        "json_loader": "json",
        "enriched_path": ["semantic", "translations"],
        "method": None
    },

    "summary": {
        "files": ["summary.txt"],
        "json_loader": "text",
        "enriched_path": ["semantic", "summary"],
        "method": None
    },

    "topic_classification": {
        "files": ["topics.json"],
        "json_loader": "json",
        "enriched_path": ["semantic", "topic_classification"],
        "method": None
    },

    "key_entities": {
        "files": ["entities.json"],
        "json_loader": "json",
        "enriched_path": ["semantic", "key_entities"],
        "method": None
    },

    "emotions": {
        "files": ["emotions.json"],
        "json_loader": "json",
        "enriched_path": ["semantic", "emotions"],
        "method": None
    },

    "keywords": {
        "files": ["keywords.json"],
        "json_loader": "json",
        "enriched_path": ["semantic", "keywords"],
        "method": None
    },

    "narrative_type": {
        "files": ["type.txt"],
        "json_loader": "text",
        "enriched_path": ["semantic", "narrative_type"],
        "method": None
    },

    "style": {
        "files": ["style.txt"],
        "json_loader": "text",
        "enriched_path": ["semantic", "style"],
        "method": None
    },

    # -----------------------------
    # LINKS
    # -----------------------------
    "related_texts": {
        "files": ["related.json"],
        "json_loader": "json",
        "enriched_path": ["links", "related_texts"],
        "method": None
    },

    "related_images": {
        "files": ["related.json"],
        "json_loader": "json",
        "enriched_path": ["links", "related_images"],
        "method": None
    },

    "generated_from": {
        "files": ["origin.txt"],
        "json_loader": "text",
        "enriched_path": ["links", "generated_from"],
        "method": None
    },

    # -----------------------------
    # METADATA
    # -----------------------------
    "creation_date": {
        "files": ["creation_date.txt"],
        "json_loader": "text",
        "enriched_path": ["metadata", "creation_date"],
        "method": None
    },

    "author": {
        "files": ["author.txt"],
        "json_loader": "text",
        "enriched_path": ["metadata", "author"],
        "method": None
    },

    "confidence_scores": {
        "files": ["confidence_scores.json"],
        "json_loader": "json",
        "enriched_path": ["metadata", "confidence_scores"],
        "method": None
    },

    "processing_history": {
        "files": ["history.json"],
        "json_loader": "json",
        "enriched_path": ["metadata", "processing_history"],
        "method": None
    },
}
