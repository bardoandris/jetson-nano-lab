from openai import OpenAI

client = OpenAI(
    base_url="http://${JETSON_HOST}:8080/v1",
    api_key="not-needed",  # vLLM / llama.cpp typically do not enforce a key
)

completion = client.chat.completions.create(
    model="my_model",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(completion.choices[0].message.content)