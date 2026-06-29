import streamlit as st

import database as db
from ui.ui_utils import (topbar, go)
from config import (SUPPORTED_TYPES, MAX_UPLOAD_MB, REVIEWER_ROLES)
from utils.file_handler import extract_text
from pipeline import run_pipeline
import state

# =========================================================================== #
#  PAGE: Upload
# =========================================================================== #
def page_upload():
    ss = state.get_state()
    topbar("Upload RFP Document", "Upload your RFP document and let AI analyze it for you.", "☁️")
    up = st.file_uploader("Drag & drop your file here", type=SUPPORTED_TYPES,
                          label_visibility="collapsed")
    st.caption(f"Supported formats: {', '.join(t.upper() for t in SUPPORTED_TYPES)}  ·  "
               f"Max file size: {MAX_UPLOAD_MB}MB")

    with st.expander("Deal details (optional) — set client, region, deadline & reviewer", expanded=bool(up)):
        c1, c2 = st.columns(2)
        deal = c1.text_input("Deal / Project name", placeholder="e.g. Acme Cloud Migration RFP")
        client = c2.text_input("Client name", placeholder="e.g. Acme Corp")
        c3, c4, c5 = st.columns(3)
        region = c3.text_input("Region", placeholder="e.g. North America")
        deadline = c4.text_input("Deadline", placeholder="e.g. 2026-08-15")
        role = c5.selectbox("Assign reviewer role", REVIEWER_ROLES)
        use_web = st.checkbox("Use live web search / pricing (Agent 2)", value=True)

    if up and st.button("⚡ Analyze & Generate Response", type="primary", use_container_width=True):
        try:
            raw = extract_text(up.name, up.getvalue())
        except Exception as e:
            st.error(f"Could not read that file: {e}"); return
        if len(raw.strip()) < 30:
            st.error("That file has almost no readable text."); return
        rid = db.create_rfp(deal or up.name, client, region, deadline, "", "",
                            up.name, raw, role, "", use_web)
        bar = st.progress(0.0, text="Starting…")
        
        run_pipeline(rid, raw, use_web, progress=lambda lab, f: bar.progress(f, text=lab))
        bar.empty()
        st.success("✅ Analysis complete. Opening Dashboard…")
        go("Dashboard", rid)

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("<div class='card'><h3>📄 Upload Guidelines</h3>"
                    "<div class='muted' style='line-height:2'>"
                    "✅ Ensure the document is clear and readable<br>"
                    "✅ All pages should be included<br>"
                    f"✅ Supported formats: {', '.join(t.upper() for t in SUPPORTED_TYPES)}<br>"
                    f"✅ Maximum file size: {MAX_UPLOAD_MB}MB</div></div>", unsafe_allow_html=True)
    with g2:
        rows = ""
        for r in db.list_rfps()[:4]:
            rows += (f"<div class='feed'><div class='fi ic-red'>📕</div><div style='flex:1'>"
                     f"<div class='ft'>{r['file_name'] or r['deal_name']}</div>"
                     f"<div class='fd'>{(r.get('updated_at') or '')[:10]}</div></div></div>")
        st.markdown(f"<div class='card'><h3>🗂️ Recent Uploads</h3>{rows or '<div class=muted>No uploads yet.</div>'}</div>",
                    unsafe_allow_html=True)
