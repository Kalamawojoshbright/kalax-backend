"""
KalaX Backend - Working with Gemini API
Deploy this to Render.com
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
from datetime import datetime
import json
import re
import uvicorn

app = FastAPI()

# Enable CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# GEMINI API CONFIGURATION
# ============================================

GEMINI_API_KEY = "AIzaSyAU_pIonfIoRhlpnkK5CX-HZveGv_5pqkQ"
genai.configure(api_key=GEMINI_API_KEY)

# ✅ WORKING MODEL - Confirmed working
MODEL_NAME = "gemini-2.5-flash"

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
        "timestamp": str(datetime.now())
    }

# ============================================
# CHAT ENDPOINT - Gemini AI
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer any question using Gemini AI"""
    try:
        print(f"📨 Chat request: {request.message[:100]}...")
        
        # Create model instance
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Generate response
        response = model.generate_content(request.message)
        
        print(f"✅ Gemini response sent")
        
        return ChatResponse(
            response=response.text,
            source="gemini"
        )
        
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        
        # Fallback response
        return ChatResponse(
            response=get_local_answer(request.message),
            source="local_fallback"
        )

# ============================================
# DRAW ENDPOINT - Gemini AI
# ============================================

@app.post("/draw", response_model=DrawResponse)
async def draw(request: DrawRequest):
    """Generate drawing code using Gemini AI"""
    try:
        print(f"🎨 Draw request: {request.command[:100]}...")
        
        model = genai.GenerativeModel(MODEL_NAME)
        
        prompt = f"""Generate JavaScript drawing code for: "{request.command}"

Return ONLY valid JSON. No other text.
Format: {{"code": "function draw(ctx, canvas) {{ ... }}", "explanation": "description"}}

Requirements:
- Canvas is 700x500 pixels
- Use ctx.fillStyle, ctx.strokeStyle, ctx.beginPath()
- Add labels with ctx.fillText()
- Make it educational

Generate NOW:"""
        
        response = model.generate_content(prompt)
        
        # Extract JSON
        json_match = re.search(r'\{[\s\S]*\}', response.text)
        if json_match:
            try:
                result = json.loads(json_match.group())
                if result.get("code"):
                    return DrawResponse(
                        success=True,
                        code=result["code"],
                        explanation=result.get("explanation", f"Drawing of {request.command}")
                    )
            except:
                pass
        
        # Fallback
        return get_fallback_drawing(request.command)
        
    except Exception as e:
        print(f"❌ Draw error: {e}")
        return get_fallback_drawing(request.command)

# ============================================
# LOCAL FALLBACK FUNCTIONS
# ============================================

def get_local_answer(message):
    m = message.lower()
    
    if "photosynthesis" in m:
        return "🌿 **Photosynthesis**\n\nPlants make their own food using sunlight!\n\n**Equation:** 6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂\n\n**Two stages:**\n1. Light reaction - captures sunlight\n2. Calvin cycle - makes glucose"
    
    if "mitosis" in m:
        return "🔬 **Mitosis (PMAT)**\n\n**Stages:**\n• **P**rophase - Chromosomes condense\n• **M**etaphase - Line up at center\n• **A**naphase - Separate to poles\n• **T**elophase - Two new cells form"
    
    if "newton" in m:
        return "⚡ **Newton's Laws**\n\n**1st Law (Inertia):** Objects keep doing what they're doing\n**2nd Law (F=ma):** Force = mass × acceleration\n**3rd Law (Action-Reaction):** Every action has equal opposite reaction"
    
    if "hello" in m or "hi" in m:
        return "👋 Hello! I'm KalaX AI, created by Kalamawo Joshua Bright. Ask me anything about science, math, or say 'Draw a...'"
    
    return f"📚 I'm KalaX AI. Ask me 'What is photosynthesis?' or 'Draw a human skeleton'"

def get_fallback_drawing(command):
    cmd = command.lower()
    
    if "skeleton" in cmd:
        return DrawResponse(success=True, code=SKELETON_CODE, explanation="Human skeleton")
    if "brain" in cmd:
        return DrawResponse(success=True, code=BRAIN_CODE, explanation="Human brain")
    if "circle" in cmd:
        return DrawResponse(success=True, code=CIRCLE_CODE, explanation="Circle")
    if "square" in cmd:
        return DrawResponse(success=True, code=SQUARE_CODE, explanation="Square")
    if "heart" in cmd:
        return DrawResponse(success=True, code=HEART_CODE, explanation="Heart shape")
    
    return DrawResponse(success=False, error="Try 'draw a skeleton', 'draw a brain', or 'draw a circle'")

