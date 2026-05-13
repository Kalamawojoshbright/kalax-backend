"""
KalaX Backend - AI Powered Educational Assistant
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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Configuration (Internal - No Branding)
AI_API_KEY = "AIzaSyAU_pIonfIoRhlpnkK5CX-HZveGv_5pqkQ"
genai.configure(api_key=AI_API_KEY)
AI_MODEL = "gemini-2.5-flash"

class ChatRequest(BaseModel):
    message: str

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

@app.get("/")
async def root():
    return {"status": "online", "service": "KalaX Backend"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": str(datetime.now())}

@app.post("/learn/chat")
async def chat(request: ChatRequest):
    try:
        model = genai.GenerativeModel(AI_MODEL)
        response = model.generate_content(request.message)
        return ChatResponse(response=response.text, source="ai")
    except Exception as e:
        return ChatResponse(response=get_fallback_answer(request.message), source="local")

@app.post("/draw")
async def draw(request: DrawRequest):
    # Local drawings first (fast & reliable)
    local = get_local_drawing(request.command)
    if local:
        return local
    
    try:
        model = genai.GenerativeModel(AI_MODEL)
        prompt = f"""Generate JavaScript canvas drawing code for: "{request.command}"

Return ONLY JSON: {{"code": "function draw(ctx, canvas) {{ ... }}", "explanation": "description"}}

