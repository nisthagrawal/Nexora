from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from app.models import ScreeningReport
from app.pipeline import screen

app = FastAPI(title="Nexora Screening API", version="0.1.0", description="Evidence-aware identity-document screening prototype.")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/screen", response_model=ScreeningReport)
async def create_screening(document: UploadFile = File(...), person_image: UploadFile | None = File(None), document_type: str = Form("Identity document")) -> ScreeningReport:
    if not document.content_type or not document.content_type.startswith("image/"):
        raise HTTPException(415, "Document must be an image.")
    return screen(await document.read(), await person_image.read() if person_image else None, document_type)