# ============================================
# FALLBACK DRAWING CODES
# ============================================

SKELETON_CODE = """function draw(ctx, canvas) {
    const cx = canvas.width/2;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.beginPath();
    ctx.ellipse(cx,80,35,45,0,0,2*Math.PI);
    ctx.fillStyle='#f5f5dc'; ctx.fill(); ctx.stroke();
    ctx.fillStyle='#8B7355';
    ctx.beginPath(); ctx.ellipse(cx-15,70,6,8,0,0,2*Math.PI); ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx+15,70,6,8,0,0,2*Math.PI); ctx.fill();
    ctx.beginPath(); ctx.moveTo(cx,130); ctx.lineTo(cx,350); ctx.stroke();
    for(let i=0;i<7;i++){let y=160+i*25;
        ctx.beginPath(); ctx.moveTo(cx,y); ctx.quadraticCurveTo(cx-40,y+10,cx-35,y); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx,y); ctx.quadraticCurveTo(cx+40,y+10,cx+35,y); ctx.stroke();
    }
    ctx.beginPath(); ctx.moveTo(cx-30,160); ctx.lineTo(cx-70,220); ctx.lineTo(cx-55,290); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx+30,160); ctx.lineTo(cx+70,220); ctx.lineTo(cx+55,290); ctx.stroke();
    ctx.beginPath(); ctx.ellipse(cx,355,45,20,0,0,2*Math.PI); ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx-25,365); ctx.lineTo(cx-30,440); ctx.lineTo(cx-40,470); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx+25,365); ctx.lineTo(cx+30,440); ctx.lineTo(cx+40,470); ctx.stroke();
    ctx.fillStyle='#333'; ctx.font='12px "Segoe UI"'; ctx.fillText('Human Skeleton',cx-60,30);
}"""

BRAIN_CODE = """function draw(ctx, canvas) {
    const cx=canvas.width/2, cy=canvas.height/2.5;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.beginPath(); ctx.ellipse(cx-45,cy,60,80,-0.1,0,2*Math.PI); ctx.fillStyle='#FFB6C1'; ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx+45,cy,60,80,0.1,0,2*Math.PI); ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx,cy-20,30,25,0,0,2*Math.PI); ctx.fillStyle='#FFC0CB'; ctx.fill();
    ctx.beginPath(); ctx.moveTo(cx-10,cy+55); ctx.lineTo(cx,cy+100); ctx.lineTo(cx+10,cy+55); ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx,cy+40,35,25,0,0,2*Math.PI); ctx.fill();
    ctx.fillStyle='#333'; ctx.font='12px "Segoe UI"'; ctx.fillText('Human Brain',cx-40,30);
}"""

CIRCLE_CODE = """function draw(ctx, canvas) {
    const cx=canvas.width/2, cy=canvas.height/2;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.beginPath(); ctx.arc(cx,cy,120,0,2*Math.PI);
    ctx.strokeStyle='#0f3460'; ctx.lineWidth=3; ctx.stroke();
    ctx.beginPath(); ctx.arc(cx,cy,5,0,2*Math.PI); ctx.fillStyle='#e94560'; ctx.fill();
    ctx.fillStyle='#333'; ctx.font='14px "Segoe UI"'; ctx.fillText('Circle',cx-25,cy-130);
}"""

SQUARE_CODE = """function draw(ctx, canvas) {
    const cx=canvas.width/2, cy=canvas.height/2;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.strokeRect(cx-80,cy-80,160,160);
    ctx.fillStyle='#333'; ctx.font='14px "Segoe UI"'; ctx.fillText('Square',cx-25,cy-90);
}"""

HEART_CODE = """function draw(ctx, canvas) {
    const cx=canvas.width/2, cy=canvas.height/2;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.beginPath();
    ctx.moveTo(cx,cy+40);
    ctx.bezierCurveTo(cx-90,cy-40,cx-140,cy+40,cx,cy+120);
    ctx.bezierCurveTo(cx+140,cy+40,cx+90,cy-40,cx,cy+40);
    ctx.fillStyle='#FF6B6B'; ctx.fill();
    ctx.fillStyle='#333'; ctx.font='14px "Segoe UI"'; ctx.fillText('Heart',cx-20,cy-50);
}"""

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)