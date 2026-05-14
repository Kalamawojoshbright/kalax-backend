"""
KalaX Backend - SECURE VERSION
NO hardcoded API keys - Uses environment variables only
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="KalaX Backend", version="2.0.0")

# CORS - Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# SECURE: Gemini API Key from Environment Variable
# NEVER hardcode API keys in source code!
# ============================================

# Try to import Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google Generative AI package not installed")

# Load API key from environment variable (SECURE)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_AVAILABLE and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        MODEL_NAME = "gemini-2.0-flash-exp"
        GEMINI_READY = True
        logger.info("✅ Gemini AI configured securely from environment variable")
    except Exception as e:
        GEMINI_READY = False
        logger.error(f"❌ Gemini initialization failed: {e}")
else:
    GEMINI_READY = False
    if not GEMINI_API_KEY:
        logger.warning("⚠️ GEMINI_API_KEY environment variable not set")
    if not GEMINI_AVAILABLE:
        logger.warning("⚠️ google-generativeai package not installed")

# ============================================
# REQUEST MODELS
# ============================================

class ChatRequest(BaseModel):
    message: str
    subject: Optional[str] = "general"

class ChatResponse(BaseModel):
    response: str
    provider: str  # "gemini" or "local"

class MathRequest(BaseModel):
    expression: str
    type: str = "diagram"

class MathResponse(BaseModel):
    success: bool
    diagram_type: str
    svg: Optional[str] = None
    graph_data: Optional[dict] = None
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
        "gemini_available": GEMINI_READY,
        "creator": "Kalamawo Joshua Bright"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": str(datetime.now()),
        "gemini_available": GEMINI_READY
    }

# ============================================
# CHAT ENDPOINT - SECURE (Backend only)
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer ANY question using Gemini AI (secure backend-only)"""
    
    logger.info(f"📨 Chat request: {request.message[:100]}...")
    
    # Try Gemini if available
    if GEMINI_READY:
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(request.message)
            logger.info(f"✅ Gemini response sent")
            return ChatResponse(
                response=response.text,
                provider="gemini"
            )
        except Exception as e:
            logger.error(f"❌ Gemini error: {e}")
    
    # Fallback to local responses
    logger.info("📚 Using local fallback response")
    return ChatResponse(
        response=get_local_response(request.message),
        provider="local"
    )

# ============================================
# MATH DIAGRAM ENDPOINT
# ============================================

@app.post("/math/diagram", response_model=MathResponse)
async def math_diagram(request: MathRequest):
    """Generate mathematical diagrams"""
    
    expr = request.expression.lower()
    
    # Check for graph/function
    if "plot" in expr or "graph" in expr or ("y=" in expr and "draw" not in expr):
        func = extract_function(request.expression)
        if func:
            graph_data = generate_graph_points(func)
            if graph_data["success"]:
                return MathResponse(
                    success=True,
                    diagram_type="graph",
                    graph_data=graph_data,
                    explanation=f"Graph of y = {func}"
                )
    
    # Diagram mapping
    diagram_map = {
        "circle": FULL_PAGE_CIRCLE,
        "square": FULL_PAGE_SQUARE,
        "rectangle": FULL_PAGE_RECTANGLE,
        "triangle": FULL_PAGE_TRIANGLE,
        "right triangle": FULL_PAGE_RIGHT_TRIANGLE,
        "equilateral": FULL_PAGE_EQUILATERAL,
        "pentagon": FULL_PAGE_PENTAGON,
        "hexagon": FULL_PAGE_HEXAGON,
        "octagon": FULL_PAGE_OCTAGON,
        "star": FULL_PAGE_STAR,
        "cube": FULL_PAGE_CUBE,
        "sphere": FULL_PAGE_SPHERE,
        "cylinder": FULL_PAGE_CYLINDER,
        "sine wave": FULL_PAGE_SINE_WAVE,
        "cosine wave": FULL_PAGE_COSINE_WAVE,
        "parabola": FULL_PAGE_PARABOLA,
        "hyperbola": FULL_PAGE_HYPERBOLA,
        "coordinate plane": FULL_PAGE_COORDINATE_PLANE,
        "bar chart": FULL_PAGE_BAR_CHART,
        "pie chart": FULL_PAGE_PIE_CHART,
        "venn": FULL_PAGE_VENN,
        "right angle": FULL_PAGE_RIGHT_ANGLE,
        "parallel lines": FULL_PAGE_PARALLEL_LINES,
        "perpendicular": FULL_PAGE_PERPENDICULAR,
        "number line": FULL_PAGE_NUMBER_LINE,
        "heart": FULL_PAGE_HEART
    }
    
    for key, svg in diagram_map.items():
        if key in expr:
            return MathResponse(
                success=True,
                diagram_type="svg",
                svg=svg,
                explanation=f"{key.title()} diagram"
            )
    
    # Fallback
    return MathResponse(
        success=False,
        diagram_type="error",
        error="Try: 'Plot y = x^2', 'Draw a circle', 'What is photosynthesis?'"
    )

