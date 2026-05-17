from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
from io import BytesIO
import os
import google.generativeai as genai
from pydantic import BaseModel
from typing import Optional
import re
import json
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

class ChatRequest(BaseModel):
    message: str
    subject: Optional[str] = "general"

class ChatResponse(BaseModel):
    response: str
    source: str

class DrawRequest(BaseModel):
    command: str
    style: Optional[str] = "educational"

class DrawResponse(BaseModel):
    success: bool
    drawing_type: str
    code: Optional[str] = None
    explanation: Optional[str] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    return {"status": "online", "service": "KalaX Backend", "creator": "Kalamawo Joshua Bright"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": str(datetime.now())}

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(request.message)
        return ChatResponse(response=response.text, source="gemini")
    except Exception as e:
        return ChatResponse(response=f"Gemini error: {str(e)}", source="local")

@app.post("/draw", response_model=DrawResponse)
async def draw(request: DrawRequest):
    # Simple fallback – you can expand with your own drawing functions
    return DrawResponse(success=False, drawing_type="error", explanation="Draw endpoint ready for custom shapes")

# ========== PLOT ENDPOINT (no numpy, safe eval) ==========
@app.post("/plot")
async def plot_expression(request: Request):
    try:
        body = await request.json()
        expr = body.get("expression", "").strip()
        if not expr:
            return Response(status_code=400, content="No expression")

        def safe_eval(x):
            e = expr.replace('^', '**')
            allowed = {
                'x': x,
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
                'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
                'sqrt': math.sqrt, 'exp': math.exp, 'log': math.log,
                'log10': math.log10, 'abs': abs,
                'pi': math.pi, 'e': math.e
            }
            try:
                return eval(e, {"__builtins__": {}}, allowed)
            except:
                return None

        low = expr.lower()
        if any(t in low for t in ['sin', 'cos', 'tan']):
            x_min, x_max = -2*math.pi, 2*math.pi
        elif 'log' in low:
            x_min, x_max = 0.1, 8
        else:
            x_min, x_max = -6, 6

        step = (x_max - x_min) / 400
        x_vals = []
        y_vals = []
        x = x_min
        while x <= x_max + 1e-9:
            y = safe_eval(x)
            if y is not None and abs(y) < 100:
                x_vals.append(x)
                y_vals.append(y)
            x += step

        if not x_vals:
            return Response(status_code=400, content="No valid points")

        fig, ax = plt.subplots(figsize=(7, 5), dpi=100)
        ax.plot(x_vals, y_vals, 'b-', linewidth=2)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_title(f'y = {expr}', fontsize=12)
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return Response(content=buf.getvalue(), media_type="image/png")
    except Exception as e:
        return Response(status_code=500, content=f"Plot error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)