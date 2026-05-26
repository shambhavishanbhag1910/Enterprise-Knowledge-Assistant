import os
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()


def generate_with_ollama(prompt: str) -> str:
    """
    Generate answer using a local Ollama model.
    """
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model_name = os.getenv("OLLAMA_MODEL", "gemma3:1b")

    url = f"{base_url}/api/generate"

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_p": 0.9,
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()

    except requests.exceptions.ConnectionError:
        return (
            "Ollama is not running. Please start the Ollama container and pull a model."
        )

    except requests.exceptions.Timeout:
        return (
            "Ollama request timed out. Try using a smaller model such as gemma3:1b."
        )

    except Exception as error:
        return f"Error while calling Ollama: {str(error)}"


def generate_llm_answer(prompt: str, provider: Optional[str] = None) -> str:
    """
    Main LLM generation function.
    Currently supports Ollama.
    Later we can add OpenAI, Azure OpenAI, Gemini, Anthropic, etc.
    """
    selected_provider = provider or os.getenv("LLM_PROVIDER", "ollama")

    if selected_provider == "ollama":
        return generate_with_ollama(prompt)

    return f"Unsupported LLM provider: {selected_provider}"