# ============================================
# HELPER FUNCTIONS
# ============================================

def extract_function(expression: str) -> str:
    """Extract mathematical function from expression"""
    match = re.search(r'y\s*=\s*(.+?)(?:\s|$)', expression.lower())
    if match:
        return match[1].strip()
    match = re.search(r'plot\s+(.+?)(?:\s|$)', expression.lower())
    if match:
        return match[1].strip()
    return None

def generate_graph_points(func: str) -> dict:
    """Generate x,y points for a mathematical function"""
    x_values = []
    y_values = []
    x_min, x_max = -6, 6
    step = 0.05
    
    x = x_min
    while x <= x_max:
        try:
            f = func.replace('^', '**')
            safe_dict = {
                "x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "sqrt": math.sqrt, "exp": math.exp, "log": math.log, "pi": math.pi,
                "abs": abs
            }
            y = eval(f, {"__builtins__": {}}, safe_dict)
            if math.isfinite(y) and abs(y) < 20:
                x_values.append(round(x, 2))
                y_values.append(round(y, 2))
        except:
            pass
        x += step
    
    return {
        "success": len(x_values) > 1,
        "x_values": x_values,
        "y_values": y_values,
        "function": func
    }

def get_local_response(message: str) -> str:
    """Local responses when Gemini is unavailable"""
    m = message.lower()
    
    if "photosynthesis" in m:
        return """🌿 **Photosynthesis**

Plants make their own food using sunlight!

**Equation:** 6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂

**Two stages:**
1. Light reaction - captures sunlight, releases oxygen
2. Calvin cycle - makes glucose from CO₂

**Where it happens:** Chloroplasts in leaves"""

    if "mitosis" in m:
        return """🔬 **Mitosis (PMAT)**

Cell division that produces 2 identical cells!

**Stages:**
• **P**rophase - Chromosomes condense
• **M**etaphase - Line up at center
• **A**naphase - Separate to opposite poles
• **T**elophase - Two new cells form"""

    if "newton" in m:
        return """⚡ **Newton's Laws**

**1st Law (Inertia):** Objects keep doing what they're doing
**2nd Law (F=ma):** Force = mass × acceleration
**3rd Law (Action-Reaction):** Every action has equal opposite reaction"""

    if "hello" in m or "hi" in m:
        return """👋 Hello! I'm KalaX Learn!

Try:
• "What is photosynthesis?"
• "Plot y = x^2"
• "Draw a circle"

Created by Kalamawo Joshua Bright"""

    return f"""📚 **KalaX Learn**

Try these commands:
• 'What is photosynthesis?' - Science
• 'Plot y = x^2' - Parabola graph
• 'Draw a circle' - Geometry

Created by Kalamawo Joshua Bright"""

# ============================================
# FULL PAGE SVG DIAGRAMS (900x700)
# ============================================

FULL_PAGE_CIRCLE = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Circle Geometry</text>
    <circle cx="450" cy="370" r="200" fill="none" stroke="#0f3460" stroke-width="4"/>
    <line x1="450" y1="370" x2="650" y2="370" stroke="#e94560" stroke-width="3" stroke-dasharray="8,6"/>
    <circle cx="450" cy="370" r="8" fill="#e94560"/>
    <text x="560" y="350" fill="#e94560" font-size="20">Radius (r)</text>
    <text x="450" y="400" text-anchor="middle" fill="#0f3460" font-size="20">Center</text>
    <text x="450" y="660" text-anchor="middle" fill="#555" font-size="16">Area = πr² | Circumference = 2πr | π ≈ 3.14159</text>
