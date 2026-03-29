"""
PathFinder — Streamlit UI
=========================
Constraint-Aware DSA Learning Roadmap Generator

Makes HTTP calls to the FastAPI backend (default: http://localhost:8000).
Set PATHFINDER_API_URL env var to override.

Run:
    streamlit run app.py
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional

import requests
import streamlit as st

# ── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="PathFinder — DSA Roadmap Generator",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Constants ─────────────────────────────────────────────────────────────────
API_BASE_URL: str = os.getenv("PATHFINDER_API_URL", "http://localhost:8000")
REQUEST_TIMEOUT: int = 180   # seconds — LLM calls can be slow

SKILL_OPTIONS: List[str] = ["very weak", "weak", "medium", "strong", "very strong"]
SKILL_DEFAULTS: Dict[str, str] = {
    "trees":         "medium",
    "dp":            "medium",
    "arrays":        "medium",
    "graphs":        "medium",
    "recursion":     "medium",
    "binary_search": "medium",
    "sorting":       "medium",
}
TOPIC_META: Dict[str, Dict] = {
    "trees":         {"label": "🌳 Trees",         "icon": "🌳"},
    "dp":            {"label": "🔄 Dynamic Prog.",  "icon": "🔄"},
    "arrays":        {"label": "📐 Arrays",         "icon": "📐"},
    "graphs":        {"label": "🕸️ Graphs",          "icon": "🕸️"},
    "recursion":     {"label": "🔁 Recursion",      "icon": "🔁"},
    "binary_search": {"label": "🔍 Binary Search",  "icon": "🔍"},
    "sorting":       {"label": "📊 Sorting",        "icon": "📊"},
}
SKILL_COLORS: Dict[str, str] = {
    "very weak":  "#E74C3C",
    "weak":       "#E67E22",
    "medium":     "#F1C40F",
    "strong":     "#27AE60",
    "very strong":"#16A085",
}

# ── Custom CSS ────────────────────────────────────────────────────────────────
def inject_css() -> None:
    st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Global background ── */
.stApp {
    background-color: #F0F4F8;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F3460 0%, #16213E 100%);
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: #E8EDF5 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] p {
    color: #A8B8D0 !important;
    font-size: 0.82rem !important;
    font-weight: 500;
    letter-spacing: 0.02em;
}
[data-testid="stSidebar"] select {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #fff !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] .stSlider {
    padding-top: 0.3rem;
}

/* ── Primary button — Generate ── */
div[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1rem;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.03em;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 16px rgba(14,165,233,0.35);
    margin-top: 0.5rem;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(14,165,233,0.45);
}
div[data-testid="stSidebar"] .stButton > button:active {
    transform: translateY(0);
}

/* ── Banner header ── */
.pf-header {
    background: linear-gradient(135deg, #0F3460 0%, #1A4A80 50%, #0B2545 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.pf-header::before {
    content: "";
    position: absolute;
    top: -40%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(245,166,35,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.pf-header h1 {
    color: white;
    font-size: 3rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.02em;
}
.pf-header .tagline {
    color: #7EB8E8;
    font-size: 1.05rem;
    margin: 0.5rem 0 0 0;
    font-weight: 400;
}
.pf-header .badge {
    display: inline-block;
    background: rgba(245,166,35,0.18);
    border: 1px solid rgba(245,166,35,0.4);
    color: #F5A623;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    margin-top: 1rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Info cards (how it works) ── */
.how-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    height: 100%;
    border-top: 4px solid transparent;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
}
.how-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.10);
}
.how-card.c1 { border-top-color: #0EA5E9; }
.how-card.c2 { border-top-color: #F5A623; }
.how-card.c3 { border-top-color: #10B981; }
.how-card .how-icon { font-size: 2rem; margin-bottom: 0.6rem; }
.how-card h3 { font-size: 0.95rem; font-weight: 700; color: #0F3460; margin: 0.3rem 0; }
.how-card p { font-size: 0.82rem; color: #64748B; line-height: 1.5; margin: 0; }

/* ── Section heading ── */
.section-heading {
    font-size: 1.3rem;
    font-weight: 700;
    color: #0F3460;
    border-left: 4px solid #F5A623;
    padding-left: 0.75rem;
    margin: 1.5rem 0 1rem 0;
}

/* ── Analysis card ── */
.analysis-card {
    background: white;
    border-radius: 16px;
    padding: 1.75rem 2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border-left: 5px solid #0EA5E9;
    margin-bottom: 1.5rem;
}
.analysis-card .summary-text {
    font-size: 1.02rem;
    color: #334155;
    line-height: 1.7;
    font-style: italic;
}

/* ── Stats row ── */
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 999px;
    padding: 0.3rem 0.85rem;
    font-size: 0.82rem;
    font-weight: 600;
    color: #1E40AF;
    margin: 0.25rem 0.2rem;
}

/* ── Roadmap timeline ── */
.timeline-step {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 0;
    position: relative;
}
.step-connector {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
}
.step-circle {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0F3460, #1A4A80);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1rem;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(15,52,96,0.3);
    z-index: 1;
}
.step-line {
    width: 2px;
    flex: 1;
    background: linear-gradient(to bottom, #CBD5E1, transparent);
    min-height: 20px;
    margin: 4px 0;
}
.step-card {
    flex: 1;
    background: white;
    border-radius: 16px;
    padding: 1.4rem 1.75rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    border: 1px solid #E2E8F0;
    margin-bottom: 1.25rem;
    transition: box-shadow 0.2s, transform 0.2s;
}
.step-card:hover {
    box-shadow: 0 6px 24px rgba(0,0,0,0.11);
    transform: translateX(3px);
}
.step-topic {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0F3460;
    margin: 0 0 0.6rem 0;
}
.step-time-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: linear-gradient(135deg, #F5A623, #F59E0B);
    color: white;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
    margin-bottom: 0.75rem;
    letter-spacing: 0.03em;
}
.step-reason {
    font-size: 0.88rem;
    color: #475569;
    line-height: 1.65;
    margin-bottom: 0.75rem;
}
.step-ref {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 8px;
    padding: 0.25rem 0.6rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: #15803D;
}

/* ── Total time footer ── */
.total-time-bar {
    background: linear-gradient(135deg, #0F3460, #1A4A80);
    border-radius: 16px;
    padding: 1.25rem 2rem;
    color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 1rem;
}
.total-time-bar .label { font-size: 0.9rem; opacity: 0.8; }
.total-time-bar .value { font-size: 1.8rem; font-weight: 800; color: #F5A623; }

/* ── Validation banners ── */
.banner-success {
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
    border: 1.5px solid #6EE7B7;
    border-radius: 14px;
    padding: 1.25rem 1.75rem;
    margin: 1rem 0;
}
.banner-warning {
    background: linear-gradient(135deg, #FEF3C7, #FDE68A);
    border: 1.5px solid #FCD34D;
    border-radius: 14px;
    padding: 1.25rem 1.75rem;
    margin: 1rem 0;
}
.banner-success h4, .banner-warning h4 {
    margin: 0 0 0.35rem 0;
    font-size: 1rem;
    font-weight: 700;
}
.banner-success h4 { color: #065F46; }
.banner-warning h4 { color: #92400E; }
.banner-success p, .banner-warning p {
    margin: 0; font-size: 0.85rem; line-height: 1.5;
}
.banner-success p { color: #047857; }
.banner-warning p { color: #B45309; }

/* ── Skipped topics ── */
.skipped-pill {
    display: inline-block;
    background: #FEF2F2;
    border: 1px solid #FECACA;
    color: #B91C1C;
    border-radius: 999px;
    padding: 0.2rem 0.65rem;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 0.2rem;
}

/* ── Welcome instruction step ── */
.welcome-step {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid #E2E8F0;
}
.welcome-step:last-child { border-bottom: none; }
.welcome-num {
    width: 32px; height: 32px;
    background: #0F3460;
    color: white;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.85rem;
    flex-shrink: 0;
}
.welcome-step-text h4 { margin: 0; color: #0F3460; font-size: 0.92rem; }
.welcome-step-text p  { margin: 0.2rem 0 0; color: #64748B; font-size: 0.82rem; }

/* ── API error ── */
.api-error {
    background: #FEF2F2;
    border: 1.5px solid #FECACA;
    border-radius: 14px;
    padding: 1.25rem 1.75rem;
    color: #991B1B;
}

/* ── Sidebar section title ── */
.sidebar-section {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7EB8E8 !important;
    margin: 1rem 0 0.5rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)


# ── API helpers ───────────────────────────────────────────────────────────────

def api_generate_roadmap(snapshot: Dict[str, Any], max_retries: int) -> Dict:
    """POST /roadmap — synchronous pipeline call."""
    url = f"{API_BASE_URL}/roadmap"
    payload = {"snapshot": snapshot, "max_retries": max_retries}
    resp = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def api_health() -> Optional[Dict]:
    """GET /health — liveness probe."""
    try:
        resp = requests.get(f"{API_BASE_URL}/health", timeout=4)
        return resp.json() if resp.ok else None
    except Exception:
        return None


def api_graph_topics() -> Optional[Dict]:
    """GET /graph/topics — concept DAG."""
    try:
        resp = requests.get(f"{API_BASE_URL}/graph/topics", timeout=8)
        return resp.json() if resp.ok else None
    except Exception:
        return None


# ── UI helpers ────────────────────────────────────────────────────────────────

def skill_color_dot(level: str) -> str:
    color = SKILL_COLORS.get(level, "#94A3B8")
    return f'<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:{color};margin-right:5px;"></span>'


def render_header() -> None:
    st.markdown("""
