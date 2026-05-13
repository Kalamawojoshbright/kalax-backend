"""
KalaX Backend - Clean Architecture
No exposed API keys. All sensitive data in environment variables.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import sys
import math
import re
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import services, with fallback if files don't exist
try:
    from services.gemini_service import ask_gemini, generate_drawing_code
except ImportError:
    # Fallback if services not available
    def ask_gemini(prompt):
        return None
    def generate_drawing_code(command):
        return None

try:
    from services.router import classify_request, get_biology_type, get_geometry_type
except ImportError:
    def classify_request(p): return "gemini"
    def get_biology_type(p): return None
    def get_geometry_type(p): return None

try:
    from services.biology_engine import get_biology_diagram
except ImportError:
    def get_biology_diagram(t): return None

try:
    from services.graph_engine import generate_graph_data
except ImportError:
    def generate_graph_data(f, a=-8, b=8):
        return {"success": False}

try:
    from services.geometry_engine import generate_geometry_svg
except ImportError:
    def generate_geometry_svg(s):
        return None

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
    type: str
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
    
    # For now, send all to Gemini (except drawing commands)
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
    
    cmd = request.command.lower()
    
    # CIRCLE
    if "circle" in cmd:
        svg = get_circle_svg()
        return DrawResponse(
            success=True,
            type="svg",
            svg=svg,
            explanation="Circle with center and radius"
        )
    
    # SQUARE
    if "square" in cmd:
        svg = get_square_svg()
        return DrawResponse(
            success=True,
            type="svg",
            svg=svg,
            explanation="Square - all sides equal, 4 right angles"
        )
    
    # TRIANGLE
    if "triangle" in cmd or "right angle" in cmd:
        svg = get_triangle_svg()
        return DrawResponse(
            success=True,
            type="svg",
            svg=svg,
            explanation="Right Angle Triangle - a² + b² = c²"
        )
    
    # SKELETON
    if "skeleton" in cmd:
        svg = get_skeleton_svg()
        return DrawResponse(
            success=True,
            type="svg",
            svg=svg,
            explanation="Human Skeleton - 206 bones"
        )
    
    # BRAIN
    if "brain" in cmd:
        svg = get_brain_svg()
        return DrawResponse(
            success=True,
            type="svg",
            svg=svg,
            explanation="Human Brain - Cerebrum, Cerebellum, Brain Stem"
        )
    
    # HEART
    if "heart" in cmd:
        svg = get_heart_svg()
        return DrawResponse(
            success=True,
            type="svg",
            svg=svg,
            explanation="Human Heart - 4 chambers"
        )
    
    # GRAPH / PLOT
    if "plot" in cmd or "graph" in cmd or "y =" in cmd:
        func = extract_function(request.command)
        if func:
            graph_data = generate_graph_points(func)
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
            explanation=gemini_result.get("explanation", f"Drawing of {request.command}")
        )
    
    # Fallback error
    return DrawResponse(
        success=False,
        type="error",
        error="Try 'Draw a circle', 'Draw a square', 'Draw a skeleton', or 'Plot y = x^2'"
    )

# ============================================
# SVG GENERATORS (Built-in to avoid file issues)
# ============================================

def get_circle_svg():
    return '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="400" fill="#f8f9fa"/>
        <circle cx="200" cy="200" r="120" fill="none" stroke="#0f3460" stroke-width="3"/>
        <line x1="200" y1="200" x2="320" y2="200" stroke="#e94560" stroke-width="2" stroke-dasharray="5,5"/>
        <circle cx="200" cy="200" r="5" fill="#e94560"/>
        <text x="260" y="190" fill="#e94560" font-size="14">Radius (r)</text>
        <text x="200" y="220" text-anchor="middle" fill="#0f3460" font-size="14">Center</text>
    </svg>'''

def get_square_svg():
    return '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="400" fill="#f8f9fa"/>
        <rect x="100" y="100" width="200" height="200" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/>
        <line x1="100" y1="100" x2="300" y2="100" stroke="#e94560" stroke-width="2" marker-end="url(#arrow)"/>
        <text x="200" y="90" text-anchor="middle" fill="#e94560" font-size="14">Side</text>
        <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3z" fill="#e94560"/></marker></defs>
    </svg>'''

def get_triangle_svg():
    return '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="400" fill="#f8f9fa"/>
        <polygon points="80,300 300,300 80,100" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/>
        <polygon points="80,280 100,280 100,300" fill="none" stroke="#e94560" stroke-width="2"/>
        <text x="90" y="295" text-anchor="middle" fill="#e94560" font-size="14">90°</text>
        <text x="190" y="320" text-anchor="middle" fill="#0f3460" font-size="14">Base</text>
        <text x="65" y="200" text-anchor="middle" fill="#0f3460" font-size="14" transform="rotate(-90 65 200)">Height</text>
    </svg>'''

def get_skeleton_svg():
    return '''<svg width="500" height="500" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
        <rect width="500" height="500" fill="#f5f5dc"/>
        <text x="250" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f3460">Human Skeleton</text>
        <!-- Skull -->
        <ellipse cx="250" cy="80" cx="35" cy="45" fill="#f0e6d2" stroke="#8B7355" stroke-width="2"/>
        <circle cx="235" cy="70" r="6" fill="#8B7355"/>
        <circle cx="265" cy="70" r="6" fill="#8B7355"/>
        <!-- Spine -->
        <line x1="250" y1="130" x2="250" y2="350" stroke="#8B7355" stroke-width="3"/>
        <!-- Ribs -->
        <path d="M250,160 Q210,170 215,160" fill="none" stroke="#8B7355" stroke-width="2"/>
        <path d="M250,180 Q205,190 210,180" fill="none" stroke="#8B7355" stroke-width="2"/>
        <path d="M250,200 Q200,210 205,200" fill="none" stroke="#8B7355" stroke-width="2"/>
        <path d="M250,160 Q290,170 285,160" fill="none" stroke="#8B7355" stroke-width="2"/>
        <path d="M250,180 Q295,190 290,180" fill="none" stroke="#8B7355" stroke-width="2"/>
        <path d="M250,200 Q300,210 295,200" fill="none" stroke="#8B7355" stroke-width="2"/>
        <!-- Arms -->
        <line x1="220" y1="160" x2="180" y2="220" x2="190" y2="280" stroke="#8B7355" stroke-width="3"/>
        <line x1="280" y1="160" x2="320" y2="220" x2="310" y2="280" stroke="#8B7355" stroke-width="3"/>
        <!-- Pelvis -->
        <ellipse cx="250" cy="360" rx="50" ry="20" fill="#f0e6d2" stroke="#8B7355" stroke-width="2"/>
        <!-- Legs -->
        <line x1="225" y1="370" x2="220" y2="440" x2="210" y2="470" stroke="#8B7355" stroke-width="3"/>
        <line x1="275" y1="370" x2="280" y2="440" x2="290" y2="470" stroke="#8B7355" stroke-width="3"/>
        <text x="250" y="490" text-anchor="middle" font-size="12" fill="#666">Human Skeleton - 206 bones</text>
    </svg>'''

def get_brain_svg():
    return '''<svg width="500" height="400" viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="500" height="400" fill="#fff9e6"/>
        <text x="250" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f3460">Human Brain</text>
        <ellipse cx="205" cy="180" rx="70" ry="90" fill="#FFB6C1" stroke="#FF69B4" stroke-width="2"/>
        <ellipse cx="295" cy="180" rx="70" ry="90" fill="#FFB6C1" stroke="#FF69B4" stroke-width="2"/>
        <ellipse cx="250" cy="160" rx="35" ry="30" fill="#FFC0CB" stroke="#FF69B4" stroke-width="1"/>
        <path d="M240,260 L250,310 L260,260" fill="#FFB6C1" stroke="#FF69B4" stroke-width="2"/>
        <ellipse cx="250" cy="280" rx="40" ry="25" fill="#FFB6C1" stroke="#FF69B4" stroke-width="2"/>
        <text x="250" y="380" text-anchor="middle" font-size="12" fill="#666">Cerebrum | Cerebellum | Brain Stem</text>
    </svg>'''

def get_heart_svg():
    return '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="400" fill="#fff0f0"/>
        <text x="200" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#c62828">Human Heart</text>
        <path d="M200,340 C100,250 60,300 200,380 C340,300 300,250 200,340" fill="#FF6B6B" stroke="#c62828" stroke-width="2"/>
        <ellipse cx="175" cy="280" rx="30" ry="35" fill="#E74C3C" stroke="#c62828" stroke-width="1"/>
        <ellipse cx="225" cy="280" rx="30" ry="35" fill="#E74C3C" stroke="#c62828" stroke-width="1"/>
        <ellipse cx="165" cy="230" rx="28" ry="22" fill="#E74C3C" stroke="#c62828" stroke-width="1"/>
        <ellipse cx="235" cy="230" rx="28" ry="22" fill="#E74C3C" stroke="#c62828" stroke-width="1"/>
        <text x="200" y="380" text-anchor="middle" font-size="12" fill="#666">4 chambers: Atria (top) and Ventricles (bottom)</text>
    </svg>'''

# ============================================
# HELPER FUNCTIONS
# ============================================

def extract_function(message: str) -> str:
    """Extract mathematical function from message"""
    match = re.search(r'y\s*=\s*(.+?)(?:\s|$)', message.lower())
    if match:
        return match.group(1).strip()
    match = re.search(r'plot\s+(.+?)(?:\s|$)', message.lower())
    if match:
        return match.group(1).strip()
    return None

def generate_graph_points(function: str) -> dict:
    """Generate x,y points for a mathematical function"""
    x_values = []
    y_values = []
    x_min = -8
    x_max = 8
    step = 0.1
    
    x = x_min
    while x <= x_max:
        try:
            # Convert ^ to ** for Python
            func = function.replace('^', '**')
            # Safe evaluation with math functions
            allowed_locals = {
                "x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "sqrt": math.sqrt, "exp": math.exp, "log": math.log, "pi": math.pi,
                "abs": abs
            }
            y = eval(func, {"__builtins__": {}}, allowed_locals)
            
            if math.isfinite(y) and abs(y) < 50:
                x_values.append(round(x, 2))
                y_values.append(round(y, 2))
        except:
            pass
        
        x += step
    
    return {
        "success": len(x_values) > 1,
        "x_values": x_values,
        "y_values": y_values,
        "function": function
    }

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