</svg>'''

FULL_PAGE_SQUARE = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Square Geometry</text>
    <rect x="250" y="200" width="400" height="400" fill="rgba(15,52,96,0.08)" stroke="#0f3460" stroke-width="4"/>
    <line x1="250" y1="200" x2="650" y2="200" stroke="#e94560" stroke-width="3"/>
    <text x="450" y="180" text-anchor="middle" fill="#e94560" font-size="22">Side (s)</text>
    <text x="450" y="660" text-anchor="middle" fill="#555" font-size="16">Area = s² | Perimeter = 4s | All angles = 90°</text>
</svg>'''

FULL_PAGE_RECTANGLE = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Rectangle Geometry</text>
    <rect x="180" y="220" width="540" height="280" fill="rgba(15,52,96,0.08)" stroke="#0f3460" stroke-width="4"/>
    <line x1="180" y1="220" x2="720" y2="220" stroke="#e94560" stroke-width="3"/>
    <text x="450" y="200" text-anchor="middle" fill="#e94560" font-size="22">Length (l)</text>
    <line x1="180" y1="220" x2="180" y2="500" stroke="#4ecdc4" stroke-width="3"/>
    <text x="150" y="360" text-anchor="middle" fill="#4ecdc4" font-size="22">Width (w)</text>
    <text x="450" y="660" text-anchor="middle" fill="#555" font-size="16">Area = l × w | Perimeter = 2(l + w)</text>
</svg>'''

FULL_PAGE_TRIANGLE = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Triangle Geometry</text>
    <polygon points="200,580 700,580 450,180" fill="rgba(15,52,96,0.08)" stroke="#0f3460" stroke-width="4"/>
    <text x="450" y="620" text-anchor="middle" fill="#0f3460" font-size="22">Base (b)</text>
    <line x1="450" y1="180" x2="450" y2="580" stroke="#4ecdc4" stroke-width="3" stroke-dasharray="8,6"/>
    <text x="470" y="380" fill="#4ecdc4" font-size="22">Height (h)</text>
    <text x="450" y="670" text-anchor="middle" fill="#555" font-size="16">Area = ½ × base × height | Sum of angles = 180°</text>
</svg>'''

FULL_PAGE_RIGHT_TRIANGLE = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Right Triangle (Pythagorean Theorem)</text>
    <polygon points="200,560 650,560 200,180" fill="rgba(15,52,96,0.08)" stroke="#0f3460" stroke-width="4"/>
    <polygon points="200,530 230,530 230,560" fill="none" stroke="#e94560" stroke-width="3"/>
    <text x="215" y="550" text-anchor="middle" fill="#e94560" font-size="20">90°</text>
    <text x="425" y="605" text-anchor="middle" fill="#0f3460" font-size="20">Base (b)</text>
    <text x="150" y="370" text-anchor="middle" fill="#0f3460" font-size="20">Height (h)</text>
    <text x="500" y="320" fill="#666" font-size="20">Hypotenuse (c)</text>
    <text x="450" y="670" text-anchor="middle" fill="#555" font-size="16">a² + b² = c² (Pythagorean Theorem)</text>
</svg>'''

FULL_PAGE_EQUILATERAL = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Equilateral Triangle</text>
    <polygon points="450,120 200,580 700,580" fill="rgba(15,52,96,0.08)" stroke="#0f3460" stroke-width="4"/>
    <text x="450" y="95" text-anchor="middle" fill="#e94560" font-size="20">60°</text>
    <text x="160" y="600" text-anchor="middle" fill="#e94560" font-size="20">60°</text>
    <text x="740" y="600" text-anchor="middle" fill="#e94560" font-size="20">60°</text>
    <line x1="450" y1="120" x2="450" y2="580" stroke="#4ecdc4" stroke-width="3" stroke-dasharray="8,6"/>
    <text x="470" y="350" fill="#4ecdc4" font-size="22">Height (h)</text>
    <text x="450" y="670" text-anchor="middle" fill="#555" font-size="16">All sides equal | All angles = 60°</text>
</svg>'''

FULL_PAGE_PENTAGON = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Regular Pentagon</text>
    <polygon points="450,100 700,220 620,500 280,500 200,220" fill="rgba(15,52,96,0.08)" stroke="#0f3460" stroke-width="4"/>
    <text x="450" y="670" text-anchor="middle" fill="#555" font-size="16">Pentagon: 5 sides | Interior angle = 108°</text>
</svg>'''

FULL_PAGE_HEXAGON = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Regular Hexagon</text>
    <polygon points="450,100 700,210 700,490 450,600 200,490 200,210" fill="rgba(15,52,96,0.08)" stroke="#0f3460" stroke-width="4"/>
    <text x="450" y="670" text-anchor="middle" fill="#555" font-size="16">Hexagon: 6 sides | Interior angle = 120°</text>
</svg>'''

