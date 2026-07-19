from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# 🔑 Replace these with your real keys
STABILITY_API_KEY = "sk-Gyhxq4ipCuDDhCj1EiqVILp7SQ2Tgm1FnCYIbBQSCZnh70gS"
MCP_SECRET_KEY = "sdxl_secret_key"

# ⭐ MCP Initialization Endpoint (GET + POST allowed)
@app.get("/initialize")
@app.post("/initialize")
def initialize():
    return {
        "protocolVersion": "2025-03-26",
        "capabilities": {
            "imageGeneration": True
        },
        "serverInfo": {
            "name": "SDXL MCP Server",
            "version": "1.0.0"
        }
    }

# ⭐ JSON Model for Image Generation
class ImageRequest(BaseModel):
    prompt: str

# ⭐ Image Generation Endpoint
@app.post("/mcp/generate-image")
def generate_image(request: ImageRequest, authorization: str = Header(None)):
    # Authorization check
    if authorization != f"Bearer {MCP_SECRET_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    prompt = request.prompt

    # Stability API request
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={"Authorization": f"Bearer {STABILITY_API_KEY}"},
        json={"prompt": prompt}
    )

    # Return the image URL + prompt
    return {
        "image_url": response.json().get("image_url"),
        "prompt": prompt
    }
