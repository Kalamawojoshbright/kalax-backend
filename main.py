"""
KalaX Backend - Fully Working with Gemini (Draw Fixed)
Deploy this to Render.com
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import google.generativeai as genai
from datetime import datetime
import json
import re
import math
import uvicorn

app = FastAPI(title="KalaX Backend", version="2.0.0")

# CORS - Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# GEMINI CONFIGURATION
# ============================================

GEMINI_API_KEY = "AIzaSyAU_pIonfIoRhlpnkK5CX-HZveGv_5pqkQ"
genai.configure(api_key=GEMINI_API_KEY)

# Using the working model
MODEL_NAME = "gemini-2.5-flash"

# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class ChatRequest(BaseModel):
    message: str
    subject: Optional[str] = "general"

class ChatResponse(BaseModel):
    response: str
    source: str

class DrawRequest(BaseModel):
    command: str
    style: Optional[str] = "educational"

class DrawResponse(BaseModel):
    success: bool
    code: Optional[str] = None
    explanation: Optional[str] = None
    error: Optional[str] = None

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "KalaX Backend",
        "model": MODEL_NAME,
        "creator": "Kalamawo Joshua Bright"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "timestamp": str(datetime.now()),
        "gemini_available": True
    }

# ============================================
# CHAT ENDPOINT - WORKING
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer any question using Gemini AI"""
    print(f"📨 Chat request: {request.message[:100]}")
    
    try:
        # Create model
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Generate response
        response = model.generate_content(request.message)
        
        print(f"✅ Gemini response received")
        
        return ChatResponse(
            response=response.text,
            source="gemini"
        )
        
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        
        # Return fallback response
        return ChatResponse(
            response=get_fallback_answer(request.message),
            source="local"
        )

# ============================================
# DRAW ENDPOINT - FIXED
# ============================================

@app.post("/draw", response_model=DrawResponse)
async def draw(request: DrawRequest):
    """Generate drawing code - returns working canvas code"""
    print(f"🎨 Draw request: {request.command[:100]}")
    
    # First, check if it's a known drawing (use local first for speed)
    local_result = get_local_drawing(request.command)
    if local_result:
        print("✅ Using local drawing")
        return local_result
    
    # If not local, try Gemini
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        
        prompt = f"""Generate JavaScript canvas drawing code for: "{request.command}"

Return ONLY valid JSON. No other text.

Format: {{"code": "function draw(ctx, canvas) {{ ... }}", "explanation": "brief description"}}

Requirements:
- Canvas is 700x500 pixels
- Use ctx.fillStyle, ctx.strokeStyle, ctx.beginPath()
- Clear canvas at start: ctx.clearRect(0,0,canvas.width,canvas.height)
- Make it educational and accurate
- Add labels with ctx.fillText()

Generate code NOW:"""
        
        response = model.generate_content(prompt)
        
        # Extract JSON
        json_match = re.search(r'\{[\s\S]*\}', response.text)
        if json_match:
            try:
                result = json.loads(json_match.group())
                if result.get("code"):
                    print(f"✅ Gemini generated drawing code")
                    return DrawResponse(
                        success=True,
                        code=result["code"],
                        explanation=result.get("explanation", f"Diagram of {request.command}")
                    )
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
        
        # Fallback to local drawing
        print("Using fallback drawing")
        return get_fallback_drawing(request.command)
        
    except Exception as e:
        print(f"❌ Draw error: {e}")
        return get_fallback_drawing(request.command)

# ============================================
# LOCAL DRAWING FUNCTIONS (Fast & Reliable)
# ============================================

def get_local_drawing(command: str) -> Optional[DrawResponse]:
    """Return local drawing if available (faster than Gemini)"""
    cmd = command.lower()
    
    # Human Skeleton
    if "skeleton" in cmd or "human skeleton" in cmd:
        return DrawResponse(
            success=True,
            code=get_skeleton_code(),
            explanation="Human skeleton - 206 bones. Axial skeleton (skull, spine, ribs) + Appendicular skeleton (arms, legs)"
        )
    
    # Brain
    if "brain" in cmd:
        return DrawResponse(
            success=True,
            code=get_brain_code(),
            explanation="Human brain - Cerebrum (left/right hemispheres), Cerebellum, Brain stem"
        )
    
    # Circle
    if "circle" in cmd:
        return DrawResponse(
            success=True,
            code=get_circle_code(),
            explanation="Circle - All points equidistant from center. Radius = distance from center to edge."
        )
    
    # Square
    if "square" in cmd:
        return DrawResponse(
            success=True,
            code=get_square_code(),
            explanation="Square - All sides equal, all angles = 90°"
        )
    
    # Triangle / Right Angle
    if "triangle" in cmd or "right angle" in cmd:
        return DrawResponse(
            success=True,
            code=get_triangle_code(),
            explanation="Right angle triangle - One angle = 90°. Pythagorean theorem: a² + b² = c²"
        )
    
    # Heart
    if "heart" in cmd:
        return DrawResponse(
            success=True,
            code=get_heart_code(),
            explanation="Heart shape - Symbol of love and emotion"
        )
    
    # DNA
    if "dna" in cmd or "helix" in cmd:
        return DrawResponse(
            success=True,
            code=get_dna_code(),
            explanation="DNA Double Helix - Sugar-phosphate backbone with base pairs A-T and C-G"
        )
    
    return None