FULL_PAGE_OCTAGON = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Regular Octagon</text>
    <polygon points="450,100 650,150 720,320 650,510 450,600 250,510 180,320 250,150" fill="rgba(15,52,96,0.08)" stroke="#0f3460" stroke-width="4"/>
    <text x="450" y="670" text-anchor="middle" fill="#555" font-size="16">Octagon: 8 sides | Interior angle = 135°</text>
</svg>'''

FULL_PAGE_STAR = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Five-Pointed Star</text>
    <polygon points="450,100 510,280 700,280 550,400 620,580 450,470 280,580 350,400 200,280 390,280" fill="rgba(255,215,0,0.15)" stroke="#FFD700" stroke-width="4"/>
    <text x="450" y="670" text-anchor="middle" fill="#555" font-size="16">Star polygon | Golden ratio proportions</text>
</svg>'''

FULL_PAGE_CUBE = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Cube (3D Square)</text>
    <polygon points="350,200 550,200 620,250 420,250" fill="rgba(15,52,96,0.15)" stroke="#0f3460" stroke-width="3"/>
    <polygon points="350,200 420,250 420,450 350,400" fill="rgba(15,52,96,0.08)" stroke="#0f3460" stroke-width="3"/>
    <polygon points="420,250 620,250 620,450 420,450" fill="rgba(15,52,96,0.12)" stroke="#0f3460" stroke-width="3"/>
    <text x="450" y="670" text-anchor="middle" fill="#555" font-size="16">Cube: Volume = s³ | Surface Area = 6s²</text>
</svg>'''

FULL_PAGE_SPHERE = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Sphere (3D Circle)</text>
    <circle cx="450" cy="370" r="180" fill="rgba(15,52,96,0.08)" stroke="#0f3460" stroke-width="4"/>
    <ellipse cx="450" cy="370" rx="180" ry="50" fill="none" stroke="#e94560" stroke-width="2"/>
    <ellipse cx="450" cy="370" rx="50" ry="180" fill="none" stroke="#4ecdc4" stroke-width="2"/>
    <text x="450" y="670" text-anchor="middle" fill="#555" font-size="16">Sphere: Volume = ⁴⁄₃πr³ | Surface Area = 4πr²</text>
</svg>'''

FULL_PAGE_CYLINDER = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Cylinder (3D)</text>
    <ellipse cx="450" cy="180" rx="160" ry="45" fill="rgba(15,52,96,0.15)" stroke="#0f3460" stroke-width="3"/>
    <rect x="290" y="180" width="320" height="340" fill="rgba(15,52,96,0.08)" stroke="#0f3460" stroke-width="3"/>
    <ellipse cx="450" cy="520" rx="160" ry="45" fill="rgba(15,52,96,0.12)" stroke="#0f3460" stroke-width="3"/>
    <line x1="290" y1="180" x2="290" y2="520" stroke="#e94560" stroke-width="3" stroke-dasharray="8,6"/>
    <text x="260" y="350" text-anchor="end" fill="#e94560" font-size="22">Height (h)</text>
    <text x="450" y="670" text-anchor="middle" fill="#555" font-size="16">Volume = πr²h | Surface Area = 2πrh + 2πr²</text>
</svg>'''

FULL_PAGE_SINE_WAVE = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Sine Wave: y = sin(x)</text>
    <g transform="translate(0, 100)">
        <path d="M50,250 Q90,100 130,250 T210,250 T290,250 T370,250 T450,250 T530,250 T610,250 T690,250 T770,250 T850,250" fill="none" stroke="#e94560" stroke-width="4"/>
        <line x1="50" y1="250" x2="850" y2="250" stroke="#333" stroke-width="2"/>
        <line x1="450" y1="50" x2="450" y2="450" stroke="#333" stroke-width="1.5" stroke-dasharray="6,4"/>
        <text x="860" y="255" fill="#333" font-size="18">x</text>
        <text x="460" y="45" fill="#333" font-size="18">y</text>
    </g>
</svg>'''

