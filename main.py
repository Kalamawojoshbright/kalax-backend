"""
KalaX Backend – Complete Modular Platform
Includes: K‑Learn (graphs, chat, draw), Agriculture, School Reports, Measurement, Attendance
Deploy to Render.com
"""

from fastapi import FastAPI, Response, Request
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

# ========== MATPLOTLIB (low DPI for reliability) ==========
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

# ========== REQUEST MODELS (for existing endpoints) ==========
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
        "modules": ["K-Learn", "Agriculture", "School", "Measurement", "Attendance"]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "gemini_model": MODEL_NAME,
        "timestamp": str(datetime.now())
    }

# ========== K‑LEARN MODULE (existing) ==========
@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(request.message)
        return ChatResponse(response=response.text, source="gemini")
    except Exception as e:
        print(f"Gemini error: {e}")
        return ChatResponse(response=get_fallback_answer(request.message), source="local")

@app.post("/draw", response_model=DrawResponse)
async def draw(request: DrawRequest):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""Generate a JavaScript drawing function for: "{request.command}"
Return ONLY valid JSON in this exact format:
{{"type":"canvas_code","code":"function draw(ctx, canvas){{ ... }}","explanation":"description"}}
Requirements:
- Canvas is 700x500 pixels
- Use ctx.fillStyle, ctx.strokeStyle, ctx.beginPath()
- Add labels with ctx.fillText()
- Make it educational and accurate
- Use appropriate colors
Generate the function NOW:"""
        response = model.generate_content(prompt)
        json_match = re.search(r'\{[\s\S]*\}', response.text)
        if json_match:
            result = json.loads(json_match.group())
            if result.get("code"):
                return DrawResponse(
                    success=True,
                    drawing_type="canvas_code",
                    code=result["code"],
                    explanation=result.get("explanation", f"AI-generated diagram of {request.command}")
                )
        return get_fallback_drawing(request.command)
    except Exception as e:
        print(f"Draw error: {e}")
        return get_fallback_drawing(request.command)

# ========== TEXTBOOK GRAPH PLOTTING (no recursion) ==========
def safe_eval(expr: str, x: float) -> float:
    expr = expr.replace('^', '**')
    allowed = {
        'x': x,
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
        'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
        'exp': math.exp, 'log': math.log, 'log10': math.log10,
        'sqrt': math.sqrt, 'abs': abs,
        'pi': math.pi, 'e': math.e
    }
    try:
        return eval(expr, {"__builtins__": {}}, allowed)
    except:
        return float('nan')

def generate_plot_image(expr: str) -> bytes:
    expr_lower = expr.lower()
    if any(f in expr_lower for f in ['sin', 'cos', 'tan']):
        x_min, x_max = -2 * math.pi, 2 * math.pi
    elif 'log' in expr_lower:
        x_min, x_max = 0.1, 8
    else:
        x_min, x_max = -6, 6

    steps = 400
    x_vals = []
    y_vals = []
    for i in range(steps + 1):
        x = x_min + (x_max - x_min) * i / steps
        y = safe_eval(expr, x)
        if abs(y) < 100:
            x_vals.append(x)
            y_vals.append(y)

    if not x_vals:
        raise Exception("No valid points generated")

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'y = {expr}')
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title(f'y = {expr}', fontsize=12)
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
        return Response(status_code=400, content="No expression provided")
    try:
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            img_bytes = await loop.run_in_executor(pool, generate_plot_image, expr)
        return Response(content=img_bytes, media_type="image/png")
    except Exception as e:
        print(traceback.format_exc())
        return Response(status_code=500, content=f"Plot error: {str(e)}")

# ========== AGRICULTURE MODULE ==========
@app.post("/agriculture/treatment")
async def get_treatment(request: dict):
    crop = request.get("crop", "").strip()
    disease = request.get("disease", "").strip()
    if not crop or not disease:
        return {"error": "Please provide both crop and disease names."}
    prompt = f"""
You are an agricultural expert in Uganda. Recommend a treatment plan for {crop} affected by {disease}.
Include:
1. Brief description of the disease (symptoms, how it spreads).
2. Organic / low‑cost remedy (accessible to small‑scale farmers).
3. Chemical treatment (if available and necessary) – include safety precautions.
4. Prevention tips for the next season.
Write in simple, clear English, using bullet points. Be practical and encouraging.
"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        advice = response.text
    except Exception as e:
        advice = f"⚠️ Gemini error: {str(e)}. Please consult a local agricultural extension officer."
    return {"crop": crop, "disease": disease, "advice": advice, "source": "gemini" if "Gemini error" not in advice else "fallback"}

