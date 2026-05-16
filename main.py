import numpy as np
import matplotlib
matplotlib.use('Agg')  # non‑interactive backend
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re
from fastapi.responses import JSONResponse, Response

# Ensure textbook style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 14,
    'axes.linewidth': 1.5,
    'xtick.major.width': 1.5,
    'ytick.major.width': 1.5,
    'grid.linewidth': 0.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'figure.figsize': (8, 6)
})

def safe_eval_expression(expr: str, x: np.ndarray):
    """Safely evaluate math expression using numpy."""
    # Replace ^ with **
    expr = expr.replace('^', '**')
    # Allow only math functions and x
    allowed_names = {
        'x': x,
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'log': np.log, 'log10': np.log10,
        'sqrt': np.sqrt, 'abs': np.abs
    }
    # Using eval is safe because we control the namespace
    return eval(expr, {"__builtins__": {}}, allowed_names)

@app.post("/plot")
async def plot_expression(request: dict):
    expr = request.get("expression", "").strip()
    if not expr:
        return JSONResponse(status_code=400, content={"error": "No expression"})

    # Determine domain
    x_min, x_max = -8, 8
    if any(func in expr for func in ['sin', 'cos', 'tan']):
        x_min, x_max = -2*np.pi, 2*np.pi
    elif 'log' in expr:
        x_min, x_max = 0.1, 8

    x = np.linspace(x_min, x_max, 1000)
    try:
        y = safe_eval_expression(expr, x)
        # Mask inf/nan
        y = np.ma.masked_invalid(y)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Invalid expression: {e}"})

    # Create textbook-style plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, 'b-', linewidth=2.5, label=f'y = {expr}')

    # Axes with arrows
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)

    # Grid (square style)
    ax.grid(True, which='major', linestyle='-', linewidth=0.5, color='gray', alpha=0.7)
    ax.grid(True, which='minor', linestyle=':', linewidth=0.3, color='gray', alpha=0.5)
    ax.minorticks_on()

    # Labels & title
    ax.set_xlabel('x', fontsize=14, labelpad=10)
    ax.set_ylabel('y', fontsize=14, labelpad=10)
    ax.set_title(f'Graph of y = {expr}', fontsize=16, fontweight='bold', pad=20)

    # Mark intercepts
    # x‑intercepts (where y changes sign)
    x_roots = []
    for i in range(len(x)-1):
        if y[i]*y[i+1] < 0:
            x_root = x[i] - y[i]*(x[i+1]-x[i])/(y[i+1]-y[i])
            x_roots.append(x_root)
    for xr in x_roots:
        ax.plot(xr, 0, 'ro', markersize=6)
        ax.annotate(f'({xr:.2f},0)', (xr, 0), xytext=(5, 5), textcoords='offset points', fontsize=10)

    # y‑intercept (x=0)
    if np.any(np.abs(x) < 0.01):
        idx = np.argmin(np.abs(x))
        y0 = y[idx]
        if not np.isnan(y0):
            ax.plot(0, y0, 'ro', markersize=6)
            ax.annotate(f'(0,{y0:.2f})', (0, y0), xytext=(5, 5), textcoords='offset points', fontsize=10)

    # Legend
    ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)

    # Tight layout to avoid clipping
    fig.tight_layout()

    # Convert to PNG
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
    buf.seek(0)
    plt.close(fig)

    return Response(content=buf.getvalue(), media_type="image/png")