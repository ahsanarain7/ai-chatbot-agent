# utils/openai_chat.py
import os
from openai import OpenAI

def get_ai_response(history, file_context=""):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not api_key.startswith("sk-"):
        raise ValueError(
            "OPENAI_API_KEY not set or invalid. Put a valid key in your .env or Streamlit secrets."
        )

    client = OpenAI(api_key=api_key)


    messages = []
    if file_context:
        messages.append({"role": "system", "content": file_context})
    for m in history:
        messages.append({"role": m["role"], "content": m["content"]})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
    )
    return completion.choices[0].message.content
