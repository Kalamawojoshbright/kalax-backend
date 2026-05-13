"""
KalaX Learn - Complete AI + ALL Mathematical Diagrams
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import math
import re
from datetime import datetime

# Gemini AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAnsRMTOQpJalknuvfLNkfiMwkob6EQ7yE")
if GEMINI_AVAILABLE and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    MODEL_NAME = "gemini-2.0-flash-exp"
else:
    MODEL_NAME = None

# ============================================
# REQUEST MODELS
# ============================================

class ChatRequest(BaseModel):
    message: str
    subject: Optional[str] = "general"

class ChatResponse(BaseModel):
    response: str
    source: str

class MathRequest(BaseModel):
    expression: str
    type: str = "diagram"

class MathResponse(BaseModel):
    success: bool
    diagram_type: str
    svg: Optional[str] = None
    graph_data: Optional[dict] = None
    explanation: Optional[str] = None
    error: Optional[str] = None

# ============================================
# HEALTH ENDPOINTS
# ============================================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "KalaX Learn",
        "gemini": GEMINI_AVAILABLE and MODEL_NAME is not None,
        "creator": "Kalamawo Joshua Bright"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": str(datetime.now())}

# ============================================
# CHAT ENDPOINT - Gemini AI
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer ANY question using Gemini AI"""
    
    # Try Gemini first
    if GEMINI_AVAILABLE and MODEL_NAME:
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(request.message)
            return ChatResponse(response=response.text, source="gemini")
        except Exception as e:
            print(f"Gemini error: {e}")
    
    # Fallback responses
    return ChatResponse(response=get_local_response(request.message), source="local")

# ============================================
# MATH DIAGRAM ENDPOINT - ALL DIAGRAMS
# ============================================

