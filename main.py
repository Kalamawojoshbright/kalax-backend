"""
KalaX Learn - Complete All Subjects + Math Calculator + Large Diagrams
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="KalaX Learn", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# GEMINI AI - For all subjects
# ============================================

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_AVAILABLE and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        MODEL_NAME = "gemini-2.0-flash-exp"
        GEMINI_READY = True
        logger.info("✅ AI configured")
    except:
        GEMINI_READY = False
else:
    GEMINI_READY = False

# ============================================
# REQUEST MODELS
# ============================================

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class MathRequest(BaseModel):
    expression: str

class MathResponse(BaseModel):
    success: bool
    result: Optional[str] = None
    steps: Optional[str] = None
    error: Optional[str] = None

class GraphRequest(BaseModel):
    function: str

class GraphResponse(BaseModel):
    success: bool
    grid_data: Optional[dict] = None
    error: Optional[str] = None

# ============================================
# HEALTH ENDPOINTS
# ============================================

@app.get("/")
async def root():
    return {"status": "online", "service": "KalaX Learn"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ============================================
# CHAT ENDPOINT - ALL SUBJECTS
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer ANY question - all subjects"""
    
    logger.info(f"Question: {request.message[:100]}...")
    
    # Check if it's a math calculation first
    math_result = solve_math(request.message)
    if math_result:
        return ChatResponse(response=math_result)
    
    # Try AI for all subjects
    if GEMINI_READY:
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(request.message)
            return ChatResponse(response=response.text)
        except Exception as e:
            logger.error(f"AI error: {e}")
    
    # Fallback responses for all subjects
    return ChatResponse(response=get_subject_answer(request.message))

# ============================================
# MATH CALCULATOR - SOLVES ANY MATH
# ============================================

@app.post("/math/calculate", response_model=MathResponse)
async def calculate(request: MathRequest):
    """Calculate any math problem with steps"""
    
    result = solve_math_with_steps(request.expression)
    if result:
        return MathResponse(success=True, result=result["answer"], steps=result["steps"])
    
    return MathResponse(success=False, error="Could not calculate. Try: 15+23, 45*3, or (2+3)*4")

# ============================================
# GRAPH ENDPOINT - LARGE DIAGRAMS
# ============================================

@app.post("/graph", response_model=GraphResponse)
async def generate_graph(request: GraphRequest):
    """Generate large mathematical graph"""
    
    func = request.function.replace('^', '**')
    
    try:
        x_values = []
        y_values = []
        x_min, x_max = -8, 8
        step = 0.05
        
        x = x_min
        while x <= x_max:
            try:
                safe_dict = {
                    "x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                    "sqrt": math.sqrt, "exp": math.exp, "log": math.log, 
                    "pi": math.pi, "abs": abs
                }
                y = eval(func, {"__builtins__": {}}, safe_dict)
                if math.isfinite(y) and abs(y) < 30:
                    x_values.append(round(x, 2))
                    y_values.append(round(y, 2))
            except:
                pass
            x += step
        
        if len(x_values) < 2:
            return GraphResponse(
                success=False,
                error="Could not generate graph. Try: x**2, 2*x+3, sin(x)"
            )
        
        y_min = min(y_values)
        y_max = max(y_values)
        y_min = math.floor(y_min) - 1
        y_max = math.ceil(y_max) + 1
        
        return GraphResponse(
            success=True,
            grid_data={
                "x_values": x_values,
                "y_values": y_values,
                "function": request.function,
                "x_min": x_min,
                "x_max": x_max,
                "y_min": y_min,
                "y_max": y_max
            }
        )
        
    except Exception as e:
        return GraphResponse(success=False, error=str(e))

# ============================================
# MATH SOLVER FUNCTIONS
# ============================================

