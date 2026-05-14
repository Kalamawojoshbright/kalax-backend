"""
KalaX Learn - Graph Paper Style + AI Assistant
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
# GEMINI AI - No branding, just works
# ============================================

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_AVAILABLE and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        MODEL_NAME = "gemini-2.0-flash-exp"
        GEMINI_READY = True
        logger.info("✅ AI configured")
    except:
        GEMINI_READY = False
else:
    GEMINI_READY = False

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
    return {"status": "healthy"}

# ============================================
# CHAT ENDPOINT - Answers questions
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer any question using AI"""
    
    logger.info(f"Question: {request.message[:100]}...")
    
    if GEMINI_READY:
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(request.message)
            return ChatResponse(response=response.text)
        except Exception as e:
            logger.error(f"AI error: {e}")
    
    return ChatResponse(response=get_local_answer(request.message))

# ============================================
# GRAPH ENDPOINT - Graph paper style
# ============================================

@app.post("/graph", response_model=GraphResponse)
async def generate_graph(request: GraphRequest):
    """Generate graph paper style mathematical graph"""
    
    func = request.function.replace('^', '**')
    
    try:
        # Generate points
        x_values = []
        y_values = []
        x_min, x_max = -6, 6
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
                if math.isfinite(y) and abs(y) < 20:
                    x_values.append(round(x, 2))
                    y_values.append(round(y, 2))
            except:
                pass
            x += step
        
        if len(x_values) < 2:
            return GraphResponse(
                success=False,
                error="Could not generate graph. Try: x**2, 2*x+3, sin(x)"
            )
        
        # Calculate y range
        y_min = min(y_values)
        y_max = max(y_values)
        y_min = math.floor(y_min) - 1
        y_max = math.ceil(y_max) + 1
        
        return GraphResponse(
            success=True,
            grid_data={
                "x_values": x_values,
                "y_values": y_values,
                "function": request.function,
                "x_min": x_min,
                "x_max": x_max,
                "y_min": y_min,
                "y_max": y_max
            }
        )
        
    except Exception as e:
        return GraphResponse(success=False, error=str(e))

# ============================================
# LOCAL ANSWERS (Fallback)
# ============================================

def get_local_answer(message: str) -> str:
    m = message.lower()
    
    if "photosynthesis" in m:
        return """🌿 **Photosynthesis**

Plants make food using sunlight!

**Equation:** 6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂

**Two stages:**
1. Light reaction - captures sunlight, releases oxygen
2. Calvin cycle - makes glucose from CO₂"""
    
    if "mitosis" in m:
        return """🔬 **Mitosis (PMAT)**

• **P**rophase - Chromosomes condense
• **M**etaphase - Line up at center
• **A**naphase - Separate to poles
• **T**elophase - Two new cells form"""
    
    if "newton" in m:
        return """⚡ **Newton's Laws**

1st: Objects keep doing what they're doing
2nd: Force = mass × acceleration (F = ma)
3rd: Every action has equal opposite reaction"""
    
    return """📚 **KalaX Learn**

Try:
• "Plot y = x^2" - Parabola graph
• "What is photosynthesis?" - Science
• "Draw a circle" - Geometry

Created by Kalamawo Joshua Bright"""

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)