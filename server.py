import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

import os
import requests
from mcp.server.fastmcp import FastMCP

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
logger.info(f"Incoming headers: {dict(request.headers)}")
def generate_image(prompt: str) -> dict:
    """Generate an image from a text prompt using Stability AI's SDXL model.

    Args:
        prompt: The text prompt describing the image to generate.
    """
    if not STABILITY_API_KEY:
        raise RuntimeError(
            "STABILITY_API_KEY is not set. Configure it as an environment "
            "variable on your hosting platform."
        )

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

    return {"image_url": data.get("image_url"), "prompt": prompt}


if __name__ == "__main__":
    # Streamable HTTP transport exposes a single MCP endpoint (default: /mcp)
    # that implements the full JSON-RPC handshake Octonous expects.
    mcp.run(transport="streamable-http")