def solve_math(question: str) -> str:
    """Solve math problems and return answer"""
    q = question.lower().strip()
    
    # Arithmetic like 15+23, 45*3, 100/4
    match = re.search(r'(\d+)\s*([\+\-\*\/])\s*(\d+)', q)
    if match:
        a = float(match.group(1))
        op = match.group(2)
        b = float(match.group(3))
        
        if op == '+': result = a + b
        elif op == '-': result = a - b
        elif op == '*': result = a * b
        elif op == '/': result = a / b if b != 0 else "undefined"
        else: return None
        
        return f"🧮 {a} {op} {b} = {result}"
    
    # Algebra: solve for x like 2x+5=13
    eq_match = re.search(r'(\d+)x\s*\+\s*(\d+)\s*=\s*(\d+)', q)
    if eq_match:
        a = float(eq_match.group(1))
        b = float(eq_match.group(2))
        c = float(eq_match.group(3))
        x = (c - b) / a
        steps = f"Step 1: {a}x + {b} = {c}\nStep 2: {a}x = {c - b}\nStep 3: x = {x}"
        return f"📐 x = {x}\n\n{steps}"
    
    # Quadratic: ax²+bx+c=0
    quad_match = re.search(r'(\d+)x\^2\s*\+\s*(\d+)x\s*\+\s*(\d+)\s*=\s*0', q)
    if quad_match:
        a = float(quad_match.group(1))
        b = float(quad_match.group(2))
        c = float(quad_match.group(3))
        discriminant = b**2 - 4*a*c
        if discriminant >= 0:
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return f"📐 x = {x1:.2f} or x = {x2:.2f}"
        else:
            return "📐 No real solutions (discriminant negative)"
    
    return None

def solve_math_with_steps(expression: str) -> dict:
    """Solve math with step-by-step explanation"""
    q = expression.lower().strip()
    
    match = re.search(r'(\d+)\s*([\+\-\*\/])\s*(\d+)', q)
    if match:
        a = float(match.group(1))
        op = match.group(2)
        b = float(match.group(3))
        
        if op == '+': 
            result = a + b
            steps = f"Add {a} and {b}"
        elif op == '-': 
            result = a - b
            steps = f"Subtract {b} from {a}"
        elif op == '*': 
            result = a * b
            steps = f"Multiply {a} by {b}"
        elif op == '/': 
            result = a / b if b != 0 else "undefined"
            steps = f"Divide {a} by {b}"
        else: 
            return None
        
        return {"answer": str(result), "steps": steps}
    
    return None

# ============================================
# SUBJECT ANSWERS - ALL SUBJECTS
# ============================================