@app.post("/math/diagram", response_model=MathResponse)
async def math_diagram(request: MathRequest):
    """Generate ANY mathematical diagram"""
    
    expr = request.expression.lower()
    
    # ========== 1. FUNCTIONS (GRAPHS) ==========
    if "plot" in expr or "graph" in expr or ("y=" in expr and not "draw" in expr):
        func = extract_function(request.expression)
        if func:
            graph_data = generate_graph(func)
            if graph_data["success"]:
                return MathResponse(
                    success=True,
                    diagram_type="graph",
                    graph_data=graph_data,
                    explanation=f"Graph of y = {func}"
                )
    
    # ========== 2. BASIC SHAPES ==========
    if "circle" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=CIRCLE_SVG, 
            explanation="Circle: All points equidistant from center. Area = πr², Circumference = 2πr")
    
    if "square" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=SQUARE_SVG,
            explanation="Square: All sides equal, 4 right angles. Area = s², Perimeter = 4s")
    
    if "rectangle" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=RECTANGLE_SVG,
            explanation="Rectangle: Opposite sides equal. Area = length × width")
    
    if "triangle" in expr:
        if "equilateral" in expr:
            return MathResponse(success=True, diagram_type="svg", svg=EQUILATERAL_TRIANGLE_SVG,
                explanation="Equilateral Triangle: All sides equal, all angles = 60°")
        elif "right" in expr:
            return MathResponse(success=True, diagram_type="svg", svg=RIGHT_TRIANGLE_SVG,
                explanation="Right Triangle: a² + b² = c² (Pythagorean Theorem)")
        else:
            return MathResponse(success=True, diagram_type="svg", svg=TRIANGLE_SVG,
                explanation="Triangle: 3 sides, sum of angles = 180°")
    
    # ========== 3. POLYGONS ==========
    if "pentagon" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=PENTAGON_SVG,
            explanation="Pentagon: 5-sided polygon. Interior angle = 108°")
    
    if "hexagon" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=HEXAGON_SVG,
            explanation="Hexagon: 6-sided polygon. Interior angle = 120°")
    
    if "heptagon" in expr or "septagon" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=HEPTAGON_SVG,
            explanation="Heptagon: 7-sided polygon. Interior angle ≈ 128.6°")
    
    if "octagon" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=OCTAGON_SVG,
            explanation="Octagon: 8-sided polygon. Interior angle = 135°")
    
    if "nonagon" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=NONAGON_SVG,
            explanation="Nonagon: 9-sided polygon. Interior angle = 140°")
    
    if "decagon" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=DECAGON_SVG,
            explanation="Decagon: 10-sided polygon. Interior angle = 144°")
    
    if "star" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=STAR_SVG,
            explanation="5-point star: Regular star polygon")
    
    # ========== 4. QUADRILATERALS ==========
    if "parallelogram" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=PARALLELOGRAM_SVG,
            explanation="Parallelogram: Opposite sides parallel and equal. Area = base × height")
    
    if "trapezoid" in expr or "trapezium" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=TRAPEZOID_SVG,
            explanation="Trapezoid: One pair of parallel sides. Area = ½(a+b) × height")
    
    if "rhombus" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=RHOMBUS_SVG,
            explanation="Rhombus: All sides equal, opposite angles equal")
    
    if "kite" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=KITE_SVG,
            explanation="Kite: Adjacent sides equal, one pair of opposite angles equal")
    
    # ========== 5. 3D SHAPES ==========
    if "cube" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=CUBE_SVG,
            explanation="Cube: Volume = s³, Surface Area = 6s²")
    
    if "cuboid" in expr or "rectangular prism" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=CUBOID_SVG,
            explanation="Cuboid: Volume = l × w × h")
    
    if "sphere" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=SPHERE_SVG,
            explanation="Sphere: Volume = ⁴⁄₃πr³, Surface Area = 4πr²")
    
    if "cylinder" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=CYLINDER_SVG,
            explanation="Cylinder: Volume = πr²h, Surface Area = 2πrh + 2πr²")
    
    if "cone" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=CONE_SVG,
            explanation="Cone: Volume = ⅓πr²h")
    
    if "pyramid" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=PYRAMID_SVG,
            explanation="Square Pyramid: Volume = ⅓ × base area × height")
    
    # ========== 6. TRIGONOMETRIC WAVES ==========
    if "sine wave" in expr or "sin wave" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=SINE_WAVE_SVG,
            explanation="y = sin(x) | Amplitude = 1, Period = 2π")
    
    if "cosine wave" in expr or "cos wave" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=COSINE_WAVE_SVG,
            explanation="y = cos(x) | Amplitude = 1, Period = 2π")
    
    if "tangent wave" in expr or "tan wave" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=TANGENT_WAVE_SVG,
            explanation="y = tan(x) | Asymptotes at π/2 + kπ")
    
    # ========== 7. SPECIAL CURVES ==========
    if "parabola" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=PARABOLA_SVG,
            explanation="Parabola: y = x² | U-shaped curve")
    
    if "hyperbola" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=HYPERBOLA_SVG,
            explanation="Hyperbola: y = 1/x | Two separate curves")
    
    if "ellipse" in expr or "oval" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=ELLIPSE_SVG,
            explanation="Ellipse: Area = π × a × b")
    
    if "exponential" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=EXPONENTIAL_SVG,
            explanation="Exponential: y = eˣ | Rapid growth")
    
    if "logarithmic" in expr or "log curve" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=LOGARITHMIC_SVG,
            explanation="Logarithmic: y = ln(x) | Slow growth")
    
    # ========== 8. ANGLES ==========
    if "right angle" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=RIGHT_ANGLE_SVG,
            explanation="Right Angle: Exactly 90 degrees")
    
    if "acute angle" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=ACUTE_ANGLE_SVG,
            explanation="Acute Angle: Less than 90 degrees")
    
    if "obtuse angle" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=OBTUSE_ANGLE_SVG,
            explanation="Obtuse Angle: Between 90° and 180°")
    
    if "reflex angle" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=REFLEX_ANGLE_SVG,
            explanation="Reflex Angle: Between 180° and 360°")
    
    # ========== 9. CHARTS & PLOTS ==========
    if "number line" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=NUMBER_LINE_SVG,
            explanation="Number line: Visual representation of numbers")
    
    if "coordinate plane" in expr or "cartesian plane" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=COORDINATE_PLANE_SVG,
            explanation="Cartesian Plane: x-axis (horizontal), y-axis (vertical)")
    
    if "bar chart" in expr or "bar graph" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=BAR_CHART_SVG,
            explanation="Bar Chart: Categorical data visualization")
    
    if "pie chart" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=PIE_CHART_SVG,
            explanation="Pie Chart: Data as percentages of a circle")
    
    if "venn diagram" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=VENN_DIAGRAM_SVG,
            explanation="Venn Diagram: Set intersections and relationships")
    
    if "histogram" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=HISTOGRAM_SVG,
            explanation="Histogram: Distribution of numerical data")
    
    if "line graph" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=LINE_GRAPH_SVG,
            explanation="Line Graph: Trends over time")
    
    # ========== 10. GEOMETRIC CONSTRUCTIONS ==========
    if "vector" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=VECTOR_SVG,
            explanation="Vector: Quantity with magnitude and direction")
    
    if "ray" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=RAY_SVG,
            explanation="Ray: Line starting at a point extending infinitely")
    
    if "line segment" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=LINE_SEGMENT_SVG,
            explanation="Line Segment: Part of a line with two endpoints")
    
    if "parallel lines" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=PARALLEL_LINES_SVG,
            explanation="Parallel Lines: Lines that never intersect")
    
    if "perpendicular lines" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=PERPENDICULAR_LINES_SVG,
            explanation="Perpendicular Lines: Lines that intersect at 90°")
    
    # ========== 11. TRANSFORMATIONS ==========
    if "translation" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=TRANSLATION_SVG,
            explanation="Translation: Moving a shape without rotation")
    
    if "rotation" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=ROTATION_SVG,
            explanation="Rotation: Turning a shape around a point")
    
    if "reflection" in expr or "mirror" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=REFLECTION_SVG,
            explanation="Reflection: Mirror image of a shape")
    
    # ========== 12. FRACTALS ==========
    if "sierpinski" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=SIERPINSKI_SVG,
            explanation="Sierpinski Triangle: Self-similar fractal")
    
    if "koch snowflake" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=KOCH_SNOWFLAKE_SVG,
            explanation="Koch Snowflake: Infinite perimeter fractal")
    
    # ========== 13. HEART & SPECIAL SHAPES ==========
    if "heart" in expr:
        return MathResponse(success=True, diagram_type="svg", svg=HEART_SVG,
            explanation="Heart shape: Symmetrical geometric curve")
    
    # ========== FALLBACK ==========
    return MathResponse(
        success=False,
        diagram_type="error",
        error="Try: 'Plot y = x^2', 'Draw a circle', 'Draw a pentagon', 'Draw a cube', 'Draw sine wave'"
    )

