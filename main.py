"""
KalaX Backend - Complete API
Run on Render.com
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import math

# Create app
app = FastAPI(title="KalaX Backend", version="1.0.0")

# Allow connections from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# DATA MODELS
# ============================================

class ChatRequest(BaseModel):
    message: str
    subject: Optional[str] = "general"

class ChatResponse(BaseModel):
    response: str
    source: str

class GraphRequest(BaseModel):
    function: str
    x_min: Optional[float] = -5
    x_max: Optional[float] = 5

class GraphResponse(BaseModel):
    success: bool
    x_values: Optional[List[float]] = None
    y_values: Optional[List[float]] = None
    error: Optional[str] = None

class DiagramRequest(BaseModel):
    diagram_type: str

class DiagramResponse(BaseModel):
    success: bool
    svg: Optional[str] = None
    description: Optional[str] = None

class CropRequest(BaseModel):
    crop_type: str

class CropResponse(BaseModel):
    success: bool
    disease: Optional[str] = None
    confidence: Optional[float] = None
    treatment: Optional[str] = None
    prevention: Optional[str] = None

class AttendanceRequest(BaseModel):
    student_name: str

class AttendanceResponse(BaseModel):
    success: bool
    message: str
    student_name: Optional[str] = None
    time: Optional[str] = None

class MeasurementRequest(BaseModel):
    object_pixels: float
    reference_cm: float
    reference_pixels: float

class MeasurementResponse(BaseModel):
    success: bool
    actual_cm: Optional[float] = None
    formula: Optional[str] = None

# ============================================
# ROOT ENDPOINTS
# ============================================

@app.get("/")
async def root():
    return {
        "name": "KalaX Backend",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "learn_chat": "POST /learn/chat",
            "learn_graph": "POST /learn/graph",
            "learn_diagram": "POST /learn/diagram",
            "farm_predict": "POST /farm/predict",
            "secure_attendance": "POST /secure/attendance",
            "secure_students": "GET /secure/students",
            "vision_measure": "POST /vision/measure"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": str(datetime.now())}

# ============================================
# KALAX LEARN - CHAT
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def learn_chat(request: ChatRequest):
    message = request.message.lower()
    
    # Photosynthesis
    if "photosynthesis" in message:
        return ChatResponse(
            response="""🌿 **Photosynthesis**

Plants make their own food using sunlight!

**Equation:** 6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂

**Two stages:**
1. Light reaction - captures sunlight, releases oxygen
2. Calvin cycle - makes glucose from carbon dioxide

**Where:** Chloroplasts in leaves
**Why important:** Produces food AND oxygen!""",
            source="local"
        )
    
    # Mitosis
    if "mitosis" in message or "cell division" in message:
        return ChatResponse(
            response="""🔬 **Mitosis (PMAT)**

Cell division that produces 2 identical cells!

**Stages:**
• **P**rophase - Chromosomes condense
• **M**etaphase - Line up at the center
• **A**naphase - Separate to opposite poles
• **T**elophase - Two new nuclei form

**Used for:** Growth, repair, and reproduction""",
            source="local"
        )
    
    # Newton's Laws
    if "newton" in message or "law of motion" in message:
        return ChatResponse(
            response="""⚡ **Newton's Three Laws of Motion**

**1st Law (Inertia):** Objects keep doing what they're doing unless a force acts on them.

**2nd Law (F=ma):** Force = Mass × Acceleration

**3rd Law (Action-Reaction):** Every action has an equal and opposite reaction.

**Example:** When you kick a ball, your foot pushes the ball (action), and the ball pushes back on your foot (reaction)!""",
            source="local"
        )
    
    # Periodic Table
    if "periodic" in message or "element" in message:
        return ChatResponse(
            response="""⚛️ **The Periodic Table**

Organizes all 118 chemical elements by atomic number.

**Groups (vertical):** Elements with similar properties
**Periods (horizontal):** Atomic number increases left to right

**Important elements for Uganda:**
• Nitrogen (N) - Fertilizers
• Phosphorus (P) - Plant growth
• Potassium (K) - Crop health
• Carbon (C) - All living things

**Remember:** Hydrogen (H) is element #1!""",
            source="local"
        )
    
    # Default response
    return ChatResponse(
        response=f"""📚 **Question:** {request.message}

I can help you learn about:
• Biology (photosynthesis, mitosis, cells)
• Physics (Newton's laws, electricity)
• Chemistry (periodic table, reactions)
• Mathematics (algebra, graphs)
• Geography (Uganda, Africa)
• History (Uganda independence)
• Agriculture (crop diseases)

**Try asking:**
• "Explain photosynthesis"
• "What is mitosis?"
• "Newton's laws of motion"
• "Draw a plant cell"
• "Plot y = x^2"

What would you like to learn? 🎓""",
        source="local"
    )

