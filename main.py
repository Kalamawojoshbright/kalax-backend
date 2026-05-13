"""
KalaX Backend - Realistic Educational Diagrams
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
from datetime import datetime
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "AIzaSyAU_pIonfIoRhlpnkK5CX-HZveGv_5pqkQ"
genai.configure(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class DrawRequest(BaseModel):
    command: str

class DrawResponse(BaseModel):
    success: bool
    svg: Optional[str] = None
    code: Optional[str] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/learn/chat")
async def chat(request: ChatRequest):
    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(request.message)
        return ChatResponse(response=response.text)
    except Exception as e:
        return ChatResponse(response=f"Error: {str(e)}")

@app.post("/draw")
async def draw(request: DrawRequest):
    cmd = request.command.lower()
    
    # Return SVG diagrams (realistic educational diagrams)
    if "brain" in cmd:
        return DrawResponse(success=True, svg=BRAIN_SVG)
    if "skeleton" in cmd or "human skeleton" in cmd:
        return DrawResponse(success=True, svg=SKELETON_SVG)
    if "heart" in cmd:
        return DrawResponse(success=True, svg=HEART_SVG)
    if "eye" in cmd:
        return DrawResponse(success=True, svg=EYE_SVG)
    if "lung" in cmd or "lungs" in cmd:
        return DrawResponse(success=True, svg=LUNGS_SVG)
    if "kidney" in cmd:
        return DrawResponse(success=True, svg=KIDNEY_SVG)
    if "circle" in cmd:
        return DrawResponse(success=True, svg=CIRCLE_SVG)
    if "square" in cmd:
        return DrawResponse(success=True, svg=SQUARE_SVG)
    if "triangle" in cmd:
        return DrawResponse(success=True, svg=TRIANGLE_SVG)
    
    return DrawResponse(success=False, error="Try: brain, skeleton, heart, eye, lungs, kidney, circle, square, triangle")

# ============================================
# REALISTIC EDUCATIONAL DIAGRAMS (SVG)
# ============================================

BRAIN_SVG = """<svg width="600" height="500" viewBox="0 0 600 500" xmlns="http://www.w3.org/2000/svg">
    <rect width="600" height="500" fill="#f8f9fa" rx="10"/>
    <text x="300" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Human Brain - Lateral View</text>
    
    <!-- Frontal Lobe -->
    <path d="M 250 120 Q 180 100 150 160 Q 130 220 160 260 Q 180 280 220 270" fill="#FFB3BA" stroke="#333" stroke-width="2"/>
    <text x="180" y="200" text-anchor="middle" font-size="12" fill="#333">Frontal Lobe</text>
    
    <!-- Parietal Lobe -->
    <path d="M 250 120 Q 320 100 360 140 Q 380 180 360 230 Q 340 270 300 280 Q 260 280 220 270" fill="#BAFFC9" stroke="#333" stroke-width="2"/>
    <text x="300" y="200" text-anchor="middle" font-size="12" fill="#333">Parietal Lobe</text>
    
    <!-- Occipital Lobe -->
    <path d="M 360 140 Q 400 160 410 200 Q 415 240 390 270 Q 360 290 340 280 Q 360 230 360 140" fill="#BAE1FF" stroke="#333" stroke-width="2"/>
    <text x="390" y="220" text-anchor="middle" font-size="11" fill="#333">Occipital<br/>Lobe</text>
    
    <!-- Temporal Lobe -->
    <path d="M 160 260 Q 180 300 220 340 Q 260 370 300 370 Q 340 360 360 330 Q 340 280 300 280 Q 240 280 200 270" fill="#FFFFBA" stroke="#333" stroke-width="2"/>
    <text x="260" y="330" text-anchor="middle" font-size="12" fill="#333">Temporal Lobe</text>
    
    <!-- Cerebellum -->
    <path d="M 340 340 Q 370 360 380 390 Q 380 420 350 440 Q 320 450 300 430 Q 310 390 340 340" fill="#FFD4BA" stroke="#333" stroke-width="2"/>
    <text x="350" y="400" text-anchor="middle" font-size="11" fill="#333">Cerebellum</text>
    
    <!-- Brain Stem -->
    <path d="M 270 370 L 260 420 L 280 440 L 300 420 L 290 370 Z" fill="#E6BABA" stroke="#333" stroke-width="2"/>
    <text x="280" y="420" text-anchor="middle" font-size="10" fill="#333">Brain<br/>Stem</text>
    
    <!-- Corpus Callosum -->
    <path d="M 220 160 Q 260 130 310 150" fill="none" stroke="#666" stroke-width="2" stroke-dasharray="4,2"/>
    <text x="260" y="145" text-anchor="middle" font-size="11" fill="#666">Corpus Callosum</text>
    
    <!-- Labels -->
    <text x="300" y="480" text-anchor="middle" font-size="12" fill="#666">The brain controls thoughts, memory, emotion, touch, motor skills, vision, breathing, and temperature.</text>
