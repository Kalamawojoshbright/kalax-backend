"""
KalaX Backend – Stable textbook graphs (no recursion, low DPI for speed)
Deploy to Render.com
"""

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
from datetime import datetime
import json
import re
import os
import math
import traceback
from io import BytesIO
import asyncio
import concurrent.futures

# ========== MATPLOTLIB (low DPI for reliability) ==========
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Low but acceptable resolution – fast and stable
plt.rcParams.update({
    'font.size': 10,
    'axes.linewidth': 1.2,
    'figure.dpi': 100,
    'savefig.dpi': 100,
    'figure.figsize': (7, 5)
})

# ========== FASTAPI APP ==========
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== GEMINI API ==========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# ========== REQUEST MODELS ==========
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

# ========== HEALTH ==========
@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "KalaX Backend",
        "model": MODEL_NAME,
        "creator": "Kalamawo Joshua Bright"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "gemini_model": MODEL_NAME,
        "timestamp": str(datetime.now())
    }

# ========== CHAT ==========
@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(request.message)
        return ChatResponse(response=response.text, source="gemini")
    except Exception as e:
        print(f"Gemini error: {e}")
        return ChatResponse(response=get_fallback_answer(request.message), source="local")

# ========== DRAW ==========
@app.post("/draw", response_model=DrawResponse)
async def draw(request: DrawRequest):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""Generate a JavaScript drawing function for: "{request.command}"

Return ONLY valid JSON in this exact format:
{{"type":"canvas_code","code":"function draw(ctx, canvas){{ ... }}","explanation":"description"}}

Requirements:
- Canvas is 700x500 pixels
- Use ctx.fillStyle, ctx.strokeStyle, ctx.beginPath()
- Add labels with ctx.fillText()
- Make it educational and accurate
- Use appropriate colors

