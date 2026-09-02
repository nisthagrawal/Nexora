# Demo and production scope

## Reliable live demo

Open `demo/index.html` locally and select **Run clean passport sample** or **Run altered-DOB sample**. Both use synthetic data. The second shows a realistic error pattern: a date changes while the original MRZ check digit remains, producing explainable High Risk evidence.

## Production roadmap

1. Replace regex/Tesseract adapter with PaddleOCR plus document-template parsers and bounding boxes.
2. Implement ICAO MRZ formats appropriate to supported documents, then configurable country rules.
3. Add model-serving adapters for forgery localisation and ArcFace/AdaFace-style face match; report calibration, confidence and model version.
4. Add signed government/issuer database adapters only with governing-agency approval.
5. Complete DPIA, security assessment, bias/error evaluation and human-review operating procedure before any real deployment.

## Research credit

MIDV-2020 informs document understanding evaluation; SIDTD and FakeIDet datasets inform forensic evaluation; DocFace+ informs document-to-selfie matching. Cite the papers/datasets and their licences. Do not imply that their code, weights or government data are bundled unless each asset's licence and permission explicitly allows it.
