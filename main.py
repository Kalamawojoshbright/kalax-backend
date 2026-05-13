"""
KalaX Backend - Mathematical Graph System
Textbook style graphs with proper grid lines
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import math
import re
from datetime import datetime

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# REQUEST MODELS
# ============================================

class ChatRequest(BaseModel):
    message: str
    subject: Optional[str] = "general"

class ChatResponse(BaseModel):
    response: str
    source: str

class GraphRequest(BaseModel):
    function: str
    x_min: Optional[float] = -6
    x_max: Optional[float] = 6

class GraphResponse(BaseModel):
    success: bool
    grid_data: Optional[dict] = None
    error: Optional[str] = None

# ============================================
# HEALTH ENDPOINTS
# ============================================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "KalaX Math Graph",
        "creator": "Kalamawo Joshua Bright"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": str(datetime.now())}

# ============================================
# CHAT ENDPOINT
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer math questions"""
    return ChatResponse(
        response=get_math_response(request.message),
        source="local"
    )

# ============================================
# GRAPH ENDPOINT - Textbook Style
# ============================================

@app.post("/graph", response_model=GraphResponse)
async def generate_graph(request: GraphRequest):
    """Generate textbook-style graph data with grid"""
    try:
        func = request.function.replace('^', '**')
        
        # Calculate range based on function type
        x_min, x_max = get_optimal_range(func)
        
        # Generate points
        x_values, y_values = generate_points(func, x_min, x_max)
        
        if len(x_values) < 2:
            return GraphResponse(
                success=False,
                error="Could not generate graph. Try 'x**2', '2*x+3', or 'sin(x)'"
            )
        
        # Generate grid lines data
        grid_data = {
            "x_min": x_min,
            "x_max": x_max,
            "y_min": get_y_min(y_values),
            "y_max": get_y_max(y_values),
            "x_values": x_values,
            "y_values": y_values,
            "function": request.function,
            "grid_lines_x": generate_grid_lines_x(x_min, x_max),
            "grid_lines_y": generate_grid_lines_y(get_y_min(y_values), get_y_max(y_values))
        }
        
        return GraphResponse(
            success=True,
            grid_data=grid_data
        )
        
    except Exception as e:
        return GraphResponse(success=False, error=str(e))

# ============================================
# MATH RESPONSES
# ============================================

def get_math_response(message: str) -> str:
    m = message.lower()
    
    if "photosynthesis" in m:
        return "🌿 **Photosynthesis**\n\n6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂"
    
    if "mitosis" in m:
        return "🔬 **Mitosis**\n\nStages: Prophase → Metaphase → Anaphase → Telophase"
    
    if "newton" in m:
        return "⚡ **Newton's Laws**\n\n1. Inertia\n2. F = ma\n3. Action-Reaction"
    
    if "hello" in m or "hi" in m:
        return "👋 Hello! I'm KalaX Math.\n\nTry:\n• 'Plot y = x^2'\n• 'Graph y = 2x + 3'\n• 'Plot y = sin(x)'\n• 'Graph y = x^3 - 2x'"
    
    return f"""📐 **KalaX Math Graph**

Try these commands:
• 'Plot y = x^2' - Parabola
• 'Plot y = 2x + 3' - Straight line
• 'Plot y = sin(x)' - Sine wave
• 'Plot y = x^3' - Cubic curve
• 'Plot y = |x|' - Absolute value
• 'Plot y = 1/x' - Hyperbola

Created by Kalamawo Joshua Bright"""

# ============================================
# GRAPH HELPER FUNCTIONS
# ============================================

def get_optimal_range(func: str):
    """Determine optimal x-range based on function type"""
    if "sin" in func or "cos" in func:
        return -2 * math.pi, 2 * math.pi
    elif "sqrt" in func:
        return 0, 8
    elif "log" in func:
        return 0.1, 8
    elif "1/x" in func:
        return -5, 5
    else:
        return -6, 6

def generate_points(func: str, x_min: float, x_max: float):
    """Generate x,y points for the function"""
    x_values = []
    y_values = []
    step = (x_max - x_min) / 400
    
    x = x_min
    while x <= x_max:
        try:
            # Create safe evaluation environment
            safe_dict = {
                "x": x,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "asin": math.asin, "acos": math.acos, "atan": math.atan,
                "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
                "sqrt": math.sqrt, "exp": math.exp, "log": math.log, "log10": math.log10,
                "pi": math.pi, "e": math.e, "abs": abs,
                "floor": math.floor, "ceil": math.ceil
            }
            y = eval(func, {"__builtins__": {}}, safe_dict)
            
            if math.isfinite(y) and abs(y) < 50:
                x_values.append(round(x, 3))
                y_values.append(round(y, 3))
        except:
            pass
        x += step
    
    return x_values, y_values

def get_y_min(y_values):
    if not y_values:
        return -5
    min_y = min(y_values)
    return math.floor(min_y) - 1 if min_y > -10 else -10

def get_y_max(y_values):
    if not y_values:
        return 5
    max_y = max(y_values)
    return math.ceil(max_y) + 1 if max_y < 10 else 10

def generate_grid_lines_x(x_min: float, x_max: float):
    """Generate grid line positions for x-axis"""
    lines = []
    start = math.ceil(x_min)
    end = math.floor(x_max)
    for x in range(start, end + 1):
        lines.append(x)
    return lines

def generate_grid_lines_y(y_min: float, y_max: float):
    """Generate grid line positions for y-axis"""
    lines = []
    start = math.ceil(y_min)
    end = math.floor(y_max)
    for y in range(start, end + 1):
        lines.append(y)
    return lines

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)