FULL_PAGE_COSINE_WAVE = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Cosine Wave: y = cos(x)</text>
    <g transform="translate(0, 100)">
        <path d="M50,150 Q90,250 130,150 T210,150 T290,150 T370,150 T450,150 T530,150 T610,150 T690,150 T770,150 T850,150" fill="none" stroke="#e94560" stroke-width="4"/>
        <line x1="50" y1="250" x2="850" y2="250" stroke="#333" stroke-width="2"/>
        <text x="860" y="255" fill="#333" font-size="18">x</text>
        <text x="460" y="45" fill="#333" font-size="18">y</text>
    </g>
</svg>'''

FULL_PAGE_PARABOLA = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Parabola: y = x²</text>
    <path d="M150,500 Q300,200 450,150 Q600,200 750,500" fill="none" stroke="#e94560" stroke-width="4"/>
    <line x1="80" y1="500" x2="820" y2="500" stroke="#333" stroke-width="2"/>
    <line x1="450" y1="80" x2="450" y2="550" stroke="#333" stroke-width="2"/>
    <text x="830" y="510" fill="#333" font-size="18">x</text>
    <text x="460" y="70" fill="#333" font-size="18">y</text>
</svg>'''

FULL_PAGE_HYPERBOLA = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Hyperbola: y = 1/x</text>
    <path d="M200,300 Q280,220 380,180" fill="none" stroke="#e94560" stroke-width="4"/>
    <path d="M200,400 Q280,480 380,520" fill="none" stroke="#e94560" stroke-width="4"/>
    <path d="M700,300 Q620,220 520,180" fill="none" stroke="#4ecdc4" stroke-width="4"/>
    <path d="M700,400 Q620,480 520,520" fill="none" stroke="#4ecdc4" stroke-width="4"/>
    <line x1="80" y1="350" x2="820" y2="350" stroke="#333" stroke-width="2"/>
    <line x1="450" y1="80" x2="450" y2="620" stroke="#333" stroke-width="2"/>
</svg>'''

FULL_PAGE_COORDINATE_PLANE = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Cartesian Coordinate Plane</text>
    <line x1="80" y1="350" x2="820" y2="350" stroke="#333" stroke-width="3"/>
    <line x1="450" y1="80" x2="450" y2="620" stroke="#333" stroke-width="3"/>
    <polygon points="810,345 830,350 810,355" fill="#333"/>
    <polygon points="445,90 450,70 455,90" fill="#333"/>
    <text x="835" y="360" fill="#333" font-size="20">x</text>
    <text x="460" y="65" fill="#333" font-size="20">y</text>
    <text x="460" y="365" fill="#333" font-size="18">O</text>
</svg>'''

FULL_PAGE_BAR_CHART = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Bar Chart</text>
    <rect x="100" y="500" width="80" height="100" fill="#0f3460"/>
    <rect x="220" y="420" width="80" height="180" fill="#e94560"/>
    <rect x="340" y="340" width="80" height="260" fill="#4ecdc4"/>
    <rect x="460" y="260" width="80" height="340" fill="#ff9800"/>
    <rect x="580" y="180" width="80" height="420" fill="#9c27b0"/>
    <rect x="700" y="460" width="80" height="140" fill="#00bcd4"/>
    <line x1="60" y1="600" x2="820" y2="600" stroke="#333" stroke-width="2"/>
    <line x1="60" y1="100" x2="60" y2="600" stroke="#333" stroke-width="2"/>
    <text x="140" y="630" text-anchor="middle" font-size="14">A</text><text x="260" y="630" text-anchor="middle" font-size="14">B</text>
    <text x="380" y="630" text-anchor="middle" font-size="14">C</text><text x="500" y="630" text-anchor="middle" font-size="14">D</text>
    <text x="620" y="630" text-anchor="middle" font-size="14">E</text><text x="740" y="630" text-anchor="middle" font-size="14">F</text>
</svg>'''

FULL_PAGE_PIE_CHART = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Pie Chart</text>
    <circle cx="400" cy="380" r="180" fill="white" stroke="#333" stroke-width="3"/>
    <path d="M400,380 L400,200 A180,180 0 0,1 578,332 Z" fill="#0f3460"/>
    <path d="M400,380 L578,332 A180,180 0 0,1 490,538 Z" fill="#e94560"/>
    <path d="M400,380 L490,538 A180,180 0 0,1 310,538 Z" fill="#4ecdc4"/>
    <path d="M400,380 L310,538 A180,180 0 0,1 250,300 Z" fill="#ff9800"/>
    <path d="M400,380 L250,300 A180,180 0 0,1 400,200 Z" fill="#9c27b0"/>
</svg>'''