</svg>"""

SKELETON_SVG = """<svg width="500" height="600" viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg">
    <rect width="500" height="600" fill="#f8f9fa" rx="10"/>
    <text x="250" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Human Skeleton</text>
    
    <!-- Skull -->
    <path d="M 200 60 Q 200 40 220 35 Q 250 30 280 35 Q 300 40 300 60 Q 300 90 280 100 Q 250 110 220 100 Q 200 90 200 60" fill="#F5DEB3" stroke="#8B7355" stroke-width="2"/>
    <text x="250" y="80" text-anchor="middle" font-size="11" fill="#8B7355">Skull</text>
    <!-- Jaw -->
    <path d="M 215 95 Q 230 120 270 120 Q 285 95" fill="none" stroke="#8B7355" stroke-width="2"/>
    <text x="250" y="125" text-anchor="middle" font-size="9" fill="#8B7355">Mandible</text>
    
    <!-- Spine -->
    <line x1="250" y1="140" x2="250" y2="400" stroke="#8B7355" stroke-width="3"/>
    
    <!-- Clavicles -->
    <path d="M 220 145 Q 180 155 160 165" stroke="#A0522D" stroke-width="3" fill="none"/>
    <path d="M 280 145 Q 320 155 340 165" stroke="#A0522D" stroke-width="3" fill="none"/>
    <text x="155" y="170" font-size="9" fill="#A0522D">Clavicle</text>
    
    <!-- Scapulae -->
    <path d="M 160 165 Q 150 200 155 230" stroke="#A0522D" stroke-width="2" fill="none"/>
    <path d="M 340 165 Q 350 200 345 230" stroke="#A0522D" stroke-width="2" fill="none"/>
    <text x="145" y="200" font-size="9" fill="#A0522D">Scapula</text>
    
    <!-- Ribcage -->
    <path d="M 250 170 Q 210 175 200 190 Q 195 210 210 230" stroke="#A0522D" stroke-width="2" fill="none"/>
    <path d="M 250 170 Q 290 175 300 190 Q 305 210 290 230" stroke="#A0522D" stroke-width="2" fill="none"/>
    <path d="M 250 200 Q 215 205 205 220" stroke="#A0522D" stroke-width="2" fill="none"/>
    <path d="M 250 200 Q 285 205 295 220" stroke="#A0522D" stroke-width="2" fill="none"/>
    <path d="M 250 230 Q 220 235 210 250" stroke="#A0522D" stroke-width="2" fill="none"/>
    <path d="M 250 230 Q 280 235 290 250" stroke="#A0522D" stroke-width="2" fill="none"/>
    <text x="200" y="210" font-size="9" fill="#A0522D">Ribcage</text>
    
    <!-- Humerus -->
    <line x1="165" y1="240" x2="150" y2="330" stroke="#A0522D" stroke-width="3"/>
    <line x1="335" y1="240" x2="350" y2="330" stroke="#A0522D" stroke-width="3"/>
    <text x="140" y="290" font-size="9" fill="#A0522D">Humerus</text>
    
    <!-- Radius & Ulna -->
    <line x1="150" y1="335" x2="155" y2="430" stroke="#A0522D" stroke-width="2"/>
    <line x1="160" y1="335" x2="165" y2="430" stroke="#A0522D" stroke-width="2"/>
    <line x1="350" y1="335" x2="345" y2="430" stroke="#A0522D" stroke-width="2"/>
    <line x1="340" y1="335" x2="335" y2="430" stroke="#A0522D" stroke-width="2"/>
    <text x="130" y="390" font-size="8" fill="#A0522D">Radius/Ulna</text>
    
    <!-- Pelvis -->
    <path d="M 220 400 Q 250 380 280 400 Q 290 430 280 450 Q 250 460 220 450 Q 210 430 220 400" fill="#F5DEB3" stroke="#A0522D" stroke-width="2"/>
    <text x="250" y="430" text-anchor="middle" font-size="10" fill="#A0522D">Pelvis</text>
    
    <!-- Femur -->
    <line x1="230" y1="460" x2="220" y2="540" stroke="#A0522D" stroke-width="4"/>
    <line x1="270" y1="460" x2="280" y2="540" stroke="#A0522D" stroke-width="4"/>
    <text x="200" y="500" font-size="9" fill="#A0522D">Femur</text>
    
    <!-- Patella -->
    <circle cx="218" cy="545" r="8" fill="#F5DEB3" stroke="#A0522D" stroke-width="1"/>
    <circle cx="282" cy="545" r="8" fill="#F5DEB3" stroke="#A0522D" stroke-width="1"/>
    
    <!-- Tibia & Fibula -->
    <line x1="215" y1="555" x2="210" y2="590" stroke="#A0522D" stroke-width="2"/>
    <line x1="225" y1="555" x2="230" y2="590" stroke="#A0522D" stroke-width="2"/>
    <line x1="275" y1="555" x2="270" y2="590" stroke="#A0522D" stroke-width="2"/>
    <line x1="285" y1="555" x2="290" y2="590" stroke="#A0522D" stroke-width="2"/>
    
    <!-- Feet -->
    <ellipse cx="220" cy="595" rx="25" ry="6" fill="#F5DEB3" stroke="#A0522D" stroke-width="1"/>
    <ellipse cx="280" cy="595" rx="25" ry="6" fill="#F5DEB3" stroke="#A0522D" stroke-width="1"/>
    
    <text x="250" y="580" text-anchor="middle" font-size="11" fill="#666">The skeleton provides structure, protects organs, and enables movement.</text>
