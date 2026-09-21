import argparse
import base64
import mimetypes
from pathlib import Path

from openai import OpenAI

MODEL_NAME = "unsloth/gemma-4-E2B-it-GGUF:Q4_K_S"


def detect_image_mime_type(image_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(image_path)
    allowed_types = {
        "image/png",
        "image/jpeg",
        "image/gif",
        "image/bmp",
        "image/webp",
    }
    if mime_type not in allowed_types:
        raise ValueError(f"Unsupported image type: {image_path}")
    return mime_type


def read_image_as_data_url(image_path: str) -> str:
    path = Path(image_path)
    mime_type = detect_image_mime_type(str(path))
    with path.open("rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ask a local Gemma model how many apples are in an image.")
    parser.add_argument("image", help="Path to the image file to analyze")
    return parser.parse_args()


args = parse_args()
image_data_url = read_image_as_data_url(args.image)

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="not-needed",  # llama.cpp / OpenAI-compatible servers often ignore this
)

completion = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Given the image, how many apples are present in the image? "
                        "Answer the question with only a number (eg. 1, 10, 0)."
                    ),
                },
                {
                    "type": "image_url",
                    "image_url": {"url": image_data_url},
                },
            ],
        }
    ],
    temperature=0.2,
    max_tokens=10,
)

print(completion.choices[0].message.content)