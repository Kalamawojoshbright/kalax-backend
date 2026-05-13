"""
KalaX Backend - Clean Architecture
No exposed API keys. All sensitive data in environment variables.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime

# Import services
from services.gemini_service import ask_gemini, generate_drawing_code
from services.router import classify_request, get_biology_type, get_geometry_type
from services.biology_engine import get_biology_diagram
from services.graph_engine import generate_graph_data
from services.geometry_engine import generate_geometry_svg

app = FastAPI(title="KalaX Backend", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# REQUEST MODELS
# ============================================

class ChatRequest(BaseModel):
    message: str
    subject: Optional[str] = "general"

class ChatResponse(BaseModel):
    response: str
    source: str

class DrawRequest(BaseModel):
    command: str

class DrawResponse(BaseModel):
    success: bool
    type: str  # "svg", "graph_data", "gemini_code", "error"
    svg: Optional[str] = None
    graph_data: Optional[dict] = None
    code: Optional[str] = None
    explanation: Optional[str] = None
    error: Optional[str] = None

# ============================================
# HEALTH ENDPOINTS
# ============================================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "KalaX Backend",
        "version": "2.0.0",
        "creator": "Kalamawo Joshua Bright"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": str(datetime.now())
    }

# ============================================
# CHAT ENDPOINT
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Route chat requests to appropriate handler"""
    
    # First, classify the request
    request_type = classify_request(request.message)
    
    # For now, send all to Gemini (except drawing commands)
    if request_type == "gemini":
        response = ask_gemini(request.message)
        if response:
            return ChatResponse(response=response, source="gemini")
    
    # Fallback
    return ChatResponse(
        response=get_local_fallback(request.message),
        source="local"
    )

# ============================================
# DRAW ENDPOINT
# ============================================

@app.post("/draw", response_model=DrawResponse)
async def draw(request: DrawRequest):
    """Route drawing requests to appropriate engine"""
    
    request_type = classify_request(request.command)
    
    # BIOLOGY DIAGRAMS
    if request_type == "biology":
        bio_type = get_biology_type(request.command)
        if bio_type:
            diagram = get_biology_diagram(bio_type)
            if diagram and diagram.get("svg"):
                return DrawResponse(
                    success=True,
                    type="svg",
                    svg=diagram["svg"],
                    explanation=diagram["description"]
                )
    
    # GEOMETRY SHAPES
    if request_type == "geometry":
        geo_type = get_geometry_type(request.command)
        if geo_type:
            shape = generate_geometry_svg(geo_type)
            if shape:
                return DrawResponse(
                    success=True,
                    type="svg",
                    svg=shape["svg"],
                    explanation=shape["description"]
                )
    
    # GRAPHS
    if request_type == "graph":
        # Extract function from command
        func = extract_function(request.command)
        if func:
            graph_data = generate_graph_data(func)
            if graph_data["success"]:
                return DrawResponse(
                    success=True,
                    type="graph_data",
                    graph_data=graph_data,
                    explanation=f"Graph of y = {func}"
                )
    
    # Try Gemini for custom drawings
    gemini_result = generate_drawing_code(request.command)
    if gemini_result and gemini_result.get("code"):
        return DrawResponse(
            success=True,
            type="gemini_code",
            code=gemini_result["code"],
            explanation=gemini_result.get("explanation", f"AI-generated drawing of {request.command}")
        )
    
    # Fallback error
    return DrawResponse(
        success=False,
        type="error",
        error="Could not generate drawing. Try 'Draw a circle', 'Draw a skeleton', or 'Plot y = x^2'"
    )

# ============================================
# HELPER FUNCTIONS
# ============================================

def extract_function(message: str) -> str:
    """Extract mathematical function from message"""
    import re
    match = re.search(r'y\s*=\s*(.+?)(?:\s|$)', message.lower())
    if match:
        return match.group(1).strip()
    return None

def get_local_fallback(message: str) -> str:
    """Local responses when Gemini is unavailable"""
    m = message.lower()
    
    if "photosynthesis" in m:
        return "🌿 **Photosynthesis**\n\nPlants make food using sunlight!\n\n6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂"
    
    if "mitosis" in m:
        return "🔬 **Mitosis**\n\nStages: Prophase → Metaphase → Anaphase → Telophase"
    
    if "newton" in m:
        return "⚡ **Newton's Laws**\n\n1. Inertia\n2. F = ma\n3. Action-Reaction"
    
    return f"Ask me about photosynthesis, mitosis, or say 'Draw a circle'"

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)