</svg>"""

HEART_SVG = """<svg width="550" height="500" viewBox="0 0 550 500" xmlns="http://www.w3.org/2000/svg">
    <rect width="550" height="500" fill="#f8f9fa" rx="10"/>
    <text x="275" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Human Heart</text>
    
    <!-- Aorta -->
    <path d="M 275 100 Q 300 80 310 110 Q 320 140 290 150" fill="#E8A0A0" stroke="#C0392B" stroke-width="2"/>
    <text x="310" y="100" font-size="10" fill="#C0392B">Aorta</text>
    
    <!-- Pulmonary Artery -->
    <path d="M 260 130 Q 230 140 220 160 Q 215 180 230 190" fill="#A0C0E8" stroke="#1565C0" stroke-width="2"/>
    <text x="210" y="155" font-size="9" fill="#1565C0">Pulmonary<br/>Artery</text>
    
    <!-- Superior Vena Cava -->
    <path d="M 290 140 Q 340 150 340 180" fill="none" stroke="#2980B9" stroke-width="3"/>
    <text x="345" y="155" font-size="9" fill="#2980B9">Superior<br/>Vena Cava</text>
    
    <!-- Right Atrium -->
    <path d="M 310 180 Q 350 200 340 240 Q 330 270 290 260 Q 280 230 310 180" fill="#E8A0A0" stroke="#C0392B" stroke-width="2"/>
    <text x="330" y="225" text-anchor="middle" font-size="11" fill="#C0392B">Right<br/>Atrium</text>
    
    <!-- Left Atrium -->
    <path d="M 230 170 Q 190 190 200 230 Q 210 260 250 250 Q 260 220 230 170" fill="#E8A0A0" stroke="#C0392B" stroke-width="2"/>
    <text x="210" y="215" text-anchor="middle" font-size="11" fill="#C0392B">Left<br/>Atrium</text>
    
    <!-- Right Ventricle -->
    <path d="M 300 270 Q 360 300 340 370 Q 320 430 270 410 Q 260 360 300 270" fill="#FFB3B3" stroke="#C0392B" stroke-width="2"/>
    <text x="320" y="350" text-anchor="middle" font-size="11" fill="#C0392B">Right<br/>Ventricle</text>
    
    <!-- Left Ventricle -->
    <path d="M 240 260 Q 180 290 195 370 Q 210 420 250 400 Q 270 350 240 260" fill="#FFB3B3" stroke="#C0392B" stroke-width="2"/>
    <text x="210" y="335" text-anchor="middle" font-size="11" fill="#C0392B">Left<br/>Ventricle</text>
    
    <!-- Septum -->
    <line x1="270" y1="250" x2="275" y2="400" stroke="#C0392B" stroke-width="2" stroke-dasharray="4,2"/>
    
    <!-- Valves -->
    <text x="290" y="275" font-size="9" fill="#666">Tricuspid<br/>Valve</text>
    <text x="240" y="275" font-size="9" fill="#666">Mitral<br/>Valve</text>
    
    <!-- Blood Flow Arrows -->
    <text x="360" y="200" font-size="16" fill="#1565C0">↓</text>
    <text x="360" y="300" font-size="16" fill="#1565C0">↓</text>
    <text x="190" y="250" font-size="16" fill="#E74C3C">↑</text>
    <text x="190" y="380" font-size="16" fill="#E74C3C">↑</text>
    
    <!-- Labels -->
    <text x="275" y="465" text-anchor="middle" font-size="12" fill="#666">The heart pumps blood throughout the body. It has 4 chambers: 2 atria and 2 ventricles.</text>