def get_subject_answer(question: str) -> str:
    q = question.lower()
    
    # BIOLOGY
    if "photosynthesis" in q:
        return """🌿 **Photosynthesis**

Plants make their own food using sunlight!

**Equation:** 6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂

**Two stages:**
1. Light reaction - captures sunlight, releases oxygen
2. Calvin cycle - makes glucose from CO₂

**Where:** Chloroplasts in leaves"""
    
    if "mitosis" in q:
        return """🔬 **Mitosis (PMAT)**

Cell division that produces 2 identical cells!

**Stages:**
• **P**rophase - Chromosomes condense
• **M**etaphase - Line up at center
• **A**naphase - Separate to opposite poles
• **T**elophase - Two new cells form

**Used for:** Growth, repair, and reproduction"""
    
    if "cell" in q:
        return """🔬 **The Cell**

Basic unit of life!

**Parts:**
• **Nucleus** - Contains DNA, controls the cell
• **Mitochondria** - Power house, produces energy
• **Cell Membrane** - Controls what enters/exits
• **Ribosomes** - Make proteins

**Two types:** Animal cell and Plant cell"""
    
    # PHYSICS
    if "newton" in q:
        return """⚡ **Newton's Three Laws of Motion**

**1st Law (Inertia):** Objects keep doing what they're doing unless a force acts on them.

**2nd Law (F = ma):** Force = Mass × Acceleration

**3rd Law (Action-Reaction):** Every action has an equal and opposite reaction.

**Example:** When you kick a ball, your foot pushes the ball (action), and the ball pushes back on your foot (reaction)!"""
    
    if "gravity" in q:
        return """🌍 **Gravity**

Gravity is the force that pulls objects toward Earth!

**Key facts:**
• Acceleration: 9.8 m/s²
• Your weight = mass × gravity (W = mg)
• Moon's gravity is 1/6 of Earth's
• Keeps planets in orbit around the Sun"""
    
    if "electricity" in q:
        return """⚡ **Electricity**

Flow of electric charge!

**Key concepts:**
• **Voltage (V)** - Electrical pressure
• **Current (I)** - Flow of electrons
• **Resistance (R)** - Opposition to flow

**Ohm's Law:** V = I × R"""
    
    # CHEMISTRY
    if "periodic table" in q:
        return """⚛️ **The Periodic Table**

Organizes all 118 chemical elements by atomic number.

**Groups (vertical):** Elements with similar properties
**Periods (horizontal):** Atomic number increases left to right

**Important groups:**
• Group 1: Alkali Metals (very reactive)
• Group 18: Noble Gases (unreactive)"""
    
    if "atom" in q:
        return """⚛️ **The Atom**

Smallest unit of matter!

**Structure:**
• **Protons (+)** - In nucleus, determines the element
• **Neutrons (0)** - In nucleus, adds mass
• **Electrons (-)** - Orbit the nucleus in shells"""
    
    # MATHEMATICS
    if "circle" in q and "area" in q:
        return """📐 **Area of a Circle**

Formula: A = πr²

Where:
• A = Area
• π ≈ 3.14159
• r = radius

Example: If radius = 5, Area = 3.14 × 25 = 78.5"""
    
    if "pythagorean" in q or "pythagoras" in q:
        return """📐 **Pythagorean Theorem**

For a right triangle: a² + b² = c²

Where:
• a and b are the legs (shorter sides)
• c is the hypotenuse (longest side)

Example: If a = 3, b = 4, then c = √(9+16) = √25 = 5"""
    
    # GEOGRAPHY
    if "uganda" in q:
        return """🇺🇬 **Uganda - The Pearl of Africa!**

**Capital:** Kampala
**Location:** East Africa (crossed by the Equator!)
**Major Lakes:** Victoria, Kyoga, Albert, Edward
**Major River:** The Nile starts from Jinja!
**Independence:** October 9, 1962 from Britain
**Population:** ~45 million people"""
    
    if "africa" in q:
        return """🌍 **Africa**

Second largest continent!

**Size:** 30.4 million km² (20% of Earth's land)
**Countries:** 54 recognized countries
**Population:** ~1.4 billion people

**Major features:**
• Sahara Desert (largest hot desert)
• Nile River (longest river)
• Lake Victoria (largest lake in Africa)
• Mount Kilimanjaro (highest peak)"""
    
    # HISTORY
    if "world war" in q:
        return """📜 **World War II (1939-1945)**

**Key facts:**
• Fought between Allies (USA, UK, USSR) and Axis (Germany, Italy, Japan)
• Over 70 million people died
• Ended with Allied victory
• Led to creation of United Nations"""
    
    # ENGLISH
    if "noun" in q:
        return """📖 **Nouns**

A noun is a person, place, thing, or idea!

**Examples:**
• Person: teacher, doctor, John
• Place: school, Kampala, Africa
• Thing: book, phone, tree
• Idea: love, freedom, happiness"""
    
    # COMPUTER SCIENCE
    if "binary" in q:
        return """💻 **Binary Number System**

Computers use binary (Base-2): only 0 and 1!

**Why?** Computers understand ON (1) and OFF (0)

**Example:** Binary 1010 = 1×8 + 0×4 + 1×2 + 0×1 = 10 decimal

**Letter 'A' in binary:** 01000001!"""
    
    # DEFAULT
    return f"""📚 **KalaX Learn**

I can help with ALL subjects!

**Try these commands:**

📈 **Math Graphs:**
• "Plot y = x^2" - Parabola
• "Plot y = sin(x)" - Sine wave
• "Plot y = 2x+3" - Straight line

🧮 **Math Calculations:**
• "15 + 23"
• "2x + 5 = 13"
• "Area of circle radius 5"

🔬 **Science:**
• "What is photosynthesis?"
• "Explain mitosis"
• "Newton's laws"
• "Periodic table"

🌍 **Geography:**
• "Tell me about Uganda"
• "Facts about Africa"

📜 **History:**
• "World War II"

Created by Kalamawo Joshua Bright"""

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)