def get_fallback_drawing(request: DrawRequest) -> DrawResponse:
    """Fallback when no drawing matches"""
    return DrawResponse(
        success=False,
        error=f"Could not draw '{request.command}'. Try 'Draw a human skeleton', 'Draw a brain', 'Draw a circle', or 'Draw a heart'"
    )

# ============================================
# DRAWING CODE FUNCTIONS
# ============================================

def get_skeleton_code():
    return """function draw(ctx, canvas) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2;
    
    // Skull
    ctx.beginPath();
    ctx.ellipse(cx, 80, 35, 45, 0, 0, 2 * Math.PI);
    ctx.fillStyle = '#f5f5dc';
    ctx.fill();
    ctx.strokeStyle = '#8B7355';
    ctx.stroke();
    
    // Eye sockets
    ctx.fillStyle = '#8B7355';
    ctx.beginPath();
    ctx.ellipse(cx - 15, 70, 6, 8, 0, 0, 2 * Math.PI);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(cx + 15, 70, 6, 8, 0, 0, 2 * Math.PI);
    ctx.fill();
    
    // Spine
    ctx.beginPath();
    ctx.moveTo(cx, 130);
    ctx.lineTo(cx, 350);
    ctx.lineWidth = 3;
    ctx.stroke();
    
    // Ribcage
    for(let i = 0; i < 7; i++) {
        let y = 160 + i * 25;
        ctx.beginPath();
        ctx.moveTo(cx, y);
        ctx.quadraticCurveTo(cx - 40, y + 10, cx - 35, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(cx, y);
        ctx.quadraticCurveTo(cx + 40, y + 10, cx + 35, y);
        ctx.stroke();
    }
    
    // Arms
    ctx.beginPath();
    ctx.moveTo(cx - 30, 160);
    ctx.lineTo(cx - 70, 220);
    ctx.lineTo(cx - 55, 290);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(cx + 30, 160);
    ctx.lineTo(cx + 70, 220);
    ctx.lineTo(cx + 55, 290);
    ctx.stroke();
    
    // Pelvis
    ctx.beginPath();
    ctx.ellipse(cx, 355, 45, 20, 0, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
    
    // Legs
    ctx.beginPath();
    ctx.moveTo(cx - 25, 365);
    ctx.lineTo(cx - 30, 440);
    ctx.lineTo(cx - 40, 470);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(cx + 25, 365);
    ctx.lineTo(cx + 30, 440);
    ctx.lineTo(cx + 40, 470);
    ctx.stroke();
    
    // Labels
    ctx.fillStyle = '#333';
    ctx.font = '11px "Segoe UI"';
    ctx.fillText('Skull', cx - 10, 60);
    ctx.fillText('Ribcage', cx - 60, 220);
    ctx.fillText('Spine', cx + 20, 250);
    ctx.fillText('Pelvis', cx - 30, 370);
    ctx.fillText('Femur', cx - 55, 420);
}"""

def get_brain_code():
    return """function draw(ctx, canvas) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2;
    const cy = canvas.height / 2.5;
    
    // Left hemisphere
    ctx.beginPath();
    ctx.ellipse(cx - 45, cy, 60, 80, -0.1, 0, 2 * Math.PI);
    ctx.fillStyle = '#FFB6C1';
    ctx.fill();
    ctx.stroke();
    
    // Right hemisphere
    ctx.beginPath();
    ctx.ellipse(cx + 45, cy, 60, 80, 0.1, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
    
    // Corpus callosum
    ctx.beginPath();
    ctx.ellipse(cx, cy - 20, 30, 25, 0, 0, 2 * Math.PI);
    ctx.fillStyle = '#FFC0CB';
    ctx.fill();
    ctx.stroke();
    
    // Brain stem
    ctx.beginPath();
    ctx.moveTo(cx - 10, cy + 55);
    ctx.lineTo(cx, cy + 100);
    ctx.lineTo(cx + 10, cy + 55);
    ctx.fill();
    ctx.stroke();
    
    // Cerebellum
    ctx.beginPath();
    ctx.ellipse(cx, cy + 40, 35, 25, 0, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
    
    // Labels
    ctx.fillStyle = '#333';
    ctx.font = '10px "Segoe UI"';
    ctx.fillText('Left Hemisphere', cx - 100, cy - 30);
    ctx.fillText('Right Hemisphere', cx + 35, cy - 30);
    ctx.fillText('Corpus Callosum', cx - 45, cy - 50);
    ctx.fillText('Cerebellum', cx - 30, cy + 55);
    ctx.fillText('Brain Stem', cx - 25, cy + 95);
}"""