</svg>"""

EYE_SVG = """<svg width="550" height="400" viewBox="0 0 550 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="550" height="400" fill="#f8f9fa" rx="10"/>
    <text x="275" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Human Eye</text>
    
    <!-- Sclera -->
    <ellipse cx="275" cy="180" rx="140" ry="80" fill="#FFF8DC" stroke="#8B7355" stroke-width="2"/>
    <text x="180" y="140" font-size="11" fill="#8B7355">Sclera</text>
    
    <!-- Cornea -->
    <ellipse cx="340" cy="180" rx="50" ry="38" fill="none" stroke="#87CEEB" stroke-width="2"/>
    <text x="370" y="160" font-size="10" fill="#87CEEB">Cornea</text>
    
    <!-- Iris -->
    <ellipse cx="320" cy="180" rx="40" ry="35" fill="#4A7023"/>
    <text x="320" y="145" font-size="11" fill="#4A7023">Iris</text>
    
    <!-- Pupil -->
    <circle cx="325" cy="180" r="15" fill="black"/>
    <text x="325" y="165" text-anchor="middle" font-size="10" fill="white">Pupil</text>
    
    <!-- Lens -->
    <ellipse cx="300" cy="180" rx="20" ry="12" fill="#FFFACD" stroke="#DAA520" stroke-width="1"/>
    <text x="270" y="200" font-size="10" fill="#DAA520">Lens</text>
    
    <!-- Retina -->
    <path d="M 140 180 Q 150 250 200 280 Q 250 300 300 300" fill="none" stroke="#E74C3C" stroke-width="2" stroke-dasharray="4,2"/>
    <text x="170" y="290" font-size="10" fill="#E74C3C">Retina</text>
    
    <!-- Optic Nerve -->
    <path d="M 145 185 Q 100 200 80 220 Q 60 240 50 250" fill="none" stroke="#8B4513" stroke-width="4"/>
    <text x="60" y="235" font-size="10" fill="#8B4513">Optic<br/>Nerve</text>
    
    <!-- Aqueous Humor -->
    <text x="350" y="210" font-size="9" fill="#666">Aqueous<br/>Humor</text>
    
    <!-- Vitreous Humor -->
    <text x="230" y="230" font-size="9" fill="#666">Vitreous<br/>Humor</text>
    
    <text x="275" y="370" text-anchor="middle" font-size="12" fill="#666">The eye captures light and sends signals to the brain, allowing us to see.</text>
