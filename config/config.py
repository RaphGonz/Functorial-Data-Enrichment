import yaml

with open("config/services.yml") as f:
    data = yaml.safe_load(f)

SERVICE_CONFIG = data["services"]
