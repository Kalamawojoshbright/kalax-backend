"""
KalaX Backend - Complete Working Version
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import math
import re
from datetime import datetime

app = FastAPI()

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
        "creator": "Kalamawo Joshua Bright"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": str(datetime.now())}

# ============================================
# CHAT ENDPOINT
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer questions"""
    return ChatResponse(
        response=get_response(request.message),
        source="local"
    )

# ============================================
# DRAW ENDPOINT
# ============================================

@app.post("/draw", response_model=DrawResponse)
async def draw(request: DrawRequest):
    """Draw diagrams"""
    cmd = request.command.lower()
    
    # BIOLOGY DIAGRAMS
    if "skeleton" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_skeleton_svg(),
            explanation="Human Skeleton - 206 bones"
        )
    
    if "brain" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_brain_svg(),
            explanation="Human Brain - Cerebrum, Cerebellum, Brain Stem"
        )
    
    if "heart" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_heart_svg(),
            explanation="Human Heart - 4 chambers"
        )
    
    if "eye" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_eye_svg(),
            explanation="Human Eye - Cornea, Iris, Pupil, Lens, Retina"
        )
    
    if "lung" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_lungs_svg(),
            explanation="Respiratory System - Lungs, Trachea, Bronchi"
        )
    
    # GEOMETRIC SHAPES
    if "circle" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_circle_svg(),
            explanation="Circle: Area = πr², Circumference = 2πr"
        )
    
    if "square" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_square_svg(),
            explanation="Square: Area = s², Perimeter = 4s"
        )
    
    if "triangle" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_triangle_svg(),
            explanation="Right Triangle: a² + b² = c²"
        )
    
    # MATHEMATICAL GRAPHS
    if "plot" in cmd or "graph" in cmd or "y=" in cmd:
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
    
    # CELL DIAGRAMS
    if "animal cell" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_animal_cell_svg(),
            explanation="Animal Cell - Nucleus, Mitochondria, Cell Membrane"
        )
    
    if "plant cell" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_plant_cell_svg(),
            explanation="Plant Cell - Cell Wall, Chloroplasts, Vacuole"
        )
    
    # FALLBACK
    return DrawResponse(
        success=False,
        type="error",
        error="Try: 'Draw a skeleton', 'Draw a brain', 'Draw a heart', 'Draw a circle', or 'Plot y = x^2'"
    )

# ============================================
# RESPONSE GENERATOR
# ============================================

def get_response(message: str) -> str:
    m = message.lower()
    
    if "photosynthesis" in m:
        return """🌿 **Photosynthesis**

Plants make their own food using sunlight!

**Equation:** 6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂

**Two stages:**
1. Light reaction - captures sunlight, releases oxygen
2. Calvin cycle - makes glucose from CO₂

**Where:** Chloroplasts in leaves"""

    if "mitosis" in m:
        return """🔬 **Mitosis (PMAT)**

Cell division stages:
• **P**rophase - Chromosomes condense
• **M**etaphase - Line up at center
• **A**naphase - Separate to poles
• **T**elophase - Two new cells form

**Result:** 2 identical daughter cells!"""

    if "newton" in m:
        return """⚡ **Newton's Laws**

**1st Law (Inertia):** Objects keep doing what they're doing
**2nd Law (F=ma):** Force = mass × acceleration
**3rd Law (Action-Reaction):** Every action has equal opposite reaction"""

    if "hello" in m or "hi" in m:
        return "👋 Hello! I'm KalaX AI. Try 'Draw a skeleton', 'Draw a brain', or 'What is photosynthesis?'"

    return f"""📚 I'm KalaX AI.

Try these commands:
• 'Draw a skeleton' - Human skeleton diagram
• 'Draw a brain' - Brain anatomy
• 'Draw a heart' - Heart diagram
• 'Draw a circle' - Geometry
• 'Plot y = x^2' - Mathematical graph
• 'What is photosynthesis?' - Science explanation

Created by Kalamawo Joshua Bright"""

# ============================================
# SVG DIAGRAMS
# ============================================