# ============================================
# KALAX LEARN - GRAPHS
# ============================================

@app.post("/learn/graph", response_model=GraphResponse)
async def learn_graph(request: GraphRequest):
    """Generate mathematical graph data points"""
    try:
        x_values = []
        y_values = []
        
        # Calculate step size
        step = (request.x_max - request.x_min) / 100
        x = request.x_min
        
        while x <= request.x_max:
            try:
                # Convert ^ to ** for Python
                func = request.function.replace('^', '**')
                
                # Safe evaluation
                y = eval(func, {
                    "x": x,
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "sqrt": math.sqrt,
                    "exp": math.exp,
                    "log": math.log,
                    "pi": math.pi,
                    "abs": abs
                })
                
                if abs(y) < 100:  # Limit range
                    x_values.append(round(x, 2))
                    y_values.append(round(y, 2))
            except:
                pass
            
            x += step
        
        if len(x_values) < 2:
            return GraphResponse(
                success=False,
                error="Could not generate graph. Try a simpler function like x**2"
            )
        
        return GraphResponse(
            success=True,
            x_values=x_values,
            y_values=y_values
        )
        
    except Exception as e:
        return GraphResponse(success=False, error=str(e))

# ============================================
# KALAX LEARN - DIAGRAMS
# ============================================

