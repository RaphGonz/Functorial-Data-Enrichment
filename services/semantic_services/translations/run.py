# services/semantic_services/description/run.py

import argparse
import json
from pathlib import Path

from ollama import chat
from pydantic import BaseModel


class TranslationPair(BaseModel):
    language: str  # e.g. "english", "french" or "japanese"
    translation: str


class TranslationsOutput(BaseModel):
    translations: list[TranslationPair]


PROMPT_PATH = Path(__file__).parent / "prompt.txt"
MODEL = "llama3.1:8b" # à ajuster selon le modèle disponible


def main(input_path: str, output_dir: str, languages: list[str]) -> None:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    text = input_path.read_text(encoding="utf-8")
    prompt = PROMPT_PATH.read_text(encoding="utf-8")

    # Inject languages explicitly into the prompt
    prompt_filled = (
        prompt
        .replace("{{TEXT}}", text)
        .replace("{{LANGUAGES}}", ", ".join(languages))
    )

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt_filled,
            }
        ],
        format=TranslationsOutput.model_json_schema(),
    )

    translations = TranslationsOutput.model_validate_json(response.message.content)

    out_file = output_dir / "translations.json"
    out_file.write_text(
        translations.model_dump_json(indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translations")
    parser.add_argument("--input", required=True, help="Path to input text file")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument(
        "--languages",
        required=True,
        help="Comma-separated list of target languages (e.g. english,french,japanese)",
    )

    args = parser.parse_args()
    languages = [l.strip() for l in args.languages.split(",") if l.strip()]

    main(args.input, args.output, languages)
