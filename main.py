"""
KalaX Backend - Professional Biology Diagrams
Anatomically accurate SVG diagrams
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import math
import re
from datetime import datetime

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
    return {"status": "healthy", "timestamp": str(datetime.now())}

# ============================================
# CHAT ENDPOINT
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer questions using local responses"""
    return ChatResponse(
        response=get_local_fallback(request.message),
        source="local"
    )

# ============================================
# DRAW ENDPOINT
# ============================================

@app.post("/draw", response_model=DrawResponse)
async def draw(request: DrawRequest):
    """Route drawing requests"""
    
    cmd = request.command.lower()
    
    # ========== PROFESSIONAL BIOLOGY DIAGRAMS ==========
    
    if "skeleton" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_professional_skeleton(),
            explanation="Human Skeleton - 206 bones. Axial skeleton (skull, spine, ribs) + Appendicular skeleton (arms, legs)"
        )
    
    if "brain" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_professional_brain(),
            explanation="Human Brain - Cerebrum (thinking), Cerebellum (balance), Brain Stem (life functions)"
        )
    
    if "heart" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_professional_heart(),
            explanation="Human Heart - Pumps blood through 4 chambers: Right/Left Atrium, Right/Left Ventricle"
        )
    
    if "eye" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_professional_eye(),
            explanation="Human Eye - Light enters through cornea, focused by lens, detected by retina"
        )
    
    if "lung" in cmd or "lungs" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_professional_lungs(),
            explanation="Respiratory System - Oxygen enters lungs, CO₂ exits. Gas exchange occurs in alveoli"
        )
    
    if "cell" in cmd and "animal" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_animal_cell(),
            explanation="Animal Cell - Nucleus (DNA), Mitochondria (energy), Cell membrane (control)"
        )
    
    if "cell" in cmd and "plant" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_plant_cell(),
            explanation="Plant Cell - Cell wall (structure), Chloroplasts (photosynthesis), Vacuole (storage)"
        )
    
    # ========== GEOMETRIC SHAPES ==========
    
    if "circle" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_circle_svg(),
            explanation="Circle: All points equidistant from center. Area = πr², Circumference = 2πr"
        )
    
    if "square" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_square_svg(),
            explanation="Square: All sides equal, 4 right angles (90°). Area = s², Perimeter = 4s"
        )
    
    if "triangle" in cmd or "right angle" in cmd:
        return DrawResponse(
            success=True,
            type="svg",
            svg=get_triangle_svg(),
            explanation="Right Triangle: Pythagorean Theorem a² + b² = c²"
        )
    
    # ========== MATHEMATICAL GRAPHS ==========
    
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
    
    # ========== FALLBACK ==========
    
    return DrawResponse(
        success=False,
        type="error",
        error="Try: 'Draw a skeleton', 'Draw a brain', 'Draw a heart', 'Draw a circle', or 'Plot y = x^2'"
    )

# ============================================
# PROFESSIONAL BIOLOGY SVG DIAGRAMS
# ============================================