# ============================================
# GRAPH FUNCTIONS
# ============================================

def extract_function(expression: str) -> str:
    match = re.search(r'y\s*=\s*(.+?)(?:\s|$)', expression.lower())
    if match:
        return match[1].strip()
    match = re.search(r'plot\s+(.+?)(?:\s|$)', expression.lower())
    if match:
        return match[1].strip()
    return None

def generate_graph(func: str) -> dict:
    x_values = []
    y_values = []
    x_min, x_max = -6, 6
    step = 0.05
    
    x = x_min
    while x <= x_max:
        try:
            f = func.replace('^', '**')
            safe_dict = {
                "x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "sqrt": math.sqrt, "exp": math.exp, "log": math.log, "pi": math.pi,
                "abs": abs
            }
            y = eval(f, {"__builtins__": {}}, safe_dict)
            if math.isfinite(y) and abs(y) < 20:
                x_values.append(round(x, 2))
                y_values.append(round(y, 2))
        except:
            pass
        x += step
    
    return {
        "success": len(x_values) > 1,
        "x_values": x_values,
        "y_values": y_values,
        "function": func
    }

# ============================================
# LOCAL RESPONSES (Fallback)
# ============================================

def get_local_response(message: str) -> str:
    m = message.lower()
    
    if "photosynthesis" in m:
        return "🌿 **Photosynthesis**\n\n6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂"
    if "mitosis" in m:
        return "🔬 **Mitosis**\n\nStages: Prophase → Metaphase → Anaphase → Telophase"
    if "newton" in m:
        return "⚡ **Newton's Laws**\n\n1. Inertia, 2. F = ma, 3. Action-Reaction"
    if "hello" in m or "hi" in m:
        return "👋 Hello! I'm KalaX Learn. Try 'Plot y = x^2', 'Draw a circle', or 'What is photosynthesis?'"
    
    return f"""📚 **KalaX Learn**

I can help with:
• Answering ANY question using Gemini AI
• Drawing ALL mathematical diagrams

**Try these commands:**
• 'Plot y = x^2' - Parabola graph
• 'Draw a circle' - Geometric circle
• 'Draw a pentagon' - 5-sided polygon
• 'Draw a cube' - 3D cube
• 'Draw sine wave' - Trigonometric wave
• 'What is photosynthesis?' - Science question

Created by Kalamawo Joshua Bright"""

# ============================================
# SVG DIAGRAMS - COMPLETE COLLECTION
# ============================================

CIRCLE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><circle cx="200" cy="200" r="120" fill="none" stroke="#0f3460" stroke-width="3"/><line x1="200" y1="200" x2="320" y2="200" stroke="#e94560" stroke-width="2" stroke-dasharray="5,5"/><circle cx="200" cy="200" r="5" fill="#e94560"/><text x="260" y="190" fill="#e94560" font-size="14">Radius (r)</text><text x="200" y="220" text-anchor="middle" fill="#0f3460" font-size="14">Center</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Area = πr² | Circumference = 2πr</text></svg>'''

SQUARE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><rect x="100" y="100" width="200" height="200" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><line x1="100" y1="100" x2="300" y2="100" stroke="#e94560" stroke-width="2"/><text x="200" y="90" text-anchor="middle" fill="#e94560" font-size="14">Side (s)</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Area = s² | Perimeter = 4s | All angles = 90°</text></svg>'''

RECTANGLE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><rect x="80" y="120" width="240" height="160" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><line x1="80" y1="120" x2="320" y2="120" stroke="#e94560" stroke-width="2"/><text x="200" y="110" text-anchor="middle" fill="#e94560" font-size="14">Length (l)</text><line x1="80" y1="120" x2="80" y2="280" stroke="#4ecdc4" stroke-width="2"/><text x="65" y="200" text-anchor="middle" fill="#4ecdc4" font-size="14">Width (w)</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Area = l × w | Perimeter = 2(l + w)</text></svg>'''

TRIANGLE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="80,300 300,300 200,100" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><text x="190" y="320" text-anchor="middle" fill="#0f3460" font-size="14">Base</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Area = ½ × base × height | Sum of angles = 180°</text></svg>'''

RIGHT_TRIANGLE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="80,300 300,300 80,100" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><polygon points="80,280 100,280 100,300" fill="none" stroke="#e94560" stroke-width="2"/><text x="90" y="295" text-anchor="middle" fill="#e94560" font-size="14">90°</text><text x="190" y="320" text-anchor="middle" fill="#0f3460" font-size="14">Base (b)</text><text x="65" y="200" text-anchor="middle" fill="#0f3460" font-size="14">Height (h)</text><text x="240" y="170" fill="#666" font-size="12">Hypotenuse (c)</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">a² + b² = c² (Pythagorean Theorem)</text></svg>'''

EQUILATERAL_TRIANGLE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="200,80 80,320 320,320" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><text x="200" y="60" text-anchor="middle" fill="#e94560" font-size="14">60°</text><text x="65" y="335" text-anchor="middle" fill="#e94560" font-size="14">60°</text><text x="335" y="335" text-anchor="middle" fill="#e94560" font-size="14">60°</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">All sides equal | All angles = 60°</text></svg>'''