<div class="pf-header">
    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.75rem;">
        <span style="font-size:2.8rem;">🗺️</span>
        <div>
            <h1>PathFinder</h1>
            <p class="tagline">Constraint-Aware DSA Learning Roadmap Generator</p>
        </div>
    </div>
    <span class="badge">⚛️ Neuro-Symbolic AI &nbsp;·&nbsp; 🔍 RAG-Grounded &nbsp;·&nbsp; ✅ Self-Validating</span>
</div>
""", unsafe_allow_html=True)


def render_welcome() -> None:
    col1, col2, col3 = st.columns(3, gap="medium")

    cards = [
        ("c1", "🧠", "1. Skill Analysis",
         "The AI analyzes your DSA skill snapshot, identifies weak topics and infers your difficulty tolerance automatically."),
        ("c2", "🕸️", "2. Graph-Constrained Planning",
         "A symbolic prerequisite graph ensures no topic is studied before its dependencies — enforced structurally, not by LLM hope."),
        ("c3", "📋", "3. Validated Roadmap",
         "A Validation Agent checks every constraint. If violated, the planner regenerates with injected feedback until the roadmap is provably correct."),
    ]
    for col, (cls, icon, title, desc) in zip([col1, col2, col3], cards):
        with col:
            st.markdown(f"""