def get_professional_skeleton():
    return '''<svg width="500" height="600" viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="500" height="600" fill="#faf8f0"/>
        <text x="250" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Human Skeleton</text>
        
        <!-- Skull -->
        <ellipse cx="250" cy="80" rx="40" ry="50" fill="#f0e6d2" stroke="#8B7355" stroke-width="2"/>
        <ellipse cx="250" cy="110" rx="28" ry="18" fill="#f0e6d2" stroke="#8B7355" stroke-width="1.5"/>
        <!-- Eye sockets -->
        <ellipse cx="232" cy="75" rx="8" ry="10" fill="#8B7355"/>
        <ellipse cx="268" cy="75" rx="8" ry="10" fill="#8B7355"/>
        <!-- Nose cavity -->
        <path d="M245,90 L250,98 L255,90" fill="#8B7355" stroke="#8B7355" stroke-width="1"/>
        
        <!-- Spine (Vertebral column) -->
        <line x1="250" y1="135" x2="250" y2="400" stroke="#8B7355" stroke-width="3"/>
        <!-- Vertebrae marks -->
        <g stroke="#a08060" stroke-width="1.5">
            <line x1="238" y1="150" x2="262" y2="150"/>
            <line x1="236" y1="170" x2="264" y2="170"/>
            <line x1="234" y1="190" x2="266" y2="190"/>
            <line x1="233" y1="210" x2="267" y2="210"/>
            <line x1="233" y1="230" x2="267" y2="230"/>
            <line x1="234" y1="250" x2="266" y2="250"/>
            <line x1="235" y1="270" x2="265" y2="270"/>
            <line x1="237" y1="290" x2="263" y2="290"/>
            <line x1="239" y1="310" x2="261" y2="310"/>
            <line x1="241" y1="330" x2="259" y2="330"/>
            <line x1="243" y1="350" x2="257" y2="350"/>
            <line x1="245" y1="370" x2="255" y2="370"/>
        </g>
        
        <!-- Ribcage -->
        <g fill="none" stroke="#8B7355" stroke-width="2">
            <path d="M250,155 Q210,165 200,175 Q195,180 200,185"/>
            <path d="M250,155 Q290,165 300,175 Q305,180 300,185"/>
            <path d="M250,175 Q205,185 195,198 Q190,205 195,210"/>
            <path d="M250,175 Q295,185 305,198 Q310,205 305,210"/>
            <path d="M250,195 Q200,205 190,220 Q185,228 190,235"/>
            <path d="M250,195 Q300,205 310,220 Q315,228 310,235"/>
            <path d="M250,215 Q198,228 188,245 Q183,252 188,258"/>
            <path d="M250,215 Q302,228 312,245 Q317,252 312,258"/>
            <path d="M250,235 Q200,248 192,262 Q188,268 192,274"/>
            <path d="M250,235 Q300,248 308,262 Q312,268 308,274"/>
            <path d="M250,255 Q205,265 198,278 Q195,284 198,290"/>
            <path d="M250,255 Q295,265 302,278 Q305,284 302,290"/>
        </g>
        
        <!-- Sternum (breastbone) -->
        <rect x="245" y="155" width="10" height="140" rx="3" fill="#f0e6d2" stroke="#8B7355" stroke-width="1.5"/>
        
        <!-- Clavicles (collarbones) -->
        <path d="M250,140 Q220,130 190,135" fill="none" stroke="#8B7355" stroke-width="3"/>
        <path d="M250,140 Q280,130 310,135" fill="none" stroke="#8B7355" stroke-width="3"/>
        
        <!-- Scapulae (shoulder blades) -->
        <path d="M190,140 Q170,160 175,190 Q180,200 190,195" fill="#f0e6d2" stroke="#8B7355" stroke-width="1.5"/>
        <path d="M310,140 Q330,160 325,190 Q320,200 310,195" fill="#f0e6d2" stroke="#8B7355" stroke-width="1.5"/>
        
        <!-- Arms -->
        <!-- Left Humerus -->
        <line x1="190" y1="160" x2="155" y2="230" stroke="#8B7355" stroke-width="3"/>
        <circle cx="155" cy="230" r="8" fill="#f0e6d2" stroke="#8B7355" stroke-width="1.5"/>
        <!-- Left Radius/Ulna -->
        <line x1="155" y1="235" x2="135" y2="310" stroke="#8B7355" stroke-width="2.5"/>
        <line x1="155" y1="235" x2="148" y2="310" stroke="#8B7355" stroke-width="2"/>
        <!-- Left Hand -->
        <ellipse cx="140" cy="320" rx="12" ry="8" fill="#f0e6d2" stroke="#8B7355" stroke-width="1.5"/>
        
        <!-- Right Humerus -->
        <line x1="310" y1="160" x2="345" y2="230" stroke="#8B7355" stroke-width="3"/>
        <circle cx="345" cy="230" r="8" fill="#f0e6d2" stroke="#8B7355" stroke-width="1.5"/>
        <!-- Right Radius/Ulna -->
        <line x1="345" y1="235" x2="365" y2="310" stroke="#8B7355" stroke-width="2.5"/>
        <line x1="345" y1="235" x2="352" y2="310" stroke="#8B7355" stroke-width="2"/>
        <!-- Right Hand -->
        <ellipse cx="360" cy="320" rx="12" ry="8" fill="#f0e6d2" stroke="#8B7355" stroke-width="1.5"/>
        
        <!-- Pelvis (Hip bone) -->
        <path d="M250,400 Q220,395 200,410 Q190,420 195,435 Q200,445 220,440 L250,430 L280,440 Q300,445 305,435 Q310,420 300,410 Q280,395 250,400" fill="#f0e6d2" stroke="#8B7355" stroke-width="2"/>
        
        <!-- Legs -->
        <!-- Left Femur -->
        <line x1="225" y1="410" x2="215" y2="490" stroke="#8B7355" stroke-width="3.5"/>
        <!-- Left Knee -->
        <ellipse cx="213" cy="495" rx="10" ry="6" fill="#f0e6d2" stroke="#8B7355" stroke-width="1.5"/>
        <!-- Left Tibia/Fibula -->
        <line x1="212" y1="500" x2="200" y2="560" stroke="#8B7355" stroke-width="3"/>
        <line x1="212" y1="500" x2="210" y2="560" stroke="#8B7355" stroke-width="2"/>
        <!-- Left Foot -->
        <ellipse cx="200" cy="570" rx="20" ry="8" fill="#f0e6d2" stroke="#8B7355" stroke-width="1.5"/>
        
        <!-- Right Femur -->
        <line x1="275" y1="410" x2="285" y2="490" stroke="#8B7355" stroke-width="3.5"/>
        <!-- Right Knee -->
        <ellipse cx="287" cy="495" rx="10" ry="6" fill="#f0e6d2" stroke="#8B7355" stroke-width="1.5"/>
        <!-- Right Tibia/Fibula -->
        <line x1="288" y1="500" x2="300" y2="560" stroke="#8B7355" stroke-width="3"/>
        <line x1="288" y1="500" x2="290" y2="560" stroke="#8B7355" stroke-width="2"/>
        <!-- Right Foot -->
        <ellipse cx="300" cy="570" rx="20" ry="8" fill="#f0e6d2" stroke="#8B7355" stroke-width="1.5"/>
        
        <!-- Labels -->
        <text x="160" y="110" font-size="10" fill="#555">Skull</text>
        <text x="315" y="170" font-size="10" fill="#555">Clavicle</text>
        <text x="180" y="200" font-size="10" fill="#555">Scapula</text>
        <text x="130" y="270" font-size="10" fill="#555">Humerus</text>
        <text x="110" y="340" font-size="10" fill="#555">Radius/Ulna</text>
        <text x="260" y="300" font-size="10" fill="#555">Ribcage</text>
        <text x="260" y="370" font-size="10" fill="#555">Spine</text>
        <text x="195" y="455" font-size="10" fill="#555">Pelvis</text>
        <text x="195" y="525" font-size="10" fill="#555">Femur</text>
        <text x="180" y="585" font-size="10" fill="#555">Tibia/Fibula</text>
        
        <text x="250" y="595" text-anchor="middle" font-size="11" fill="#666" font-style="italic">Axial + Appendicular Skeleton (206 bones)</text>
    </svg>'''

