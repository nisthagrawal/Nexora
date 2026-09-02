# Dataset integration registry

Nexora does **not** bundle document or biometric datasets. They may include personal data and often require accepted licences. Keep authorised copies locally and out of Git.

| Dataset | Module | Local folder | Evaluation |
|---|---|---|---|
| MIDV-2020 | OCR/layout | `datasets/midv/` | field accuracy, detection IoU |
| SIDTD | digital forgery | `datasets/sidtd/` | precision, recall, F1, ROC-AUC |
| FMIDV | manipulation localisation | `datasets/fmidv/` | IoU, pixel F1 |
| FakeIDet2-db | physical/unseen attacks | `datasets/fakeidet2/` | precision, recall, F1, ROC-AUC |
| FakeIDet3-DB | modern/GenAI attacks | `datasets/fakeidet3/` | precision, recall, F1, ROC-AUC |
| ID-selfie data | face verification | `datasets/id_selfie/` | EER, ROC-AUC |

Do not merge these into one training dataset. Record source, version, licence, split, model version and metrics for each experiment.