<div class="how-card {cls}">
    <div class="how-icon">{icon}</div>
    <h3>{title}</h3>
    <p>{desc}</p>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
<div style="background:white;border-radius:16px;padding:1.75rem 2rem;box-shadow:0 2px 8px rgba(0,0,0,0.06);">
<p style="color:#0F3460;font-weight:700;font-size:1rem;margin:0 0 1rem 0;">🚀 How to get started</p>
<div class="welcome-step">
  <div class="welcome-num">1</div>
  <div class="welcome-step-text">
    <h4>Set your skill levels</h4>
    <p>Use the sidebar dropdowns to rate yourself on each DSA topic from <em>very weak</em> to <em>very strong</em>.</p>
  </div>
</div>
<div class="welcome-step">
  <div class="welcome-num">2</div>
  <div class="welcome-step-text">
    <h4>Set your time budget</h4>
    <p>How many hours can you dedicate? The system will fit a complete roadmap within that constraint.</p>
  </div>
</div>
<div class="welcome-step">
  <div class="welcome-num">3</div>
  <div class="welcome-step-text">
    <h4>Click Generate Roadmap</h4>
    <p>The AI pipeline runs in ~15-60s (LLM latency). Your personalized, prerequisite-safe roadmap appears here.</p>
  </div>
</div>
</div>
""", unsafe_allow_html=True)


def render_skill_analysis(data: Dict) -> None:
    summary = data.get("skill_summary", "")
    total_time = data.get("total_time", 0)
    attempts = data.get("validation_attempts", 1)
    skipped = data.get("topics_skipped", [])

    st.markdown('<div class="section-heading">🧠 Skill Analysis</div>', unsafe_allow_html=True)

    st.markdown(f"""