def get_professional_brain():
    return '''<svg width="550" height="450" viewBox="0 0 550 450" xmlns="http://www.w3.org/2000/svg">
        <rect width="550" height="450" fill="#faf8f0"/>
        <text x="275" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Human Brain</text>
        
        <!-- Left Hemisphere -->
        <path d="M275,120 Q230,100 200,130 Q170,160 165,200 Q160,240 175,270 Q190,300 220,310 Q240,315 260,310 L275,300" fill="#FFB6C1" stroke="#c92a6a" stroke-width="2"/>
        
        <!-- Right Hemisphere -->
        <path d="M275,120 Q320,100 350,130 Q380,160 385,200 Q390,240 375,270 Q360,300 330,310 Q310,315 290,310 L275,300" fill="#FFB6C1" stroke="#c92a6a" stroke-width="2"/>
        
        <!-- Corpus Callosum -->
        <path d="M230,170 Q275,150 320,170" fill="none" stroke="#e599b0" stroke-width="3"/>
        
        <!-- Brain Stem -->
        <path d="M265,300 Q260,340 255,370 L275,380 L295,370 Q290,340 285,300" fill="#FFB6C1" stroke="#c92a6a" stroke-width="2"/>
        
        <!-- Cerebellum -->
        <path d="M230,320 Q210,340 220,365 Q235,380 260,370 Q275,365 275,350" fill="#FFB6C1" stroke="#c92a6a" stroke-width="2"/>
        <path d="M320,320 Q340,340 330,365 Q315,380 290,370 Q275,365 275,350" fill="#FFB6C1" stroke="#c92a6a" stroke-width="2"/>
        
        <!-- Cerebrum Folds (Sulci/Gyri) -->
        <g stroke="#c92a6a" stroke-width="1" fill="none" opacity="0.6">
            <path d="M200,150 Q215,145 225,155"/>
            <path d="M185,180 Q200,175 210,185"/>
            <path d="M175,210 Q190,205 200,215"/>
            <path d="M185,240 Q200,235 210,245"/>
            <path d="M350,150 Q335,145 325,155"/>
            <path d="M365,180 Q350,175 340,185"/>
            <path d="M375,210 Q360,205 350,215"/>
            <path d="M365,240 Q350,235 340,245"/>
        </g>
        
        <!-- Labels -->
        <text x="275" y="65" text-anchor="middle" font-size="12" font-weight="bold" fill="#c92a6a">Cerebrum</text>
        <text x="275" y="80" text-anchor="middle" font-size="10" fill="#555">(Thinking, Memory, Movement)</text>
        
        <text x="180" y="340" font-size="11" font-weight="bold" fill="#c92a6a">Cerebellum</text>
        <text x="180" y="355" font-size="9" fill="#555">(Balance, Coordination)</text>
        
        <text x="360" y="340" font-size="11" font-weight="bold" fill="#c92a6a">Cerebellum</text>
        <text x="360" y="355" font-size="9" fill="#555">(Balance, Coordination)</text>
        
        <text x="225" y="400" font-size="11" font-weight="bold" fill="#c92a6a">Brain Stem</text>
        <text x="225" y="415" font-size="9" fill="#555">(Breathing, Heartbeat)</text>
        
        <text x="275" y="440" text-anchor="middle" font-size="11" fill="#666" font-style="italic">~86 billion neurons | Control center of body</text>
    </svg>'''

