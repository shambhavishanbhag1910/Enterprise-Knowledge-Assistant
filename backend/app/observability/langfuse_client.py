import os

from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()


def get_langfuse_client():
    """
    Return Langfuse client if credentials are configured.
    """
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    base_url = os.getenv("LANGFUSE_BASE_URL")

    if not public_key or not secret_key or not base_url:
        return None

    return get_client()


def flush_langfuse():
    """
    Flush pending Langfuse events.
    Useful for scripts and local testing.
    """
    client = get_langfuse_client()

    if client:
        client.flush()