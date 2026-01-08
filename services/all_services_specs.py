from services.service_spec import ServiceSpec
#list of all service specifications used by the orchestrator
# different from the service registry which gives the actual service instances

service_specs = [
    
    ServiceSpec(
        name="depth",
        fills=["visual.depth_map"],
        needs_image=True
    ),

    ServiceSpec(
        name="pose",
        fills=["visual.pose_detection"],
        needs_image=True
    ),

    ServiceSpec(
        name="pointcloud",
        fills=["visual.pointcloud_3d"],
        needs_image=True,
    ),

    ServiceSpec(
        name="object_detection",
        fills=["visual.object_detection"],
        needs_image=True,
    ),
    ServiceSpec(
        name="mesh_3d",
        fills=["visual.object_detection.mesh_3d"],
        needs_fields=["visual.object_detection"]
    ),
    ServiceSpec(
        name="image_generation",
        fills=["visual.base_image"],
        needs_fields=["semantic.summary"] #On ne génère pas une image à partir du texte brut ça n'a aucun sens
    ),
    ServiceSpec(
        name="description",
        fills=["semantic.base_text"], #ce service sert à générer une description textuelle de l'image
        needs_image=True
    ),
    ServiceSpec(
        name="emotions",
        fills=["semantic.emotions"],
        needs_text=True
    ),
    ServiceSpec(
        name="key_entities",
        fills=["semantic.key_entities"],
        needs_text=True
    ),
    ServiceSpec(
        name="keywords",
        fills=["semantic.keywords"],
        needs_text=True
    ),
    ServiceSpec(
        name="language",
        fills=["semantic.language"],
        needs_text=True
    ),
    ServiceSpec(
        name="narrative_type",
        fills=["semantic.narrative_type"],
        needs_text=True
    ),
    ServiceSpec(
        name="style",
        fills=["semantic.style"],
        needs_text=True
    ),
    ServiceSpec(
        name="summary",
        fills=["semantic.summary"],
        needs_text=True
    ),
    ServiceSpec(
        name="topic_classification",
        fills=["semantic.topic_classification"],
        needs_text=True
    ),
    ServiceSpec(
        name="translations",
        fills=["semantic.translations"],
        needs_text=True
    )

]