def get_professional_heart():
    return '''<svg width="500" height="450" viewBox="0 0 500 450" xmlns="http://www.w3.org/2000/svg">
        <rect width="500" height="450" fill="#faf8f0"/>
        <text x="250" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Human Heart</text>
        
        <!-- Heart shape -->
        <path d="M250,370 C130,280 80,340 250,420 C420,340 370,280 250,370" fill="#FF6B6B" stroke="#c92a2a" stroke-width="2"/>
        
        <!-- Aorta -->
        <path d="M250,280 Q270,250 260,210 Q250,190 230,200 Q220,210 225,230 Q230,250 250,270" fill="#FF6B6B" stroke="#c92a2a" stroke-width="2"/>
        
        <!-- Pulmonary Artery -->
        <path d="M265,290 Q290,275 295,250 Q298,235 285,230" fill="none" stroke="#c92a2a" stroke-width="2.5"/>
        
        <!-- Superior Vena Cava -->
        <path d="M220,270 Q200,250 195,220 Q190,200 200,190" fill="none" stroke="#4a6fa5" stroke-width="2.5"/>
        
        # Divide into chambers
        <!-- Septum (dividing wall) -->
        <line x1="250" y1="305" x2="250" y2="390" stroke="#a04040" stroke-width="2"/>
        
        <!-- Right Atrium -->
        <path d="M200,320 Q220,305 245,310 L240,335 Q220,345 200,335 Z" fill="#ff8888" stroke="#c92a2a" stroke-width="1.5"/>
        
        <!-- Left Atrium -->
        <path d="M300,320 Q280,305 255,310 L260,335 Q280,345 300,335 Z" fill="#ff8888" stroke="#c92a2a" stroke-width="1.5"/>
        
        <!-- Right Ventricle -->
        <path d="M200,360 Q225,345 248,350 L248,395 Q220,410 200,395 Z" fill="#ff4444" stroke="#c92a2a" stroke-width="1.5"/>
        
        <!-- Left Ventricle -->
        <path d="M300,360 Q275,345 252,350 L252,395 Q280,410 300,395 Z" fill="#ff4444" stroke="#c92a2a" stroke-width="1.5"/>
        
        # Labels
        <text x="140" y="290" font-size="11" font-weight="bold" fill="#4a6fa5">Superior</text>
        <text x="140" y="305" font-size="11" font-weight="bold" fill="#4a6fa5">Vena Cava</text>
        
        <text x="310" y="250" font-size="11" font-weight="bold" fill="#c92a2a">Aorta</text>
        
        <text x="320" y="280" font-size="10" fill="#c92a2a">Pulmonary</text>
        <text x="320" y="293" font-size="10" fill="#c92a2a">Artery</text>
        
        <text x="155" y="330" font-size="11" font-weight="bold" fill="#c92a2a">Right</text>
        <text x="155" y="343" font-size="11" font-weight="bold" fill="#c92a2a">Atrium</text>
        
        <text x="335" y="330" font-size="11" font-weight="bold" fill="#c92a2a">Left</text>
        <text x="335" y="343" font-size="11" font-weight="bold" fill="#c92a2a">Atrium</text>
        
        <text x="155" y="405" font-size="11" font-weight="bold" fill="#c92a2a">Right</text>
        <text x="155" y="418" font-size="11" font-weight="bold" fill="#c92a2a">Ventricle</text>
        
        <text x="335" y="405" font-size="11" font-weight="bold" fill="#c92a2a">Left</text>
        <text x="335" y="418" font-size="11" font-weight="bold" fill="#c92a2a">Ventricle</text>
        
        <text x="250" y="442" text-anchor="middle" font-size="11" fill="#666" font-style="italic">Pumps ~7,500 liters of blood daily | 4 chambers</text>
    </svg>'''

