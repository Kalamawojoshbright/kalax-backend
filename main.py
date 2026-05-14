"""
KalaX Learn - Gemini AI Priority
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

app = FastAPI(title="KalaX Learn")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# GEMINI AI - MUST WORK
# ============================================

import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logger.error("❌ GEMINI_API_KEY not set in environment!")
    GEMINI_READY = False
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        MODEL_NAME = "gemini-1.5-flash"
        GEMINI_READY = True
        logger.info("✅ Gemini AI Ready")
    except Exception as e:
        logger.error(f"❌ Gemini init error: {e}")
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
# ENDPOINTS
# ============================================

@app.get("/")
async def root():
    return {"status": "online", "service": "KalaX Learn", "gemini": GEMINI_READY}

@app.get("/health")
async def health():
    return {"status": "healthy", "gemini_ready": GEMINI_READY}

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer using Gemini AI ONLY"""
    
    logger.info(f"Question: {request.message}")
    
    # ONLY use Gemini - no local fallback
    if GEMINI_READY:
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(request.message)
            return ChatResponse(response=response.text)
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return ChatResponse(response=f"Gemini error: {str(e)}")
    
    return ChatResponse(response="⚠️ Gemini API key not configured. Please add GEMINI_API_KEY to environment variables.")

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