"""
Geometry Engine - Generates SVG for geometric shapes
"""

def generate_geometry_svg(shape_type: str) -> dict:
    """Generate SVG for geometric shapes"""
    
    if shape_type == "circle":
        svg = '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="400" fill="#f8f9fa"/>
            <circle cx="200" cy="200" r="120" fill="none" stroke="#0f3460" stroke-width="3"/>
            <line x1="200" y1="200" x2="320" y2="200" stroke="#e94560" stroke-width="2" stroke-dasharray="5,5"/>
            <circle cx="200" cy="200" r="5" fill="#e94560"/>
            <text x="260" y="190" fill="#e94560" font-size="14">Radius (r)</text>
            <text x="200" y="220" text-anchor="middle" fill="#0f3460" font-size="14">Center</text>
        </svg>'''
        description = "Circle: All points equidistant from center. Area = πr², Circumference = 2πr"
    
    elif shape_type == "square":
        svg = '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="400" fill="#f8f9fa"/>
            <rect x="100" y="100" width="200" height="200" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/>
            <line x1="100" y1="100" x2="300" y2="100" stroke="#e94560" stroke-width="2" marker-end="url(#arrow)"/>
            <text x="200" y="90" text-anchor="middle" fill="#e94560" font-size="14">Side</text>
            <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3z" fill="#e94560"/></marker></defs>
        </svg>'''
        description = "Square: All sides equal, all angles = 90°. Area = s², Perimeter = 4s"
    
    elif shape_type == "triangle":
        svg = '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="400" fill="#f8f9fa"/>
            <polygon points="80,300 300,300 80,100" fill="rgba(15,52,96,0.1)" stroke="#0f3460" stroke-width="3"/>
            <polygon points="80,280 100,280 100,300" fill="none" stroke="#e94560" stroke-width="2"/>
            <text x="90" y="295" text-anchor="middle" fill="#e94560" font-size="14">90°</text>
            <text x="190" y="320" text-anchor="middle" fill="#0f3460" font-size="14">Base</text>
            <text x="65" y="200" text-anchor="middle" fill="#0f3460" font-size="14" transform="rotate(-90 65 200)">Height</text>
        </svg>'''
        description = "Right Triangle: a² + b² = c² (Pythagorean Theorem)"
    
    else:
        return None
    
    return {"svg": svg, "description": description}