def get_professional_eye():
    return '''<svg width="500" height="400" viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="500" height="400" fill="#faf8f0"/>
        <text x="250" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Human Eye</text>
        
        <!-- Eye shape (outer) -->
        <ellipse cx="250" cy="200" rx="140" ry="80" fill="#ffffff" stroke="#333" stroke-width="2"/>
        
        <!-- Sclera label -->
        <text x="350" y="140" font-size="11" font-weight="bold" fill="#555">Sclera</text>
        <text x="350" y="155" font-size="9" fill="#666">(White outer layer)</text>
        <line x1="370" y1="160" x2="380" y2="190" stroke="#999" stroke-width="1"/>
        
        # Cornea (transparent front)
        <ellipse cx="250" cy="200" rx="60" ry="65" fill="#e8f4f8" stroke="#4a90a4" stroke-width="1.5" opacity="0.6"/>
        <text x="250" y="120" font-size="11" font-weight="bold" fill="#4a90a4">Cornea</text>
        <text x="250" y="135" font-size="9" fill="#666">(Clear front window)</text>
        
        # Iris (colored part)
        <circle cx="250" cy="200" r="45" fill="#4a7023" stroke="#2d4a15" stroke-width="1.5"/>
        <text x="250" y="270" font-size="11" font-weight="bold" fill="#2d4a15">Iris</text>
        <text x="250" y="285" font-size="9" fill="#666">(Controls light entry)</text>
        
        # Pupil
        <circle cx="250" cy="200" r="20" fill="#000000"/>
        <text x="250" y="315" font-size="11" font-weight="bold" fill="#000">Pupil</text>
        <text x="250" y="330" font-size="9" fill="#666">(Light enters here)</text>
        
        # Light reflections
        <circle cx="240" cy="188" r="6" fill="white" opacity="0.8"/>
        <circle cx="260" cy="210" r="3" fill="white" opacity="0.6"/>
        
        # Lens
        <ellipse cx="250" cy="200" rx="25" ry="18" fill="#fff3c9" stroke="#c4a44a" stroke-width="1.5"/>
        <text x="180" y="190" font-size="11" font-weight="bold" fill="#c4a44a">Lens</text>
        <text x="180" y="205" font-size="9" fill="#666">(Focuses light)</text>
        <line x1="200" y1="195" x2="220" y2="200" stroke="#c4a44a" stroke-width="1"/>
        
        # Optic nerve
        <path d="M380,200 Q420,210 450,250 Q460,270 455,290" fill="none" stroke="#e89b3e" stroke-width="4"/>
        <circle cx="455" cy="295" r="12" fill="#e89b3e" stroke="#c47a2e" stroke-width="1.5"/>
        <text x="445" y="340" font-size="11" font-weight="bold" fill="#e89b3e">Optic Nerve</text>
        <text x="445" y="355" font-size="9" fill="#666">(To brain)</text>
        
        # Retina label
        <text x="350" y="250" font-size="11" font-weight="bold" fill="#7a5a3e">Retina</text>
        <text x="350" y="265" font-size="9" fill="#666">(Light detection)</text>
        <line x1="380" y1="260" x2="370" y2="235" stroke="#999" stroke-width="1"/>
        
        <text x="250" y="385" text-anchor="middle" font-size="11" fill="#666" font-style="italic">Light → Cornea → Pupil → Lens → Retina → Optic Nerve → Brain</text>
    </svg>'''