def get_skeleton_svg():
    return '''<svg width="500" height="600" viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="500" height="600" fill="#faf8f0"/>
        <text x="250" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Human Skeleton</text>
        <!-- Skull -->
        <ellipse cx="250" cy="80" rx="40" ry="50" fill="#f0e6d2" stroke="#8B7355" stroke-width="2"/>
        <!-- Eye sockets -->
        <ellipse cx="232" cy="75" rx="8" ry="10" fill="#8B7355"/>
        <ellipse cx="268" cy="75" rx="8" ry="10" fill="#8B7355"/>
        <!-- Spine -->
        <line x1="250" y1="135" x2="250" y2="400" stroke="#8B7355" stroke-width="3"/>
        <!-- Ribs -->
        <g fill="none" stroke="#8B7355" stroke-width="2">
            <path d="M250,160 Q210,170 215,160"/><path d="M250,160 Q290,170 285,160"/>
            <path d="M250,180 Q205,190 210,180"/><path d="M250,180 Q295,190 290,180"/>
            <path d="M250,200 Q200,210 205,200"/><path d="M250,200 Q300,210 295,200"/>
            <path d="M250,220 Q198,228 203,220"/><path d="M250,220 Q302,228 297,220"/>
        </g>
        <!-- Arms -->
        <line x1="220" y1="160" x2="180" y2="220" x2="190" y2="280" stroke="#8B7355" stroke-width="3"/>
        <line x1="280" y1="160" x2="320" y2="220" x2="310" y2="280" stroke="#8B7355" stroke-width="3"/>
        <!-- Pelvis -->
        <ellipse cx="250" cy="360" rx="50" ry="20" fill="#f0e6d2" stroke="#8B7355" stroke-width="2"/>
        <!-- Legs -->
        <line x1="225" y1="370" x2="220" y2="440" x2="210" y2="470" stroke="#8B7355" stroke-width="3"/>
        <line x1="275" y1="370" x2="280" y2="440" x2="290" y2="470" stroke="#8B7355" stroke-width="3"/>
        <!-- Labels -->
        <text x="250" y="590" text-anchor="middle" font-size="12" fill="#666">206 bones | Axial + Appendicular skeleton</text>
    </svg>'''

def get_brain_svg():
    return '''<svg width="550" height="400" viewBox="0 0 550 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="550" height="400" fill="#faf8f0"/>
        <text x="275" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Human Brain</text>
        <!-- Left Hemisphere -->
        <path d="M275,120 Q230,100 200,130 Q170,160 165,200 Q160,240 175,270 Q190,300 220,310 L275,300" fill="#FFB6C1" stroke="#c92a6a" stroke-width="2"/>
        <!-- Right Hemisphere -->
        <path d="M275,120 Q320,100 350,130 Q380,160 385,200 Q390,240 375,270 Q360,300 330,310 L275,300" fill="#FFB6C1" stroke="#c92a6a" stroke-width="2"/>
        <!-- Brain Stem -->
        <path d="M265,300 Q260,340 255,370 L275,380 L295,370 Q290,340 285,300" fill="#FFB6C1" stroke="#c92a6a" stroke-width="2"/>
        <!-- Cerebellum -->
        <path d="M230,320 Q210,340 220,365 Q235,380 260,370 L275,350" fill="#FFB6C1" stroke="#c92a6a" stroke-width="2"/>
        <path d="M320,320 Q340,340 330,365 Q315,380 290,370 L275,350" fill="#FFB6C1" stroke="#c92a6a" stroke-width="2"/>
        <!-- Labels -->
        <text x="275" y="60" text-anchor="middle" font-size="12" font-weight="bold" fill="#c92a6a">Cerebrum</text>
        <text x="180" y="340" font-size="11" font-weight="bold" fill="#c92a6a">Cerebellum</text>
        <text x="360" y="340" font-size="11" font-weight="bold" fill="#c92a6a">Cerebellum</text>
        <text x="230" y="390" font-size="11" font-weight="bold" fill="#c92a6a">Brain Stem</text>
    </svg>'''

