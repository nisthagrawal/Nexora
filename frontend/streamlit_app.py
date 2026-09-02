from pathlib import Path
import sys
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.pipeline import screen

st.set_page_config(page_title="Nexora Screening", page_icon="🛂", layout="wide")
st.title("NEXORA SCREENING")
st.caption("Evidence-aware identity-document screening • Human review remains the final decision")

with st.sidebar:
    st.header("Case input")
    document_type = st.selectbox("Document type", ["Passport", "National ID", "Visa", "Permit", "Driving licence"])
    document = st.file_uploader("Document image", type=["png", "jpg", "jpeg"])
    person = st.file_uploader("Presented-person image (optional)", type=["png", "jpg", "jpeg"])
    run = st.button("Screen document", type="primary", disabled=document is None)

if run and document:
    with st.spinner("Collecting and reconciling evidence…"):
        report = screen(document.getvalue(), person.getvalue() if person else None, document_type)
    risk = report.risk
    emoji = {"LOW RISK": "🟢", "REVIEW REQUIRED": "🟠", "HIGH RISK": "🔴"}[risk.outcome.value]
    left, mid, right = st.columns(3)
    left.metric("Document", report.document_type)
    mid.metric("Status", f"{emoji} {risk.outcome.value}")
    right.metric("Risk", f"{risk.score}/100")
    st.warning("This result is decision support, not an automated clearance or refusal.")
    st.subheader("Evidence summary")
    for result in report.module_results:
        icon = "✅" if result.status in {"PASS", "COMPLETE"} else "⚠️"
        with st.expander(f"{icon} {result.module_name.upper()} — {result.status}", expanded=True):
            st.write(result.explanation)
            if result.evidence:
                st.dataframe([item.model_dump(exclude_none=True) for item in result.evidence], use_container_width=True, hide_index=True)
    st.subheader("Contradictions")
    if report.contradictions:
        for item in report.contradictions: st.error(item.explanation)
    else: st.success("No conflicting structured claims were detected.")
    st.subheader("Risk rationale")
    for reason in risk.reasons: st.write(f"• {reason}")
    st.caption(f"Recommended action: {risk.recommended_action}")
    with st.expander("Configurable score breakdown"):
        st.json(risk.score_breakdown)
else:
    st.info("Upload a document image to begin. The Phase 1 forgery and face adapters intentionally report their availability until real models are configured.")
