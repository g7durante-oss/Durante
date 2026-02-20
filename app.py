from pathlib import Path
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Whisper Mobile Transcriber")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
async def home() -> str:
    index_file = STATIC_DIR / "index.html"
    return index_file.read_text(encoding="utf-8")


@app.post("/api/transcribe")
async def transcribe(file: UploadFile = File(...)) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Envie um arquivo de áudio válido.")

    suffix = Path(file.filename).suffix or ".mp3"
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(await file.read())
            temp_path = Path(temp_file.name)

        import whisper

        model = whisper.load_model("base")
        result = model.transcribe(str(temp_path), language="pt")
        text = (result.get("text") or "").strip()

        if not text:
            raise HTTPException(status_code=422, detail="Não foi possível extrair texto do áudio.")

        return {"text": text}
    finally:
        if 'temp_path' in locals() and temp_path.exists():
            temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