</svg>"""

LUNGS_SVG = """<svg width="550" height="450" viewBox="0 0 550 450" xmlns="http://www.w3.org/2000/svg">
    <rect width="550" height="450" fill="#f8f9fa" rx="10"/>
    <text x="275" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Respiratory System</text>
    
    <!-- Trachea -->
    <rect x="260" y="60" width="30" height="80" fill="#D2B48C" stroke="#8B4513" stroke-width="2" rx="5"/>
    <text x="275" y="55" text-anchor="middle" font-size="12" fill="#8B4513">Trachea</text>
    
    <!-- Bronchi -->
    <path d="M 260 130 Q 230 150 200 160" stroke="#8B4513" stroke-width="6" fill="none"/>
    <path d="M 290 130 Q 320 150 350 160" stroke="#8B4513" stroke-width="6" fill="none"/>
    <text x="200" y="150" font-size="10" fill="#8B4513">Bronchus</text>
    <text x="355" y="150" font-size="10" fill="#8B4513">Bronchus</text>
    
    <!-- Left Lung -->
    <path d="M 200 160 Q 140 200 130 280 Q 120 370 160 400 Q 200 420 240 380 Q 250 320 230 260 Q 210 200 200 160" fill="#FFB6C1" stroke="#FF69B4" stroke-width="2"/>
    
    <!-- Right Lung -->
    <path d="M 350 160 Q 410 200 420 280 Q 430 370 390 400 Q 350 420 310 380 Q 300 320 320 260 Q 340 200 350 160" fill="#FFB6C1" stroke="#FF69B4" stroke-width="2"/>
    
    <text x="180" y="300" font-size="14" fill="#FF69B4" font-weight="bold">Left<br/>Lung</text>
    <text x="370" y="300" font-size="14" fill="#FF69B4" font-weight="bold">Right<br/>Lung</text>
    
    <!-- Bronchioles (left) -->
    <path d="M 200 230 Q 180 250 170 270" stroke="#FF69B4" stroke-width="2" fill="none"/>
    <path d="M 210 300 Q 190 320 180 340" stroke="#FF69B4" stroke-width="2" fill="none"/>
    
    <!-- Bronchioles (right) -->
    <path d="M 350 230 Q 370 250 380 270" stroke="#FF69B4" stroke-width="2" fill="none"/>
    <path d="M 340 300 Q 360 320 370 340" stroke="#FF69B4" stroke-width="2" fill="none"/>
    
    <!-- Diaphragm -->
    <path d="M 80 400 Q 275 440 470 400" fill="none" stroke="#8B4513" stroke-width="3"/>
    <text x="275" y="430" text-anchor="middle" font-size="12" fill="#8B4513">Diaphragm</text>
    
    <!-- Alveoli clusters -->
    <circle cx="165" cy="275" r="5" fill="#FFB6C1" stroke="#FF69B4" stroke-width="1"/>
    <circle cx="175" cy="285" r="4" fill="#FFB6C1" stroke="#FF69B4" stroke-width="1"/>
    <circle cx="160" cy="295" r="6" fill="#FFB6C1" stroke="#FF69B4" stroke-width="1"/>
    <text x="140" y="280" font-size="9" fill="#666">Alveoli</text>
    
    <circle cx="385" cy="275" r="5" fill="#FFB6C1" stroke="#FF69B4" stroke-width="1"/>
    <circle cx="375" cy="285" r="4" fill="#FFB6C1" stroke="#FF69B4" stroke-width="1"/>
    <circle cx="390" cy="295" r="6" fill="#FFB6C1" stroke="#FF69B4" stroke-width="1"/>
    
    <text x="275" y="420" text-anchor="middle" font-size="11" fill="#666">Oxygen enters, carbon dioxide leaves during breathing.</text>
