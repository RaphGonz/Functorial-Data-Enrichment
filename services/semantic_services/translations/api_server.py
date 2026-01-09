# services/semantic_services/translations/api_server.py

import os
from services.docker_api_server import create_service_app


def build_translations_command(req) -> list[str]:
    """
    - source: req.input_path
    - sortie: req.outdir/translations.json
    - args: --languages (comma-separated) taken from req.extra["languages"]
    """
    input_path = req.input_path
    outdir = req.outdir

    os.makedirs(outdir, exist_ok=True)

    extra = req.extra or {}
    languages = extra.get("languages")

    if isinstance(languages, list):
        languages_arg = ",".join([str(x).strip() for x in languages if str(x).strip()])
    elif isinstance(languages, str):
        languages_arg = ",".join([x.strip() for x in languages.split(",") if x.strip()])
    else:
        # default set (change if you want)
        languages_arg = "english,french,spanish,german,italian,japanese"

    cmd = [
        "python3",
        "/app/semantic_services/translations/run.py",
        "--input",
        input_path,
        "--output",
        outdir,
        "--languages",
        languages_arg,
    ]

    return cmd


app = create_service_app("translations", build_translations_command)