# ========== SCHOOL REPORT MODULE ==========
@app.post("/school/report")
async def generate_report(request: dict):
    name = request.get("name", "").strip()
    marks = request.get("marks", {})
    attendance = request.get("attendance", None)
    grade = request.get("grade", "")
    if not name or not marks:
        return {"error": "Missing student name or marks"}
    marks_str = ", ".join([f"{subj}: {score}%" for subj, score in marks.items()])
    prompt = f"""
You are a primary school teacher in Uganda. Write a short, encouraging report for student {name}.
Grade: {grade if grade else 'Not specified'}
Marks: {marks_str}
Attendance: {attendance}% (if provided)
Include:
- A positive opening statement.
- Specific strengths in at least two subjects.
- One or two areas for improvement (kindly worded).
- A general comment about effort and behaviour.
- An encouraging closing sentence.
Keep the language simple and warm. The report should be no longer than 100 words.
"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        report = response.text
    except Exception as e:
        report = f"⚠️ Gemini unavailable: {str(e)}. Please prepare a report manually."
    return {"student": name, "report": report, "generated_by": "Gemini 2.5 Flash"}

# ========== MEASUREMENT MODULE ==========
@app.post("/measure")
async def measure_object(request: dict):
    ref_cm = request.get("reference_actual_cm")
    ref_px = request.get("reference_pixels")
    obj_px = request.get("object_pixels")
    if not all([ref_cm, ref_px, obj_px]):
        return {"error": "Missing required fields"}
    obj_cm = (obj_px / ref_px) * ref_cm
    obj_inches = obj_cm / 2.54
    result = {
        "actual_cm": round(obj_cm, 2),
        "actual_inches": round(obj_inches, 2),
        "method": "reference_object_measurement"
    }
    if request.get("explain"):
        prompt = f"An object measured {obj_cm:.2f} cm ({obj_inches:.2f} inches) using a reference object of known size {ref_cm} cm. Explain how this measurement works and give a real‑world example. Write in simple English for a student."
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            result["explanation"] = response.text
        except:
            result["explanation"] = "Measurement based on proportion: object size = (object pixels / reference pixels) × reference actual size."
    return result

# ========== ATTENDANCE MODULE (simple logging, no face) ==========
attendance_logs = []

@app.post("/attendance/log")
async def log_attendance(request: dict):
    name = request.get("name")
    date = request.get("date")
    time = request.get("time")
    if not name or not date or not time:
        return {"error": "Missing name, date, or time"}
    attendance_logs.append({"name": name, "date": date, "time": time})
    return {"status": "logged", "student": name, "datetime": f"{date} {time}"}

@app.post("/attendance/summary")
async def attendance_summary(request: dict):
    filter_date = request.get("date")
    filtered = [log for log in attendance_logs if filter_date is None or log["date"] == filter_date]
    if not filtered:
        return {"summary": "No attendance records found for this date."}
    present = set(log["name"] for log in filtered)
    summary_text = f"On {filter_date or 'all days'}, {len(present)} students were present: {', '.join(present)}."
    if request.get("gemini", False):
        prompt = f"Write a short, professional attendance report for a class. Details: {summary_text}"
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            summary_text = response.text
        except:
            pass
    return {"summary": summary_text, "total_present": len(present), "logs": filtered}

# ========== FALLBACK FUNCTIONS (for K‑Learn) ==========
def get_fallback_answer(message):
    m = message.lower()
    if "photosynthesis" in m:
        return "🌿 **Photosynthesis**\n\nPlants make their own food using sunlight!\n\n**Equation:** 6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂"
    if "mitosis" in m:
        return "🔬 **Mitosis (PMAT)**\n\nStages: Prophase → Metaphase → Anaphase → Telophase"
    if "newton" in m:
        return "⚡ **Newton's Laws**\n\n1st: Inertia, 2nd: F=ma, 3rd: Action-Reaction"
    return "I'm KalaX AI. Ask me about science, math, or crops."

def get_fallback_drawing(command):
    # Simplified fallback – you can keep your original drawing functions if needed
    return DrawResponse(success=False, drawing_type="error", explanation="Draw endpoint ready for custom shapes")

# ========== RUN ==========
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)