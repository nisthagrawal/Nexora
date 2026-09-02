from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.models import ScreeningReport
from app.pipeline import screen
from app.pipeline.orchestrator import run_screening

app = FastAPI(title="Nexora Screening API", version="0.1.0", description="Evidence-aware identity-document screening prototype.")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/screen", response_model=ScreeningReport)
async def create_screening(document: UploadFile = File(...), person_image: UploadFile | None = File(None), document_type: str = Form("Identity document")) -> ScreeningReport:
    if not document.content_type or not document.content_type.startswith("image/"):
        raise HTTPException(415, "Document must be an image.")
    return screen(await document.read(), await person_image.read() if person_image else None, document_type)


@app.post("/screening")
async def create_full_screening(document: UploadFile = File(...), person_image: UploadFile | None = File(None)) -> dict:
    if not document.filename:
        raise HTTPException(400, "A document file is required.")
    try:
        return run_screening(await document.read(), document.filename, document.content_type, await person_image.read() if person_image else None)
    except ValueError as error:
        raise HTTPException(415, str(error)) from error