PENTAGON_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="200,60 340,160 280,320 120,320 60,160" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Pentagon: 5 sides | Interior angle = 108°</text></svg>'''

HEXAGON_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="200,60 340,130 340,270 200,340 60,270 60,130" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Hexagon: 6 sides | Interior angle = 120°</text></svg>'''

HEPTAGON_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="200,50 340,100 380,230 310,350 90,350 20,230 60,100" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Heptagon: 7 sides | Interior angle ≈ 128.6°</text></svg>'''

OCTAGON_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="200,60 320,100 360,200 320,300 200,340 80,300 40,200 80,100" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Octagon: 8 sides | Interior angle = 135°</text></svg>'''

NONAGON_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="200,50 290,80 350,160 360,260 310,340 220,360 130,340 50,280 40,180" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Nonagon: 9 sides | Interior angle = 140°</text></svg>'''

DECAGON_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="200,50 270,70 340,130 360,200 340,270 270,330 200,350 130,330 60,270 40,200 60,130 130,70" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Decagon: 10 sides | Interior angle = 144°</text></svg>'''

STAR_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="200,40 240,160 380,160 260,240 310,360 200,280 90,360 140,240 20,160 160,160" fill="rgba(255,215,0,0.2)" stroke="#FFD700" stroke-width="3"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">5-point Star | Golden ratio proportions</text></svg>'''

PARALLELOGRAM_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="80,280 280,280 220,120 20,120" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><text x="150" y="300" text-anchor="middle" fill="#e94560" font-size="12">Base</text><line x1="80" y1="280" x2="80" y2="120" stroke="#4ecdc4" stroke-width="1.5" stroke-dasharray="4,4"/><text x="60" y="200" text-anchor="middle" fill="#4ecdc4" font-size="12">Height</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Area = base × height</text></svg>'''

TRAPEZOID_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="80,280 320,280 260,120 140,120" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><line x1="140" y1="120" x2="140" y2="280" stroke="#ff9800" stroke-width="1.5" stroke-dasharray="4,4"/><text x="125" y="200" text-anchor="middle" fill="#ff9800" font-size="12">Height</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Area = ½ × (a + b) × height</text></svg>'''

RHOMBUS_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="200,60 320,200 200,340 80,200" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Rhombus: All sides equal, opposite angles equal</text></svg>'''

KITE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="200,60 300,160 200,340 100,160" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Kite: Adjacent sides equal, one pair of opposite angles equal</text></svg>'''

CUBE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="140,100 260,100 300,140 180,140" fill="rgba(15,52,96,0.2)" stroke="#0f3460" stroke-width="2"/><polygon points="140,100 180,140 180,260 140,220" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="2"/><polygon points="180,140 300,140 300,260 180,260" fill="rgba(15,52,96,0.15)" stroke="#0f3460" stroke-width="2"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Cube: Volume = s³ | Surface Area = 6s²</text></svg>'''

CUBOID_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="120,100 240,100 280,140 160,140" fill="rgba(15,52,96,0.2)" stroke="#0f3460" stroke-width="2"/><polygon points="120,100 160,140 160,280 120,240" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="2"/><polygon points="160,140 280,140 280,280 160,280" fill="rgba(15,52,96,0.15)" stroke="#0f3460" stroke-width="2"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Cuboid: Volume = l × w × h</text></svg>'''

SPHERE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><circle cx="200" cy="200" r="100" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><ellipse cx="200" cy="200" rx="100" ry="30" fill="none" stroke="#e94560" stroke-width="1.5"/><ellipse cx="200" cy="200" rx="30" ry="100" fill="none" stroke="#4ecdc4" stroke-width="1.5"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Sphere: Volume = ⁴⁄₃πr³ | Surface Area = 4πr²</text></svg>'''

CYLINDER_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><ellipse cx="200" cy="100" rx="80" ry="25" fill="rgba(15,52,96,0.2)" stroke="#0f3460" stroke-width="2"/><rect x="120" y="100" width="160" height="200" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="2"/><ellipse cx="200" cy="300" rx="80" ry="25" fill="rgba(15,52,96,0.15)" stroke="#0f3460" stroke-width="2"/><line x1="120" y1="100" x2="120" y2="300" stroke="#e94560" stroke-width="2" stroke-dasharray="5,5"/><text x="100" y="200" text-anchor="end" fill="#e94560" font-size="12">Height (h)</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Volume = πr²h | Surface Area = 2πrh + 2πr²</text></svg>'''

CONE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><ellipse cx="200" cy="320" rx="80" ry="20" fill="rgba(15,52,96,0.15)" stroke="#0f3460" stroke-width="2"/><polygon points="120,320 200,80 280,320" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="2"/><line x1="200" y1="80" x2="200" y2="320" stroke="#e94560" stroke-width="2" stroke-dasharray="5,5"/><text x="210" y="200" fill="#e94560" font-size="12">Height (h)</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Volume = ⅓πr²h</text></svg>'''

PYRAMID_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="120,320 280,320 200,100" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="2"/><polygon points="280,320 200,280 200,100" fill="rgba(15,52,96,0.05)" stroke="#0f3460" stroke-width="2"/><polygon points="120,320 200,280 200,100" fill="rgba(15,52,96,0.05)" stroke="#0f3460" stroke-width="2"/><line x1="200" y1="100" x2="200" y2="320" stroke="#e94560" stroke-width="2" stroke-dasharray="5,5"/><text x="210" y="210" fill="#e94560" font-size="12">Height (h)</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Volume = ⅓ × base area × height</text></svg>'''

