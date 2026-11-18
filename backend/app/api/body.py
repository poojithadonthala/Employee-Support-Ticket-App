from fastapi import HTTPException, Request


async def json_object_body(request: Request) -> dict:
    """Read a JSON object after authentication and ticket authorization."""
    try:
        payload = await request.json()
    except Exception as exc:  # noqa: BLE001 - invalid JSON is a client error
        raise HTTPException(status_code=400, detail="Request body must be valid JSON.") from exc
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Request body must be a JSON object.")
    return payload
