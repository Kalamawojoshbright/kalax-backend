import matplotlib
matplotlib.use('Agg')  # non‑interactive backend for Render
import matplotlib.pyplot as plt
import numpy as np
import io
import base64"""
KalaX Learn – Corrected & Stable Version
Deploy to Render.com
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import math
import logging

# --- 1. Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 2. Create the FastAPI instance (app) FIRST ---
app = FastAPI(title="KalaX Learn")

# --- 3. Add CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. Debug Print (Temporary) ---
# This will appear in Render logs to verify the key is being read.
api_key = os.getenv("GEMINI_API_KEY")
logger.info(f"DEBUG: GEMINI_API_KEY is {'SET' if api_key else 'NOT SET'}")

# --- 5. Gemini AI Setup (Now using app, which exists) ---
GEMINI_READY = False
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
        MODEL_NAME = "gemini-2.5-flash"
        GEMINI_READY = True
        logger.info("✅ Gemini AI configured with model: " + MODEL_NAME)
    except Exception as e:
        logger.error(f"Gemini init error: {e}")
else:
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY environment variable not set")

# --- 6. Define Pydantic Models ---
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class GraphRequest(BaseModel):
    function: str

class GraphResponse(BaseModel):
    success: bool
    grid_data: dict = None
    error: str = None

# ============================================
# 7. API ENDPOINTS (Decorators placed AFTER app definition)
# ============================================

@app.get("/")
async def root():
    return {"status": "online", "service": "KalaX Learn", "gemini_ready": GEMINI_READY}

@app.get("/health")
async def health():
    return {"status": "healthy", "gemini_ready": GEMINI_READY}

# --- Minimal test endpoint to verify Gemini directly ---
@app.get("/test-gemini")
async def test_gemini():
    if not GEMINI_READY:
        return {"error": "Gemini not ready", "key_present": bool(os.getenv("GEMINI_API_KEY"))}
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content("Say 'Gemini is working'")
        return {"success": True, "response": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer any question using Gemini AI"""
    logger.info(f"Question: {request.message[:100]}...")
    
    if GEMINI_READY:
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(request.message)
            return ChatResponse(response=response.text)
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return ChatResponse(response=f"Gemini error: {str(e)}")
    else:
        return ChatResponse(response="⚠️ Gemini API not configured. Please set GEMINI_API_KEY in Render environment.")

@app.post("/graph", response_model=GraphResponse)
async def generate_graph(request: GraphRequest):
    """Generate full mathematical graph with grid, axes, labels"""
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
                    "x": x,
                    "sin": math.sin, "cos": math.cos, "tan": math.tan,
                    "asin": math.asin, "acos": math.acos, "atan": math.atan,
                    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
                    "sqrt": math.sqrt, "exp": math.exp, "log": math.log,
                    "log10": math.log10, "pi": math.pi, "e": math.e,
                    "abs": abs
                }
                y = eval(func, {"__builtins__": {}}, safe_dict)
                if math.isfinite(y) and abs(y) < 50:
                    x_values.append(round(x, 2))
                    y_values.append(round(y, 2))
            except:
                pass
            x += step
        
        if len(x_values) < 2:
            return GraphResponse(success=False, error="Could not generate graph. Try: x**2, sin(x), 2*x+3")
        
        y_min = min(y_values)
        y_max = max(y_values)
        # Add padding
        y_min = math.floor(y_min) - 1 if y_min > -10 else -10
        y_max = math.ceil(y_max) + 1 if y_max < 10 else 10
        
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
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)