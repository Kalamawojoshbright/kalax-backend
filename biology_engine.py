"""
Biology Engine - Serves pre-made educational SVG diagrams
NO hardcoded SVG paths - uses asset files
"""

import os
from pathlib import Path

# Path to biology assets
ASSETS_DIR = Path(__file__).parent.parent / "assets" / "biology"

def get_biology_diagram(diagram_type: str) -> dict:
    """
    Return biology diagram SVG and description
    Uses actual SVG files, not hardcoded paths
    """
    
    diagrams = {
        "skeleton": {
            "file": "skeleton.svg",
            "description": "Human Skeleton - 206 bones. Axial skeleton (skull, spine, ribs) + Appendicular skeleton (limbs)"
        },
        "brain": {
            "file": "brain.svg",
            "description": "Human Brain - Cerebrum (left/right hemispheres), Cerebellum, Brain Stem"
        },
        "heart": {
            "file": "heart.svg",
            "description": "Human Heart - 4 chambers: Left/Right Atrium, Left/Right Ventricle"
        },
        "eye": {
            "file": "eye.svg",
            "description": "Human Eye - Cornea, Iris, Pupil, Lens, Retina, Optic Nerve"
        },
        "lungs": {
            "file": "lungs.svg",
            "description": "Respiratory System - Trachea, Bronchi, Lungs, Diaphragm"
        }
    }
    
    if diagram_type not in diagrams:
        return None
    
    info = diagrams[diagram_type]
    svg_path = ASSETS_DIR / info["file"]
    
    if not svg_path.exists():
        # Fallback: return None (frontend will show message)
        return None
    
    with open(svg_path, 'r') as f:
        svg_content = f.read()
    
    return {
        "svg": svg_content,
        "description": info["description"]
    }