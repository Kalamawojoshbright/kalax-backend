"""
KalaX Backend – Complete Platform
Modules: Learn (graphs/chat), Agriculture (image diagnosis), Vision (attendance logging), Tool (measurement)
Deploy to Render.com
"""

from fastapi import FastAPI, Response, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
from datetime import datetime
import json
import re
import os
import math
import traceback
from io import BytesIO
import asyncio
import concurrent.futures
import base64

# ========== MATPLOTLIB ==========
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 10,
    'axes.linewidth': 1.2,
    'figure.dpi': 100,
    'savefig.dpi': 100,
    'figure.figsize': (7, 5)
})

# ========== FASTAPI APP ==========
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== GEMINI API ==========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"
VISION_MODEL = "gemini-2.5-flash"  # Supports vision

# ========== REQUEST MODELS ==========
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
    drawing_type: str
    code: Optional[str] = None
    explanation: Optional[str] = None
    error: Optional[str] = None

# ========== HEALTH & ROOT ==========
@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "KalaX Backend",
        "model": MODEL_NAME,
        "creator": "Kalamawo Joshua Bright",
        "modules": ["Learn", "Agriculture", "Vision", "Tool"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": str(datetime.now())}

# ========== K‑LEARN MODULE (existing) ==========
@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(request.message)
        return ChatResponse(response=response.text, source="gemini")
    except Exception as e:
        return ChatResponse(response=get_fallback_answer(request.message), source="local")

@app.post("/draw", response_model=DrawResponse)
async def draw(request: DrawRequest):
    # Simplified for brevity – keep your existing logic
    return DrawResponse(success=False, drawing_type="error", explanation="Draw endpoint ready")

# ========== TEXTBOOK GRAPH PLOTTING ==========
def safe_eval(expr: str, x: float) -> float:
    expr = expr.replace('^', '**')
    allowed = {
        'x': x, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt, 'abs': abs,
        'pi': math.pi, 'e': math.e
    }
    try:
        return eval(expr, {"__builtins__": {}}, allowed)
    except:
        return float('nan')

def generate_plot_image(expr: str) -> bytes:
    if any(f in expr.lower() for f in ['sin','cos','tan']):
        x_min, x_max = -2*math.pi, 2*math.pi
    elif 'log' in expr.lower():
        x_min, x_max = 0.1, 8
    else:
        x_min, x_max = -6, 6
    steps = 400
    x_vals, y_vals = [], []
    for i in range(steps+1):
        x = x_min + (x_max - x_min) * i / steps
        y = safe_eval(expr, x)
        if abs(y) < 100:
            x_vals.append(x)
            y_vals.append(y)
    if not x_vals:
        raise Exception("No valid points")
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'y = {expr}')
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title(f'y = {expr}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    return buf.getvalue()

@app.post("/plot")
async def plot_expression(request: dict):
    expr = request.get("expression", "").strip()
    if not expr:
        return Response(status_code=400, content="No expression")
    try:
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            img_bytes = await loop.run_in_executor(pool, generate_plot_image, expr)
        return Response(content=img_bytes, media_type="image/png")
    except Exception as e:
        return Response(status_code=500, content=f"Plot error: {str(e)}")

# ========== AGRICULTURE MODULE (NEW: Image Diagnosis) ==========
@app.post("/agriculture/detect")
async def detect_crop_disease(file: UploadFile = File(...)):
    """Upload a crop leaf image → Gemini Vision returns diagnosis + treatment."""
    if not file.content_type.startswith("image/"):
        return {"error": "File must be an image"}
    contents = await file.read()
    # Encode image to base64 for Gemini
    image_b64 = base64.b64encode(contents).decode('utf-8')
    prompt = """
You are an agricultural expert in Uganda. Analyze this crop leaf image.
Identify the likely disease or pest, and provide:
1. Disease name and confidence.
2. Symptoms visible.
3. Organic/low-cost remedy.
4. Chemical treatment (if needed).
5. Prevention tips.
Be concise, practical, and encouraging. Use bullet points.
"""
    try:
        model = genai.GenerativeModel(VISION_MODEL)
        response = model.generate_content([prompt, {"mime_type": file.content_type, "data": image_b64}])
        diagnosis = response.text
    except Exception as e:
        diagnosis = f"⚠️ Analysis failed: {str(e)}. Please consult a local expert."
    return {"diagnosis": diagnosis, "source": "Gemini Vision"}

# ========== SCHOOL REPORT MODULE ==========
@app.post("/school/report")
async def generate_report(request: dict):
    name = request.get("name", "").strip()
    marks = request.get("marks", {})
    attendance = request.get("attendance")
    grade = request.get("grade", "")
    if not name or not marks:
        return {"error": "Missing name or marks"}
    marks_str = ", ".join([f"{subj}: {score}%" for subj, score in marks.items()])
    prompt = f"Write a short, encouraging school report for {name} (Grade {grade}). Marks: {marks_str}. Attendance: {attendance}%. Include strengths, areas for improvement, and a positive closing."
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return {"student": name, "report": response.text}
    except Exception as e:
        return {"error": str(e)}

# ========== MEASUREMENT MODULE ==========
@app.post("/measure")
async def measure_object(request: dict):
    ref_cm = request.get("reference_actual_cm")
    ref_px = request.get("reference_pixels")
    obj_px = request.get("object_pixels")
    if not all([ref_cm, ref_px, obj_px]):
        return {"error": "Missing fields"}
    obj_cm = (obj_px / ref_px) * ref_cm
    obj_inches = obj_cm / 2.54
    result = {"actual_cm": round(obj_cm, 2), "actual_inches": round(obj_inches, 2)}
    if request.get("explain"):
        result["explanation"] = f"Object is {round(obj_cm,2)} cm, about the size of a { 'fingertip' if obj_cm < 3 else 'banana' if obj_cm < 15 else 'ruler'}."
    return result

# ========== ATTENDANCE LOGGING (simple, no face) ==========
attendance_logs = []

@app.post("/attendance/log")
async def log_attendance(request: dict):
    name = request.get("name")
    date = request.get("date")
    time = request.get("time")
    if not name or not date or not time:
        return {"error": "Missing fields"}
    attendance_logs.append({"name": name, "date": date, "time": time})
    return {"status": "logged", "student": name}

@app.post("/attendance/summary")
async def attendance_summary(request: dict):
    filter_date = request.get("date")
    filtered = [log for log in attendance_logs if filter_date is None or log["date"] == filter_date]
    present = set(log["name"] for log in filtered)
    summary = f"On {filter_date or 'all days'}, {len(present)} students present: {', '.join(present)}"
    return {"summary": summary, "total": len(present)}

# ========== FALLBACK ==========
def get_fallback_answer(message):
    return "I'm KalaX AI. Ask me about math, science, or upload a crop image in Agriculture."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)