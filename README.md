# SDXL MCP Server

A real Model Context Protocol (MCP) server, built on the official `mcp` Python SDK, that connects Octonous to Stability AI's SDXL image generation API.

It exposes one MCP tool — `generate_image` — that Octonous can discover and call automatically once connected.

---

## 🚀 Features

- Built on the official MCP Python SDK (`FastMCP`), so the JSON-RPC 2.0 handshake, protocol version negotiation, and `tools/list` / `tools/call` dispatch are handled for you
- A single `generate_image` MCP tool backed by Stability AI's SDXL model
- Secrets read from environment variables — nothing hardcoded in source
- Ready for deployment on Render, Railway, or any public hosting platform

---

## 📦 Requirements

See `requirements.txt`:
```
mcp[cli]
requests
uvicorn
```

---

## 🧩 Server Structure
```
server.py
requirements.txt
README.md
```

---

## 🔐 Environment Variables

Set these on your hosting platform (never commit real values to the repo):

- `STABILITY_API_KEY` — your Stability AI API key
- `MCP_SECRET_KEY` — optional shared secret if you add your own auth layer
- `PORT` — port to listen on (defaults to 8000; Render usually injects this automatically)

> ⚠️ If you previously committed real keys to this repo, rotate them now — anything pushed to a public GitHub repo should be considered compromised.

---

## 🌐 MCP Endpoint

FastMCP's Streamable HTTP transport exposes a single MCP endpoint (default path: `/mcp`) that implements the full MCP handshake:

1. Octonous sends a JSON-RPC `initialize` request
2. The server replies with its protocol version, capabilities, and `serverInfo`
3. Octonous sends the `initialized` notification to complete the handshake
4. Octonous calls `tools/list` to discover `generate_image`, then `tools/call` to run it

Use this server's public URL + `/mcp` path when connecting it in Octonous.

---

## 🖥️ Running Locally

```
export STABILITY_API_KEY=your-key-here
python server.py
```

The server will start on `http://localhost:8000/mcp`.

---

## ☁️ Deploying on Render

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
python server.py
```

Set `STABILITY_API_KEY` (and any other secrets) under Render's Environment tab — do not hardcode them in `server.py`.

Render will give you a public URL like:
```
https://your-app-name.onrender.com
```

Use `https://your-app-name.onrender.com/mcp` as the MCP server URL in Octonous.

---

## 🎨 Example Prompt
```
romantic toxic rap aesthetic, neon pink and black, glossy finish
```

---

## ❤️ Author

Jessica (MissJess9063)
Public MCP server for SDXL image generation.
