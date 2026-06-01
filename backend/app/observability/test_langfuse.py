from backend.app.observability.langfuse_client import get_langfuse_client


if __name__ == "__main__":
    client = get_langfuse_client()

    if not client:
        print("Langfuse is not configured. Please check .env.")
    else:
        authenticated = client.auth_check()
        print(f"Langfuse authenticated: {authenticated}")