"""
Router Service - Classifies and routes requests to correct engine
"""

def classify_request(prompt: str) -> str:
    """Determine what type of request this is"""
    p = prompt.lower()
    
    # Graph requests
    if any(word in p for word in ['plot', 'graph', 'y =', 'function']):
        return "graph"
    
    # Geometry requests
    if any(word in p for word in ['triangle', 'circle', 'square', 'rectangle', 'angle']):
        return "geometry"
    
    # Biology requests
    if any(word in p for word in ['skeleton', 'brain', 'heart', 'eye', 'lung', 'cell']):
        return "biology"
    
    # Physics requests
    if any(word in p for word in ['circuit', 'newton', 'motion', 'force', 'electricity']):
        return "physics"
    
    # Default to Gemini AI
    return "gemini"

def get_biology_type(prompt: str) -> str:
    """Extract specific biology diagram type"""
    p = prompt.lower()
    
    if "skeleton" in p:
        return "skeleton"
    if "brain" in p:
        return "brain"
    if "heart" in p:
        return "heart"
    if "eye" in p:
        return "eye"
    if "lung" in p:
        return "lungs"
    
    return None

def get_geometry_type(prompt: str) -> str:
    """Extract specific geometry shape"""
    p = prompt.lower()
    
    if "circle" in p:
        return "circle"
    if "square" in p:
        return "square"
    if "triangle" in p:
        return "triangle"
    if "rectangle" in p:
        return "rectangle"
    
    return None