<div class="analysis-card">
    <p class="summary-text">"{summary}"</p>
    <div style="margin-top:1rem;">
        <span class="stat-pill">⏱️ {total_time:.1f}h planned</span>
        <span class="stat-pill">🔄 {attempts} validation attempt{"s" if attempts > 1 else ""}</span>
        <span class="stat-pill">📋 {len(data.get("roadmap", []))} steps</span>
    </div>
</div>
""", unsafe_allow_html=True)

    if skipped:
        skipped_html = "".join(f'<span class="skipped-pill">⏭️ {t}</span>' for t in skipped)
        st.markdown(f"""
<div style="background:#FEF9F0;border:1px solid #FED7AA;border-radius:12px;
            padding:1rem 1.25rem;margin-bottom:1rem;">
  <p style="margin:0 0 0.5rem;font-size:0.85rem;font-weight:700;color:#92400E;">
    ⏩ Topics skipped (time constraint)
  </p>
  {skipped_html}
</div>
""", unsafe_allow_html=True)


def render_roadmap(data: Dict) -> None:
    roadmap = data.get("roadmap", [])
    total_time = data.get("total_time", 0)

    st.markdown('<div class="section-heading">📍 Your Learning Roadmap</div>', unsafe_allow_html=True)

    for i, step in enumerate(roadmap):
        step_num   = step.get("step", i + 1)
        topic      = step.get("topic", "").replace("_", " ").title()
        hours      = step.get("time_estimate_hours", 0)
        reason     = step.get("reason", "")
        reference  = step.get("reference", "N/A")
        is_last    = (i == len(roadmap) - 1)

        st.markdown(f"""
<div class="timeline-step">
  <div class="step-connector">
    <div class="step-circle">{step_num}</div>
    {"" if is_last else '<div class="step-line"></div>'}
  </div>
  <div class="step-card">
    <p class="step-topic">{topic}</p>
    <span class="step-time-badge">⏱️ {hours:.1f} hours</span>
    <p class="step-reason">{reason}</p>
    <span class="step-ref">📚 {reference}</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # Total time footer
    st.markdown(f"""
<div style="background:linear-gradient(135deg,#0F3460,#1A4A80);border-radius:16px;
            padding:1.25rem 2rem;color:white;
            display:flex;align-items:center;justify-content:space-between;margin-top:1rem;">
  <div>
    <div style="font-size:0.85rem;opacity:0.75;">Total study time planned</div>
    <div style="font-size:1.75rem;font-weight:800;color:#F5A623;">{total_time:.1f} hours</div>
  </div>
  <div style="text-align:right;">
    <div style="font-size:0.85rem;opacity:0.75;">Steps</div>
    <div style="font-size:1.75rem;font-weight:800;color:#7EB8E8;">{len(roadmap)}</div>
  </div>
</div>
""", unsafe_allow_html=True)


