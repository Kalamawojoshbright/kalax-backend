"""
KalaX Learn - Gemini AI + Full Screen
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import math
import re
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="KalaX Learn", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# GEMINI AI CONFIGURATION
# ============================================

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Gemini package not installed")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_AVAILABLE and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        MODEL_NAME = "gemini-2.0-flash-exp"
        GEMINI_READY = True
        logger.info("✅ Gemini AI configured successfully")
    except Exception as e:
        GEMINI_READY = False
        logger.error(f"Gemini init error: {e}")
else:
    GEMINI_READY = False
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set")

# ============================================
# REQUEST MODELS
# ============================================

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class GraphRequest(BaseModel):
    function: str

class GraphResponse(BaseModel):
    success: bool
    grid_data: Optional[dict] = None
    error: Optional[str] = None

# ============================================
# HEALTH ENDPOINTS
# ============================================

@app.get("/")
async def root():
    return {"status": "online", "service": "KalaX Learn"}

@app.get("/health")
async def health():
    return {"status": "healthy", "gemini": GEMINI_READY}

# ============================================
# CHAT ENDPOINT - GEMINI ANSWERS
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer using Gemini AI"""
    
    logger.info(f"Question: {request.message[:100]}")
    
    # Check if math calculation
    math_answer = solve_math(request.message)
    if math_answer:
        return ChatResponse(response=math_answer)
    
    # Use Gemini AI
    if GEMINI_READY:
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(request.message)
            return ChatResponse(response=response.text)
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return ChatResponse(response=get_fallback_answer(request.message))
    
    return ChatResponse(response=get_fallback_answer(request.message))

# ============================================
# MATH SOLVER
# ============================================

def solve_math(question: str) -> str:
    q = question.lower().strip()
    
    # Simple arithmetic
    match = re.search(r'(\d+)\s*([\+\-\*\/])\s*(\d+)', q)
    if match:
        a = float(match.group(1))
        op = match.group(2)
        b = float(match.group(3))
        
        if op == '+': result = a + b
        elif op == '-': result = a - b
        elif op == '*': result = a * b
        elif op == '/': result = a / b if b != 0 else "undefined"
        else: return None
        
        return f"🧮 {a} {op} {b} = {result}"
    
    # Algebra: 2x+5=13
    eq_match = re.search(r'(\d+)x\s*\+\s*(\d+)\s*=\s*(\d+)', q)
    if eq_match:
        a = float(eq_match.group(1))
        b = float(eq_match.group(2))
        c = float(eq_match.group(3))
        x = (c - b) / a
        return f"📐 {a}x + {b} = {c}\n\nx = {x}"
    
    return None

def get_fallback_answer(question: str) -> str:
    q = question.lower()
    
    if "photosynthesis" in q:
        return "🌿 Photosynthesis: Plants convert CO₂ and H₂O into glucose and oxygen using sunlight.\n\n6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂"
    
    if "mitosis" in q:
        return "🔬 Mitosis: Cell division stages: Prophase → Metaphase → Anaphase → Telophase"
    
    if "newton" in q:
        return "⚡ Newton's Laws: 1) Inertia, 2) F=ma, 3) Action-Reaction"
    
    return f"I'm KalaX, your study assistant. Ask me anything!"

# ============================================
# GRAPH ENDPOINT
# ============================================

@app.post("/graph", response_model=GraphResponse)
async def generate_graph(request: GraphRequest):
    func = request.function.replace('^', '**')
    
    try:
        x_values = []
        y_values = []
        x_min, x_max = -8, 8
        step = 0.05
        
        x = x_min
        while x <= x_max:
            try:
                safe_dict = {
                    "x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                    "sqrt": math.sqrt, "exp": math.exp, "log": math.log,
                    "pi": math.pi, "abs": abs
                }
                y = eval(func, {"__builtins__": {}}, safe_dict)
                if math.isfinite(y) and abs(y) < 30:
                    x_values.append(round(x, 2))
                    y_values.append(round(y, 2))
            except:
                pass
            x += step
        
        if len(x_values) < 2:
            return GraphResponse(success=False, error="Could not generate graph")
        
        y_min = min(y_values)
        y_max = max(y_values)
        
        return GraphResponse(
            success=True,
            grid_data={
                "x_values": x_values,
                "y_values": y_values,
                "function": request.function,
                "x_min": x_min,
                "x_max": x_max,
                "y_min": math.floor(y_min) - 1,
                "y_max": math.ceil(y_max) + 1
            }
        )
    except Exception as e:
        return GraphResponse(success=False, error=str(e))

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)