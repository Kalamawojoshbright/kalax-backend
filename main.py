"""
KalaX Backend - Complete Educational Diagrams
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
    error: Optional[str] = None

@app.get("/")
async def root():
    return {"status": "online", "service": "KalaX Backend"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": str(datetime.now())}

@app.post("/learn/chat")
async def chat(request: ChatRequest):
    """Answer ANY question using Gemini AI"""
    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(request.message)
        return ChatResponse(response=response.text)
    except Exception as e:
        return ChatResponse(response=f"Error: {str(e)}")

@app.post("/draw")
async def draw(request: DrawRequest):
    """Generate educational diagrams"""
    cmd = request.command.lower()
    
    # Professional SVG diagrams
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
    if "cell" in cmd or "animal cell" in cmd:
        return DrawResponse(success=True, svg=CELL_SVG)
    if "plant cell" in cmd:
        return DrawResponse(success=True, svg=PLANT_CELL_SVG)
    if "neuron" in cmd:
        return DrawResponse(success=True, svg=NEURON_SVG)
    if "mitosis" in cmd:
        return DrawResponse(success=True, svg=MITOSIS_SVG)
    if "photosynthesis" in cmd:
        return DrawResponse(success=True, svg=PHOTOSYNTHESIS_SVG)
    if "circle" in cmd:
        return DrawResponse(success=True, svg=CIRCLE_SVG)
    if "square" in cmd:
        return DrawResponse(success=True, svg=SQUARE_SVG)
    if "triangle" in cmd:
        return DrawResponse(success=True, svg=TRIANGLE_SVG)
    
    return DrawResponse(success=False, error="Try: brain, skeleton, heart, eye, lungs, kidney, cell, plant cell, neuron, mitosis, photosynthesis")

# ============================================
# PROFESSIONAL SVG DIAGRAMS
# ============================================

BRAIN_SVG = '''<svg width="650" height="500" viewBox="0 0 650 500" xmlns="http://www.w3.org/2000/svg">
    <rect width="650" height="500" fill="#FAFAFA" rx="15"/>
    <text x="325" y="35" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Human Brain - Lateral View</text>
    <line x1="50" y1="55" x2="600" y2="55" stroke="#ddd" stroke-width="1"/>
    <path d="M 280 100 Q 200 80 160 130 Q 130 170 140 220 Q 150 260 190 280 Q 230 290 270 270" fill="#FFB3BA" stroke="#333" stroke-width="2"/>
    <text x="200" y="190" text-anchor="middle" font-size="13" font-weight="bold">Frontal Lobe</text>
    <text x="200" y="210" text-anchor="middle" font-size="10" fill="#666">(Decision, Speech)</text>
    <path d="M 280 100 Q 360 80 400 120 Q 430 160 420 210 Q 410 260 360 280 Q 310 290 270 270" fill="#BAFFC9" stroke="#333" stroke-width="2"/>
    <text x="340" y="180" text-anchor="middle" font-size="13" font-weight="bold">Parietal Lobe</text>
    <text x="340" y="200" text-anchor="middle" font-size="10" fill="#666">(Touch, Taste)</text>
    <path d="M 400 120 Q 460 140 470 190 Q 480 240 450 280 Q 420 310 380 290 Q 430 240 400 120" fill="#BAE1FF" stroke="#333" stroke-width="2"/>
    <text x="445" y="210" text-anchor="middle" font-size="13" font-weight="bold">Occipital Lobe</text>
    <text x="445" y="230" text-anchor="middle" font-size="10" fill="#666">(Vision)</text>
    <path d="M 160 230 Q 180 300 220 340 Q 260 370 320 370 Q 370 360 400 320 Q 360 300 320 280 Q 260 270 210 250" fill="#FFFFBA" stroke="#333" stroke-width="2"/>
    <text x="280" y="340" text-anchor="middle" font-size="13" font-weight="bold">Temporal Lobe</text>
    <text x="280" y="360" text-anchor="middle" font-size="10" fill="#666">(Hearing, Memory)</text>
    <path d="M 370 320 Q 420 340 430 390 Q 440 440 390 460 Q 350 470 320 440 Q 340 390 370 320" fill="#FFD4BA" stroke="#333" stroke-width="2"/>
    <text x="385" y="410" text-anchor="middle" font-size="13" font-weight="bold">Cerebellum</text>
    <text x="385" y="430" text-anchor="middle" font-size="10" fill="#666">(Balance)</text>
    <path d="M 300 380 L 290 440 L 310 460 L 330 440 L 320 380 Z" fill="#E6BABA" stroke="#333" stroke-width="2"/>
    <text x="310" y="440" text-anchor="middle" font-size="12" font-weight="bold">Brain</text>
    <text x="310" y="455" text-anchor="middle" font-size="12" font-weight="bold">Stem</text>
</svg>'''

SKELETON_SVG = '''<svg width="500" height="650" viewBox="0 0 500 650" xmlns="http://www.w3.org/2000/svg">
    <rect width="500" height="650" fill="#FAFAFA" rx="15"/>
    <text x="250" y="35" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Human Skeleton</text>
    <line x1="50" y1="55" x2="450" y2="55" stroke="#ddd" stroke-width="1"/>
    <path d="M 210 70 Q 210 45 230 40 Q 250 35 270 40 Q 290 45 290 70 Q 290 100 270 110 Q 250 120 230 110 Q 210 100 210 70" fill="#F5DEB3" stroke="#8B7355" stroke-width="2"/>
    <text x="250" y="85" text-anchor="middle" font-size="12" font-weight="bold">Skull</text>
    <line x1="250" y1="130" x2="250" y2="400" stroke="#A0522D" stroke-width="3"/>
    <path d="M 225 155 Q 190 165 170 175" stroke="#A0522D" stroke-width="3" fill="none"/>
    <path d="M 275 155 Q 310 165 330 175" stroke="#A0522D" stroke-width="3" fill="none"/>
    <text x="165" y="185" font-size="10">Clavicle</text>
    <path d="M 170 175 Q 155 215 160 250" stroke="#A0522D" stroke-width="2" fill="none"/>
    <path d="M 330 175 Q 345 215 340 250" stroke="#A0522D" stroke-width="2" fill="none"/>
    <path d="M 250 170 Q 215 175 205 190 Q 200 210 215 230" stroke="#A0522D" stroke-width="2" fill="none"/>
    <path d="M 250 170 Q 285 175 295 190 Q 300 210 285 230" stroke="#A0522D" stroke-width="2" fill="none"/>
    <path d="M 250 200 Q 220 205 215 220" stroke="#A0522D" stroke-width="2" fill="none"/>
    <path d="M 250 200 Q 280 205 285 220" stroke="#A0522D" stroke-width="2" fill="none"/>
    <text x="195" y="215" font-size="10">Ribcage</text>
    <line x1="165" y1="260" x2="150" y2="340" stroke="#A0522D" stroke-width="3"/>
    <line x1="335" y1="260" x2="350" y2="340" stroke="#A0522D" stroke-width="3"/>
    <text x="140" y="300" font-size="10">Humerus</text>
    <line x1="150" y1="345" x2="155" y2="420" stroke="#A0522D" stroke-width="2"/>
    <line x1="350" y1="345" x2="345" y2="420" stroke="#A0522D" stroke-width="2"/>
    <path d="M 220 400 Q 250 380 280 400 Q 290 430 280 450 Q 250 460 220 450 Q 210 430 220 400" fill="#F5DEB3" stroke="#A0522D" stroke-width="2"/>
    <text x="250" y="435" text-anchor="middle" font-size="11" font-weight="bold">Pelvis</text>
    <line x1="230" y1="460" x2="220" y2="550" stroke="#A0522D" stroke-width="4"/>
    <line x1="270" y1="460" x2="280" y2="550" stroke="#A0522D" stroke-width="4"/>
    <text x="200" y="510" font-size="10">Femur</text>
    <line x1="218" y1="560" x2="215" y2="600" stroke="#A0522D" stroke-width="2"/>
    <line x1="228" y1="560" x2="230" y2="600" stroke="#A0522D" stroke-width="2"/>
    <line x1="280" y1="560" x2="278" y2="600" stroke="#A0522D" stroke-width="2"/>
    <line x1="290" y1="560" x2="292" y2="600" stroke="#A0522D" stroke-width="2"/>
    <text x="250" y="590" text-anchor="middle" font-size="10">Tibia/Fibula</text>
    <ellipse cx="220" cy="610" rx="25" ry="6" fill="#F5DEB3" stroke="#A0522D" stroke-width="1"/>
    <ellipse cx="280" cy="610" rx="25" ry="6" fill="#F5DEB3" stroke="#A0522D" stroke-width="1"/>
</svg>'''

HEART_SVG = '''<svg width="550" height="500" viewBox="0 0 550 500" xmlns="http://www.w3.org/2000/svg">
    <rect width="550" height="500" fill="#FAFAFA" rx="15"/>
    <text x="275" y="35" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Human Heart</text>
    <line x1="50" y1="55" x2="500" y2="55" stroke="#ddd" stroke-width="1"/>
    <path d="M 275 100 Q 310 80 320 120 Q 330 160 290 170" fill="#E8A0A0" stroke="#C0392B" stroke-width="2"/>
    <text x="320" y="110" font-size="11" font-weight="bold">Aorta</text>
    <path d="M 260 130 Q 230 140 220 170" fill="none" stroke="#1565C0" stroke-width="3"/>
    <text x="210" y="160" font-size="10">Pulmonary Artery</text>
    <text x="210" y="172" font-size="9">(to lungs)</text>
    <path d="M 295 145 Q 340 155 340 185" fill="none" stroke="#2980B9" stroke-width="3"/>
    <text x="348" y="165" font-size="10">Superior Vena Cava</text>
    <path d="M 315 190 Q 360 210 350 250 Q 340 280 300 270 Q 290 240 315 190" fill="#E8A0A0" stroke="#C0392B" stroke-width="2"/>
    <text x="335" y="235" text-anchor="middle" font-size="11" font-weight="bold">Right Atrium</text>
    <path d="M 235 180 Q 190 200 200 240 Q 210 270 255 260 Q 265 230 235 180" fill="#E8A0A0" stroke="#C0392B" stroke-width="2"/>
    <text x="215" y="230" text-anchor="middle" font-size="11" font-weight="bold">Left Atrium</text>
    <path d="M 305 280 Q 370 310 350 380 Q 330 440 280 420 Q 265 370 305 280" fill="#FFB3B3" stroke="#C0392B" stroke-width="2"/>
    <text x="330" y="365" text-anchor="middle" font-size="11" font-weight="bold">Right Ventricle</text>
    <path d="M 245 270 Q 180 300 200 380 Q 220 430 260 410 Q 280 360 245 270" fill="#FFB3B3" stroke="#C0392B" stroke-width="2"/>
    <text x="220" y="350" text-anchor="middle" font-size="11" font-weight="bold">Left Ventricle</text>
    <line x1="270" y1="260" x2="280" y2="410" stroke="#C0392B" stroke-width="2" stroke-dasharray="4,3"/>
    <text x="285" y="340" font-size="9">Septum</text>
    <text x="275" y="470" text-anchor="middle" font-size="12" fill="#666">The heart pumps blood to lungs (blue) and body (red)</text>
</svg>'''

EYE_SVG = '''<svg width="550" height="400" viewBox="0 0 550 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="550" height="400" fill="#FAFAFA" rx="15"/>
    <text x="275" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Human Eye</text>
    <line x1="50" y1="50" x2="500" y2="50" stroke="#ddd" stroke-width="1"/>
    <ellipse cx="275" cy="180" rx="140" ry="80" fill="#FFF8DC" stroke="#8B7355" stroke-width="2"/>
    <text x="165" y="145" font-size="11" font-weight="bold">Sclera</text>
    <text x="165" y="158" font-size="9">(white of eye)</text>
    <ellipse cx="340" cy="180" rx="50" ry="38" fill="none" stroke="#87CEEB" stroke-width="2"/>
    <text x="380" y="160" font-size="10" font-weight="bold">Cornea</text>
    <ellipse cx="320" cy="180" rx="40" ry="35" fill="#4A7023"/>
    <text x="320" y="145" text-anchor="middle" font-size="11" font-weight="bold">Iris</text>
    <circle cx="325" cy="180" r="15" fill="black"/>
    <text x="325" y="165" text-anchor="middle" font-size="10" fill="white">Pupil</text>
    <ellipse cx="300" cy="180" rx="20" ry="12" fill="#FFFACD" stroke="#DAA520" stroke-width="1"/>
    <text x="270" y="205" font-size="10" font-weight="bold">Lens</text>
    <path d="M 140 180 Q 150 260 200 290 Q 250 310 300 310" fill="none" stroke="#E74C3C" stroke-width="2" stroke-dasharray="4,2"/>
    <text x="160" y="300" font-size="10">Retina</text>
    <path d="M 145 185 Q 100 200 80 220" fill="none" stroke="#8B4513" stroke-width="4"/>
    <text x="60" y="225" font-size="10" font-weight="bold">Optic</text>
    <text x="60" y="238" font-size="10" font-weight="bold">Nerve</text>
    <text x="275" y="370" text-anchor="middle" font-size="12" fill="#666">Light enters through pupil, focused by lens, detected by retina</text>
</svg>'''

LUNGS_SVG = '''<svg width="550" height="450" viewBox="0 0 550 450" xmlns="http://www.w3.org/2000/svg">
    <rect width="550" height="450" fill="#FAFAFA" rx="15"/>
    <text x="275" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Respiratory System</text>
    <line x1="50" y1="50" x2="500" y2="50" stroke="#ddd" stroke-width="1"/>
    <rect x="260" y="60" width="30" height="80" fill="#D2B48C" stroke="#8B4513" stroke-width="2" rx="5"/>
    <text x="275" y="55" text-anchor="middle" font-size="12" font-weight="bold">Trachea</text>
    <text x="275" y="152" text-anchor="middle" font-size="9">(windpipe)</text>
    <path d="M 260 130 Q 230 150 200 160" stroke="#8B4513" stroke-width="5" fill="none"/>
    <path d="M 290 130 Q 320 150 350 160" stroke="#8B4513" stroke-width="5" fill="none"/>
    <text x="200" y="152" font-size="10">Bronchus</text>
    <text x="340" y="152" font-size="10">Bronchus</text>
    <path d="M 200 160 Q 140 200 130 280 Q 120 370 160 400 Q 200 420 240 380 Q 250 320 230 260 Q 210 200 200 160" fill="#FFB6C1" stroke="#FF69B4" stroke-width="2"/>
    <path d="M 350 160 Q 410 200 420 280 Q 430 370 390 400 Q 350 420 310 380 Q 300 320 320 260 Q 340 200 350 160" fill="#FFB6C1" stroke="#FF69B4" stroke-width="2"/>
    <text x="170" y="300" text-anchor="middle" font-size="14" font-weight="bold">Left</text>
    <text x="170" y="318" text-anchor="middle" font-size="14" font-weight="bold">Lung</text>
    <text x="380" y="300" text-anchor="middle" font-size="14" font-weight="bold">Right</text>
    <text x="380" y="318" text-anchor="middle" font-size="14" font-weight="bold">Lung</text>
    <path d="M 80 400 Q 275 440 470 400" fill="none" stroke="#8B4513" stroke-width="3"/>
    <text x="275" y="435" text-anchor="middle" font-size="12" font-weight="bold">Diaphragm</text>
    <text x="275" y="450" text-anchor="middle" font-size="11" fill="#666">Oxygen enters, CO₂ exits during breathing</text>
</svg>'''

KIDNEY_SVG = '''<svg width="550" height="400" viewBox="0 0 550 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="550" height="400" fill="#FAFAFA" rx="15"/>
    <text x="275" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Kidney Anatomy</text>
    <line x1="50" y1="50" x2="500" y2="50" stroke="#ddd" stroke-width="1"/>
    <path d="M 120 120 Q 100 180 110 250 Q 120 300 170 300 Q 200 300 210 250 Q 220 180 200 120 Q 170 100 120 120" fill="#FFDAB9" stroke="#E65100" stroke-width="2"/>
    <text x="160" y="320" text-anchor="middle" font-size="13" font-weight="bold">Left Kidney</text>
    <path d="M 340 120 Q 320 180 330 250 Q 340 300 390 300 Q 420 300 430 250 Q 440 180 420 120 Q 390 100 340 120" fill="#FFDAB9" stroke="#E65100" stroke-width="2"/>
    <text x="380" y="320" text-anchor="middle" font-size="13" font-weight="bold">Right Kidney</text>
    <path d="M 275 160 L 210 170" stroke="#E74C3C" stroke-width="3" fill="none"/>
    <path d="M 275 160 L 340 170" stroke="#E74C3C" stroke-width="3" fill="none"/>
    <text x="275" y="150" text-anchor="middle" font-size="10" font-weight="bold" fill="#E74C3C">Renal Artery</text>
    <path d="M 210 240 L 275 250 L 340 240" stroke="#2980B9" stroke-width="3" fill="none"/>
    <text x="275" y="270" text-anchor="middle" font-size="10" font-weight="bold" fill="#2980B9">Renal Vein</text>
    <path d="M 170 300 Q 200 340 275 350 Q 350 340 380 300" stroke="#8B4513" stroke-width="3" fill="none"/>
    <text x="275" y="370" text-anchor="middle" font-size="11">Ureters</text>
    <ellipse cx="275" cy="385" rx="50" ry="12" fill="#D2B48C" stroke="#8B4513" stroke-width="2"/>
    <text x="275" y="390" text-anchor="middle" font-size="10">Bladder</text>
</svg>'''

CELL_SVG = '''<svg width="600" height="450" viewBox="0 0 600 450" xmlns="http://www.w3.org/2000/svg">
    <rect width="600" height="450" fill="#FAFAFA" rx="15"/>
    <text x="300" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Animal Cell</text>
    <line x1="50" y1="50" x2="550" y2="50" stroke="#ddd" stroke-width="1"/>
    <ellipse cx="300" cy="200" rx="200" ry="150" fill="none" stroke="#0f3460" stroke-width="2" stroke-dasharray="8,4"/>
    <text x="520" y="90" font-size="11" font-weight="bold">Cell Membrane</text>
    <ellipse cx="300" cy="170" rx="70" ry="55" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="300" y="160" text-anchor="middle" font-size="14" font-weight="bold">Nucleus</text>
    <circle cx="300" cy="195" r="15" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
    <text x="300" y="200" text-anchor="middle" font-size="9">DNA</text>
    <ellipse cx="180" cy="140" rx="40" ry="25" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
    <text x="180" y="120" text-anchor="middle" font-size="11" font-weight="bold">Mitochondria</text>
    <text x="180" y="135" text-anchor="middle" font-size="9">(Power House)</text>
    <path d="M 450 200 Q 490 190 480 220 Q 500 210 490 240" fill="none" stroke="#6a1b9a" stroke-width="2"/>
    <text x="500" y="225" font-size="11" font-weight="bold">ER</text>
    <path d="M 480 280 L 510 280 L 500 300 L 530 300 L 520 320" fill="none" stroke="#c62828" stroke-width="2"/>
    <text x="535" y="305" font-size="11" font-weight="bold">Golgi</text>
    <circle cx="420" cy="300" r="5" fill="#c62828"/>
    <circle cx="435" cy="312" r="5" fill="#c62828"/>
    <circle cx="410" cy="320" r="5" fill="#c62828"/>
    <text x="450" y="330" font-size="10">Ribosomes</text>
</svg>'''

PLANT_CELL_SVG = '''<svg width="600" height="450" viewBox="0 0 600 450" xmlns="http://www.w3.org/2000/svg">
    <rect width="600" height="450" fill="#FAFAFA" rx="15"/>
    <text x="300" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Plant Cell</text>
    <line x1="50" y1="50" x2="550" y2="50" stroke="#ddd" stroke-width="1"/>
    <rect x="80" y="70" width="440" height="330" rx="10" fill="none" stroke="#8B4513" stroke-width="3"/>
    <text x="540" y="100" font-size="11" font-weight="bold">Cell Wall</text>
    <rect x="95" y="85" width="410" height="300" rx="8" fill="none" stroke="#0f3460" stroke-width="2" stroke-dasharray="6,3"/>
    <text x="540" y="130" font-size="11" font-weight="bold">Cell Membrane</text>
    <ellipse cx="300" cy="170" rx="65" ry="50" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="300" y="165" text-anchor="middle" font-size="13" font-weight="bold">Nucleus</text>
    <ellipse cx="460" cy="130" rx="45" ry="30" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="460" y="115" text-anchor="middle" font-size="11" font-weight="bold">Chloroplast</text>
    <text x="460" y="130" text-anchor="middle" font-size="9">(Photosynthesis)</text>
    <ellipse cx="160" cy="280" rx="60" ry="45" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="160" y="280" text-anchor="middle" font-size="12" font-weight="bold">Vacuole</text>
    <text x="160" y="295" text-anchor="middle" font-size="9">(Storage)</text>
    <ellipse cx="180" cy="140" rx="35" ry="20" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
    <text x="180" y="120" font-size="10">Mitochondria</text>
</svg>'''

NEURON_SVG = '''<svg width="650" height="400" viewBox="0 0 650 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="650" height="400" fill="#FAFAFA" rx="15"/>
    <text x="325" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Neuron (Nerve Cell)</text>
    <line x1="50" y1="50" x2="600" y2="50" stroke="#ddd" stroke-width="1"/>
    <ellipse cx="325" cy="180" rx="50" ry="45" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="325" y="175" text-anchor="middle" font-size="13" font-weight="bold">Cell Body</text>
    <text x="325" y="192" text-anchor="middle" font-size="9">(Soma)</text>
    <line x1="325" y1="135" x2="325" y2="90" stroke="#1565c0" stroke-width="3"/>
    <text x="325" y="80" text-anchor="middle" font-size="11">Axon</text>
    <line x1="325" y1="90" x2="325" y2="70" stroke="#1565c0" stroke-width="3"/>
    <circle cx="325" cy="70" r="8" fill="#1565c0"/>
    <circle cx="335" cy="65" r="6" fill="#1565c0"/>
    <circle cx="315" cy="65" r="6" fill="#1565c0"/>
    <text x="350" y="65" font-size="10">Axon Terminals</text>
    <path d="M 310 220 Q 280 260 240 250" stroke="#1565c0" stroke-width="2" fill="none"/>
    <path d="M 290 230 Q 260 280 220 290" stroke="#1565c0" stroke-width="2" fill="none"/>
    <path d="M 340 220 Q 370 260 410 250" stroke="#1565c0" stroke-width="2" fill="none"/>
    <path d="M 360 230 Q 390 280 430 290" stroke="#1565c0" stroke-width="2" fill="none"/>
    <text x="200" y="310" text-anchor="middle" font-size="11" font-weight="bold">Dendrites</text>
    <text x="200" y="325" text-anchor="middle" font-size="9">(Receive signals)</text>
    <ellipse cx="325" cy="230" rx="40" ry="12" fill="none" stroke="#e65100" stroke-width="1.5" stroke-dasharray="4,2"/>
    <text x="400" y="235" font-size="10" fill="#e65100">Myelin Sheath</text>
    <text x="325" y="380" text-anchor="middle" font-size="12" fill="#666">Neurons transmit electrical signals throughout the body</text>
</svg>'''

MITOSIS_SVG = '''<svg width="750" height="350" viewBox="0 0 750 350" xmlns="http://www.w3.org/2000/svg">
    <rect width="750" height="350" fill="#FAFAFA" rx="15"/>
    <text x="375" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Mitosis - Cell Division (PMAT)</text>
    <line x1="50" y1="55" x2="700" y2="55" stroke="#ddd" stroke-width="1"/>
    <rect x="20" y="80" width="130" height="100" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="8"/>
    <text x="85" y="100" text-anchor="middle" font-size="13" font-weight="bold">PROPHASE</text>
    <circle cx="85" cy="140" r="22" fill="none" stroke="#333" stroke-width="2"/>
    <line x1="68" y1="125" x2="102" y2="155" stroke="#e94560" stroke-width="2"/>
    <line x1="102" y1="125" x2="68" y2="155" stroke="#e94560" stroke-width="2"/>
    <text x="85" y="195" text-anchor="middle" font-size="9">Chromosomes condense</text>
    <rect x="170" y="80" width="130" height="100" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="8"/>
    <text x="235" y="100" text-anchor="middle" font-size="13" font-weight="bold">METAPHASE</text>
    <circle cx="235" cy="140" r="22" fill="none" stroke="#333" stroke-width="2"/>
    <line x1="218" y1="140" x2="252" y2="140" stroke="#4ecdc4" stroke-width="3"/>
    <text x="235" y="195" text-anchor="middle" font-size="9">Align at center</text>
    <rect x="320" y="80" width="130" height="100" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="8"/>
    <text x="385" y="100" text-anchor="middle" font-size="13" font-weight="bold">ANAPHASE</text>
    <circle cx="385" cy="140" r="22" fill="none" stroke="#333" stroke-width="2"/>
    <line x1="372" y1="128" x2="372" y2="152" stroke="#e94560" stroke-width="2"/>
    <line x1="398" y1="128" x2="398" y2="152" stroke="#e94560" stroke-width="2"/>
    <text x="385" y="195" text-anchor="middle" font-size="9">Separate to poles</text>
    <rect x="470" y="80" width="260" height="100" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2" rx="8"/>
    <text x="600" y="100" text-anchor="middle" font-size="13" font-weight="bold">TELOPHASE</text>
    <circle cx="550" cy="140" r="16" fill="none" stroke="#333" stroke-width="2"/>
    <circle cx="640" cy="140" r="16" fill="none" stroke="#333" stroke-width="2"/>
    <text x="600" y="195" text-anchor="middle" font-size="9">Two nuclei form</text>
    <text x="155" y="135" text-anchor="middle" font-size="20">→</text>
    <text x="305" y="135" text-anchor="middle" font-size="20">→</text>
    <text x="455" y="135" text-anchor="middle" font-size="20">→</text>
    <text x="375" y="250" text-anchor="middle" font-size="14" font-weight="bold">Result: 2 identical daughter cells!</text>
    <text x="375" y="275" text-anchor="middle" font-size="11" fill="#666">Used for growth, repair, and asexual reproduction</text>
</svg>'''

PHOTOSYNTHESIS_SVG = '''<svg width="600" height="450" viewBox="0 0 600 450" xmlns="http://www.w3.org/2000/svg">
    <rect width="600" height="450" fill="#FAFAFA" rx="15"/>
    <text x="300" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Photosynthesis</text>
    <line x1="50" y1="50" x2="550" y2="50" stroke="#ddd" stroke-width="1"/>
    <circle cx="80" cy="100" r="35" fill="#FFD700"/>
    <text x="80" y="105" text-anchor="middle" font-size="12">☀️ SUN</text>
    <rect x="250" y="180" width="120" height="100" fill="#228B22" rx="10"/>
    <text x="310" y="235" text-anchor="middle" font-size="14">🌿 PLANT</text>
    <text x="180" y="160" fill="#8B4513" font-size="12">CO₂ →</text>
    <line x1="200" y1="160" x2="240" y2="200" stroke="#8B4513" stroke-width="2"/>
    <text x="180" y="300" fill="#4169E1" font-size="12">H₂O →</text>
    <line x1="200" y1="300" x2="240" y2="260" stroke="#4169E1" stroke-width="2"/>
    <text x="400" y="160" fill="#32CD32" font-size="12">← O₂</text>
    <line x1="380" y1="160" x2="410" y2="200" stroke="#32CD32" stroke-width="2"/>
    <text x="400" y="300" fill="#FFD700" font-size="12">← Glucose</text>
    <line x1="380" y1="300" x2="410" y2="260" stroke="#FFD700" stroke-width="2"/>
    <rect x="150" y="360" width="300" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="8"/>
    <text x="300" y="385" text-anchor="middle" font-size="13" font-weight="bold">6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂</text>
</svg>'''

CIRCLE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="400" fill="#FAFAFA" rx="15"/>
    <text x="200" y="35" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Circle</text>
    <circle cx="200" cy="200" r="120" fill="none" stroke="#0f3460" stroke-width="3"/>
    <circle cx="200" cy="200" r="5" fill="#e94560"/>
    <line x1="200" y1="200" x2="320" y2="200" stroke="#e94560" stroke-width="2"/>
    <text x="260" y="190" font-size="12" fill="#e94560">Radius (r)</text>
    <text x="200" y="225" text-anchor="middle" font-size="12" font-weight="bold">Center</text>
    <text x="200" y="370" text-anchor="middle" font-size="12" fill="#666">Circumference = 2πr</text>
</svg>'''

SQUARE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="400" fill="#FAFAFA" rx="15"/>
    <text x="200" y="35" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Square</text>
    <rect x="100" y="100" width="200" height="200" fill="none" stroke="#0f3460" stroke-width="3"/>
    <text x="200" y="85" text-anchor="middle" font-size="12">Side</text>
    <line x1="100" y1="100" x2="300" y2="100" stroke="#e94560" stroke-width="2"/>
    <text x="200" y="350" text-anchor="middle" font-size="12" fill="#666">Area = s² | Perimeter = 4s</text>
</svg>'''

TRIANGLE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="400" fill="#FAFAFA" rx="15"/>
    <text x="200" y="35" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">Right Angle Triangle</text>
    <polygon points="100,280 300,280 100,120" fill="none" stroke="#0f3460" stroke-width="3"/>
    <polygon points="100,260 120,260 120,280" fill="none" stroke="#e94560" stroke-width="2"/>
    <text x="115" y="275" text-anchor="middle" font-size="12" fill="#e94560">90°</text>
    <text x="200" y="330" text-anchor="middle" font-size="12" font-weight="bold">Pythagorean Theorem</text>
    <text x="200" y="350" text-anchor="middle" font-size="13" fill="#666">a² + b² = c²</text>
</svg>'''

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)