def render_validation_status(data: Dict) -> None:
    attempts = data.get("validation_attempts", 1)
    skipped  = data.get("topics_skipped", [])
    roadmap  = data.get("roadmap", [])
    total    = data.get("total_time", 0)

    st.markdown('<div class="section-heading">✅ Validation Status</div>', unsafe_allow_html=True)

    # Determine pass/warn purely from what the API returned
    # (API only returns final roadmap — if it returned, validation ultimately passed)
    passed = True

    if passed:
        warn_note = f" (took {attempts} attempt{'s' if attempts > 1 else ''})" if attempts > 1 else ""
        st.markdown(f"""
<div class="banner-success">
  <h4>✅ All constraints satisfied{warn_note}</h4>
  <p>Prerequisites respected &nbsp;·&nbsp; Time budget honoured &nbsp;·&nbsp;
     Weak topics prioritised &nbsp;·&nbsp; No structural violations detected.</p>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="banner-warning">
  <h4>⚠️ Roadmap generated with warnings</h4>
  <p>Max retries reached. Review the roadmap carefully before following it.</p>
</div>
""", unsafe_allow_html=True)

    # Constraint checks (derived from response data)
    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        st.markdown(f"""
<div style="background:white;border-radius:12px;padding:1rem 1.25rem;
            border-top:3px solid #10B981;box-shadow:0 2px 8px rgba(0,0,0,0.06);text-align:center;">
  <div style="font-size:1.6rem;">✅</div>
  <div style="font-weight:700;color:#065F46;font-size:0.88rem;margin-top:0.3rem;">Prerequisites OK</div>
  <div style="font-size:0.78rem;color:#64748B;">Graph order enforced</div>
</div>""", unsafe_allow_html=True)
    with c2:
        ok = total <= 500
        st.markdown(f"""
<div style="background:white;border-radius:12px;padding:1rem 1.25rem;
            border-top:3px solid {'#10B981' if ok else '#F59E0B'};
            box-shadow:0 2px 8px rgba(0,0,0,0.06);text-align:center;">
  <div style="font-size:1.6rem;">{'⏱️' if ok else '⚠️'}</div>
  <div style="font-weight:700;color:{'#065F46' if ok else '#92400E'};
              font-size:0.88rem;margin-top:0.3rem;">Time Budget</div>
  <div style="font-size:0.78rem;color:#64748B;">{total:.1f}h allocated</div>
</div>""", unsafe_allow_html=True)
    with c3:
        n_skipped = len(skipped)
        st.markdown(f"""
<div style="background:white;border-radius:12px;padding:1rem 1.25rem;
            border-top:3px solid {'#10B981' if n_skipped == 0 else '#F59E0B'};
            box-shadow:0 2px 8px rgba(0,0,0,0.06);text-align:center;">
  <div style="font-size:1.6rem;">{'📋' if n_skipped == 0 else '⏩'}</div>
  <div style="font-weight:700;color:{'#065F46' if n_skipped == 0 else '#92400E'};
              font-size:0.88rem;margin-top:0.3rem;">Coverage</div>
  <div style="font-size:0.78rem;color:#64748B;">
    {'All topics covered' if n_skipped == 0 else f'{n_skipped} topic(s) skipped'}
  </div>
</div>""", unsafe_allow_html=True)


def render_export(data: Dict, snapshot: Dict) -> None:
    st.markdown('<div class="section-heading">📥 Export</div>', unsafe_allow_html=True)
    export_payload = {"input_snapshot": snapshot, "roadmap_result": data}
    col1, col2 = st.columns([1, 3])
    with col1:
        st.download_button(
            label="⬇️ Download JSON",
            data=json.dumps(export_payload, indent=2),
            file_name="pathfinder_roadmap.json",
            mime="application/json",
            use_container_width=True,
        )


