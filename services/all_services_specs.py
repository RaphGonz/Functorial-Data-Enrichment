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
    )
]