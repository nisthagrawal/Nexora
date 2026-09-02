# Nexora

An evidence-aware, human-in-the-loop prototype for identity-document screening. Nexora reconciles outputs from replaceable OCR, validation, forensic, and biometric modules; it does **not** claim that an unconfigured model has performed an analysis.

## Current prototype

- interactive evidence UI at `demo/index.html`, including controlled-demo cases and Dataset & Research Mode
- FastAPI `POST /screening` endpoint for real image/PDF ingestion, PDF page rendering, measured quality evidence and a hash-addressed screening response
- OpenCV denoise/contrast preprocessing; OCR adapter with a PaddleOCR-ready boundary
- deterministic validation for expiry and document-number format
- common `ModuleResult` / `Evidence` schema
- evidence layer that detects conflicting field claims
- configurable risk engine with Low Risk / Review Required / High Risk outcomes
- explicit unavailable states for forensic and face-verification model adapters

## Run locally

```powershell
cd C:\Users\nisth\Documents\Codex\2026-08-31\files-pasted-by-the-user-sure\outputs\nexora
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.api.main:app --reload
```

Then open `demo/index.html` in a browser. Real uploads are sent to `http://127.0.0.1:8000/screening`; controlled synthetic cases remain labelled as demo evidence.

Optional Streamlit interface:

```powershell
streamlit run frontend\streamlit_app.py
```

Run checks with `pytest` (install it separately if desired). The OCR adapter uses `pytesseract`; for actual local extraction it also needs the system Tesseract executable. Replace `modules/ocr/adapter.py` with PaddleOCR for the recommended production-oriented adapter.

## Integration points

- `modules/forgery/adapter.py`: return fake probability, attack type, and suspicious regions from a trained forensic model.
- `modules/face/adapter.py`: return ArcFace/AdaFace similarity and match/non-match evidence.
- `modules/ocr/adapter.py`: emit field values, confidence, and bounding boxes from PaddleOCR/document parsing.
- `app/risk/engine.py`: calibrate configuration from held-out validation data; current defaults are transparent prototype settings, not scientific fraud probabilities.

## Documentation

- `docs/ARCHITECTURE.md` — local end-to-end pipeline and current capability boundaries
- `docs/DEMO_GUIDE.md` — mentor demonstration flow
- `docs/LIMITATIONS.md` — important accuracy, privacy and security limitations
- `docs/OPEN_SOURCE_USAGE.md` — intended open-source/research integrations and licence caution
- `datasets/README.md` — purpose-specific dataset registry; datasets are not bundled