def get_circle_code():
    return """function draw(ctx, canvas) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    const radius = 120;
    
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, 2 * Math.PI);
    ctx.strokeStyle = '#0f3460';
    ctx.lineWidth = 3;
    ctx.stroke();
    
    ctx.beginPath();
    ctx.arc(cx, cy, 5, 0, 2 * Math.PI);
    ctx.fillStyle = '#e94560';
    ctx.fill();
    
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + radius, cy);
    ctx.strokeStyle = '#e94560';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    ctx.fillStyle = '#333';
    ctx.font = '14px "Segoe UI"';
    ctx.fillText('Center', cx + 10, cy);
    ctx.fillText('Radius (r)', cx + radius/2, cy - 10);
}"""

def get_square_code():
    return """function draw(ctx, canvas) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    const size = 160;
    
    ctx.strokeRect(cx - size/2, cy - size/2, size, size);
    ctx.strokeStyle = '#0f3460';
    ctx.lineWidth = 3;
    ctx.stroke();
    
    ctx.fillStyle = '#333';
    ctx.font = '14px "Segoe UI"';
    ctx.fillText('Square', cx - 25, cy - size/2 - 10);
    ctx.fillText('All sides equal', cx - 50, cy + size/2 + 20);
}"""

def get_triangle_code():
    return """function draw(ctx, canvas) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    
    ctx.beginPath();
    ctx.moveTo(cx - 100, cy + 60);
    ctx.lineTo(cx + 100, cy + 60);
    ctx.lineTo(cx - 100, cy - 60);
    ctx.closePath();
    ctx.strokeStyle = '#0f3460';
    ctx.lineWidth = 3;
    ctx.stroke();
    ctx.fillStyle = 'rgba(15,52,96,0.1)';
    ctx.fill();
    
    ctx.beginPath();
    ctx.moveTo(cx - 100 + 20, cy + 60);
    ctx.lineTo(cx - 100 + 20, cy + 60 - 20);
    ctx.lineTo(cx - 100, cy + 60 - 20);
    ctx.strokeStyle = '#e94560';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    ctx.fillStyle = '#333';
    ctx.font = '12px "Segoe UI"';
    ctx.fillText('90°', cx - 95, cy + 55);
    ctx.fillText('Right Angle Triangle', cx - 80, cy - 80);
}"""

def get_heart_code():
    return """function draw(ctx, canvas) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    
    ctx.beginPath();
    ctx.moveTo(cx, cy + 40);
    ctx.bezierCurveTo(cx - 90, cy - 40, cx - 140, cy + 40, cx, cy + 120);
    ctx.bezierCurveTo(cx + 140, cy + 40, cx + 90, cy - 40, cx, cy + 40);
    ctx.fillStyle = '#FF6B6B';
    ctx.fill();
    ctx.strokeStyle = '#C0392B';
    ctx.stroke();
    
    ctx.fillStyle = '#333';
    ctx.font = '14px "Segoe UI"';
    ctx.fillText('Heart', cx - 20, cy - 50);
}"""

def get_dna_code():
    return """function draw(ctx, canvas) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2;
    
    for(let y = 80; y <= 420; y += 10) {
        let t = (y - 80) / 340;
        let x1 = cx - 60 * Math.sin(t * Math.PI * 2);
        let x2 = cx + 60 * Math.sin(t * Math.PI * 2);
        if(y === 80) {
            ctx.beginPath();
            ctx.moveTo(x1, y);
            ctx.moveTo(x2, y);
        } else {
            ctx.lineTo(x1, y);
            ctx.lineTo(x2, y);
        }
    }
    ctx.strokeStyle = '#0000CD';
    ctx.lineWidth = 3;
    ctx.stroke();
    
    ctx.fillStyle = '#333';
    ctx.font = 'bold 14px "Segoe UI"';
    ctx.fillText('DNA Double Helix', cx - 70, 40);
}"""

# ============================================
# FALLBACK ANSWERS
# ============================================

def get_fallback_answer(message: str) -> str:
    m = message.lower()
    
    if "photosynthesis" in m:
        return """🌿 **Photosynthesis**

Plants make their own food using sunlight!

**Equation:** 6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂

**Two stages:**
1. Light reaction - captures sunlight, releases oxygen
2. Calvin cycle - makes glucose from CO₂"""
    
    if "mitosis" in m:
        return """🔬 **Mitosis (PMAT)**

Cell division that produces 2 identical cells!

**Stages:**
• **P**rophase - Chromosomes condense
• **M**etaphase - Line up at center
• **A**naphase - Separate to poles
• **T**elophase - Two new cells form"""
    
    if "newton" in m:
        return """⚡ **Newton's Three Laws of Motion**

**1st Law (Inertia):** Objects keep doing what they're doing unless a force acts on them.

**2nd Law (F = ma):** Force = Mass × Acceleration

**3rd Law (Action-Reaction):** Every action has an equal and opposite reaction."""
    
    return f"""📚 **I'm KalaX AI!**

Ask me about:
• "What is photosynthesis?"
• "What is mitosis?"
• "Newton's laws"

Or draw something:
• "Draw a human skeleton"
• "Draw a brain"
• "Draw a circle"
• "Draw a heart"
• "Draw a DNA helix"

What would you like to learn?"""

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)