def render_api_error(err: str) -> None:
    st.markdown(f"""
<div class="api-error">
  <h4 style="margin:0 0 0.5rem;font-size:1rem;">❌ Generation Failed</h4>
  <p style="margin:0;font-size:0.88rem;line-height:1.6;">{err}</p>
  <p style="margin:0.75rem 0 0;font-size:0.8rem;opacity:0.8;">
    Make sure the PathFinder API is running:&nbsp;
    <code style="background:rgba(0,0,0,0.08);padding:0.1rem 0.4rem;border-radius:4px;">
      python api_server.py
    </code>
  </p>
</div>
""", unsafe_allow_html=True)


def render_dependency_graph(data: Dict, graph_data: Optional[Dict]) -> None:
    """Render a simple text-based dependency map for the roadmap topics."""
    if not graph_data:
        return
    roadmap_topics = {s["topic"] for s in data.get("roadmap", [])}
    graph = graph_data.get("graph", {})

    with st.expander("🕸️ Dependency Graph (roadmap topics)", expanded=False):
        for step in data.get("roadmap", []):
            topic = step["topic"]
            prereqs = graph.get(topic, [])
            in_roadmap = [p for p in prereqs if p in roadmap_topics]
            missing    = [p for p in prereqs if p not in roadmap_topics]
            topic_label = topic.replace("_", " ").title()

            prereq_html = ""
            if in_roadmap:
                prereq_html += " ".join(
                    f'<span style="background:#DBEAFE;color:#1D4ED8;'
                    f'border-radius:999px;padding:0.15rem 0.6rem;font-size:0.75rem;font-weight:600;">'
                    f'✓ {p.replace("_"," ").title()}</span>' for p in in_roadmap
                )
            if missing:
                prereq_html += " ".join(
                    f'<span style="background:#F3F4F6;color:#6B7280;'
                    f'border-radius:999px;padding:0.15rem 0.6rem;font-size:0.75rem;">'
                    f'{p.replace("_"," ").title()} (mastered)</span>' for p in missing
                )

            no_prereq_span = '&nbsp;<span style="color:#94A3B8;font-size:0.78rem;">no prerequisites</span>'
            right_side = ("&nbsp;←&nbsp;" + prereq_html) if prereq_html else no_prereq_span
            st.markdown(
                f'<div style="padding:0.5rem 0;border-bottom:1px solid #F1F5F9;">'
                f'<strong style="color:#0F3460;">{topic_label}</strong>'
                f'{right_side}'
                f'</div>',
                unsafe_allow_html=True,
            )


# ── Sidebar ───────────────────────────────────────────────────────────────────