SINE_WAVE_SVG = '''<svg width="600" height="300" viewBox="0 0 600 300"><rect width="600" height="300" fill="#f8f9fa"/><path d="M0,150 Q30,50 60,150 T120,150 T180,150 T240,150 T300,150 T360,150 T420,150 T480,150 T540,150 T600,150" fill="none" stroke="#e94560" stroke-width="3"/><line x1="0" y1="150" x2="600" y2="150" stroke="#333" stroke-width="1.5"/><line x1="300" y1="0" x2="300" y2="300" stroke="#333" stroke-width="1" stroke-dasharray="4,4"/><text x="600" y="155" fill="#333" font-size="12">x</text><text x="305" y="15" fill="#333" font-size="12">y</text><text x="300" y="290" text-anchor="middle" fill="#666" font-size="12">y = sin(x) | Amplitude = 1 | Period = 2π</text></svg>'''

COSINE_WAVE_SVG = '''<svg width="600" height="300" viewBox="0 0 600 300"><rect width="600" height="300" fill="#f8f9fa"/><path d="M0,50 Q30,150 60,50 T120,50 T180,50 T240,50 T300,50 T360,50 T420,50 T480,50 T540,50 T600,50" fill="none" stroke="#e94560" stroke-width="3"/><line x1="0" y1="150" x2="600" y2="150" stroke="#333" stroke-width="1.5"/><text x="600" y="155" fill="#333" font-size="12">x</text><text x="305" y="15" fill="#333" font-size="12">y</text><text x="300" y="290" text-anchor="middle" fill="#666" font-size="12">y = cos(x) | Amplitude = 1 | Period = 2π</text></svg>'''

TANGENT_WAVE_SVG = '''<svg width="600" height="300" viewBox="0 0 600 300"><rect width="600" height="300" fill="#f8f9fa"/><path d="M0,150 Q75,0 150,150" fill="none" stroke="#e94560" stroke-width="3"/><path d="M150,150 Q225,300 300,150" fill="none" stroke="#e94560" stroke-width="3"/><path d="M300,150 Q375,0 450,150" fill="none" stroke="#e94560" stroke-width="3"/><path d="M450,150 Q525,300 600,150" fill="none" stroke="#e94560" stroke-width="3"/><line x1="0" y1="150" x2="600" y2="150" stroke="#333" stroke-width="1.5"/><text x="600" y="155" fill="#333" font-size="12">x</text><text x="305" y="15" fill="#333" font-size="12">y</text><text x="300" y="290" text-anchor="middle" fill="#666" font-size="12">y = tan(x) | Asymptotes at π/2 + kπ</text></svg>'''

PARABOLA_SVG = '''<svg width="500" height="400" viewBox="0 0 500 400"><rect width="500" height="400" fill="#f8f9fa"/><path d="M100,300 Q250,50 400,300" fill="none" stroke="#e94560" stroke-width="3"/><line x1="50" y1="300" x2="450" y2="300" stroke="#333" stroke-width="1.5"/><line x1="250" y1="50" x2="250" y2="350" stroke="#333" stroke-width="1.5"/><text x="250" y="390" text-anchor="middle" fill="#666" font-size="12">Parabola: y = x² | U-shaped curve</text></svg>'''

HYPERBOLA_SVG = '''<svg width="500" height="400" viewBox="0 0 500 400"><rect width="500" height="400" fill="#f8f9fa"/><path d="M150,150 Q200,100 300,50" fill="none" stroke="#e94560" stroke-width="3"/><path d="M150,250 Q200,300 300,350" fill="none" stroke="#e94560" stroke-width="3"/><path d="M350,150 Q300,100 200,50" fill="none" stroke="#4ecdc4" stroke-width="3"/><path d="M350,250 Q300,300 200,350" fill="none" stroke="#4ecdc4" stroke-width="3"/><line x1="50" y1="200" x2="450" y2="200" stroke="#333" stroke-width="1.5"/><line x1="250" y1="50" x2="250" y2="350" stroke="#333" stroke-width="1.5"/><text x="250" y="390" text-anchor="middle" fill="#666" font-size="12">Hyperbola: y = 1/x | Two separate curves</text></svg>'''

