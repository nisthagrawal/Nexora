# Mentor demonstration flow

1. Start the API and open `demo/index.html`.
2. Run **Clean passport**: inspect field evidence, MRZ pass, low-risk reason and audit hash.
3. Run **Altered DOB**: click the DOB contradiction to highlight its visual region; explain that it is `SIMULATED DEMO EVIDENCE` from a controlled synthetic case.
4. Run **Poor image**: show that Nexora requests better evidence rather than calling it fraudulent.
5. Upload an image or PDF. Start screening with the API running; show real file hash, PDF-page ingestion (where applicable), measured quality, and actual adapter results/unavailability.
6. Open Dataset & Research Mode to explain separate dataset use and metrics.
7. Record an officer decision; explain that the audit event should contain hashes and structured evidence, not raw PII.
