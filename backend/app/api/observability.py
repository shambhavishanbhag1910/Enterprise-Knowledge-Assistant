from fastapi import APIRouter

from backend.app.observability.langfuse_client import get_langfuse_client

router = APIRouter(prefix="/api", tags=["Observability"])


@router.get("/observability/status")
def observability_status():
    """
    Check Langfuse configuration and authentication.
    """
    client = get_langfuse_client()

    if not client:
        return {
            "langfuse_configured": False,
            "authenticated": False,
            "message": "Langfuse credentials are not configured.",
        }

    try:
        authenticated = client.auth_check()

        return {
            "langfuse_configured": True,
            "authenticated": authenticated,
            "message": "Langfuse is configured." if authenticated else "Langfuse authentication failed.",
        }

    except Exception as error:
        return {
            "langfuse_configured": True,
            "authenticated": False,
            "message": str(error),
        }