ELLIPSE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><ellipse cx="200" cy="200" rx="140" ry="80" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/><line x1="200" y1="200" x2="340" y2="200" stroke="#e94560" stroke-width="2" stroke-dasharray="5,5"/><text x="270" y="190" fill="#e94560" font-size="12">a (semi-major)</text><line x1="200" y1="200" x2="200" y2="120" stroke="#4ecdc4" stroke-width="2" stroke-dasharray="5,5"/><text x="210" y="155" fill="#4ecdc4" font-size="12">b (semi-minor)</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Area = π × a × b</text></svg>'''

EXPONENTIAL_SVG = '''<svg width="500" height="400" viewBox="0 0 500 400"><rect width="500" height="400" fill="#f8f9fa"/><path d="M50,350 Q150,300 250,200 Q350,100 450,20" fill="none" stroke="#e94560" stroke-width="3"/><line x1="50" y1="300" x2="450" y2="300" stroke="#333" stroke-width="1.5"/><line x1="250" y1="50" x2="250" y2="350" stroke="#333" stroke-width="1.5"/><text x="250" y="390" text-anchor="middle" fill="#666" font-size="12">Exponential: y = eˣ | Rapid growth</text></svg>'''

LOGARITHMIC_SVG = '''<svg width="500" height="400" viewBox="0 0 500 400"><rect width="500" height="400" fill="#f8f9fa"/><path d="M50,50 Q150,150 250,230 Q350,280 450,310" fill="none" stroke="#e94560" stroke-width="3"/><line x1="50" y1="300" x2="450" y2="300" stroke="#333" stroke-width="1.5"/><line x1="250" y1="50" x2="250" y2="350" stroke="#333" stroke-width="1.5"/><text x="250" y="390" text-anchor="middle" fill="#666" font-size="12">Logarithmic: y = ln(x) | Slow growth</text></svg>'''

RIGHT_ANGLE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><line x1="80" y1="280" x2="280" y2="280" stroke="#0f3460" stroke-width="3"/><line x1="80" y1="280" x2="80" y2="80" stroke="#0f3460" stroke-width="3"/><polygon points="80,260 100,260 100,280" fill="none" stroke="#e94560" stroke-width="2"/><text x="90" y="275" text-anchor="middle" fill="#e94560" font-size="14">90°</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Right Angle: Exactly 90 degrees</text></svg>'''

ACUTE_ANGLE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><line x1="80" y1="280" x2="280" y2="280" stroke="#0f3460" stroke-width="3"/><line x1="80" y1="280" x2="250" y2="100" stroke="#0f3460" stroke-width="3"/><path d="M130,250 A60,60 0 0,1 190,200" fill="none" stroke="#e94560" stroke-width="2"/><text x="150" y="235" fill="#e94560" font-size="14">45°</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Acute Angle: Less than 90° (e.g., 45°)</text></svg>'''

OBTUSE_ANGLE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><line x1="80" y1="280" x2="280" y2="280" stroke="#0f3460" stroke-width="3"/><line x1="80" y1="280" x2="120" y2="120" stroke="#0f3460" stroke-width="3"/><path d="M95,250 A50,50 0 0,1 85,210" fill="none" stroke="#e94560" stroke-width="2"/><text x="80" y="240" fill="#e94560" font-size="14">120°</text><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Obtuse Angle: Between 90° and 180° (120°)</text></svg>'''

REFLEX_ANGLE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><circle cx="200" cy="200" r="120" fill="none" stroke="#333" stroke-width="1.5"/><path d="M200,80 A120,120 0 1,1 80,200" fill="none" stroke="#e94560" stroke-width="3"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Reflex Angle: Between 180° and 360°</text></svg>'''

NUMBER_LINE_SVG = '''<svg width="500" height="200" viewBox="0 0 500 200"><rect width="500" height="200" fill="#f8f9fa"/><line x1="50" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2"/><polygon points="450,95 460,100 450,105" fill="#333"/><g font-size="14" text-anchor="middle" fill="#333"><text x="50" y="120">-5</text><text x="100" y="120">-4</text><text x="150" y="120">-3</text><text x="200" y="120">-2</text><text x="250" y="120">-1</text><text x="300" y="120">0</text><text x="350" y="120">1</text><text x="400" y="120">2</text><text x="450" y="120">3</text></g><g stroke="#333" stroke-width="1.5"><line x1="50" y1="95" x2="50" y2="105"/><line x1="100" y1="95" x2="100" y2="105"/><line x1="150" y1="95" x2="150" y2="105"/><line x1="200" y1="95" x2="200" y2="105"/><line x1="250" y1="95" x2="250" y2="105"/><line x1="300" y1="95" x2="300" y2="105"/><line x1="350" y1="95" x2="350" y2="105"/><line x1="400" y1="95" x2="400" y2="105"/><line x1="450" y1="95" x2="450" y2="105"/></g><text x="250" y="180" text-anchor="middle" fill="#666" font-size="12">Number Line: Integers from -5 to 3</text></svg>'''

COORDINATE_PLANE_SVG = '''<svg width="500" height="500" viewBox="0 0 500 500"><rect width="500" height="500" fill="#f8f9fa"/><g stroke="#ddd" stroke-width="0.5"><line x1="50" y1="250" x2="450" y2="250"/><line x1="250" y1="50" x2="250" y2="450"/></g><line x1="50" y1="250" x2="450" y2="250" stroke="#333" stroke-width="2"/><line x1="250" y1="50" x2="250" y2="450" stroke="#333" stroke-width="2"/><polygon points="445,245 455,250 445,255" fill="#333"/><polygon points="245,55 250,45 255,55" fill="#333"/><text x="460" y="255" fill="#333" font-size="14">x</text><text x="255" y="45" fill="#333" font-size="14">y</text><text x="255" y="260" fill="#333" font-size="12">O</text><text x="250" y="480" text-anchor="middle" fill="#666" font-size="12">Cartesian Coordinate Plane | Origin at (0,0)</text></svg>'''