def get_heart_svg():
    return '''<svg width="500" height="450" viewBox="0 0 500 450" xmlns="http://www.w3.org/2000/svg">
        <rect width="500" height="450" fill="#faf8f0"/>
        <text x="250" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Human Heart</text>
        <!-- Heart shape -->
        <path d="M250,370 C130,280 80,340 250,420 C420,340 370,280 250,370" fill="#FF6B6B" stroke="#c92a2a" stroke-width="2"/>
        <!-- Aorta -->
        <path d="M250,280 Q270,250 260,210 Q250,190 230,200 Q220,210 225,230 Q230,250 250,270" fill="#FF6B6B" stroke="#c92a2a" stroke-width="2"/>
        <!-- Septum -->
        <line x1="250" y1="305" x2="250" y2="390" stroke="#a04040" stroke-width="2"/>
        <!-- Labels -->
        <text x="250" y="440" text-anchor="middle" font-size="12" fill="#666">4 chambers | Pumps blood throughout body</text>
    </svg>'''

def get_eye_svg():
    return '''<svg width="500" height="400" viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="500" height="400" fill="#faf8f0"/>
        <text x="250" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Human Eye</text>
        <!-- Eye shape -->
        <ellipse cx="250" cy="200" rx="140" ry="80" fill="#ffffff" stroke="#333" stroke-width="2"/>
        <!-- Iris -->
        <circle cx="250" cy="200" r="45" fill="#4a7023" stroke="#2d4a15" stroke-width="1.5"/>
        <!-- Pupil -->
        <circle cx="250" cy="200" r="20" fill="#000000"/>
        <!-- Lens -->
        <ellipse cx="250" cy="200" rx="25" ry="18" fill="#fff3c9" stroke="#c4a44a" stroke-width="1.5"/>
        <!-- Light reflections -->
        <circle cx="240" cy="188" r="6" fill="white" opacity="0.8"/>
        <!-- Labels -->
        <text x="250" y="390" text-anchor="middle" font-size="12" fill="#666">Light → Cornea → Pupil → Lens → Retina → Brain</text>
    </svg>'''

def get_lungs_svg():
    return '''<svg width="550" height="480" viewBox="0 0 550 480" xmlns="http://www.w3.org/2000/svg">
        <rect width="550" height="480" fill="#faf8f0"/>
        <text x="275" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Respiratory System</text>
        <!-- Trachea -->
        <rect x="265" y="60" width="20" height="90" rx="5" fill="#d4a574" stroke="#8B5A2B" stroke-width="2"/>
        <!-- Bronchi -->
        <path d="M275,150 Q240,170 180,200" fill="none" stroke="#d4a574" stroke-width="8"/>
        <path d="M275,150 Q310,170 370,200" fill="none" stroke="#d4a574" stroke-width="8"/>
        <!-- Left Lung -->
        <path d="M180,200 Q140,220 130,280 Q120,350 150,400 Q180,430 230,420 L270,380 Z" fill="#e8c4c4" stroke="#a06060" stroke-width="2"/>
        <!-- Right Lung -->
        <path d="M370,200 Q410,220 420,280 Q430,350 400,420 Q370,440 320,430 L280,380 Z" fill="#e8c4c4" stroke="#a06060" stroke-width="2"/>
        <!-- Diaphragm -->
        <path d="M120,420 Q275,460 430,420" fill="none" stroke="#8B5A2B" stroke-width="3"/>
        <!-- Labels -->
        <text x="275" y="470" text-anchor="middle" font-size="12" fill="#666">Oxygen enters, CO₂ exits | Gas exchange in alveoli</text>
    </svg>'''