FULL_PAGE_VENN = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Venn Diagram</text>
    <circle cx="350" cy="380" r="140" fill="rgba(15,52,96,0.15)" stroke="#0f3460" stroke-width="3"/>
    <circle cx="550" cy="380" r="140" fill="rgba(233,69,96,0.15)" stroke="#e94560" stroke-width="3"/>
    <text x="300" y="370" text-anchor="middle" font-size="22" fill="#0f3460">Set A</text>
    <text x="600" y="370" text-anchor="middle" font-size="22" fill="#e94560">Set B</text>
    <text x="450" y="390" text-anchor="middle" font-size="20" fill="#333">A ∩ B</text>
</svg>'''

FULL_PAGE_RIGHT_ANGLE = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Right Angle (90°)</text>
    <line x1="200" y1="520" x2="700" y2="520" stroke="#0f3460" stroke-width="5"/>
    <line x1="200" y1="520" x2="200" y2="120" stroke="#0f3460" stroke-width="5"/>
    <polygon points="200,480 240,480 240,520" fill="none" stroke="#e94560" stroke-width="3"/>
    <text x="220" y="505" text-anchor="middle" fill="#e94560" font-size="24">90°</text>
</svg>'''

FULL_PAGE_PARALLEL_LINES = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Parallel Lines</text>
    <line x1="150" y1="250" x2="750" y2="250" stroke="#0f3460" stroke-width="4"/>
    <line x1="150" y1="450" x2="750" y2="450" stroke="#0f3460" stroke-width="4"/>
    <line x1="300" y1="250" x2="300" y2="450" stroke="#666" stroke-width="1.5" stroke-dasharray="8,6"/>
    <text x="310" y="355" fill="#e94560" font-size="18">distance</text>
</svg>'''

FULL_PAGE_PERPENDICULAR = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Perpendicular Lines</text>
    <line x1="200" y1="500" x2="700" y2="500" stroke="#0f3460" stroke-width="4"/>
    <line x1="450" y1="150" x2="450" y2="550" stroke="#0f3460" stroke-width="4"/>
    <polygon points="445,495 455,495 455,505" fill="none" stroke="#e94560" stroke-width="3"/>
    <text x="430" y="520" fill="#e94560" font-size="22">90°</text>
</svg>'''

FULL_PAGE_NUMBER_LINE = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Number Line</text>
    <line x1="100" y1="350" x2="800" y2="350" stroke="#333" stroke-width="3"/>
    <polygon points="790,345 810,350 790,355" fill="#333"/>
    <g font-size="22" text-anchor="middle" fill="#333">
        <text x="120" y="390">-6</text><text x="200" y="390">-4</text><text x="280" y="390">-2</text>
        <text x="360" y="390">0</text><text x="440" y="390">2</text><text x="520" y="390">4</text>
        <text x="600" y="390">6</text><text x="680" y="390">8</text><text x="760" y="390">10</text>
    </g>
    <g stroke="#333" stroke-width="2">
        <line x1="120" y1="340" x2="120" y2="360"/><line x1="200" y1="340" x2="200" y2="360"/>
        <line x1="280" y1="340" x2="280" y2="360"/><line x1="360" y1="340" x2="360" y2="360"/>
        <line x1="440" y1="340" x2="440" y2="360"/><line x1="520" y1="340" x2="520" y2="360"/>
        <line x1="600" y1="340" x2="600" y2="360"/><line x1="680" y1="340" x2="680" y2="360"/>
        <line x1="760" y1="340" x2="760" y2="360"/>
    </g>
    <circle cx="360" cy="350" r="10" fill="#e94560"/>
    <text x="360" y="330" text-anchor="middle" fill="#e94560" font-size="16">0</text>
</svg>'''

FULL_PAGE_HEART = '''<svg width="900" height="700" viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
    <rect width="900" height="700" fill="#faf8f0"/>
    <rect x="20" y="20" width="860" height="660" rx="10" fill="none" stroke="#2c3e50" stroke-width="2"/>
    <text x="450" y="55" text-anchor="middle" font-size="24" font-weight="bold" fill="#2c3e50">Heart Shape</text>
    <path d="M450,620 C250,480 180,550 450,680 C720,550 650,480 450,620" fill="#FF6B6B" stroke="#c92a2a" stroke-width="3"/>
    <text x="450" y="670" text-anchor="middle" fill="#555" font-size="16">Symmetrical geometric curve</text>
</svg>'''

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)