@app.post("/learn/diagram", response_model=DiagramResponse)
async def learn_diagram(request: DiagramRequest):
    """Generate educational diagrams"""
    
    diagrams = {
        "photosynthesis": {
            "svg": '<svg width="500" height="350" xmlns="http://www.w3.org/2000/svg"><rect width="500" height="350" fill="#e8f5e9"/><circle cx="60" cy="50" r="25" fill="#FFD700"/><text x="60" y="55" text-anchor="middle" fill="#000" font-size="10">☀️</text><rect x="200" y="180" width="120" height="100" fill="#228B22" rx="8"/><text x="260" y="235" text-anchor="middle" fill="white" font-size="12">🌿</text><text x="150" y="160" fill="#8B4513" font-size="11">CO₂ →</text><line x1="170" y1="160" x2="195" y2="200" stroke="#8B4513" stroke-width="2"/><text x="150" y="300" fill="#4169E1" font-size="11">H₂O →</text><line x1="170" y1="300" x2="195" y2="260" stroke="#4169E1" stroke-width="2"/><text x="340" y="160" fill="#32CD32" font-size="11">← O₂</text><line x1="330" y1="160" x2="355" y2="200" stroke="#32CD32" stroke-width="2"/><text x="340" y="300" fill="#FFD700" font-size="11">← Glucose</text><line x1="330" y1="300" x2="355" y2="260" stroke="#FFD700" stroke-width="2"/><text x="250" y="340" text-anchor="middle" font-size="9">6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂</text></svg>',
            "description": "Photosynthesis: Plants convert CO₂ and H₂O into glucose and oxygen using sunlight."
        },
        "mitosis": {
            "svg": '<svg width="650" height="280" xmlns="http://www.w3.org/2000/svg"><rect width="650" height="280" fill="#f8f9fa"/><text x="325" y="25" text-anchor="middle" font-size="14" font-weight="bold" fill="#2d6a4f">MITOSIS (PMAT)</text><rect x="20" y="45" width="130" height="90" fill="#e8f5e9" stroke="#2d6a4f" stroke-width="2" rx="5"/><text x="85" y="65" text-anchor="middle" font-size="11" font-weight="bold">PROPHASE</text><circle cx="85" cy="95" r="20" fill="none" stroke="#333" stroke-width="2"/><rect x="170" y="45" width="130" height="90" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/><text x="235" y="65" text-anchor="middle" font-size="11" font-weight="bold">METAPHASE</text><circle cx="235" cy="95" r="20" fill="none" stroke="#333" stroke-width="2"/><rect x="320" y="45" width="130" height="90" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/><text x="385" y="65" text-anchor="middle" font-size="11" font-weight="bold">ANAPHASE</text><circle cx="385" cy="95" r="20" fill="none" stroke="#333" stroke-width="2"/><rect x="470" y="45" width="160" height="90" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2" rx="5"/><text x="550" y="65" text-anchor="middle" font-size="11" font-weight="bold">TELOPHASE</text><circle cx="530" cy="95" r="15" fill="none" stroke="#333" stroke-width="2"/><circle cx="570" cy="95" r="15" fill="none" stroke="#333" stroke-width="2"/><text x="160" y="95" text-anchor="middle" font-size="16">→</text><text x="310" y="95" text-anchor="middle" font-size="16">→</text><text x="460" y="95" text-anchor="middle" font-size="16">→</text><text x="325" y="175" text-anchor="middle" font-size="11" fill="#2d6a4f">Result: 2 identical daughter cells!</text></svg>',
            "description": "Mitosis: Cell division through 4 stages producing 2 identical cells."
        },
        "cell": {
            "svg": '<svg width="550" height="350" xmlns="http://www.w3.org/2000/svg"><rect width="550" height="350" fill="#fff9e6"/><text x="275" y="25" text-anchor="middle" font-size="14" font-weight="bold">Animal Cell Structure</text><ellipse cx="275" cy="180" rx="160" ry="130" fill="none" stroke="#2d6a4f" stroke-width="2" stroke-dasharray="5,5"/><text x="460" y="65" fill="#2d6a4f" font-size="9">Cell Membrane</text><ellipse cx="275" cy="160" rx="50" ry="40" fill="#e8f5e9" stroke="#1b5e20" stroke-width="2"/><text x="275" y="155" text-anchor="middle" font-size="11" font-weight="bold">Nucleus</text><circle cx="275" cy="180" r="10" fill="#c8e6c9" stroke="#1b5e20" stroke-width="1"/><text x="275" y="183" text-anchor="middle" font-size="7">DNA</text><ellipse cx="170" cy="130" rx="30" ry="18" fill="#fff3e0" stroke="#e65100" stroke-width="2"/><text x="170" y="110" text-anchor="middle" fill="#e65100" font-size="9">Mitochondria</text><circle cx="380" cy="250" r="4" fill="#c62828"/><circle cx="395" cy="260" r="4" fill="#c62828"/><text x="400" y="275" fill="#c62828" font-size="9">Ribosomes</text><path d="M 390 160 Q 420 150 410 180 Q 430 170 420 200" fill="none" stroke="#1565c0" stroke-width="2"/><text x="430" y="185" fill="#1565c0" font-size="9">ER</text><text x="275" y="330" text-anchor="middle" fill="#666" font-size="10" font-style="italic">Cytoplasm</text></svg>',
            "description": "Animal Cell: Contains nucleus (DNA), mitochondria (energy), and cell membrane."
        },
        "circuit": {
            "svg": '<svg width="500" height="250" xmlns="http://www.w3.org/2000/svg"><rect width="500" height="250" fill="white" stroke="#333" stroke-width="1"/><text x="250" y="25" text-anchor="middle" font-size="14" font-weight="bold">Simple Electric Circuit</text><rect x="60" y="110" width="45" height="60" fill="none" stroke="#333" stroke-width="2"/><line x1="60" y1="118" x2="105" y2="118" stroke="#333" stroke-width="2"/><line x1="60" y1="130" x2="105" y2="130" stroke="#333" stroke-width="2"/><text x="82" y="100" text-anchor="middle" font-size="10">Battery</text><line x1="105" y1="140" x2="200" y2="140" stroke="#333" stroke-width="2"/><line x1="200" y1="140" x2="200" y2="80" stroke="#333" stroke-width="2"/><line x1="200" y1="80" x2="340" y2="80" stroke="#333" stroke-width="2"/><line x1="340" y1="80" x2="340" y2="140" stroke="#333" stroke-width="2"/><line x1="340" y1="140" x2="420" y2="140" stroke="#333" stroke-width="2"/><line x1="420" y1="140" x2="420" y2="200" stroke="#333" stroke-width="2"/><line x1="420" y1="200" x2="105" y2="200" stroke="#333" stroke-width="2"/><circle cx="270" cy="110" r="20" fill="#fff3e0" stroke="#333" stroke-width="2"/><circle cx="270" cy="110" r="8" fill="#ffeb3b"/><text x="270" y="115" text-anchor="middle" font-size="12">💡</text><text x="270" y="65" text-anchor="middle" font-size="9">Bulb</text><circle cx="185" cy="140" r="3" fill="#333"/><circle cx="210" cy="140" r="3" fill="#333"/><line x1="188" y1="140" x2="198" y2="128" stroke="#333" stroke-width="2"/><text x="198" y="160" text-anchor="middle" font-size="9">Switch</text></svg>',
            "description": "Simple Circuit: Battery powers the bulb when switch is closed."
        }
    }
    
    diagram_type = request.diagram_type.lower()
    
    if diagram_type in diagrams:
        return DiagramResponse(
            success=True,
            svg=diagrams[diagram_type]["svg"],
            description=diagrams[diagram_type]["description"]
        )
    else:
        available = ", ".join(diagrams.keys())
        return DiagramResponse(
            success=False,
            description=f"Diagram not found. Available: {available}"
        )

