# services/semantic_services/description/run.py

import argparse
from pathlib import Path

from ollama import chat
from pydantic import BaseModel


class DescriptionOutput(BaseModel):
    description: str


PROMPT_PATH = Path(__file__).parent / "prompt.txt"
MODEL = "janus-pro"  # example: use a vision-capable Ollama model you installed


def main(input_path: str, output_dir: str) -> None:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    prompt = PROMPT_PATH.read_text(encoding="utf-8")

    # Ollama vision expects an image path (or bytes) passed via "images"
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [str(input_path)],
            }
        ],
        format=DescriptionOutput.model_json_schema(),
    )

    description = DescriptionOutput.model_validate_json(response.message.content)

    out_file = output_dir / "description.json"
    out_file.write_text(description.model_dump_json(indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image description semantic enrichment")
    parser.add_argument("--input", required=True, help="Path to input image file")
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()
    main(args.input, args.output)
