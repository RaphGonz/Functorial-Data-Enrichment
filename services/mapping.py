SERVICE_MAPPING = {
    # -----------------------------
    # VISUAL
    # -----------------------------
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
        "files": ["skeleton.png"],
        "json_loader": "pose",
        "enriched_path": ["visual", "pose_detection"],
        "method": None
    },

    "object_detection": {
        "files": ["objects.json"],
        "json_loader": "json",
        "enriched_path": ["visual", "object_detection"],
        "method": None
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
    "language": {
        "files": ["lang.txt"],
        "json_loader": "text",
        "enriched_path": ["semantic", "language"],
        "method": None
    },

    "translation": {
        "files": ["translation.json"],
        "json_loader": "json",
        "enriched_path": ["semantic", "translation"],
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

    "sentiment_score": {
        "files": ["sentiment.json"],
        "json_loader": "json",
        "enriched_path": ["semantic", "sentiment_score"],
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
