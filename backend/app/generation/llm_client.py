import os
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()


def generate_with_groq(prompt: str) -> str:
    """
    Generate answer using Groq API.
    """
    api_key = os.getenv("GROQ_API_KEY")
    base_url = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    if not api_key or api_key == "your_groq_api_key_here":
        return (
            "GROQ_API_KEY is not configured. "
            "Please add your Groq API key in the .env file."
        )

    url = f"{base_url}/chat/completions"

    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an enterprise document Q&A assistant. "
                    "Answer only from the provided context. "
                    "Do not invent facts. "
                    "Always mention sources."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.1,
        "top_p": 0.9,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120,
        )
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.HTTPError as error:
        return f"Groq API HTTP error: {error}. Response: {response.text}"

    except requests.exceptions.Timeout:
        return "Groq API request timed out. Please try again."

    except Exception as error:
        return f"Error while calling Groq API: {str(error)}"


def generate_llm_answer(prompt: str, provider: Optional[str] = None) -> str:
    """
    Main LLM generation function.
    Currently supports Groq.
    """
    selected_provider = provider or os.getenv("LLM_PROVIDER", "groq")

    if selected_provider.lower() == "groq":
        return generate_with_groq(prompt)

    return f"Unsupported LLM provider: {selected_provider}"