def get_circle_svg():
    return '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="400" fill="#f8f9fa"/>
        <circle cx="200" cy="200" r="120" fill="none" stroke="#0f3460" stroke-width="3"/>
        <line x1="200" y1="200" x2="320" y2="200" stroke="#e94560" stroke-width="2" stroke-dasharray="5,5"/>
        <circle cx="200" cy="200" r="5" fill="#e94560"/>
        <text x="260" y="190" fill="#e94560" font-size="14">Radius (r)</text>
        <text x="200" y="220" text-anchor="middle" fill="#0f3460" font-size="14">Center</text>
        <text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Area = πr², Circumference = 2πr</text>
    </svg>'''

def get_square_svg():
    return '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="400" fill="#f8f9fa"/>
        <rect x="100" y="100" width="200" height="200" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/>
        <line x1="100" y1="100" x2="300" y2="100" stroke="#e94560" stroke-width="2"/>
        <text x="200" y="90" text-anchor="middle" fill="#e94560" font-size="14">Side (s)</text>
        <text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Area = s², Perimeter = 4s</text>
    </svg>'''

def get_triangle_svg():
    return '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="400" fill="#f8f9fa"/>
        <polygon points="80,300 300,300 80,100" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/>
        <polygon points="80,280 100,280 100,300" fill="none" stroke="#e94560" stroke-width="2"/>
        <text x="90" y="295" text-anchor="middle" fill="#e94560" font-size="14">90°</text>
        <text x="190" y="320" text-anchor="middle" fill="#0f3460" font-size="14">Base</text>
        <text x="65" y="200" text-anchor="middle" fill="#0f3460" font-size="14" transform="rotate(-90 65 200)">Height</text>
        <text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">a² + b² = c² (Pythagorean Theorem)</text>
    </svg>'''

def get_animal_cell_svg():
    return '''<svg width="550" height="450" viewBox="0 0 550 450" xmlns="http://www.w3.org/2000/svg">
        <rect width="550" height="450" fill="#faf8f0"/>
        <text x="275" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Animal Cell Structure</text>
        <ellipse cx="275" cy="220" rx="200" ry="170" fill="#e8f8f0" stroke="#0f3460" stroke-width="3" stroke-dasharray="8,4"/>
        <ellipse cx="275" cy="190" rx="70" ry="55" fill="#e8f0e8" stroke="#2d6a4f" stroke-width="2.5"/>
        <text x="275" y="175" text-anchor="middle" font-size="12" font-weight="bold" fill="#2d6a4f">Nucleus</text>
        <ellipse cx="160" cy="150" rx="45" ry="25" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
        <text x="160" y="115" text-anchor="middle" font-size="11" font-weight="bold" fill="#e65100">Mitochondria</text>
        <text x="275" y="430" text-anchor="middle" font-size="12" fill="#666" font-style="italic">Basic unit of animal life</text>
    </svg>'''

def get_plant_cell_svg():
    return '''<svg width="550" height="450" viewBox="0 0 550 450" xmlns="http://www.w3.org/2000/svg">
        <rect width="550" height="450" fill="#faf8f0"/>
        <text x="275" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Plant Cell Structure</text>
        <rect x="60" y="60" width="430" height="340" rx="10" fill="none" stroke="#8B4513" stroke-width="3"/>
        <rect x="75" y="75" width="400" height="310" rx="8" fill="none" stroke="#0f3460" stroke-width="2.5" stroke-dasharray="6,3"/>
        <ellipse cx="275" cy="190" rx="55" ry="45" fill="#e8f0e8" stroke="#2d6a4f" stroke-width="2.5"/>
        <text x="275" y="185" text-anchor="middle" font-size="12" font-weight="bold" fill="#2d6a4f">Nucleus</text>
        <ellipse cx="420" cy="160" rx="35" ry="22" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
        <text x="420" y="130" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Chloroplast</text>
        <ellipse cx="180" cy="220" rx="55" ry="65" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
        <text x="180" y="200" text-anchor="middle" font-size="11" font-weight="bold" fill="#1565c0">Vacuole</text>
        <text x="275" y="430" text-anchor="middle" font-size="12" fill="#666" font-style="italic">Unique: Cell wall, Chloroplasts, Large vacuole</text>
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
            func = function.replace('^', '**')
            y = eval(func, {"x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                           "sqrt": math.sqrt, "exp": math.exp, "log": math.log, "pi": math.pi})
            
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

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)