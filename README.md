# SDXL MCP Server

A lightweight FastAPI-based MCP (Model Context Protocol) server that connects Octonous to Stability AI’s SDXL image generation API.  
This server exposes a single endpoint that accepts a text prompt and returns a generated image URL.

---

## 🚀 Features

- FastAPI server with a clean `/mcp/generate-image` endpoint  
- Authorization header validation using a custom MCP secret key  
- SDXL image generation via Stability AI API  
- JSON response containing the generated image URL  
- Ready for deployment on Render, Railway, or any public hosting platform  

---

## 📦 Requirements

Create a `requirements.txt` file containing:
fastapi
uvicorn
requests


---

## 🧩 Server Structure
server.py
requirements.txt
README.md


---

## 🔐 Environment Variables

Inside `server.py`, set:
STABILITY_API_KEY = "sk-Gyhxq4ipCuDDhcj1EiqVILp7SQ2Tgm1FnCYIbBQSCZnh70gS"
MCP_SECRET_KEY = "sdxl_secret_key_mj13"


These keys must match what you use in Octonous.

---

## 🌐 Endpoint

### POST `/mcp/generate-image`

**Body Parameters:**
- `prompt` — The text prompt used to generate the SDXL image.

**Headers:**
- `Authorization: Bearer <MCP_SECRET_KEY>`

**Response:**
{
"image_url": "<generated_image_url>",
"prompt": "<your_prompt>"
}


---

## 🖥️ Running Locally

Start the server with:
    uvicorn server:app --host 0.0.0.0 --port 8000


View API docs:
    http://localhost:8000/docs


---

## ☁️ Deploying on Render

**Build Command:**

pip install -r requirements.txt

**Start Command:**

uvicorn server:app --host 0.0.0.0 --port 10000


Render will give you a public URL like:
    https://your-app-name.onrender.com (your-app-name.onrender.com in Bing)


Use this URL in Octonous.

---

## 🎨 Example Prompt
romantic toxic rap aesthetic, neon pink and black, glossy finish


---

## ❤️ Author

Jessica (MissJess9063)  
Public MCP server for SDXL image generation.