Canvas: 700x500. Use ctx.fillStyle, ctx.strokeStyle, ctx.beginPath(). Clear canvas first."""
        
        response = model.generate_content(prompt)
        match = re.search(r'\{[\s\S]*\}', response.text)
        if match:
            data = json.loads(match.group())
            if data.get("code"):
                return DrawResponse(success=True, code=data["code"], explanation=data.get("explanation", ""))
        
        return DrawResponse(success=False, error="Could not generate drawing")
    except Exception as e:
        return DrawResponse(success=False, error=str(e))

def get_fallback_answer(message):
    m = message.lower()
    if "photosynthesis" in m:
        return "🌿 **Photosynthesis**\n\nPlants make food using sunlight!\n\n6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂"
    if "mitosis" in m:
        return "🔬 **Mitosis**\n\nStages: Prophase → Metaphase → Anaphase → Telophase"
    if "newton" in m:
        return "⚡ **Newton's Laws**\n\n1. Inertia\n2. F = ma\n3. Action-Reaction"
    return f"Ask me about photosynthesis, mitosis, or say 'Draw a skeleton'"

def get_local_drawing(command):
    cmd = command.lower()
    
    if "skeleton" in cmd:
        return DrawResponse(success=True, code=SKELETON_CODE, explanation="Human skeleton diagram")
    if "brain" in cmd:
        return DrawResponse(success=True, code=BRAIN_CODE, explanation="Human brain diagram")
    if "circle" in cmd:
        return DrawResponse(success=True, code=CIRCLE_CODE, explanation="Circle diagram")
    if "square" in cmd:
        return DrawResponse(success=True, code=SQUARE_CODE, explanation="Square diagram")
    if "triangle" in cmd or "right angle" in cmd:
        return DrawResponse(success=True, code=TRIANGLE_CODE, explanation="Right angle triangle")
    if "heart" in cmd:
        return DrawResponse(success=True, code=HEART_CODE, explanation="Heart shape")
    if "dna" in cmd or "helix" in cmd:
        return DrawResponse(success=True, code=DNA_CODE, explanation="DNA double helix")
    return None

# ============================================
# DRAWING CODES
# ============================================

SKELETON_CODE = """function draw(ctx, canvas) {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    const cx = canvas.width/2;
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
    ctx.fillStyle='#333'; ctx.font='11px "Segoe UI"';
    ctx.fillText('Skull',cx-10,60); ctx.fillText('Ribcage',cx-60,220);
    ctx.fillText('Spine',cx+20,250); ctx.fillText('Pelvis',cx-30,370);
}"""

BRAIN_CODE = """function draw(ctx, canvas) {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    const cx=canvas.width/2, cy=canvas.height/2.5;
    ctx.beginPath(); ctx.ellipse(cx-45,cy,60,80,-0.1,0,2*Math.PI); ctx.fillStyle='#FFB6C1'; ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx+45,cy,60,80,0.1,0,2*Math.PI); ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx,cy-20,30,25,0,0,2*Math.PI); ctx.fillStyle='#FFC0CB'; ctx.fill();
    ctx.beginPath(); ctx.moveTo(cx-10,cy+55); ctx.lineTo(cx,cy+100); ctx.lineTo(cx+10,cy+55); ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx,cy+40,35,25,0,0,2*Math.PI); ctx.fill();
    ctx.fillStyle='#333'; ctx.font='10px "Segoe UI"';
    ctx.fillText('Left Hemisphere',cx-100,cy-30); ctx.fillText('Right Hemisphere',cx+35,cy-30);
    ctx.fillText('Cerebellum',cx-30,cy+55); ctx.fillText('Brain Stem',cx-25,cy+95);
}"""

CIRCLE_CODE = """function draw(ctx, canvas) {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    const cx=canvas.width/2, cy=canvas.height/2, r=120;
    ctx.beginPath(); ctx.arc(cx,cy,r,0,2*Math.PI);
    ctx.strokeStyle='#0f3460'; ctx.lineWidth=3; ctx.stroke();
    ctx.beginPath(); ctx.arc(cx,cy,5,0,2*Math.PI); ctx.fillStyle='#e94560'; ctx.fill();
    ctx.fillStyle='#333'; ctx.font='12px "Segoe UI"';
    ctx.fillText('Center',cx+10,cy); ctx.fillText('Radius',cx+r/2,cy-10);
}"""

SQUARE_CODE = """function draw(ctx, canvas) {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    const cx=canvas.width/2, cy=canvas.height/2, s=160;
    ctx.strokeRect(cx-s/2,cy-s/2,s,s);
    ctx.fillStyle='#333'; ctx.font='12px "Segoe UI"';
    ctx.fillText('Square',cx-20,cy-s/2-10);
}"""

TRIANGLE_CODE = """function draw(ctx, canvas) {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    const cx=canvas.width/2, cy=canvas.height/2;
    ctx.beginPath();
    ctx.moveTo(cx-100,cy+60); ctx.lineTo(cx+100,cy+60); ctx.lineTo(cx-100,cy-60);
    ctx.closePath(); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(cx-100+20,cy+60); ctx.lineTo(cx-100+20,cy+60-20); ctx.lineTo(cx-100,cy+60-20);
    ctx.stroke();
    ctx.fillStyle='#333'; ctx.font='12px "Segoe UI"';
    ctx.fillText('90°',cx-95,cy+55); ctx.fillText('Right Triangle',cx-60,cy-80);
}"""

HEART_CODE = """function draw(ctx, canvas) {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    const cx=canvas.width/2, cy=canvas.height/2;
    ctx.beginPath();
    ctx.moveTo(cx,cy+40);
    ctx.bezierCurveTo(cx-90,cy-40,cx-140,cy+40,cx,cy+120);
    ctx.bezierCurveTo(cx+140,cy+40,cx+90,cy-40,cx,cy+40);
    ctx.fillStyle='#FF6B6B'; ctx.fill();
    ctx.fillStyle='#333'; ctx.font='12px "Segoe UI"';
    ctx.fillText('Heart',cx-15,cy-50);
}"""

DNA_CODE = """function draw(ctx, canvas) {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    const cx=canvas.width/2;
    for(let y=80;y<=420;y+=10){
        let t=(y-80)/340;
        let x1=cx-60*Math.sin(t*Math.PI*2);
        let x2=cx+60*Math.sin(t*Math.PI*2);
        if(y===80){ctx.beginPath();ctx.moveTo(x1,y);ctx.moveTo(x2,y);}
        else{ctx.lineTo(x1,y);ctx.lineTo(x2,y);}
    }
    ctx.strokeStyle='#0000CD'; ctx.lineWidth=3; ctx.stroke();
    ctx.fillStyle='#333'; ctx.font='bold 12px "Segoe UI"';
    ctx.fillText('DNA Double Helix',cx-60,40);
}"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)