def get_professional_lungs():
    return '''<svg width="550" height="480" viewBox="0 0 550 480" xmlns="http://www.w3.org/2000/svg">
        <rect width="550" height="480" fill="#faf8f0"/>
        <text x="275" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Respiratory System (Lungs)</text>
        
        # Trachea (windpipe)
        <rect x="265" y="60" width="20" height="90" rx="5" fill="#d4a574" stroke="#8B5A2B" stroke-width="2"/>
        
        # Larynx (voice box)
        <rect x="260" y="50" width="30" height="25" rx="5" fill="#c49061" stroke="#8B5A2B" stroke-width="2"/>
        <text x="250" y="45" font-size="11" font-weight="bold" fill="#8B5A2B">Larynx</text>
        <text x="250" y="60" font-size="9" fill="#666">(Voice box)</text>
        
        # Trachea rings
        <g stroke="#8B5A2B" stroke-width="1.5" fill="none">
            <line x1="265" y1="80" x2="285" y2="80"/>
            <line x1="265" y1="95" x2="285" y2="95"/>
            <line x1="265" y1="110" x2="285" y2="110"/>
            <line x1="265" y1="125" x2="285" y2="125"/>
        </g>
        
        # Bronchi (branches)
        <path d="M275,150 Q240,170 180,200" fill="none" stroke="#d4a574" stroke-width="8"/>
        <path d="M275,150 Q310,170 370,200" fill="none" stroke="#d4a574" stroke-width="8"/>
        
        # Left Lung
        <path d="M180,200 Q140,220 130,280 Q120,350 150,400 Q180,430 230,420 Q260,410 270,380 Q250,350 240,300 Q230,240 200,210 Z" fill="#e8c4c4" stroke="#a06060" stroke-width="2"/>
        
        # Right Lung (slightly larger)
        <path d="M370,200 Q410,220 420,280 Q430,350 400,420 Q370,440 320,430 Q290,415 280,380 Q300,350 310,300 Q320,240 350,210 Z" fill="#e8c4c4" stroke="#a06060" stroke-width="2"/>
        
        # Bronchioles (smaller branches)
        <g stroke="#c49061" stroke-width="2" fill="none">
            <path d="M200,220 Q180,250 170,290"/>
            <path d="M210,240 Q195,260 190,300"/>
            <path d="M350,220 Q370,250 380,290"/>
            <path d="M340,240 Q355,260 360,300"/>
        </g>
        
        # Alveoli (air sacs) - represented as dots
        <g fill="#e89b3e" opacity="0.6">
            <circle cx="160" cy="300" r="8"/>
            <circle cx="175" cy="320" r="7"/>
            <circle cx="155" cy="340" r="9"/>
            <circle cx="170" cy="360" r="8"/>
            <circle cx="390" cy="300" r="8"/>
            <circle cx="375" cy="320" r="7"/>
            <circle cx="395" cy="340" r="9"/>
            <circle cx="380" cy="360" r="8"/>
        </g>
        
        # Diaphragm
        <path d="M120,420 Q275,460 430,420" fill="none" stroke="#8B5A2B" stroke-width="3"/>
        <text x="275" y="450" text-anchor="middle" font-size="11" font-weight="bold" fill="#8B5A2B">Diaphragm</text>
        
        # Labels
        <text x="220" y="70" font-size="11" font-weight="bold" fill="#8B5A2B">Trachea</text>
        <text x="220" y="85" font-size="9" fill="#666">(Windpipe)</text>
        
        <text x="180" y="170" font-size="11" font-weight="bold" fill="#8B5A2B">Bronchus</text>
        <text x="340" y="170" font-size="11" font-weight="bold" fill="#8B5A2B">Bronchus</text>
        
        <text x="130" y="380" font-size="11" font-weight="bold" fill="#a06060">Left Lung</text>
        <text x="400" y="380" font-size="11" font-weight="bold" fill="#a06060">Right Lung</text>
        
        <text x="130" y="270" font-size="10" fill="#e89b3e">Bronchioles</text>
        <text x="390" y="270" font-size="10" fill="#e89b3e">Bronchioles</text>
        
        <text x="140" y="315" font-size="10" fill="#e89b3e">Alveoli</text>
        <text x="400" y="315" font-size="10" fill="#e89b3e">Alveoli</text>
        
        <text x="275" y="475" text-anchor="middle" font-size="11" fill="#666" font-style="italic">Oxygen enters, CO₂ exits | Gas exchange in alveoli</text>
    </svg>'''