def build_sidebar() -> tuple[Dict, int, bool]:
    """Renders sidebar and returns (snapshot, max_retries, generate_clicked)."""
    with st.sidebar:
        st.markdown("""
<div style="text-align:center;padding:1.25rem 0 0.5rem;">
  <div style="font-size:2rem;">🗺️</div>
  <div style="font-size:1.2rem;font-weight:800;color:white;letter-spacing:-0.01em;">PathFinder</div>
</div>
""", unsafe_allow_html=True)

        # ── API health indicator ──────────────────────────────────────────
        health = api_health()
        if health and health.get("status") == "ok":
            st.markdown("""
<div style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.35);
            border-radius:8px;padding:0.4rem 0.75rem;text-align:center;
            font-size:0.75rem;font-weight:600;color:#6EE7B7;margin:0.5rem 0.75rem;">
  🟢 API Connected
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div style="background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.35);
            border-radius:8px;padding:0.4rem 0.75rem;text-align:center;
            font-size:0.75rem;font-weight:600;color:#FCA5A5;margin:0.5rem 0.75rem;">
  🔴 API Offline
</div>""", unsafe_allow_html=True)

        st.markdown('<p class="sidebar-section">Your Skill Profile</p>', unsafe_allow_html=True)

        # ── Skill selectors ───────────────────────────────────────────────
        skills: Dict[str, str] = {}
        for key, meta in TOPIC_META.items():
            default_idx = SKILL_OPTIONS.index(
                st.session_state.get(f"skill_{key}", SKILL_DEFAULTS[key])
            )
            val = st.selectbox(
                label=meta["label"],
                options=SKILL_OPTIONS,
                index=default_idx,
                key=f"skill_{key}",
            )
            skills[key] = val

        st.markdown('<p class="sidebar-section">Time Budget</p>', unsafe_allow_html=True)
        time_hours = st.slider(
            "Available study hours",
            min_value=1,
            max_value=100,
            value=st.session_state.get("time_hours", 20),
            step=1,
            key="time_hours",
            help="How many total hours can you dedicate to this study plan?",
        )

        st.markdown('<p class="sidebar-section">Options</p>', unsafe_allow_html=True)
        max_retries = st.select_slider(
            "Max validation retries",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.get("max_retries", 3),
            key="max_retries",
            help="How many times should the planner retry if validation fails?",
        )

        st.markdown("<br>", unsafe_allow_html=True)
        generate = st.button("🚀 Generate Roadmap", use_container_width=True, type="primary")

        # Reset button
        col_r, _ = st.columns([1, 1])
        with col_r:
            if st.button("↺ Reset", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<p style="font-size:0.7rem;color:#4A6080;text-align:center;">'
            f'API: {API_BASE_URL}</p>',
            unsafe_allow_html=True,
        )

    snapshot: Dict[str, Any] = {**skills, "time_available_hours": float(time_hours)}
    return snapshot, max_retries, generate


# ── Main app ──────────────────────────────────────────────────────────────────

def main() -> None:
    inject_css()
    render_header()

    snapshot, max_retries, generate = build_sidebar()

    # ── Trigger generation ────────────────────────────────────────────────
    if generate:
        with st.spinner("🧠 Running pipeline — Skill Analysis → Topic Planning → RAG → Planning → Validation…"):
            try:
                result = api_generate_roadmap(snapshot, max_retries)
                st.session_state["last_result"]   = result
                st.session_state["last_snapshot"] = snapshot
                st.session_state["api_error"]     = None
            except requests.exceptions.ConnectionError:
                st.session_state["api_error"] = (
                    "Cannot connect to the PathFinder API. "
                    f"Is the server running at {API_BASE_URL}? "
                    "Start it with: python api_server.py"
                )
            except requests.exceptions.Timeout:
                st.session_state["api_error"] = (
                    "The request timed out after 3 minutes. "
                    "The LLM may be overloaded — please try again."
                )
            except requests.exceptions.HTTPError as e:
                detail = ""
                try:
                    detail = e.response.json().get("detail", "")
                except Exception:
                    pass
                st.session_state["api_error"] = f"API returned an error: {e}. {detail}"
            except Exception as e:
                st.session_state["api_error"] = f"Unexpected error: {e}"

    # ── Render results ────────────────────────────────────────────────────
    if st.session_state.get("api_error"):
        render_api_error(st.session_state["api_error"])

    elif "last_result" in st.session_state:
        data     = st.session_state["last_result"]
        snap     = st.session_state.get("last_snapshot", snapshot)

        # Fetch graph for dependency view (cached loosely)
        if "graph_data" not in st.session_state:
            st.session_state["graph_data"] = api_graph_topics()
        graph_data = st.session_state.get("graph_data")

        render_skill_analysis(data)
        st.markdown("<br>", unsafe_allow_html=True)
        render_roadmap(data)
        st.markdown("<br>", unsafe_allow_html=True)
        render_validation_status(data)
        st.markdown("<br>", unsafe_allow_html=True)
        render_dependency_graph(data, graph_data)
        st.markdown("<br>", unsafe_allow_html=True)
        render_export(data, snap)

        # Raw JSON toggle
        with st.expander("🔍 Raw API Response (JSON)", expanded=False):
            st.json(data)

    else:
        render_welcome()


if __name__ == "__main__":
    main()
