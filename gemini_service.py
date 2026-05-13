"""
Gemini Service - Secure API Wrapper
Uses environment variable for API key
"""

import os
import google.generativeai as genai

# Get API key from environment variable (SECURE)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"

def ask_gemini(prompt: str) -> str:
    """Send prompt to Gemini and return response"""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return None

def generate_drawing_code(command: str) -> dict:
    """Generate drawing code using Gemini"""
    prompt = f"""Generate JavaScript drawing code for: "{command}"

Return ONLY valid JSON. Format:
{{"code": "function draw(ctx, canvas) {{ ... }}", "explanation": "description"}}

Canvas: 700x500. Use ctx.fillStyle, ctx.strokeStyle, ctx.beginPath().
Make it educational and accurate.

Generate NOW:"""
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        
        import json, re
        match = re.search(r'\{[\s\S]*\}', response.text)
        if match:
            return json.loads(match.group())
    except:
        pass
    
    return None