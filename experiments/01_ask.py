import ollama

response = ollama.chat(
    model="gemma4",
    messages=[
        {"role": "user", "content": "Explain the present perfect to a 12 year old in 3 sentences."}
    ],
)

print(response["message"]["content"])