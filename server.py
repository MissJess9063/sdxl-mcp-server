
import logging
import os

import requests
import uvicorn
from mcp.server.fastmcp import Context, FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Read secrets from environment variables instead of hardcoding them.
# Set these in your hosting platform's environment/config (e.g. Render's
# "Environment" tab) — never commit real keys to the repo.
STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY", "")
MCP_SECRET_KEY = os.environ.get("MCP_SECRET_KEY", "")

PORT = int(os.environ.get("PORT", 8000))

# FastMCP handles the full MCP protocol for you: the JSON-RPC 2.0 envelope,
# the initialize/initialized handshake, protocol version negotiation, and
# tools/list & tools/call dispatch. You just declare tools below.
mcp = FastMCP("GritDesigns", host="0.0.0.0", port=PORT)


@mcp.tool()
def generate_image(ctx: Context, prompt: str) -> dict:
    """Generate an image from a text prompt using Stability AI's SDXL model.

    Args:
        prompt: The text prompt describing the image to generate.
    """
    if not STABILITY_API_KEY:
        raise RuntimeError(
            "STABILITY_API_KEY is not set. Configure it as an environment "
            "variable on your hosting platform."
        )

    # Pull the underlying HTTP request off the injected MCP Context to log
    # the headers Octonous sent along with this specific tool call.
    try:
        http_request = ctx.request_context.request
        headers = dict(http_request.headers) if http_request else {}
        logger.info(f"generate_image called | headers={headers}")
    except Exception as exc:
        logger.warning(f"Could not read request headers: {exc}")

    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Accept": "application/json",
        },
        files={"none": ""},
        data={"prompt": prompt, "output_format": "png"},
    )
    response.raise_for_status()
    data = response.json()

    # Stability's v2beta image endpoint returns a base64-encoded PNG in the
    # "image" field (not "image_url") when Accept: application/json is used.
    image_b64 = data.get("image")
    if not image_b64:
        raise RuntimeError(
            f"Stability API response did not include image data: {data}"
        )

    return {"image_url": f"data:image/png;base64,{image_b64}", "prompt": prompt}


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every HTTP request/response hitting the MCP endpoint, including
    the initialize handshake itself — not just tool calls — so Render's
    logs show exactly what Octonous is sending, with clean timestamps.
    """

    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        logger.info(
            f"--> {request.method} {request.url.path} "
            f"headers={dict(request.headers)} body={body[:2000]!r}"
        )
        response = await call_next(request)
        logger.info(f"<-- {response.status_code} for {request.url.path}")
        return response


if __name__ == "__main__":
    # Streamable HTTP transport exposes a single MCP endpoint (default: /mcp)
    # that implements the full JSON-RPC handshake Octonous expects. We wrap
    # the underlying ASGI app with logging middleware so every request,
    # including the handshake, shows up in Render's logs.
    app = mcp.streamable_http_app()
    app.add_middleware(RequestLoggingMiddleware)
    uvicorn.run(app, host="0.0.0.0", port=PORT)
