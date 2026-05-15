@app.get("/test-gemini")
async def test_gemini():
    if not GEMINI_READY:
        return {"error": "Gemini not ready", "key_present": bool(os.getenv("GEMINI_API_KEY"))}
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content("Say 'Gemini is working'")
        return {"success": True, "response": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}