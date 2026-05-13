"""
Graph Engine - Generates mathematical graph data
"""

import math

def generate_graph_data(function: str, x_min: float = -8, x_max: float = 8) -> dict:
    """Generate x,y points for a mathematical function"""
    
    x_values = []
    y_values = []
    step = (x_max - x_min) / 200
    
    x = x_min
    while x <= x_max:
        try:
            # Convert ^ to ** for Python
            func = function.replace('^', '**')
            # Safe evaluation
            y = eval(func, {
                "x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "sqrt": math.sqrt, "exp": math.exp, "log": math.log, "pi": math.pi,
                "abs": abs
            })
            
            if isfinite(y) and abs(y) < 50:
                x_values.append(round(x, 2))
                y_values.append(round(y, 2))
        except:
            pass
        
        x += step
    
    return {
        "success": len(x_values) > 1,
        "x_values": x_values,
        "y_values": y_values,
        "function": function
    }

def isfinite(x):
    return not (math.isnan(x) or math.isinf(x))