</svg>"""

KIDNEY_SVG = """<svg width="550" height="400" viewBox="0 0 550 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="550" height="400" fill="#f8f9fa" rx="10"/>
    <text x="275" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Kidney Anatomy</text>
    
    <!-- Left Kidney -->
    <path d="M 120 120 Q 100 180 110 250 Q 120 300 170 300 Q 200 300 210 250 Q 220 180 200 120 Q 170 100 120 120" fill="#FFDAB9" stroke="#E65100" stroke-width="2"/>
    <text x="160" y="310" text-anchor="middle" font-size="12" fill="#E65100">Left Kidney</text>
    
    <!-- Right Kidney -->
    <path d="M 340 120 Q 320 180 330 250 Q 340 300 390 300 Q 420 300 430 250 Q 440 180 420 120 Q 390 100 340 120" fill="#FFDAB9" stroke="#E65100" stroke-width="2"/>
    <text x="380" y="310" text-anchor="middle" font-size="12" fill="#E65100">Right Kidney</text>
    
    <!-- Renal Artery (to kidneys) -->
    <path d="M 275 160 L 210 170" stroke="#E74C3C" stroke-width="3" fill="none"/>
    <path d="M 275 160 L 340 170" stroke="#E74C3C" stroke-width="3" fill="none"/>
    <text x="275" y="150" text-anchor="middle" font-size="10" fill="#E74C3C">Renal Artery</text>
    
    <!-- Renal Vein (from kidneys) -->
    <path d="M 210 240 L 275 250 L 340 240" stroke="#2980B9" stroke-width="3" fill="none"/>
    <text x="275" y="265" text-anchor="middle" font-size="10" fill="#2980B9">Renal Vein</text>
    
    <!-- Ureters -->
    <path d="M 170 300 Q 200 340 275 350 Q 350 340 380 300" stroke="#8B4513" stroke-width="3" fill="none"/>
    <text x="275" y="365" text-anchor="middle" font-size="10" fill="#8B4513">Ureters</text>
    
    <!-- Bladder -->
    <ellipse cx="275" cy="380" rx="50" ry="15" fill="#D2B48C" stroke="#8B4513" stroke-width="2"/>
    <text x="275" y="385" text-anchor="middle" font-size="10" fill="#8B4513">Bladder</text>
    
    <!-- Label arrows -->
    <text x="100" y="200" text-anchor="middle" font-size="11" fill="#666">Filters<br/>blood</text>
    <text x="450" y="200" text-anchor="middle" font-size="11" fill="#666">Removes<br/>waste</text>
    
    <text x="275" y="395" text-anchor="middle" font-size="11" fill="#666">Kidneys filter blood, remove waste, produce urine.</text>
</svg>"""

# Simple shapes fallbacks
CIRCLE_SVG = """<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="400" fill="#f8f9fa" rx="10"/>
    <circle cx="200" cy="200" r="120" fill="none" stroke="#0f3460" stroke-width="3"/>
    <circle cx="200" cy="200" r="5" fill="#e94560"/>
    <line x1="200" y1="200" x2="320" y2="200" stroke="#e94560" stroke-width="2"/>
    <text x="200" y="105" text-anchor="middle" font-size="14" fill="#0f3460">Circle</text>
    <text x="260" y="195" font-size="12" fill="#e94560">Radius (r)</text>
    <text x="200" y="220" text-anchor="middle" font-size="12" fill="#333">Center</text>
</svg>"""

SQUARE_SVG = """<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="400" fill="#f8f9fa" rx="10"/>
    <rect x="100" y="100" width="200" height="200" fill="none" stroke="#0f3460" stroke-width="3"/>
    <text x="200" y="90" text-anchor="middle" font-size="14" fill="#0f3460">Square</text>
    <text x="200" y="340" text-anchor="middle" font-size="12" fill="#333">All sides equal, all angles 90°</text>
    <line x1="100" y1="100" x2="300" y2="100" stroke="#e94560" stroke-width="2"/>
    <text x="200" y="85" text-anchor="middle" font-size="11" fill="#e94560">Side</text>
</svg>"""

TRIANGLE_SVG = """<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="400" fill="#f8f9fa" rx="10"/>
    <polygon points="100,280 300,280 200,120" fill="none" stroke="#0f3460" stroke-width="3"/>
    <polygon points="100,260 120,260 120,280" fill="none" stroke="#e94560" stroke-width="2"/>
    <text x="120" y="275" font-size="12" fill="#e94560">90°</text>
    <text x="200" y="105" text-anchor="middle" font-size="14" fill="#0f3460">Right Angle Triangle</text>
    <text x="200" y="340" text-anchor="middle" font-size="11" fill="#333">a² + b² = c² (Pythagorean Theorem)</text>
</svg>"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)