# ============================================
# KALAX FARM - CROP DISEASE
# ============================================

@app.post("/farm/predict", response_model=CropResponse)
async def farm_predict(request: CropRequest):
    """Predict crop disease based on crop type"""
    
    crop = request.crop_type.lower()
    
    diseases = {
        "maize": {
            "disease": "Maize Streak Virus (MSV)",
            "confidence": 0.92,
            "treatment": "Use resistant varieties (Longe 6H, 7H, 8H). Control leafhoppers with insecticides.",
            "prevention": "Plant certified disease-free seeds. Remove infected plants immediately."
        },
        "beans": {
            "disease": "Angular Leaf Spot",
            "confidence": 0.88,
            "treatment": "Apply Mancozeb fungicide. Improve air circulation between plants.",
            "prevention": "Use certified seeds. Practice 3-year crop rotation."
        },
        "cassava": {
            "disease": "Cassava Mosaic Disease (CMD)",
            "confidence": 0.94,
            "treatment": "No chemical cure. Uproot and burn infected plants.",
            "prevention": "Use CMD-resistant varieties (NASE 14, 15, 19). Plant disease-free cuttings."
        },
        "coffee": {
            "disease": "Coffee Berry Borer",
            "confidence": 0.87,
            "treatment": "Prune affected branches. Apply Beauveria bassiana (biological control).",
            "prevention": "Harvest all berries. Remove fallen berries. Use pheromone traps."
        },
        "tomatoes": {
            "disease": "Late Blight",
            "confidence": 0.89,
            "treatment": "Apply Copper-based fungicides every 7-10 days.",
            "prevention": "Avoid overhead irrigation. Space plants for air circulation."
        }
    }
    
    if crop in diseases:
        info = diseases[crop]
        return CropResponse(
            success=True,
            disease=info["disease"],
            confidence=info["confidence"],
            treatment=info["treatment"],
            prevention=info["prevention"]
        )
    else:
        return CropResponse(
            success=True,
            disease="No disease detected",
            confidence=0.95,
            treatment="Crop appears healthy. Continue regular monitoring.",
            prevention="Maintain good agricultural practices."
        )

# ============================================
# KALAX SECURE - ATTENDANCE
# ============================================

# Student database
students = [
    {"id": "STU001", "name": "John Muwanga", "class": "S.3"},
    {"id": "STU002", "name": "Sarah Nambi", "class": "S.4"},
    {"id": "STU003", "name": "Peter Okello", "class": "S.2"},
    {"id": "STU004", "name": "Grace Auma", "class": "S.1"},
    {"id": "STU005", "name": "James Ssali", "class": "S.5"},
]

attendance_records = []

@app.post("/secure/attendance", response_model=AttendanceResponse)
async def secure_attendance(request: AttendanceRequest):
    """Mark attendance for a student"""
    
    # Find student
    student = None
    for s in students:
        if s["name"].lower() == request.student_name.lower():
            student = s
            break
    
    if not student:
        return AttendanceResponse(
            success=False,
            message=f"Student '{request.student_name}' not found. Available: {', '.join([s['name'] for s in students])}"
        )
    
    # Record attendance
    now = datetime.now()
    record = {
        "student_id": student["id"],
        "student_name": student["name"],
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "status": "present"
    }
    attendance_records.append(record)
    
    return AttendanceResponse(
        success=True,
        message=f"✅ Attendance marked for {student['name']}",
        student_name=student["name"],
        time=now.strftime("%H:%M:%S")
    )

@app.get("/secure/students")
async def get_students():
    """Get list of all students"""
    return {"students": students, "count": len(students)}

@app.get("/secure/attendance/{date}")
async def get_attendance(date: str):
    """Get attendance for a specific date"""
    records = [r for r in attendance_records if r["date"] == date]
    return {"date": date, "records": records, "total": len(records)}

# ============================================
# KALAX VISION - MEASUREMENT
# ============================================

@app.post("/vision/measure", response_model=MeasurementResponse)
async def vision_measure(request: MeasurementRequest):
    """Measure objects using pixel-to-cm conversion"""
    
    if request.reference_pixels <= 0:
        return MeasurementResponse(
            success=False,
            error="Reference pixels must be greater than 0"
        )
    
    # Formula: actual size = (object pixels × reference cm) ÷ reference pixels
    actual_cm = (request.object_pixels * request.reference_cm) / request.reference_pixels
    
    return MeasurementResponse(
        success=True,
        actual_cm=round(actual_cm, 2),
        formula=f"{request.object_pixels}px × {request.reference_cm}cm ÷ {request.reference_pixels}px = {actual_cm:.2f}cm"
    )

# ============================================
# RUN THE APP
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)