def get_animal_cell():
    return '''<svg width="550" height="450" viewBox="0 0 550 450" xmlns="http://www.w3.org/2000/svg">
        <rect width="550" height="450" fill="#faf8f0"/>
        <text x="275" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Animal Cell Structure</text>
        
        <!-- Cell membrane -->
        <ellipse cx="275" cy="220" rx="200" ry="170" fill="#e8f8f0" stroke="#0f3460" stroke-width="3" stroke-dasharray="8,4"/>
        <text x="440" y="80" font-size="12" font-weight="bold" fill="#0f3460">Cell Membrane</text>
        <line x1="440" y1="90" x2="460" y2="120" stroke="#0f3460" stroke-width="1"/>
        
        # Cytoplasm label
        <text x="275" y="400" text-anchor="middle" font-size="12" fill="#555" font-style="italic">Cytoplasm (jelly-like fluid)</text>
        
        # Nucleus
        <ellipse cx="275" cy="190" rx="70" ry="55" fill="#e8f0e8" stroke="#2d6a4f" stroke-width="2.5"/>
        <text x="275" y="175" text-anchor="middle" font-size="14" font-weight="bold" fill="#2d6a4f">Nucleus</text>
        <circle cx="275" cy="210" r="15" fill="#c8e6c9" stroke="#2d6a4f" stroke-width="1.5"/>
        <text x="275" y="215" text-anchor="middle" font-size="9" fill="#1b5e20">DNA</text>
        
        # Nuclear membrane label
        <line x1="345" y1="170" x2="380" y2="155" stroke="#999" stroke-width="1"/>
        <text x="385" y="155" font-size="10" fill="#555">Nuclear Membrane</text>
        
        # Mitochondria (powerhouse)
        <ellipse cx="160" cy="150" rx="45" ry="25" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
        <path d="M150,150 Q170,135 190,150" fill="none" stroke="#e65100" stroke-width="2"/>
        <text x="160" y="115" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">Mitochondria</text>
        <text x="160" y="130" text-anchor="middle" font-size="9" fill="#666">(Power House)</text>
        
        # Golgi Apparatus
        <path d="M380,260 L420,250 L410,275 L450,265 L440,290" fill="none" stroke="#6a1b9a" stroke-width="3"/>
        <text x="430" y="240" font-size="11" font-weight="bold" fill="#6a1b9a">Golgi</text>
        <text x="430" y="255" font-size="9" fill="#666">(Packaging)</text>
        
        # Endoplasmic Reticulum (ER)
        <path d="M420,140 Q460,130 450,160 Q470,150 460,180" fill="none" stroke="#1565c0" stroke-width="2.5"/>
        <text x="455" y="130" font-size="11" font-weight="bold" fill="#1565c0">ER</text>
        
        # Ribosomes
        <g fill="#c62828">
            <circle cx="130" cy="280" r="5"/>
            <circle cx="145" cy="290" r="5"/>
            <circle cx="135" cy="305" r="5"/>
            <circle cx="155" cy="315" r="5"/>
            <circle cx="380" cy="310" r="5"/>
            <circle cx="395" cy="320" r="5"/>
        </g>
        <text x="120" y="340" font-size="11" font-weight="bold" fill="#c62828">Ribosomes</text>
        <text x="120" y="355" font-size="9" fill="#666">(Protein making)</text>
        
        # Lysosome
        <circle cx="180" cy="280" r="15" fill="#ffcdd2" stroke="#c62828" stroke-width="1.5"/>
        <text x="180" y="315" font-size="11" font-weight="bold" fill="#c62828">Lysosome</text>
        <text x="180" y="330" font-size="9" fill="#666">(Waste breakdown)</text>
        
        # Vacuole (small in animal cells)
        <ellipse cx="340" cy="330" rx="20" ry="15" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5"/>
        <text x="340" y="365" font-size="10" fill="#1565c0">Vacuole</text>
        
        <text x="275" y="440" text-anchor="middle" font-size="11" fill="#666" font-style="italic">Basic unit of animal life | Contains organelles for survival</text>
    </svg>'''