BAR_CHART_SVG = '''<svg width="500" height="400" viewBox="0 0 500 400"><rect width="500" height="400" fill="#f8f9fa"/><rect x="60" y="300" width="50" height="50" fill="#0f3460"/><rect x="130" y="250" width="50" height="100" fill="#e94560"/><rect x="200" y="200" width="50" height="150" fill="#4ecdc4"/><rect x="270" y="150" width="50" height="200" fill="#ff9800"/><rect x="340" y="100" width="50" height="250" fill="#9c27b0"/><line x1="40" y1="350" x2="410" y2="350" stroke="#333" stroke-width="2"/><line x1="40" y1="50" x2="40" y2="350" stroke="#333" stroke-width="2"/><text x="85" y="370" text-anchor="middle" font-size="10">A</text><text x="155" y="370" text-anchor="middle" font-size="10">B</text><text x="225" y="370" text-anchor="middle" font-size="10">C</text><text x="295" y="370" text-anchor="middle" font-size="10">D</text><text x="365" y="370" text-anchor="middle" font-size="10">E</text><text x="250" y="390" text-anchor="middle" fill="#666" font-size="12">Bar Chart: Categorical data comparison</text></svg>'''

PIE_CHART_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><circle cx="200" cy="200" r="120" fill="white" stroke="#333" stroke-width="2"/><path d="M200,200 L200,80 A120,120 0 0,1 304,304 Z" fill="#0f3460"/><path d="M200,200 L304,304 A120,120 0 0,1 240,330 Z" fill="#e94560"/><path d="M200,200 L240,330 A120,120 0 0,1 80,240 Z" fill="#4ecdc4"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Pie Chart: Data as percentages</text></svg>'''

VENN_DIAGRAM_SVG = '''<svg width="500" height="400" viewBox="0 0 500 400"><rect width="500" height="400" fill="#f8f9fa"/><circle cx="180" cy="200" r="80" fill="rgba(15,52,96,0.2)" stroke="#0f3460" stroke-width="2"/><circle cx="320" cy="200" r="80" fill="rgba(233,69,96,0.2)" stroke="#e94560" stroke-width="2"/><text x="160" y="190" text-anchor="middle" font-size="14" fill="#0f3460">Set A</text><text x="340" y="190" text-anchor="middle" font-size="14" fill="#e94560">Set B</text><text x="250" y="205" text-anchor="middle" font-size="12" fill="#333">A ∩ B</text><text x="250" y="380" text-anchor="middle" fill="#666" font-size="12">Venn Diagram: Set intersections</text></svg>'''

HISTOGRAM_SVG = '''<svg width="500" height="400" viewBox="0 0 500 400"><rect width="500" height="400" fill="#f8f9fa"/><rect x="70" y="280" width="40" height="70" fill="#0f3460"/><rect x="120" y="220" width="40" height="130" fill="#0f3460"/><rect x="170" y="150" width="40" height="200" fill="#0f3460"/><rect x="220" y="180" width="40" height="170" fill="#0f3460"/><rect x="270" y="250" width="40" height="100" fill="#0f3460"/><rect x="320" y="300" width="40" height="50" fill="#0f3460"/><rect x="370" y="320" width="40" height="30" fill="#0f3460"/><line x1="50" y1="350" x2="430" y2="350" stroke="#333" stroke-width="2"/><line x1="50" y1="50" x2="50" y2="350" stroke="#333" stroke-width="2"/><text x="250" y="390" text-anchor="middle" fill="#666" font-size="12">Histogram: Distribution of data</text></svg>'''

LINE_GRAPH_SVG = '''<svg width="500" height="400" viewBox="0 0 500 400"><rect width="500" height="400" fill="#f8f9fa"/><polyline points="60,320 140,280 220,200 300,250 380,150 440,100" fill="none" stroke="#e94560" stroke-width="3"/><circle cx="60" cy="320" r="5" fill="#e94560"/><circle cx="140" cy="280" r="5" fill="#e94560"/><circle cx="220" cy="200" r="5" fill="#e94560"/><circle cx="300" cy="250" r="5" fill="#e94560"/><circle cx="380" cy="150" r="5" fill="#e94560"/><circle cx="440" cy="100" r="5" fill="#e94560"/><line x1="50" y1="350" x2="450" y2="350" stroke="#333" stroke-width="2"/><line x1="50" y1="50" x2="50" y2="350" stroke="#333" stroke-width="2"/><text x="250" y="390" text-anchor="middle" fill="#666" font-size="12">Line Graph: Trends over time</text></svg>'''

VECTOR_SVG = '''<svg width="500" height="300" viewBox="0 0 500 300"><rect width="500" height="300" fill="#f8f9fa"/><line x1="50" y1="150" x2="350" y2="100" stroke="#0f3460" stroke-width="3"/><polygon points="345,94 360,98 350,105" fill="#e94560"/><text x="200" y="135" text-anchor="middle" fill="#e94560" font-size="14">Vector v</text><text x="250" y="280" text-anchor="middle" fill="#666" font-size="12">Vector: Quantity with magnitude and direction</text></svg>'''

RAY_SVG = '''<svg width="500" height="300" viewBox="0 0 500 300"><rect width="500" height="300" fill="#f8f9fa"/><line x1="80" y1="150" x2="450" y2="150" stroke="#0f3460" stroke-width="3"/><circle cx="80" cy="150" r="6" fill="#e94560"/><polygon points="445,145 460,150 445,155" fill="#e94560"/><text x="250" y="280" text-anchor="middle" fill="#666" font-size="12">Ray: Starts at point, extends infinitely</text></svg>'''

LINE_SEGMENT_SVG = '''<svg width="500" height="300" viewBox="0 0 500 300"><rect width="500" height="300" fill="#f8f9fa"/><line x1="80" y1="150" x2="420" y2="150" stroke="#0f3460" stroke-width="3"/><circle cx="80" cy="150" r="6" fill="#e94560"/><circle cx="420" cy="150" r="6" fill="#e94560"/><text x="250" y="280" text-anchor="middle" fill="#666" font-size="12">Line Segment: Part of a line with two endpoints</text></svg>'''

PARALLEL_LINES_SVG = '''<svg width="500" height="300" viewBox="0 0 500 300"><rect width="500" height="300" fill="#f8f9fa"/><line x1="80" y1="100" x2="420" y2="100" stroke="#0f3460" stroke-width="3"/><line x1="80" y1="200" x2="420" y2="200" stroke="#0f3460" stroke-width="3"/><text x="250" y="280" text-anchor="middle" fill="#666" font-size="12">Parallel Lines: Lines that never intersect</text></svg>'''

PERPENDICULAR_LINES_SVG = '''<svg width="500" height="300" viewBox="0 0 500 300"><rect width="500" height="300" fill="#f8f9fa"/><line x1="100" y1="200" x2="400" y2="200" stroke="#0f3460" stroke-width="3"/><line x1="250" y1="80" x2="250" y2="220" stroke="#0f3460" stroke-width="3"/><polygon points="245,195 255,195 250,205" fill="none" stroke="#e94560" stroke-width="2"/><text x="200" y="235" fill="#e94560" font-size="14">90°</text><text x="250" y="280" text-anchor="middle" fill="#666" font-size="12">Perpendicular Lines: Intersect at 90°</text></svg>'''

TRANSLATION_SVG = '''<svg width="500" height="300" viewBox="0 0 500 300"><rect width="500" height="300" fill="#f8f9fa"/><polygon points="120,180 160,180 140,140" fill="rgba(15,52,96,0.3)" stroke="#0f3460" stroke-width="2"/><polygon points="280,180 320,180 300,140" fill="rgba(233,69,96,0.3)" stroke="#e94560" stroke-width="2"/><text x="140" y="170" text-anchor="middle" font-size="12" fill="#0f3460">Original</text><text x="300" y="170" text-anchor="middle" font-size="12" fill="#e94560">Translated</text><text x="250" y="280" text-anchor="middle" fill="#666" font-size="12">Translation: Moving a shape without rotation</text></svg>'''

ROTATION_SVG = '''<svg width="500" height="300" viewBox="0 0 500 300"><rect width="500" height="300" fill="#f8f9fa"/><polygon points="180,200 220,200 200,160" fill="rgba(15,52,96,0.3)" stroke="#0f3460" stroke-width="2"/><polygon points="280,160 300,200 250,180" fill="rgba(233,69,96,0.3)" stroke="#e94560" stroke-width="2"/><circle cx="200" cy="180" r="3" fill="#333"/><text x="250" y="280" text-anchor="middle" fill="#666" font-size="12">Rotation: Turning a shape around a point</text></svg>'''

REFLECTION_SVG = '''<svg width="500" height="300" viewBox="0 0 500 300"><rect width="500" height="300" fill="#f8f9fa"/><polygon points="120,180 160,180 140,140" fill="rgba(15,52,96,0.3)" stroke="#0f3460" stroke-width="2"/><polygon points="300,180 340,180 320,140" fill="rgba(233,69,96,0.3)" stroke="#e94560" stroke-width="2"/><line x1="230" y1="120" x2="230" y2="220" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/><text x="250" y="280" text-anchor="middle" fill="#666" font-size="12">Reflection: Mirror image of a shape</text></svg>'''

SIERPINSKI_SVG = '''<svg width="400" height="350" viewBox="0 0 400 350"><rect width="400" height="350" fill="#f8f9fa"/><polygon points="200,30 370,320 30,320" fill="none" stroke="#0f3460" stroke-width="2"/><polygon points="200,120 285,250 115,250" fill="none" stroke="#e94560" stroke-width="1.5"/><polygon points="200,170 243,220 157,220" fill="none" stroke="#4ecdc4" stroke-width="1"/><text x="200" y="340" text-anchor="middle" fill="#666" font-size="12">Sierpinski Triangle: Self-similar fractal</text></svg>'''

KOCH_SNOWFLAKE_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><polygon points="200,50 340,200 200,350 60,200" fill="none" stroke="#e94560" stroke-width="2"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Koch Snowflake: Infinite perimeter fractal</text></svg>'''

HEART_SVG = '''<svg width="400" height="400" viewBox="0 0 400 400"><rect width="400" height="400" fill="#f8f9fa"/><path d="M200,340 C100,260 60,300 200,380 C340,300 300,260 200,340" fill="#FF6B6B" stroke="#c92a2a" stroke-width="2"/><text x="200" y="380" text-anchor="middle" fill="#666" font-size="12">Heart shape | Symmetrical curve</text></svg>'''

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)