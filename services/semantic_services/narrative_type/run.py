# services/semantic_services/description/run.py

import argparse
import json
from pathlib import Path

from ollama import chat
from pydantic import BaseModel


class NarrativeTypeOutput(BaseModel):
    narrative_type: str


PROMPT_PATH = Path(__file__).parent / "prompt.txt"
MODEL = "llama3.1:8b" # à ajuster selon le modèle disponible


def main(input_path: str, output_dir: str) -> None:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    text = input_path.read_text(encoding="utf-8")
    prompt = PROMPT_PATH.read_text(encoding="utf-8")

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt.replace("{{TEXT}}", text),
            }
        ],
        format=NarrativeTypeOutput.model_json_schema(),
    )

    narrative_type = NarrativeTypeOutput.model_validate_json(response.message.content)

    out_file = output_dir / "narrative_type.json"
    out_file.write_text(
        narrative_type.model_dump_json(indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Language detected")
    parser.add_argument("--input", required=True, help="Path to input text file")
    parser.add_argument("--output", required=True, help="Output directory")

    args = parser.parse_args()
    main(args.input, args.output)
