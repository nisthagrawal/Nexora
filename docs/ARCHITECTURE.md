# Nexora architecture

```text
file/PDF → ingestion → page image → preprocessing/quality → OCR → validation
                                                       ↘ MRZ/QR adapters
                                              forensic + face adapters
                                                         ↓
                      standardized ModuleResult → evidence/contradictions → risk → human review
```

`POST /screening` is the end-to-end local API. It accepts image/PDF input, renders PDF pages using PyMuPDF, measures actual image properties, runs the currently configured module adapters, and returns page-level evidence plus a redacted audit identifier. An adapter unavailable on the machine returns `UNAVAILABLE`; it never returns a manufactured passing result.

## Current capability status

| Capability | Status |
|---|---|
| image ingestion / PDF page rendering | real local implementation |
| image quality properties | real measured implementation |
| OCR | local Tesseract fallback; replace with PaddleOCR adapter |
| deterministic expiry / number checks | implemented for extracted fields |
| MRZ | validation layer is ready; PassportEye adapter is a planned replacement |
| QR/barcode | not connected |
| forensics / face | explicit replaceable adapters, not connected by default |
| evidence / contradictions / risk | implemented, prototype thresholds only |