def get_plant_cell():
    return '''<svg width="550" height="450" viewBox="0 0 550 450" xmlns="http://www.w3.org/2000/svg">
        <rect width="550" height="450" fill="#faf8f0"/>
        <text x="275" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Plant Cell Structure</text>
        
        # Cell Wall (outer rigid layer)
        <rect x="60" y="60" width="430" height="340" rx="10" fill="none" stroke="#8B4513" stroke-width="3"/>
        <text x="460" y="80" font-size="12" font-weight="bold" fill="#8B4513">Cell Wall</text>
        <line x1="470" y1="90" x2="480" y2="110" stroke="#8B4513" stroke-width="1"/>
        
        # Cell Membrane
        <rect x="75" y="75" width="400" height="310" rx="8" fill="none" stroke="#0f3460" stroke-width="2.5" stroke-dasharray="6,3"/>
        <text x="450" y="120" font-size="11" font-weight="bold" fill="#0f3460">Cell Membrane</text>
        
        # Cytoplasm
        <text x="275" y="420" text-anchor="middle" font-size="12" fill="#555" font-style="italic">Cytoplasm</text>
        
        # Nucleus
        <ellipse cx="275" cy="190" rx="55" ry="45" fill="#e8f0e8" stroke="#2d6a4f" stroke-width="2.5"/>
        <text x="275" y="185" text-anchor="middle" font-size="12" font-weight="bold" fill="#2d6a4f">Nucleus</text>
        <circle cx="275" cy="205" r="12" fill="#c8e6c9" stroke="#2d6a4f" stroke-width="1.5"/>
        
        # Chloroplasts (unique to plants)
        <ellipse cx="420" cy="160" rx="35" ry="22" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
        <ellipse cx="420" cy="160" rx="15" ry="10" fill="#4caf50"/>
        <circle cx="415" cy="157" r="3" fill="#1b5e20"/>
        <text x="420" y="130" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Chloroplast</text>
        <text x="420" y="145" text-anchor="middle" font-size="9" fill="#666">(Photosynthesis)</text>
        
        # Another chloroplast
        <ellipse cx="150" cy="300" rx="30" ry="18" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
        
        # Mitochondria
        <ellipse cx="400" cy="280" rx="35" ry="20" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
        <path d="M392,280 Q405,270 418,280" fill="none" stroke="#e65100" stroke-width="1.5"/>
        <text x="400" y="320" text-anchor="middle" font-size="10" fill="#e65100">Mitochondria</text>
        
        # Vacuole (large - unique to plants)
        <ellipse cx="180" cy="220" rx="55" ry="65" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
        <text x="180" y="200" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565c0">Vacuole</text>
        <text x="180" y="215" text-anchor="middle" font-size="9" fill="#666">(Storage, Pressure)</text>
        
        # Golgi Apparatus
        <path d="M320,270 L350,260 L345,280 L375,270 L370,290" fill="none" stroke="#6a1b9a" stroke-width="2"/>
        <text x="350" y="250" font-size="10" font-weight="bold" fill="#6a1b9a">Golgi</text>
        
        # ER
        <path d="M350,130 Q380,120 370,145 Q390,135 380,160" fill="none" stroke="#1565c0" stroke-width="2"/>
        <text x="385" y="125" font-size="10" font-weight="bold" fill="#1565c0">ER</text>
        
        # Ribosomes
        <g fill="#c62828">
            <circle cx="320" cy="350" r="4"/>
            <circle cx="335" cy="360" r="4"/>
            <circle cx="140" cy="380" r="4"/>
            <circle cx="155" cy="390" r="4"/>
        </g>
        <text x="310" y="380" font-size="10" font-weight="bold" fill="#c62828">Ribosomes</text>
        
        <text x="275" y="445" text-anchor="middle" font-size="11" fill="#666" font-style="italic">Unique features: Cell wall, Chloroplasts, Large vacuole</text>
    </svg>'''

# ============================================
# GEOMETRIC SHAPES
# ============================================

def get_circle_svg():
    return '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="400" fill="#f8f9fa"/>
        <circle cx="200" cy="200" r="120" fill="none" stroke="#0f3460" stroke-width="3"/>
        <line x1="200" y1="200" x2="320" y2="200" stroke="#e94560" stroke-width="2" stroke-dasharray="5,5"/>
        <circle cx="200" cy="200" r="5" fill="#e94560"/>
        <text x="260" y="190" fill="#e94560" font-size="14">Radius (r)</text>
        <text x="200" y="220" text-anchor="middle" fill="#0f3460" font-size="14">Center</text>
        <text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Circle: Area = πr², Circumference = 2πr</text>
    </svg>'''

def get_square_svg():
    return '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="400" fill="#f8f9fa"/>
        <rect x="100" y="100" width="200" height="200" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/>
        <line x1="100" y1="100" x2="300" y2="100" stroke="#e94560" stroke-width="2" marker-end="url(#arrow)"/>
        <text x="200" y="90" text-anchor="middle" fill="#e94560" font-size="14">Side (s)</text>
        <text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Square: Area = s², Perimeter = 4s</text>
        <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3z" fill="#e94560"/></marker></defs>
    </svg>'''

def get_triangle_svg():
    return '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="400" fill="#f8f9fa"/>
        <polygon points="80,300 300,300 80,100" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/>
        <polygon points="80,280 100,280 100,300" fill="none" stroke="#e94560" stroke-width="2"/>
        <text x="90" y="295" text-anchor="middle" fill="#e94560" font-size="14">90°</text>
        <text x="190" y="320" text-anchor="middle" fill="#0f3460" font-size="14">Base (b)</text>
        <text x="65" y="200" text-anchor="middle" fill="#0f3460" font-size="14" transform="rotate(-90 65 200)">Height (h)</text>
        <text x="240" y="170" fill="#666" font-size="12" transform="rotate(35 240 170)">Hypotenuse (c)</text>
        <text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Pythagorean Theorem: a² + b² = c²</text>
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
    
    if "hello" in m or "hi" in m:
        return "👋 Hello! I'm KalaX AI. Try 'Draw a skeleton', 'Draw a brain', or 'Draw a circle'"
    
    return f"Ask me about science, or say 'Draw a skeleton', 'Draw a brain', 'Draw a heart'"

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)