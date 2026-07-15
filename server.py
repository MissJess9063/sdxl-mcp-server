from fastapi import FastAPI, Header, HTTPException
import requests

app = FastAPI()

# === CONFIG ===
STABILITY_API_KEY = "sk-Gyhxq4ipCuDDhCj1EiqVILp7SQ2Tgm1FnCYIbBQSCZnh70gS"
MCP_SECRET_KEY = "sdxl_secret_key_mj13" # Octonous will send this

STABILITY_API_URL = "https://api.stability.ai/v2beta/stable-image/generate/sdxl"


@app.post("/mcp/generate-image")
def generate_image(prompt: str, authorization: str = Header(None)):
    # 1. Check Authorization from Octonous
    expected_header = f"Bearer {MCP_SECRET_KEY}"
    if authorization != expected_header:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 2. Call SDXL via Stability API
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
    }

    data = {
        "prompt": prompt,
        "output_format": "png",
    }

    response = requests.post(STABILITY_API_URL, headers=headers, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"SDXL error: {response.text}")

    result = response.json()

    image_url = result.get("image_url", None)

    if not image_url:
        raise HTTPException(status_code=500, detail="No image_url in SDXL response")

    return {
        "image_url": image_url,
        "prompt": prompt,
    }