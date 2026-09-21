from openai import OpenAI

MODEL_NAME = "unsloth/gemma-4-E2B-it-GGUF:Q4_K_S"

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="not-needed",  # llama.cpp / OpenAI-compatible servers often ignore this
)

completion = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[{"role": "user", "content": "Hello!"}],
    temperature=0.7,
    max_tokens=128,
)

print(completion.choices[0].message.content)