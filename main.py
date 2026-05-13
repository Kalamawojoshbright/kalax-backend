"""
KalaX Backend - Minimal Working Version
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Enable CORS
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

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/")
async def root():
    return {"status": "online", "service": "KalaX Backend"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ============================================
# CHAT ENDPOINT
# ============================================

@app.post("/learn/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Simple chat endpoint"""
    return ChatResponse(
        response=f"You said: {request.message}",
        source="test"
    )

# ============================================
# DRAW ENDPOINT
# ============================================

class DrawRequest(BaseModel):
    command: str

class DrawResponse(BaseModel):
    success: bool
    type: str
    svg: Optional[str] = None
    explanation: Optional[str] = None
    error: Optional[str] = None

@app.post("/draw", response_model=DrawResponse)
async def draw(request: DrawRequest):
    """Simple draw endpoint"""
    return DrawResponse(
        success=True,
        type="svg",
        svg='<svg width="200" height="200"><circle cx="100" cy="100" r="80" fill="blue"/></svg>',
        explanation=f"Drew: {request.command}"
    )

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)