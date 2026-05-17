from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/plot")
async def plot_fixed():
    # Generate a simple parabola
    x = np.linspace(-5, 5, 200)
    y = x ** 2
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Test Graph (fixed)")
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return Response(content=buf.getvalue(), media_type="image/png")

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}