Generate the function NOW:"""
        response = model.generate_content(prompt)
        json_match = re.search(r'\{[\s\S]*\}', response.text)
        if json_match:
            result = json.loads(json_match.group())
            if result.get("code"):
                return DrawResponse(
                    success=True,
                    drawing_type="canvas_code",
                    code=result["code"],
                    explanation=result.get("explanation", f"AI-generated diagram of {request.command}")
                )
        return get_fallback_drawing(request.command)
    except Exception as e:
        print(f"Draw error: {e}")
        return get_fallback_drawing(request.command)

# ========== SAFE PLOTTING – NO NUMPY RECURSION ==========
def safe_eval(expr: str, x: float) -> float:
    """Evaluate a math expression for a single x value – no recursion."""
    # Replace ^ with **
    expr = expr.replace('^', '**')
    # Allowed names (math functions and constants)
    allowed = {
        'x': x,
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
        'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
        'exp': math.exp, 'log': math.log, 'log10': math.log10,
        'sqrt': math.sqrt, 'abs': abs,
        'pi': math.pi, 'e': math.e
    }
    try:
        return eval(expr, {"__builtins__": {}}, allowed)
    except:
        return float('nan')

def generate_plot_image(expr: str) -> bytes:
    """Generate a plot using point‑by‑point evaluation (no recursion)."""
    expr_lower = expr.lower()
    # Domain
    if any(f in expr_lower for f in ['sin', 'cos', 'tan']):
        x_min, x_max = -2 * math.pi, 2 * math.pi
    elif 'log' in expr_lower:
        x_min, x_max = 0.1, 8
    else:
        x_min, x_max = -6, 6

    steps = 400
    x_vals = []
    y_vals = []
    for i in range(steps + 1):
        x = x_min + (x_max - x_min) * i / steps
        y = safe_eval(expr, x)
        if abs(y) < 100:   # discard extreme values
            x_vals.append(x)
            y_vals.append(y)
        else:
            # skip point
            pass

    if not x_vals:
        raise Exception("No valid points generated")

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'y = {expr}')
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title(f'y = {expr}', fontsize=12)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()

    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    return buf.getvalue()

@app.post("/plot")
async def plot_expression(request: dict):
    expr = request.get("expression", "").strip()
    if not expr:
        return Response(status_code=400, content="No expression provided")
    try:
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            img_bytes = await loop.run_in_executor(pool, generate_plot_image, expr)
        return Response(content=img_bytes, media_type="image/png")
    except Exception as e:
        print(traceback.format_exc())
        return Response(status_code=500, content=f"Plot error: {str(e)}")

# ========== FALLBACK FUNCTIONS (unchanged) ==========
def get_fallback_answer(message):
    m = message.lower()
    if "photosynthesis" in m:
        return "🌿 **Photosynthesis**\n\nPlants make their own food using sunlight!\n\n**Equation:** 6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂\n\n**Two stages:**\n1. Light reaction - captures sunlight\n2. Calvin cycle - makes glucose"
    if "mitosis" in m:
        return "🔬 **Mitosis (PMAT)**\n\n**Stages:**\n• **P**rophase - Chromosomes condense\n• **M**etaphase - Line up at center\n• **A**naphase - Separate to poles\n• **T**elophase - Two new cells form\n\n**Result:** 2 identical daughter cells!"
    if "newton" in m:
        return "⚡ **Newton's Laws**\n\n**1st Law (Inertia):** Objects keep doing what they're doing\n**2nd Law (F=ma):** Force = mass × acceleration\n**3rd Law (Action-Reaction):** Every action has equal opposite reaction"
    if "hello" in m or "hi" in m:
        return "👋 Hello! I'm KalaX AI, created by Kalamawo Joshua Bright. Ask me anything about science, math, or say 'Draw a...'"
    return f"📚 I'm KalaX AI. Ask me 'What is photosynthesis?' or 'Draw a human skeleton'"

def get_fallback_drawing(command):
    cmd = command.lower()
    if "skeleton" in cmd:
        return DrawResponse(success=True, drawing_type="canvas_code", code=get_skeleton_code(), explanation="Human skeleton diagram")
    if "brain" in cmd:
        return DrawResponse(success=True, drawing_type="canvas_code", code=get_brain_code(), explanation="Human brain diagram")
    if "circle" in cmd:
        return DrawResponse(success=True, drawing_type="canvas_code", code=get_circle_code(), explanation="Circle with center and radius")
    if "square" in cmd:
        return DrawResponse(success=True, drawing_type="canvas_code", code=get_square_code(), explanation="Square - all sides equal")
    if "triangle" in cmd:
        return DrawResponse(success=True, drawing_type="canvas_code", code=get_triangle_code(), explanation="Right angle triangle")
    if "heart" in cmd:
        return DrawResponse(success=True, drawing_type="canvas_code", code=get_heart_code(), explanation="Heart shape")
    return DrawResponse(success=False, drawing_type="error", explanation="Try 'Draw a human skeleton', 'Draw a brain', or 'Draw a circle'")

def get_skeleton_code():
    return """function draw(ctx, canvas) {
    const cx = canvas.width/2;
    ctx.beginPath();
    ctx.ellipse(cx,80,35,45,0,0,2*Math.PI);
    ctx.fillStyle='#f5f5dc'; ctx.fill(); ctx.stroke();
    ctx.fillStyle='#8B7355';
    ctx.beginPath(); ctx.ellipse(cx-15,70,6,8,0,0,2*Math.PI); ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx+15,70,6,8,0,0,2*Math.PI); ctx.fill();
    ctx.beginPath(); ctx.moveTo(cx,130); ctx.lineTo(cx,350); ctx.stroke();
    for(let i=0;i<7;i++){let y=160+i*25;
        ctx.beginPath(); ctx.moveTo(cx,y); ctx.quadraticCurveTo(cx-40,y+10,cx-35,y); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx,y); ctx.quadraticCurveTo(cx+40,y+10,cx+35,y); ctx.stroke();
    }
    ctx.beginPath(); ctx.moveTo(cx-30,160); ctx.lineTo(cx-70,220); ctx.lineTo(cx-55,290); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx+30,160); ctx.lineTo(cx+70,220); ctx.lineTo(cx+55,290); ctx.stroke();
    ctx.beginPath(); ctx.ellipse(cx,355,45,20,0,0,2*Math.PI); ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx-25,365); ctx.lineTo(cx-30,440); ctx.lineTo(cx-40,470); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx+25,365); ctx.lineTo(cx+30,440); ctx.lineTo(cx+40,470); ctx.stroke();
}"""

def get_brain_code():
    return """function draw(ctx, canvas) {
    const cx=canvas.width/2, cy=canvas.height/2.5;
    ctx.beginPath(); ctx.ellipse(cx-45,cy,60,80,-0.1,0,2*Math.PI); ctx.fillStyle='#FFB6C1'; ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx+45,cy,60,80,0.1,0,2*Math.PI); ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx,cy-20,30,25,0,0,2*Math.PI); ctx.fillStyle='#FFC0CB'; ctx.fill();
    ctx.beginPath(); ctx.moveTo(cx-10,cy+55); ctx.lineTo(cx,cy+100); ctx.lineTo(cx+10,cy+55); ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx,cy+40,35,25,0,0,2*Math.PI); ctx.fill();
    ctx.fillStyle='#333'; ctx.font='12px "Segoe UI"';
    ctx.fillText('Left Hemisphere',cx-100,cy-30);
    ctx.fillText('Right Hemisphere',cx+35,cy-30);
    ctx.fillText('Cerebellum',cx-30,cy+55);
    ctx.fillText('Brain Stem',cx-25,cy+95);
}"""

def get_circle_code():
    return """function draw(ctx, canvas) {
    const cx=canvas.width/2, cy=canvas.height/2, r=120;
    ctx.beginPath(); ctx.arc(cx,cy,r,0,2*Math.PI);
    ctx.strokeStyle='#0f3460'; ctx.lineWidth=3; ctx.stroke();
    ctx.beginPath(); ctx.arc(cx,cy,5,0,2*Math.PI); ctx.fillStyle='#e94560'; ctx.fill();
    ctx.fillStyle='#333'; ctx.font='14px "Segoe UI"';
    ctx.fillText('Center',cx+10,cy);
    ctx.fillText('Radius (r)',cx+r/2,cy-10);
    ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(cx+r,cy); ctx.strokeStyle='#e94560'; ctx.stroke();
}"""

def get_square_code():
    return """function draw(ctx, canvas) {
    const cx=canvas.width/2, cy=canvas.height/2, size=160;
    ctx.strokeRect(cx-size/2,cy-size/2,size,size);
    ctx.fillStyle='#333'; ctx.font='14px "Segoe UI"';
    ctx.fillText('Square',cx-25,cy-size/2-10);
    ctx.fillText('All sides equal',cx-50,cy+size/2+20);
}"""

def get_triangle_code():
    return """function draw(ctx, canvas) {
    const cx=canvas.width/2, cy=canvas.height/2;
    ctx.beginPath();
    ctx.moveTo(cx-100,cy+60); ctx.lineTo(cx+100,cy+60); ctx.lineTo(cx-100,cy-60);
    ctx.closePath(); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx-100+20,cy+60); ctx.lineTo(cx-100+20,cy+60-20); ctx.lineTo(cx-100,cy+60-20); ctx.stroke();
    ctx.fillStyle='#333'; ctx.font='12px "Segoe UI"';
    ctx.fillText('90°',cx-95,cy+55);
    ctx.fillText('Right Angle Triangle',cx-80,cy-80);
}"""

def get_heart_code():
    return """function draw(ctx, canvas) {
    const cx=canvas.width/2, cy=canvas.height/2;
    ctx.beginPath();
    ctx.moveTo(cx,cy+40);
    ctx.bezierCurveTo(cx-90,cy-40,cx-140,cy+40,cx,cy+120);
    ctx.bezierCurveTo(cx+140,cy+40,cx+90,cy-40,cx,cy+40);
    ctx.fillStyle='#FF6B6B'; ctx.fill();
    ctx.fillStyle='#333'; ctx.font='14px "Segoe UI"';
    ctx.fillText('Heart',cx-20,cy-50);
}"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)