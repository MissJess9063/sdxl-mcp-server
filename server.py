from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

STABILITY_API_KEY = "sk-Gyhxq4ipCuDDhCj1EiqVILp7SQ2Tgm1FnCYIbBQSCZnh70gS"
MCP_SECRET_KEY = "sdxl_secret_key_mj13"

class ImageRequest(BaseModel):
    prompt: str

@app.post("/mcp/generate-image")
def generate_image(request: ImageRequest, authorization: str = Header(None)):
    if authorization != f"Bearer {MCP_SECRET_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    prompt = request.prompt

    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={"Authorization": f"Bearer {STABILITY_API_KEY}"},
        json={"prompt": prompt}
    )

    return {
        "image_url": response.json().get("image_url"),
        "prompt": prompt
    }
