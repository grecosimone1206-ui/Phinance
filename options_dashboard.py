"""
╔══════════════════════════════════════════════════════════╗
║         PHINANCE - Dashboard Vendita Put  v5.1           ║
║         Auto VIX &middot; IV Rank &middot; Live Timestamps             ║
╚══════════════════════════════════════════════════════════╝
Librerie: pip install streamlit numpy pandas scipy plotly yfinance
Avvio:    streamlit run options_dashboard.py
"""

import numpy as np
import pandas as pd
import scipy.stats as si
import streamlit as st
import plotly.graph_objects as go
from dataclasses import dataclass
from datetime import datetime
import io

try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                     Table, TableStyle, HRFlowable, PageBreak)
    REPORTLAB_OK = True
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab", "-q"])
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_LEFT
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                         Table, TableStyle, HRFlowable, PageBreak)
        REPORTLAB_OK = True
    except ImportError:
        REPORTLAB_OK = False

# &mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;──────────────────
# CONFIGURAZIONE PAGINA
# &mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;──────────────────
st.set_page_config(
    page_title="Phinance | Dashboard Opzioni",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════
# STRATEGIA — SPLASH SCREEN
# ═══════════════════════════════════════════════════════════

if "strategia" not in st.session_state:
    st.session_state.strategia = None

if st.session_state.strategia is None:

    # ── CSS globale splash ──
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700;9..40,800&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMain"] {
    background: #07090D !important;
    margin: 0; padding: 0;
}
[data-testid="stAppViewBlockContainer"] { padding-top: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"]   { display: none !important; }
[data-testid="stToolbar"]   { display: none !important; }
[data-testid="stDecoration"]{ display: none !important; }
footer                       { display: none !important; }
#MainMenu                    { display: none !important; }

/* ── Pulsanti Streamlit = Tab visibili ── */

/* Contenitore colonne centrato */
div[data-testid="stHorizontalBlock"] {
    justify-content: center !important;
    gap: 1rem !important;
    max-width: 460px !important;
    margin: 0 auto !important;
}

/* Reset colonne */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: 0 !important;
    padding: 0 !important;
}

/* Il pulsante stesso — stile tab rosso */
div[data-testid="stHorizontalBlock"] .stButton > button {
    position: relative !important;
    min-width: 210px !important;
    height: 54px !important;
    padding: 0 2.2rem !important;
    border-radius: 14px !important;
    border: 1px solid rgba(180,28,28,0.32) !important;
    background: rgba(160,22,22,0.07) !important;
    color: rgba(255,255,255,0.68) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    cursor: pointer !important;
    overflow: hidden !important;
    transition:
        border-color 0.25s ease,
        color        0.25s ease,
        box-shadow   0.25s ease,
        transform    0.2s  ease,
        background   0.25s ease !important;
    bottom: unset !important;
    left: unset !important;
    opacity: 1 !important;
    pointer-events: all !important;
    width: auto !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    border-color: rgba(220,45,45,0.68) !important;
    color: #ffffff !important;
    background: rgba(200,30,30,0.12) !important;
    box-shadow:
        0 0 22px  5px rgba(200,28,28,0.20),
        0 0 50px 12px rgba(200,28,28,0.09),
        inset 0 0 18px rgba(200,28,28,0.07) !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stHorizontalBlock"] .stButton > button:active {
    transform: translateY(0) !important;
}

div[data-testid="stHorizontalBlock"] .stButton > button:focus {
    outline: none !important;
    box-shadow:
        0 0 22px  5px rgba(200,28,28,0.20),
        0 0 50px 12px rgba(200,28,28,0.09) !important;
}


/* ── KEYFRAMES ── */
@keyframes spin-ring {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
@keyframes breathe {
    0%,100% { opacity: 0.55; }
    50%      { opacity: 1;    }
}
@keyframes fade-up {
    from { opacity:0; transform:translateY(22px); }
    to   { opacity:1; transform:translateY(0);    }
}
@keyframes dot-beat {
    0%,100% { box-shadow: 0 0 8px 2px rgba(210,35,35,0.7), 0 0 20px 4px rgba(210,35,35,0.3); }
    50%      { box-shadow: 0 0 14px 4px rgba(255,60,60,1),  0 0 36px 8px rgba(255,60,60,0.5); }
}

/* ── SPLASH ROOT ── */
.ph-splash {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-top: calc(50vh - 260px);
    background: #07090D;
    animation: fade-up 0.8s cubic-bezier(.22,.68,0,1.2) both;
}

/* radial ambient */
.ph-splash::before {
    content:'';
    position:absolute;
    top:38%; left:50%;
    transform:translate(-50%,-50%);
    width:700px; height:700px;
    background: radial-gradient(circle, rgba(180,25,25,0.055) 0%, transparent 65%);
    pointer-events:none;
}

/* ── RING WRAPPER ── */
.ph-ring-wrap {
    position: relative;
    width: 320px;
    height: 320px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 3.2rem;
}

/* Rotating conic arc */
.ph-ring-spin {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: conic-gradient(
        from 0deg,
        transparent 0%,
        transparent 55%,
        rgba(200,30,30,0.00) 65%,
        rgba(215,45,45,0.45) 76%,
        rgba(240,70,70,0.80) 84%,
        rgba(255,110,110,1)  90%,
        rgba(240,70,70,0.80) 96%,
        rgba(210,35,35,0.30) 100%
    );
    -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 1.8px), #fff calc(100% - 0.5px));
    mask:         radial-gradient(farthest-side, transparent calc(100% - 1.8px), #fff calc(100% - 0.5px));
    animation: spin-ring 3.8s linear infinite;
    filter: blur(0.3px);
}

/* Soft outer glow ring (static, breathing) */
.ph-ring-glow {
    position: absolute;
    inset: -6px;
    border-radius: 50%;
    border: 1px solid rgba(200,30,30,0.12);
    box-shadow:
        0 0 24px 6px  rgba(180,20,20,0.10),
        0 0 60px 14px rgba(180,20,20,0.05);
    animation: breathe 4.5s ease-in-out infinite;
}

/* Inner decorative rings */
.ph-ring-d1 {
    position:absolute; inset:14px;
    border-radius:50%;
    border:1px solid rgba(255,255,255,0.035);
}
.ph-ring-d2 {
    position:absolute; inset:28px;
    border-radius:50%;
    border:1px solid rgba(255,255,255,0.020);
}

/* ── LOGO TEXT ── */
.ph-logo-text {
    position: relative;
    z-index: 10;
    font-family: 'DM Sans', sans-serif;
    font-size: 4rem;
    font-weight: 800;
    letter-spacing: -0.045em;
    line-height: 1;
    /* white → pale blue gradient, replicates the image reference */
    background: linear-gradient(
        160deg,
        #FFFFFF  0%,
        #D8E8FF 35%,
        #7BBCFF 65%,
        #4AA0FF 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 2px 24px rgba(100,180,255,0.18));
    user-select: none;
}

/* Accent dot after text */
.ph-logo-text::after {
    content: '';
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #CC2020;
    margin-left: 5px;
    margin-bottom: 7px;
    vertical-align: bottom;
    box-shadow: 0 0 8px 2px rgba(210,35,35,0.7), 0 0 20px 4px rgba(210,35,35,0.3);
    animation: dot-beat 3.8s ease-in-out infinite;
    -webkit-text-fill-color: initial;
}

/* ── TABS ── */
.ph-tabs {
    display: flex;
    gap: 1rem;
    animation: fade-up 0.9s 0.15s cubic-bezier(.22,.68,0,1.2) both;
}

.ph-tab {
    position: relative;
    min-width: 210px;
    padding: 1rem 2.2rem;
    border-radius: 14px;
    border: 1px solid rgba(180,28,28,0.30);
    background: rgba(160,22,22,0.07);
    color: rgba(255,255,255,0.68);
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    text-align: center;
    cursor: pointer;
    user-select: none;
    overflow: hidden;
    transition:
        border-color   0.25s ease,
        color          0.25s ease,
        box-shadow     0.25s ease,
        transform      0.2s  ease,
        background     0.25s ease;
}

/* top shimmer line */
.ph-tab::after {
    content:'';
    position:absolute;
    top:0; left:15%; right:15%;
    height:1px;
    background: linear-gradient(90deg, transparent, rgba(255,80,80,0.55), transparent);
    opacity:0;
    transition: opacity 0.25s ease;
    border-radius:1px;
}

.ph-tab:hover {
    border-color: rgba(220,45,45,0.65);
    color: #ffffff;
    background: rgba(200,30,30,0.11);
    box-shadow:
        0  0 22px  5px rgba(200,28,28,0.18),
        0  0 50px 12px rgba(200,28,28,0.08),
        inset 0 0 18px rgba(200,28,28,0.06);
    transform: translateY(-2px);
}
.ph-tab:hover::after { opacity:1; }
/* Separatore tra strategie e advisor */
.ph-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    max-width: 460px;
    margin: 1.8rem auto 0;
}
.ph-divider::before, .ph-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.06);
}
.ph-divider-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.6rem;
    color: rgba(255,255,255,0.2);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

    # ── HTML della splash (logo + ring, senza tab HTML) ──
    st.markdown("""
<div class="ph-splash">

  <div class="ph-ring-wrap">
    <div class="ph-ring-glow"></div>
    <div class="ph-ring-spin"></div>
    <div class="ph-ring-d1"></div>
    <div class="ph-ring-d2"></div>
    <span class="ph-logo-text">Phinance</span>
  </div>

</div>
""", unsafe_allow_html=True)

    # ── Pulsanti Streamlit — griglia 2x2 ──
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Put Scoperta", key="splash_ps"):
            st.session_state.strategia = "put_scoperta"
            st.rerun()
    with col2:
        if st.button("Bull Put Spread", key="splash_bps"):
            st.session_state.strategia = "bull_put_spread"
            st.rerun()
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Long Call", key="splash_lc"):
            st.session_state.strategia = "long_call"
            st.rerun()
    with col4:
        if st.button("Long Put", key="splash_lp"):
            st.session_state.strategia = "long_put"
            st.rerun()

    # ── Separatore + Strategy Advisor ──
    st.markdown("""
<div class="ph-divider"><span class="ph-divider-label">AI Advisory</span></div>
""", unsafe_allow_html=True)

    col_adv_center = st.columns([1, 2, 1])
    with col_adv_center[1]:
        if st.button("Strategy Advisor", key="splash_advisor", use_container_width=True):
            st.session_state.strategia = "strategy_advisor"
            st.rerun()

    st.stop()

STRATEGIA = st.session_state.strategia


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,300&family=DM+Mono:wght@300;400;500&display=swap');

/* ── VARIABILI ── */
:root {
  --bg-base:         #060A0E;
  --bg-surface:      #0A1118;
  --bg-elevated:     #0F1822;
  --bg-card:         #0C1520;
  --border-subtle:   rgba(255,255,255,0.055);
  --border-medium:   rgba(255,255,255,0.09);
  --border-strong:   rgba(255,255,255,0.15);
  --text-primary:    #EEF4FF;
  --text-secondary:  #7A90B0;
  --text-muted:      #3E526A;
  --accent-cyan:     #00C2FF;
  --accent-cyan-soft:rgba(0,194,255,0.08);
  --accent-green:    #00E5A0;
  --accent-green-dim:rgba(0,229,160,0.08);
  --accent-gold:     #FFB547;
  --accent-gold-dim: rgba(255,181,71,0.08);
  --accent-red:      #FF5A5A;
  --accent-red-dim:  rgba(255,90,90,0.06);
  --radius-sm:       8px;
  --radius-md:       12px;
  --radius-lg:       18px;
  --radius-xl:       24px;
  --shadow-sm:       0 2px 8px rgba(0,0,0,0.3);
  --shadow-md:       0 4px 20px rgba(0,0,0,0.45);
  --shadow-lg:       0 8px 40px rgba(0,0,0,0.6);
  --shadow-glow-c:   0 0 24px rgba(0,194,255,0.12);
  --font-body:       'DM Sans', sans-serif;
  --font-mono:       'DM Mono', monospace;
  font-variant-numeric: normal;
}

/* ── RESET ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {
    background-color: var(--bg-base) !important;
    color: var(--text-primary);
    font-family: var(--font-body);
}
[data-testid="stAppViewBlockContainer"] { padding-top: 0 !important; }
.block-container { padding: 2.5rem 3rem !important; max-width: 100% !important; }
* { font-variant-numeric: normal !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1118 0%, #080E15 100%) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
[data-testid="stSidebar"] > div { padding: 2rem 1.4rem; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
    font-feature-settings: "zero" 0 !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: rgba(0,194,255,0.4) !important;
    box-shadow: 0 0 0 2px rgba(0,194,255,0.08) !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--accent-cyan) !important;
    border: 2px solid var(--bg-base) !important;
    box-shadow: 0 0 10px rgba(0,194,255,0.6) !important;
    width: 16px !important; height: 16px !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[data-testid="stSliderTrackFill"] {
    background: linear-gradient(90deg, rgba(0,194,255,0.5), var(--accent-cyan)) !important;
}
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, rgba(0,194,255,0.08), rgba(0,194,255,0.04)) !important;
    border: 1px solid rgba(0,194,255,0.2) !important;
    border-radius: var(--radius-md) !important;
    color: var(--accent-cyan) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 12px 16px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: linear-gradient(135deg, rgba(0,194,255,0.15), rgba(0,194,255,0.08)) !important;
    border-color: rgba(0,194,255,0.4) !important;
    box-shadow: 0 0 16px rgba(0,194,255,0.2) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stSidebar"] .stDownloadButton button {
    background: linear-gradient(135deg, rgba(0,229,160,0.12), rgba(0,229,160,0.06)) !important;
    border: 1.5px solid rgba(0,229,160,0.6) !important;
    border-radius: var(--radius-md) !important;
    color: var(--accent-green) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 12px 16px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 12px rgba(0,229,160,0.15) !important;
}
[data-testid="stSidebar"] .stDownloadButton button:hover {
    background: linear-gradient(135deg, rgba(0,229,160,0.22), rgba(0,229,160,0.12)) !important;
    border-color: rgba(0,229,160,0.9) !important;
    box-shadow: 0 0 22px rgba(0,229,160,0.35) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stSidebar"] hr {
    border-color: var(--border-subtle) !important;
    margin: 1.5rem 0 !important;
}

/* ── TIPOGRAFIA ── */
h1, h2, h3 { font-family: var(--font-body) !important; }
h2 {
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    border: none !important;
    margin-bottom: 1rem !important;
}
hr { border-color: var(--border-subtle) !important; }

/* ── ANIMAZIONI ── */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes pulseGlow {
    0%, 100% { opacity: 0.7; box-shadow: 0 0 4px currentColor; }
    50%       { opacity: 1;   box-shadow: 0 0 12px currentColor; }
}

/* ── HEADER ── */
.ph-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2.2rem 0 1.8rem 0;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 2rem;
    animation: fadeSlideUp 0.6s ease both;
}
.ph-logo {
    font-family: var(--font-body);
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    background: linear-gradient(120deg, #FFFFFF 0%, #80DDFF 40%, var(--accent-cyan) 70%, #0077BB 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.ph-header-right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.3rem;
}
.ph-subtitle {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--text-muted);
    letter-spacing: 0.14em;
    text-transform: uppercase;
}
.ph-tag {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    padding: 3px 10px;
    background: rgba(255,255,255,0.02);
}

/* ── SIGNAL BANNER ── */
.signal-banner {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    border-radius: var(--radius-md);
    padding: 1rem 1.6rem;
    margin-bottom: 2rem;
    border: 1px solid;
    animation: fadeSlideUp 0.6s 0.1s ease both;
}
.signal-banner.verde  { background: rgba(0,229,160,0.04);  border-color: rgba(0,229,160,0.18); }
.signal-banner.giallo { background: rgba(255,181,71,0.04);  border-color: rgba(255,181,71,0.18); }
.signal-banner.rosso  { background: rgba(255,90,90,0.04);   border-color: rgba(255,90,90,0.18); }
.signal-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}
.signal-dot.verde  { background: var(--accent-green); box-shadow: 0 0 0 4px rgba(0,229,160,0.12); animation: pulseGlow 2.5s infinite; color: var(--accent-green); }
.signal-dot.giallo { background: var(--accent-gold);  box-shadow: 0 0 0 4px rgba(255,181,71,0.12); }
.signal-dot.rosso  { background: var(--accent-red);   box-shadow: 0 0 0 4px rgba(255,90,90,0.12); }
.signal-label {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    white-space: nowrap;
}
.signal-banner.verde  .signal-label { color: var(--accent-green); }
.signal-banner.giallo .signal-label { color: var(--accent-gold); }
.signal-banner.rosso  .signal-label { color: var(--accent-red); }
.signal-text { font-family: var(--font-body); font-size: 0.88rem; color: var(--text-secondary); line-height: 1.4; }

/* ── KPI CARDS ── */
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-xl);
    padding: 1.4rem 1.5rem;
    position: relative;
    overflow: visible;
    transition: border-color 0.3s, transform 0.3s, box-shadow 0.3s;
    animation: fadeSlideUp 0.6s ease both;
    height: 148px;
    box-sizing: border-box;
    cursor: default;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.kpi-card.mini {
    min-height: unset !important;
    height: 115px !important;
    padding: 0.9rem 1rem !important;
}
.kpi-card.kpi-sm {
    height: 138px !important;
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    padding: 1rem 1.1rem !important;
    overflow: visible !important;
    box-sizing: border-box !important;
}
.kpi-card.kpi-sm .kpi-value {
    font-size: 1.45rem !important;
    margin-bottom: 0.25rem !important;
}
.kpi-card.kpi-sm .kpi-sub {
    font-size: 0.58rem !important;
    margin-bottom: 0.3rem !important;
    white-space: normal !important;
    line-height: 1.35 !important;
}
.kpi-card.kpi-sm .kpi-eyebrow {
    font-size: 0.52rem !important;
    margin-bottom: 0.3rem !important;
    overflow: visible !important;
    white-space: nowrap !important;
}
.kpi-card.kpi-sm .tip-icon {
    width: 11px !important;
    height: 11px !important;
    font-size: 0.42rem !important;
}
.kpi-card.kpi-sm .tip-box {
    font-size: 0.62rem !important;
}
.kpi-card.kpi-sm .kpi-badge {
    font-size: 0.46rem !important;
    padding: 2px 6px !important;
    white-space: nowrap !important;
}
.kpi-card:hover {
    border-color: rgba(0,194,255,0.2);
    transform: translateY(-3px);
    box-shadow: var(--shadow-md), var(--shadow-glow-c);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(0,194,255,0.3) 50%, transparent 100%);
    opacity: 0;
    transition: opacity 0.3s;
}
.kpi-card:hover::before { opacity: 1; }
.kpi-card::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 140px; height: 140px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,194,255,0.04) 0%, transparent 70%);
    pointer-events: none;
}
.kpi-eyebrow {
    font-family: var(--font-mono);
    font-size: 0.56rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
    white-space: nowrap;
    overflow: visible;
    position: relative;
}
.kpi-value {
    font-family: var(--font-body);
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 0.35rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.kpi-value.cyan  { color: var(--accent-cyan); }
.kpi-value.green { color: var(--accent-green); }
.kpi-value.gold  { color: var(--accent-gold); }
.kpi-value.red   { color: var(--accent-red); }
.kpi-sub {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    line-height: 1.4;
    margin-bottom: 0.5rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.kpi-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-family: var(--font-mono);
    font-size: 0.55rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    white-space: nowrap;
}
.kpi-badge.green { background: var(--accent-green-dim); color: var(--accent-green); border: 1px solid rgba(0,229,160,0.2); }
.kpi-badge.gold  { background: var(--accent-gold-dim);  color: var(--accent-gold);  border: 1px solid rgba(255,181,71,0.2); }
.kpi-badge.red   { background: var(--accent-red-dim);   color: var(--accent-red);   border: 1px solid rgba(255,90,90,0.2); }

/* ── KPI GRID ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}

/* ── PANELS ── */
.panel {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-xl);
    padding: 1.8rem 2rem;
    animation: fadeSlideUp 0.6s 0.2s ease both;
    height: 100%;
    transition: border-color 0.3s, box-shadow 0.3s;
}
.panel:hover {
    border-color: var(--border-medium);
    box-shadow: var(--shadow-sm);
}
.panel-title {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 1.4rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.panel-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.65rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    transition: all 0.15s;
}
.panel-row:last-child { border-bottom: none; padding-bottom: 0; }
.panel-row:hover {
    background: rgba(255,255,255,0.025);
    margin: 0 -0.6rem;
    padding: 0.65rem 0.6rem;
    border-radius: 6px;
    border-bottom-color: transparent;
}
.panel-key {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--text-secondary);
    letter-spacing: 0.02em;
    font-weight: 500;
}
.panel-val {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-weight: 500;
    text-align: right;
}
.panel-val.cyan  { color: var(--accent-cyan); }
.panel-val.green { color: var(--accent-green); }
.panel-val.red   { color: var(--accent-red); }
.panel-val.big   { font-size: 1.3rem; font-weight: 700; color: var(--accent-cyan); letter-spacing: -0.02em; }

/* ── CRISIS PANEL ── */
.crisis-panel {
    background: linear-gradient(135deg, rgba(255,90,90,0.04) 0%, rgba(10,17,24,0.95) 100%);
    border: 1px solid rgba(255,90,90,0.14);
    border-radius: var(--radius-xl);
    padding: 1.8rem 2rem;
    animation: fadeSlideUp 0.6s 0.2s ease both;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.crisis-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,90,90,0.3), transparent);
}
.crisis-header {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(255,150,150,0.95);
    margin-bottom: 1.4rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255,90,90,0.2);
}
.crisis-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.65rem 0;
    border-bottom: 1px solid rgba(255,90,90,0.06);
}
.crisis-row:last-child { border-bottom: none; }
.crisis-key { font-family: var(--font-mono); font-size: 0.63rem; color: rgba(255,150,150,0.9); font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: block; }
.crisis-val { font-family: var(--font-mono); font-size: 0.8rem; color: var(--text-secondary); font-weight: 500; }
.crisis-val.red   { color: var(--accent-red); }
.crisis-val.green { color: var(--accent-green); }
.crisis-impact {
    margin-top: 1.2rem;
    padding: 0.9rem 1.1rem;
    background: rgba(255,90,90,0.06);
    border-radius: var(--radius-sm);
    border: 1px solid rgba(255,90,90,0.1);
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: rgba(255,90,90,0.5);
    text-align: center;
    letter-spacing: 0.05em;
}

/* ── SECTION LABEL ── */
.section-label {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin: 2.5rem 0 1.2rem 0;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: var(--border-subtle); }

/* ── SIDEBAR SECTIONS ── */
.sb-section {
    font-family: var(--font-body);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    text-transform: none;
    color: var(--accent-cyan);
    padding: 1rem 0 0.5rem 0;
    margin-top: 0.5rem;
    border-top: 1px solid var(--border-subtle);
}
.sb-section:first-child { border-top: none; margin-top: 0; padding-top: 0; }

/* ── METRIC CARDS NATIVE ── */
.live-bar-wrap [data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 1.4rem 1.6rem;
    transition: border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
    animation: fadeSlideUp 0.6s 0.05s ease both;
}
.live-bar-wrap [data-testid="stMetric"]:hover {
    border-color: rgba(0,194,255,0.18);
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm), 0 0 16px rgba(0,194,255,0.06);
}
.live-bar-wrap [data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
.live-bar-wrap [data-testid="stMetricValue"] {
    font-family: var(--font-body) !important;
    font-size: 1.7rem !important;
    font-weight: 700 !important;
    color: var(--accent-cyan) !important;
    letter-spacing: -0.03em !important;
    line-height: 1.1 !important;
}
.live-bar-wrap [data-testid="stMetricDelta"] {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
}
.live-bar-wrap [data-testid="stMetricLabel"] svg {
    color: var(--text-muted) !important;
    transition: color 0.2s ease;
}
.live-bar-wrap [data-testid="stMetricLabel"]:hover svg {
    color: var(--accent-cyan) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
    background: rgba(255,255,255,0.02) !important;
    color: var(--text-muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border-medium) !important;
    padding: 12px 16px !important;
}
[data-testid="stDataFrame"] td {
    background: var(--bg-card) !important;
    color: var(--text-secondary) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    padding: 10px 16px !important;
}

/* ── FOOTER ── */
.ph-footer {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
    border-top: 1px solid var(--border-subtle);
    margin-top: 3rem;
    font-family: var(--font-mono);
    font-size: 0.6rem;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    line-height: 2.2;
}

/* ── DELTA COLORI CUSTOM ── */
/* :has() necessario perché il div wrapper e st.metric sono fratelli nel DOM, non padre-figlio */
[data-testid="stColumn"]:has(.ph-delta-green) [data-testid="stMetricDelta"] { color: var(--accent-green) !important; }
[data-testid="stColumn"]:has(.ph-delta-gold)  [data-testid="stMetricDelta"] { color: var(--accent-gold)  !important; }
[data-testid="stColumn"]:has(.ph-delta-red)   [data-testid="stMetricDelta"] { color: var(--accent-red)   !important; }
[data-testid="stColumn"]:has(.ph-delta-green) [data-testid="stMetricDelta"] svg,
[data-testid="stColumn"]:has(.ph-delta-gold)  [data-testid="stMetricDelta"] svg,
[data-testid="stColumn"]:has(.ph-delta-red)   [data-testid="stMetricDelta"] svg { display: none !important; }
/* ── SPLASH SCREEN ── */
.splash-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    padding: 2rem;
    animation: fadeSlideUp 0.8s ease both;
}
.splash-logo {
    font-family: var(--font-body);
    font-size: 3.2rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #00C2FF 0%, #00E5A0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.4rem;
}
.splash-sub {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 3rem;
}
.splash-cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    width: 100%;
    max-width: 760px;
}
.splash-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-xl);
    padding: 2rem 2rem 1.8rem;
    cursor: pointer;
    transition: border-color 0.3s, transform 0.3s, box-shadow 0.3s;
    position: relative;
    overflow: hidden;
}
.splash-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--card-accent, #00C2FF), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}
.splash-card:hover {
    border-color: var(--border-strong);
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}
.splash-card:hover::before { opacity: 1; }
.splash-card-icon {
    font-size: 2rem;
    margin-bottom: 1rem;
}
.splash-card-title {
    font-family: var(--font-body);
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.4rem;
    letter-spacing: -0.02em;
}
.splash-card-sub {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.splash-card-desc {
    font-family: var(--font-body);
    font-size: 0.78rem;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 1.2rem;
}
.splash-card-badge {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 0.55rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.7rem;
    border-radius: 100px;
    border: 1px solid;
}
.splash-card-badge.cyan {
    color: var(--accent-cyan);
    border-color: rgba(0,194,255,0.25);
    background: rgba(0,194,255,0.06);
}
.splash-card-badge.green {
    color: var(--accent-green);
    border-color: rgba(0,229,160,0.25);
    background: rgba(0,229,160,0.06);
}
.splash-footer {
    font-family: var(--font-mono);
    font-size: 0.55rem;
    color: var(--text-muted);
    letter-spacing: 0.1em;
    margin-top: 2.5rem;
    text-align: center;
}
/* Pannello analisi spread BPS */
.spread-analysis {
    background: linear-gradient(135deg, rgba(0,229,160,0.04) 0%, rgba(0,194,255,0.04) 100%);
    border: 1px solid rgba(0,229,160,0.15);
    border-radius: var(--radius-xl);
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.5rem;
    animation: fadeSlideUp 0.6s ease both;
    animation-delay: 0.25s;
}
.spread-analysis-title {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent-green);
    margin-bottom: 1rem;
}
.spread-rule {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    padding: 0.5rem 0.9rem;
    border-radius: 8px;
    display: inline-block;
    margin-top: 0.4rem;
}
.spread-rule.ok {
    background: rgba(0,229,160,0.08);
    border: 1px solid rgba(0,229,160,0.2);
    color: var(--accent-green);
}
.spread-rule.warn {
    background: rgba(255,181,71,0.08);
    border: 1px solid rgba(255,181,71,0.2);
    color: var(--accent-gold);
}
.spread-rule.bad {
    background: rgba(255,90,90,0.08);
    border: 1px solid rgba(255,90,90,0.2);
    color: var(--accent-red);
}

/* ── TOOLTIP GRECHE ── */
.greek-tooltip {
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
}
.greek-tooltip .tip-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 13px; height: 13px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    font-size: 0.5rem;
    color: var(--text-muted);
    cursor: help;
    font-family: var(--font-body);
    font-style: normal;
    flex-shrink: 0;
    transition: background 0.2s, border-color 0.2s;
}
.greek-tooltip:hover .tip-icon {
    background: rgba(0,194,255,0.12);
    border-color: rgba(0,194,255,0.3);
    color: var(--accent-cyan);
}
.greek-tooltip .tip-box {
    visibility: hidden;
    opacity: 0;
    position: absolute;
    bottom: calc(100% + 8px);
    left: 50%;
    transform: translateX(-50%);
    min-width: 220px;
    max-width: 260px;
    background: #0F1E2E;
    border: 1px solid rgba(0,194,255,0.2);
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    font-family: var(--font-body);
    font-size: 0.62rem;
    color: var(--text-secondary);
    line-height: 1.5;
    z-index: 9999;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6);
    transition: opacity 0.2s, visibility 0.2s;
    pointer-events: none;
    white-space: normal;
    text-transform: none;
    letter-spacing: 0;
}
.greek-tooltip:hover .tip-box {
    visibility: visible;
    opacity: 1;
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.07); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.12); }
</style>
""", unsafe_allow_html=True)

# ── Forza punto decimale negli input sidebar ──
import streamlit.components.v1 as _components
_components.html("""
<script>
(function() {
    function fixDecimal() {
        const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return;
        sidebar.querySelectorAll('input').forEach(function(inp) {
            if (inp._phinanceFixed) return;
            inp._phinanceFixed = true;
            inp.addEventListener('keypress', function(e) {
                if (e.key === ',') { e.preventDefault(); document.execCommand('insertText', false, '.'); }
            });
            inp.addEventListener('input', function() {
                if (this.value.includes(',')) {
                    const pos = this.selectionStart;
                    this.value = this.value.replace(/,/g, '.');
                    try { this.setSelectionRange(pos, pos); } catch(e) {}
                }
            });
        });
    }
    const mo = new MutationObserver(fixDecimal);
    mo.observe(window.parent.document.body, { childList: true, subtree: true });
    setInterval(fixDecimal, 500);
})();
</script>
""", height=0)


# ═══════════════════════════════════════════════════════════
# FUNZIONI DATI &mdash; yfinance + VIX + IV Rank
# ═══════════════════════════════════════════════════════════

TICKER_DISPONIBILI = {
    "NASDAQ 100 (QQQ)":              "QQQ",
    "S&P 500 (SPY)":                 "SPY",
    "S&P 500 Indice (^GSPC)":        "^GSPC",
    "Dow Jones (^DJI)":              "^DJI",
    "Apple (AAPL)":                  "AAPL",
    "Tesla (TSLA)":                  "TSLA",
    "Nvidia (NVDA)":                 "NVDA",
    "Microsoft (MSFT)":              "MSFT",
    "Amazon (AMZN)":                 "AMZN",
    "Altro (inserisci manualmente)": "MANUALE",
}

def ora_adesso() -> str:
    try:
        import pytz
        tz = pytz.timezone("Europe/Rome")
        return datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")
    except ImportError:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def fmt(value, decimals=2) -> str:
    """Formato europeo: separatore migliaia = punto, decimale = virgola."""
    s = f"{value:,.{decimals}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

@st.cache_data(ttl=300)
def recupera_dati_mercato(ticker: str) -> dict:
    """
    Recupera da Yahoo Finance:
    - Prezzo Spot + variazione %
    - Volatilità Storica 30gg annualizzata
    - IV Rank (calcolato su 252 giorni di vol. storica rolling)
    - VIX corrente (scaricato in automatico)
    Ogni dato registra il proprio timestamp di aggiornamento.
    """
    ts = ora_adesso()
    try:
        # ── Dati sottostante ──
        s = yf.Ticker(ticker)
        h = s.history(period="1y")          # 1 anno per IV Rank
        if h.empty:
            return {"errore": f"Nessun dato trovato per '{ticker}'"}

        spot = float(h["Close"].iloc[-1])
        var  = ((spot - float(h["Close"].iloc[-2])) / float(h["Close"].iloc[-2]) * 100) if len(h) >= 2 else 0.0

        # Volatilità storica 30gg annualizzata
        ret     = np.log(h["Close"] / h["Close"].shift(1)).dropna()
        vol_30  = float(ret.tail(30).std() * np.sqrt(252) * 100)

        # ── IV Rank ──
        # Calcoliamo la vol. storica rolling 30gg su tutto l'anno
        # IV Rank = (vol oggi - vol min 1Y) / (vol max - vol min) * 100
        vol_rolling = ret.rolling(30).std() * np.sqrt(252) * 100
        vol_rolling = vol_rolling.dropna()
        if len(vol_rolling) >= 10:
            v_min = float(vol_rolling.min())
            v_max = float(vol_rolling.max())
            v_now = float(vol_rolling.iloc[-1])
            iv_rank = round((v_now - v_min) / (v_max - v_min) * 100, 1) if v_max > v_min else 50.0
        else:
            iv_rank = 50.0

        ts_spot = ts
        ts_vol  = ts

        # ── VIX automatico (VXN per QQQ, VIX per tutti gli altri) ──
        try:
            vix_symbol = "^VXN" if ticker.upper() in ("QQQ", "^NDX") else "^VIX"
            vix_ticker = yf.Ticker(vix_symbol)
            vix_h      = vix_ticker.history(period="5d")
            vix_val    = round(float(vix_h["Close"].iloc[-1]), 2) if not vix_h.empty else None
            ts_vix     = ts
        except Exception:
            vix_val = None
            ts_vix  = "Non disponibile"

        # Nome esteso
        try:
            nome = s.info.get("longName", ticker)
        except Exception:
            nome = ticker

        return {
            "prezzo_spot":  round(spot, 2),
            "variazione_gg":round(var, 2),
            "vol_storica":  round(vol_30, 2),
            "iv_rank":      iv_rank,
            "vix":          vix_val,
            "vix_symbol":   vix_symbol if 'vix_symbol' in dir() else "^VIX",
            "nome":         nome,
            "ultimo_agg":   h.index[-1].strftime("%d/%m/%Y"),
            "ts_spot":      ts_spot,
            "ts_vol":       ts_vol,
            "ts_vix":       ts_vix,
            "ts_ivrank":    ts,
            "errore":       None,
        }
    except Exception as e:
        return {"errore": str(e)}


# ═══════════════════════════════════════════════════════════
# MOTORE BLACK-SCHOLES
# ═══════════════════════════════════════════════════════════

@dataclass
class Par:
    S: float; K: float; T: float; r: float; sigma: float

def d1d2(p: Par):
    if p.T <= 0 or p.sigma <= 0: return 0.0, 0.0
    d1 = (np.log(p.S/p.K) + (p.r + 0.5*p.sigma**2)*p.T) / (p.sigma*np.sqrt(p.T))
    return d1, d1 - p.sigma*np.sqrt(p.T)

def prezzo_put(p: Par) -> float:
    d1, d2 = d1d2(p)
    return max(p.K*np.exp(-p.r*p.T)*si.norm.cdf(-d2) - p.S*si.norm.cdf(-d1), 0.0)

def prob_ok(p: Par) -> float:
    _, d2 = d1d2(p); return si.norm.cdf(d2)

def calc_greche(p: Par) -> dict:
    if p.T <= 0: return dict(delta=0, gamma=0, theta=0, vega=0, rho=0)
    d1, d2 = d1d2(p); f = si.norm.pdf(d1)
    return {
        "delta": round(-si.norm.cdf(-d1), 4),
        "gamma": round(f/(p.S*p.sigma*np.sqrt(p.T)), 6),
        "theta": round((-(p.S*f*p.sigma)/(2*np.sqrt(p.T)) + p.r*p.K*np.exp(-p.r*p.T)*si.norm.cdf(-d2))/365, 4),
        "vega":  round(p.S*f*np.sqrt(p.T)/100, 4),
        "rho":   round(-p.K*p.T*np.exp(-p.r*p.T)*si.norm.cdf(-d2)/100, 4),
    }

def calc_semaforo(iv, vol, ivr, vix=None):
    """Usa sia IV vs Vol.Storica che IV Rank per segnale più preciso."""
    ratio = iv/vol if vol > 0 else 1.0
    # Verde se entrambi i segnali sono positivi
    if ratio >= 1.20 and ivr >= 50:
        return {"c":"verde",  "l":"Condizioni Ottime",      "d":f"VIX {fmt(vix,2) if vix else fmt(iv,1)+'%'} &middot; IV Rank {fmt(ivr,0)}/100 &mdash; premi gonfiati, ottimo per vendere"}
    if ratio >= 1.20 or ivr >= 50:
        return {"c":"giallo", "l":"Condizioni Parzialmente Favorevoli", "d":f"VIX {fmt(vix,2) if vix else fmt(iv,1)+'%'} &middot; IV Rank {fmt(ivr,0)}/100 &mdash; un segnale positivo, l'altro neutro. Valutare con attenzione"}
    if ratio >= 0.85:
        return {"c":"giallo", "l":"Condizioni nella Norma",  "d":f"VIX {fmt(vix,2) if vix else fmt(iv,1)+'%'} &middot; IV Rank {fmt(ivr,0)}/100 &mdash; valutare il premio"}
    return          {"c":"rosso",  "l":"Condizioni Sfavorevoli",  "d":f"VIX {fmt(vix,2) if vix else fmt(iv,1)+'%'} &middot; IV Rank {fmt(ivr,0)}/100 &mdash; premi insufficienti, meglio aspettare"}

def strike_target(S, sigma, T, r, pt):
    if T <= 0 or sigma <= 0: return S
    return round(S*np.exp((r-0.5*sigma**2)*T + sigma*np.sqrt(T)*si.norm.ppf(1.0-pt)), 2)

def calc_wcs(S, K, prem, n, crash, mult=100):
    Sc        = S * (1 - crash / 100)
    lc_gross  = max(K - Sc, 0)                  # perdita lorda per azione (senza premio)
    lc_net    = lc_gross - prem                  # perdita netta per azione (al netto del premio)
    return {
        "Sc":       round(Sc, 2),
        "lc":       round(lc_net, 2),            # per contratto, netto
        "lt_gross": round(lc_gross * n * mult, 2),  # perdita lorda totale
        "lt":       round(lc_net * n * mult, 2),    # perdita netta totale
        "pt":       round(prem * n * mult, 2),
        "crash":    crash,
    }

def chiama_claude(prompt: str) -> str:
    """Chiama Claude API con web search abilitato. Gestisce il loop tool-use automaticamente."""
    import os, urllib.request, json as _json

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return "ERRORE: variabile ANTHROPIC_API_KEY non trovata. Configurala nei Secrets di Streamlit Cloud."

    def _post(payload: dict) -> dict:
        data = _json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "anthropic-beta": "web-search-2025-03-05",
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return _json.loads(resp.read().decode("utf-8"))

    messages = [{"role": "user", "content": prompt}]
    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 2000,
        "tools": [{"type": "web_search_20250305", "name": "web_search"}],
        "messages": messages,
    }

    try:
        # Loop tool-use: continua finché stop_reason != "end_turn"
        for _ in range(6):  # max 6 iterazioni di ricerca
            resp = _post(payload)
            stop = resp.get("stop_reason", "end_turn")

            if stop == "end_turn":
                # Estrai tutto il testo dai blocchi content
                testo = " ".join(
                    b["text"] for b in resp.get("content", [])
                    if b.get("type") == "text"
                )
                return testo.strip()

            if stop == "tool_use":
                # Aggiungi risposta assistant al contesto
                messages.append({"role": "assistant", "content": resp["content"]})
                # Costruisci tool_result per ogni tool_use
                tool_results = []
                for block in resp["content"]:
                    if block.get("type") == "tool_use":
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block["id"],
                            "content": block.get("content", ""),
                        })
                messages.append({"role": "user", "content": tool_results})
                payload["messages"] = messages
            else:
                break

        return "ERRORE: risposta inattesa dal modello."

    except Exception as e:
        return f"ERRORE chiamata API: {e}"


def costruisci_prompt_ai(strategia, params, dati_mercato) -> str:
    """Costruisce il prompt per Claude in base al sottostante e alla strategia."""
    spot     = params["spot"]
    nome     = params["nome"]
    tk       = params.get("ticker", "")
    dte      = params["dte"]
    sigma    = params["sigma"]
    iv_rank  = params.get("iv_rank", 0)
    vol_st   = params.get("vol_st", 0)
    vix      = params.get("vix", 0)
    var      = params.get("var", 0)

    # Tipo sottostante
    indici = ["SPY", "QQQ", "^GSPC", "^DJI", "IVV", "VOO"]
    is_indice = any(i in tk.upper() for i in indici)
    tipo_label = "indice azionario" if is_indice else "azione"

    if strategia == "put_scoperta":
        K      = params["K"]
        prem   = params["prem"]
        n      = params["n_contratti"]
        mc     = params.get("mc", 0)
        marg   = params.get("marg_tot", mc * n)
        credito_tot = round(prem * n * 100, 2)
        strat_str = f"Put Scoperta — Strike {K:.2f}, Premio {prem:.4f}/az., Credito totale +{credito_tot:.2f}€, Margine {marg:.2f}€"
    else:
        K_v    = params["bps_K_venduta"]
        K_c    = params["bps_K_comprata"]
        credito= params["bps_credito"]
        n      = params["n_contratti"]
        marg   = params.get("bps_margine_tot", 0)
        credito_tot = round(credito * n * 100, 2)
        strat_str = (f"Bull Put Spread — Strike venduto {K_v:.2f} / Strike comprato {K_c:.2f}, "
                     f"Credito netto {credito:.2f}/az. (+{credito_tot:.2f}€ totale), Margine {marg:.2f}€")

    contesto_tipo = (
        "Analizza il contesto macro USA: Fed, tassi di interesse, inflazione, stagionalità degli indici, "
        "sentiment risk-on/risk-off e trend recente del mercato azionario americano."
        if is_indice else
        "Analizza il contesto societario e settoriale: trend del settore di appartenenza, "
        "momentum relativo vs indice di riferimento (S&P 500), eventuali catalyst imminenti "
        "(earnings, guidance, news rilevanti) e posizionamento rispetto al mercato."
    )

    prompt = f"""Agisci come un Senior Derivatives Analyst specializzato in strategie short premium su opzioni.

IMPORTANTE: Prima di rispondere, usa il web search per cercare:
1. Notizie recenti su {nome} ({tk}) degli ultimi 7 giorni
2. Situazione attuale del mercato e sentiment (data di oggi: {datetime.now().strftime("%d/%m/%Y")})
3. Prossimi eventi rilevanti per {tk} (dati macro, earnings, Fed, ecc.)
Usa solo fonti aggiornate. Non usare mai dati del training se puoi trovarli con la ricerca.

Ti vengono forniti i parametri di una posizione aperta su {nome} ({tk}), un {tipo_label}.

PARAMETRI DELLA POSIZIONE:
- Strategia: {strat_str}
- Prezzo spot: {spot:.2f}
- Variazione giornaliera: {var:+.2f}%
- DTE: {dte} giorni
- IV IND: {sigma*100:.1f}%
- IV Rank: {iv_rank:.0f}/100
- Volatilità storica 30gg: {vol_st:.1f}%
- VIX: {vix:.2f}

Produci un report professionale e neutro in italiano, strutturato esattamente così:

──────────────────────────────────────
1. ANALISI DEL SOTTOSTANTE
──────────────────────────────────────
{contesto_tipo}
Basati esclusivamente su notizie e dati trovati con la ricerca web di oggi.
Massimo 5 righe. Sintetico e concreto.

──────────────────────────────────────
2. LETTURA DELLA VOLATILITÀ
──────────────────────────────────────
Analizza il rapporto tra IV IND ({sigma*100:.1f}%), IV Rank ({iv_rank:.0f}/100) e Vol. Storica ({vol_st:.1f}%).
Il VIX è a {vix:.2f}.
Rispondi: è un buon momento per vendere premium su questo sottostante?
La volatilità implicita compensa adeguatamente il rischio?

──────────────────────────────────────
3. VALUTAZIONE DELLA POSIZIONE
──────────────────────────────────────
Valuta se la struttura del trade è solida nel contesto attuale.
Dai un giudizio netto su una sola riga: SOLIDA / ACCETTABILE / RISCHIOSA
Seguito da motivazione in massimo 3 righe.

──────────────────────────────────────
4. RISCHI SPECIFICI DA MONITORARE
──────────────────────────────────────
Elenca esattamente 3 rischi concreti e specifici per questa posizione nei prossimi {dte} giorni.
Basati su eventi reali trovati con la ricerca web — niente generalità.

──────────────────────────────────────
5. INDICATORI DA TENERE D'OCCHIO
──────────────────────────────────────
Elenca esattamente 4 elementi con date reali: dati macro imminenti, eventi societari, livelli tecnici chiave.
Usa solo eventi trovati con la ricerca web, con date precise.

──────────────────────────────────────
Stile: professionale, neutro, sintetico. Niente previsioni di prezzo. Niente sensazionalismo.
Lunghezza totale: massimo una pagina A4."""
    return prompt


def costruisci_prompt_advisor(ticker: str, nome: str, dati: dict) -> str:
    """Prompt istituzionale per Strategy Advisor — classifica regime e seleziona strategia."""
    spot     = dati.get("prezzo_spot", 0)
    vix      = dati.get("vix", 0) or 0
    iv_rank  = dati.get("iv_rank", 50)
    vol_st   = dati.get("vol_storica", 0) or 0
    var      = dati.get("variazione_gg", 0) or 0
    vix_sym  = dati.get("vix_symbol", "^VIX")
    oggi     = datetime.now().strftime("%d/%m/%Y")

    return f"""Sei un portfolio manager senior specializzato in derivati con background quantitativo istituzionale (hedge fund / investment bank).

Il tuo compito è analizzare {nome} ({ticker}) e produrre una raccomandazione di strategia in opzioni di qualità istituzionale.

DATI DI MERCATO ATTUALI ({oggi}):
- Prezzo spot: {spot:.2f}
- Variazione giornaliera: {var:+.2f}%
- Volatilità storica 30gg: {vol_st:.1f}%
- {vix_sym.replace('^','')}: {vix:.2f}
- IV Rank: {iv_rank:.0f}/100
- Rapporto IV/HV: {(vix/vol_st if vol_st > 0 else 0):.2f}x

ISTRUZIONI:
Esegui una ricerca web approfondita su:
1. Condizioni macro attuali (Fed, inflazione, tassi)
2. Notizie e catalyst recenti su {nome}
3. Posizionamento istituzionale e sentiment di mercato
4. Livelli tecnici chiave e trend su {ticker}
5. Put/call ratio e skew di volatilità se disponibili

Poi produci un report ESATTAMENTE in questo formato (usa i separatori ─────):

─────────────────────────────────────
SINTESI ESECUTIVA
[1-2 righe: situazione attuale e raccomandazione principale]

─────────────────────────────────────
REGIME DI MERCATO
Volatilità: [BASSA / MEDIA / ALTA / ESTREMA] — motivazione breve
Trend: [RIALZISTA / RIBASSISTA / LATERALE] — timeframe e motivazione
Contesto: [RISK-ON / RISK-OFF / NEUTRO] — motivazione
Classificazione: [es. "Alta volatilità, laterale, risk-off post-correzione"]

─────────────────────────────────────
SNAPSHOT INDICATORI
[Tabella con i valori chiave trovati con la ricerca: IV implicita, VIX, IV Rank, trend tecnico, momentum, sentiment]

─────────────────────────────────────
STRATEGIA CONSIGLIATA
Nome: [strategia specifica]
Confidenza: [BASSA / MEDIA / ALTA]
Driver principali: [3 bullet con motivazioni quantitative precise]
Parametri suggeriti: [DTE, strike, larghezza spread se applicabile]
Perché NON le alternative: [breve motivazione per ciascuna strategia scartata]

─────────────────────────────────────
RAGIONAMENTO ISTITUZIONALE
[Paragrafo dettagliato, tono da strategist derivati. Includi: contesto macro, struttura della volatilità, positioning istituzionale, logica del trade]

─────────────────────────────────────
ANALISI SCENARI

SCENARIO BASE (probabilità ~50%):
- Evoluzione volatilità attesa
- Impatto sulla strategia
- Azione consigliata

SCENARIO RIALZISTA (probabilità ~25%):
- Evoluzione volatilità attesa
- Impatto sulla strategia
- Azione consigliata

SCENARIO RIBASSISTA (probabilità ~25%):
- Evoluzione volatilità attesa
- Impatto sulla strategia
- Azione consigliata

─────────────────────────────────────
RISCHI DA MONITORARE
[4 rischi specifici con trigger precisi e livelli di prezzo/volatilità]

─────────────────────────────────────
CONDIZIONE NO-TRADE
[Se il contesto non è favorevole per nessuna strategia, spiega perché e quando rientrare]
─────────────────────────────────────

Usa solo dati trovati con la ricerca web. Sii preciso, analitico, istituzionale. Niente generici."""
    """Genera un PDF con l'analisi AI della posizione."""
    if not REPORTLAB_OK:
        return None
    import io as _io
    buf = _io.BytesIO()
    W, H = A4
    BG      = colors.HexColor("#080C10")
    CYAN    = colors.HexColor("#00C2FF")
    GREEN   = colors.HexColor("#00E5A0")
    MUTED   = colors.HexColor("#8B9FC0")
    SURFACE = colors.HexColor("#0F1E2E")
    BORDER  = colors.HexColor("#243550")
    WHITE   = colors.HexColor("#E8EDF5")
    DARK    = colors.HexColor("#060A0E")
    TEXT    = colors.HexColor("#C8D4E8")
    data_oggi = datetime.now().strftime("%d/%m/%Y")
    strat_label = "Vendita Put Scoperta" if strategia == "put_scoperta" else "Bull Put Spread"

    def on_page(canv, doc):
        canv.saveState()
        canv.setFillColor(BG)
        canv.rect(0, 0, W, H, fill=1, stroke=0)
        canv.setFillColor(DARK)
        canv.rect(0, H - 1.6*cm, W, 1.6*cm, fill=1, stroke=0)
        canv.setFont("Helvetica-Bold", 12)
        canv.setFillColor(CYAN)
        canv.drawString(1.5*cm, H - 1.05*cm, "Phinance")
        canv.setFont("Helvetica", 8)
        canv.setFillColor(WHITE)
        canv.drawString(4.2*cm, H - 1.05*cm, f"| Analisi AI — {strat_label} — {nome}")
        canv.setFillColor(MUTED)
        canv.drawRightString(W - 1.5*cm, H - 1.05*cm, data_oggi)
        canv.setStrokeColor(BORDER)
        canv.setLineWidth(0.5)
        canv.line(1.5*cm, H - 1.6*cm, W - 1.5*cm, H - 1.6*cm)
        canv.setFont("Helvetica", 7)
        canv.setFillColor(MUTED)
        canv.drawCentredString(W/2, 0.65*cm,
            "Solo a scopo educativo — non costituisce consulenza finanziaria — Phinance v5.1")
        canv.line(1.5*cm, 1.05*cm, W - 1.5*cm, 1.05*cm)
        canv.restoreState()

    doc = SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=2.4*cm, bottomMargin=1.8*cm)

    def ps(name, font="Helvetica", size=9, color=None, align=TA_LEFT, leading=None, spaceBefore=0, spaceAfter=0):
        c = color if color is not None else TEXT
        return ParagraphStyle(name, fontName=font, fontSize=size, textColor=c,
                              alignment=align, leading=leading or size*1.4,
                              spaceBefore=spaceBefore, spaceAfter=spaceAfter)

    s_title    = ps("t",    "Helvetica-Bold", 18, CYAN,  spaceAfter=4)
    s_sub      = ps("s",    "Helvetica",       9, MUTED, spaceAfter=6)
    s_section  = ps("h2",   "Helvetica-Bold", 10, CYAN,  spaceBefore=10, spaceAfter=3)
    s_body     = ps("b",    "Helvetica",       8, TEXT,  leading=13, spaceAfter=2)
    s_solida   = ps("sol",  "Helvetica-Bold",  9, GREEN, spaceAfter=2)
    s_accett   = ps("acc",  "Helvetica-Bold",  9, colors.HexColor("#FFB547"), spaceAfter=2)
    s_risch    = ps("ris",  "Helvetica-Bold",  9, colors.HexColor("#FF5A5A"), spaceAfter=2)

    # I 5 titoli sezione attesi — usati per distinguerli dai punti elenco nel corpo
    TITOLI_SEZIONE = {
        "1. ANALISI DEL SOTTOSTANTE",
        "2. LETTURA DELLA VOLATILITÀ",
        "3. VALUTAZIONE DELLA POSIZIONE",
        "4. RISCHI SPECIFICI DA MONITORARE",
        "5. INDICATORI DA TENERE D'OCCHIO",
    }

    story = []
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Analisi AI della Posizione", s_title))
    story.append(Paragraph(f"{nome}  ·  {strat_label}  ·  {data_oggi}", s_sub))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
    story.append(Spacer(1, 0.3*cm))

    import re as _re

    def pulisci(t):
        t = _re.sub(r'\*\*(.*?)\*\*', r'\1', t)
        t = _re.sub(r'\*(.*?)\*',     r'\1', t)
        t = _re.sub(r'^#{1,3}\s*',    '',    t, flags=_re.MULTILINE)
        t = _re.sub(r'^\s*[-•]\s*',   '',    t, flags=_re.MULTILINE)
        return t.strip()

    def is_titolo_sezione(r):
        """True solo se la riga corrisponde a uno dei 5 titoli sezione attesi."""
        r_upper = _re.sub(r'^[1-5][\.\)]\s*', lambda m: m.group(0), r).upper().strip()
        # Controlla corrispondenza esatta o parziale con i titoli attesi
        for t in TITOLI_SEZIONE:
            if t in r_upper or r_upper in t:
                return True
        return False

    sezioni = _re.split(r'─{10,}', testo)
    trovata_prima_sezione = False
    for blocco in sezioni:
        blocco = blocco.strip()
        if not blocco:
            continue
        righe = [r for r in blocco.split("\n") if r.strip()]
        if not righe:
            continue

        prima = pulisci(righe[0])
        if is_titolo_sezione(prima):
            trovata_prima_sezione = True
            story.append(Spacer(1, 0.2*cm))
            story.append(Paragraph(prima.upper(), s_section))
            story.append(HRFlowable(width="100%", thickness=0.3, color=BORDER))
            story.append(Spacer(1, 0.1*cm))
            corpo = righe[1:]
        else:
            # Prima della sezione 1: mostra il testo ma salta righe che sono titoli ridondanti
            # (es. "REPORT PROFESSIONALE - ...")
            corpo = [_re.sub(r'\bPROFESSIONALE\b\s*[-–]?\s*', '', pulisci(r), flags=_re.IGNORECASE).strip()
                     if _re.search(r'\bPROFESSIONALE\b', r, _re.IGNORECASE) else r
                     for r in righe]
            corpo = [r for r in corpo if r.strip()]

        for riga in corpo:
            riga = pulisci(riga)
            if not riga:
                continue
            # Colora giudizio posizione
            r_up = riga.upper().strip()
            if r_up in ("SOLIDA", "✓ SOLIDA", "POSIZIONE: SOLIDA"):
                story.append(Paragraph(riga, s_solida))
            elif r_up in ("ACCETTABILE", "✓ ACCETTABILE", "POSIZIONE: ACCETTABILE"):
                story.append(Paragraph(riga, s_accett))
            elif r_up in ("RISCHIOSA", "✗ RISCHIOSA", "POSIZIONE: RISCHIOSA"):
                story.append(Paragraph(riga, s_risch))
            elif "SOLIDA" in r_up and len(riga) < 30:
                story.append(Paragraph(riga, s_solida))
            elif "ACCETTABILE" in r_up and len(riga) < 30:
                story.append(Paragraph(riga, s_accett))
            elif "RISCHIOSA" in r_up and len(riga) < 30:
                story.append(Paragraph(riga, s_risch))
            else:
                story.append(Paragraph(riga, s_body))

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    buf.seek(0)
    return buf.getvalue()


def genera_pdf_scenari(strategia, params):
    """
    Genera un PDF con UN unico scenario completo spot -10% → +10%,
    50 prezzi, valori BS a T residuo = DTE/2.
    """
    if not REPORTLAB_OK:
        return None

    # ── Estrai parametri ─────────────────────────────────────────────────────
    spot      = params["spot"]
    sigma     = params["sigma"]
    T         = params["T"]
    r         = params["r"]
    nome      = params["nome"]
    dte       = params["dte"]
    data_oggi = datetime.now().strftime("%d/%m/%Y")

    if strategia == "put_scoperta":
        K      = params["K"]
        prem   = params["prem"]
        n      = params["n_contratti"]
        mult   = 100
        K_ref  = K
    else:
        K_v    = params["bps_K_venduta"]
        K_c    = params["bps_K_comprata"]
        credito= params["bps_credito"]
        n      = params["n_contratti"]
        mult   = 100
        pv_reale = params.get("prezzo_put_venduta")
        pc_reale = params.get("prezzo_put_comprata")
        K_ref  = K_v

    # ── Monte Carlo per sintesi statistica (pagina 1) ────────────────────────
    np.random.seed(42)
    prezzi_sim = spot * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*np.random.standard_normal(10000))
    p75 = float(np.percentile(prezzi_sim, 75))
    p50 = float(np.percentile(prezzi_sim, 50))
    p10 = float(np.percentile(prezzi_sim, 10))
    pct_pos = float(np.mean(prezzi_sim > K_ref)) * 100
    pct_neg = 100 - pct_pos

    T_residuo = max(T * 0.5, 1/365)

    def bs_put_price(S, K_opt, T_opt, r_opt, sig):
        if T_opt <= 0 or S <= 0:
            return max(K_opt - S, 0)
        from scipy.stats import norm as _norm
        d1 = (np.log(S/K_opt) + (r_opt + 0.5*sig**2)*T_opt) / (sig*np.sqrt(T_opt))
        d2 = d1 - sig*np.sqrt(T_opt)
        return max(round(K_opt*np.exp(-r_opt*T_opt)*_norm.cdf(-d2) - S*_norm.cdf(-d1), 2), 0.0)

    # ── Setup ReportLab ───────────────────────────────────────────────────────
    buf = io.BytesIO()
    W, H = A4

    # Palette — testi fuori tabella su sfondo scuro
    BG      = colors.HexColor("#080C10")
    CYAN    = colors.HexColor("#00C2FF")
    GREEN   = colors.HexColor("#00E5A0")
    RED     = colors.HexColor("#FF5A5A")
    MUTED   = colors.HexColor("#8B9FC0")
    SURFACE = colors.HexColor("#0F1E2E")
    BORDER  = colors.HexColor("#243550")
    WHITE   = colors.HexColor("#E8EDF5")
    DARK    = colors.HexColor("#060A0E")
    TEXT    = colors.HexColor("#C8D4E8")   # testo leggibile su sfondo scuro

    strat_label = "Vendita Put Scoperta" if strategia == "put_scoperta" else "Bull Put Spread"

    def on_page(canv, doc):
        canv.saveState()
        # Sfondo scuro sull'intera pagina
        canv.setFillColor(BG)
        canv.rect(0, 0, W, H, fill=1, stroke=0)
        # Header band
        canv.setFillColor(DARK)
        canv.rect(0, H - 1.6*cm, W, 1.6*cm, fill=1, stroke=0)
        canv.setFont("Helvetica-Bold", 12)
        canv.setFillColor(CYAN)
        canv.drawString(1.5*cm, H - 1.05*cm, "Phinance")
        canv.setFont("Helvetica", 8)
        canv.setFillColor(WHITE)
        canv.drawString(4.2*cm, H - 1.05*cm, f"| Analisi Scenari — {strat_label}")
        canv.setFillColor(MUTED)
        canv.drawRightString(W - 1.5*cm, H - 1.05*cm, data_oggi)
        canv.setStrokeColor(BORDER)
        canv.setLineWidth(0.5)
        canv.line(1.5*cm, H - 1.6*cm, W - 1.5*cm, H - 1.6*cm)
        # Footer
        canv.setFont("Helvetica", 7)
        canv.setFillColor(MUTED)
        canv.drawCentredString(W/2, 0.65*cm,
            "Solo a scopo educativo — non costituisce consulenza finanziaria — Phinance v5.1")
        canv.line(1.5*cm, 1.05*cm, W - 1.5*cm, 1.05*cm)
        canv.restoreState()

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=2.4*cm, bottomMargin=1.8*cm,
    )

    def ps(name, font="Helvetica", size=9, color=None, align=TA_LEFT,
           leading=None, spaceBefore=0, spaceAfter=0):
        c = color if color is not None else TEXT
        return ParagraphStyle(name, fontName=font, fontSize=size,
                              textColor=c, alignment=align,
                              leading=leading or size*1.4,
                              spaceBefore=spaceBefore, spaceAfter=spaceAfter)

    s_title   = ps("title", "Helvetica-Bold", 18, CYAN,  TA_LEFT, spaceAfter=4)
    s_sub     = ps("sub",   "Helvetica",       9, MUTED, TA_LEFT, spaceAfter=2)
    s_h2      = ps("h2",    "Helvetica-Bold", 11, CYAN,  TA_LEFT, spaceBefore=8, spaceAfter=4)
    s_body    = ps("body",  "Helvetica",       8, TEXT,  TA_LEFT, leading=13, spaceAfter=3)
    s_nota    = ps("nota",  "Helvetica",       7, MUTED, TA_LEFT, leading=11, spaceAfter=3)
    s_comment = ps("comm",  "Helvetica",       8, TEXT,  TA_LEFT, leading=12)

    story = []

    # ═══════════════════════════════════════════════════════
    # PAGINA 1 — INTRO + PARAMETRI + STATISTICHE
    # ═══════════════════════════════════════════════════════
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Analisi Scenari — Report Operativo", s_title))
    story.append(Paragraph(f"{nome}  ·  {strat_label}  ·  Generato il {data_oggi}", s_sub))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
    story.append(Spacer(1, 0.35*cm))

    story.append(Paragraph(
        "Questo report analizza la posizione su una fascia <b>\u221210% / +10%</b> rispetto allo spot, "
        "con 30 livelli equidistanti. Valori calcolati con <b>Black-Scholes</b> a T residuo = DTE/2.",
        s_body))
    story.append(Paragraph(
        "Il P&L include il credito gi\xe0 incassato. Solo a scopo educativo — non costituisce consulenza finanziaria.",
        s_nota))
    story.append(Spacer(1, 0.3*cm))

    # ── Tabella parametri ────────────────────────────────────────────────────
    story.append(Paragraph("Parametri operazione", s_h2))
    if strategia == "put_scoperta":
        param_rows = [
            ["Strumento",   nome,          "Strike",           f"{K:.2f}"],
            ["Prezzo Spot", f"{spot:.2f}", "Premio / az.",     f"{prem:.4f}"],
            ["DTE",         f"{dte} gg",   "Contratti",        str(n)],
            ["IV",          f"{sigma*100:.1f}%", "Credito tot.", f"+{prem*n*mult:.2f} \u20ac"],
        ]
    else:
        pv_str = f"{pv_reale:.2f}" if pv_reale else f"{credito:.4f}"
        pc_str = f"{pc_reale:.2f}" if pc_reale else "\u2014"
        param_rows = [
            ["Strumento",    nome,              "Strike vend.",     f"{K_v:.2f}"],
            ["Prezzo Spot",  f"{spot:.2f}",     "Strike comp.",     f"{K_c:.2f}"],
            ["DTE",          f"{dte} gg",       "Put vend. (bid)",  pv_str],
            ["IV",           f"{sigma*100:.1f}%","Put comp. (ask)", pc_str],
            ["Contratti",    str(n),            "Credito netto",    f"{credito:.2f} (+{credito*n*mult:.0f}\u20ac)"],
        ]

    total_w = W - 3*cm
    col_w4  = [total_w*0.20, total_w*0.30, total_w*0.24, total_w*0.26]
    param_style = TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), SURFACE),
        ("GRID",        (0,0), (-1,-1), 0.3, BORDER),
        ("FONTNAME",    (0,0), (0,-1),  "Helvetica-Bold"),
        ("FONTNAME",    (2,0), (2,-1),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 8),
        ("TEXTCOLOR",   (0,0), (0,-1),  MUTED),
        ("TEXTCOLOR",   (2,0), (2,-1),  MUTED),
        ("TEXTCOLOR",   (1,0), (1,-1),  WHITE),
        ("TEXTCOLOR",   (3,0), (3,-1),  CYAN),
        ("PADDING",     (0,0), (-1,-1), 6),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("WORDWRAP",    (0,0), (-1,-1), True),
    ])
    story.append(Table(param_rows, colWidths=col_w4, style=param_style))
    story.append(Spacer(1, 0.3*cm))

    # ── Sintesi statistica ───────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.3, color=BORDER))
    story.append(Paragraph("Sintesi statistica", s_h2))
    stat_rows = [
        ["Prezzo mediano",      f"{p50:.2f}",  "Prob. sopra strike",   f"{pct_pos:.1f}%  \u2713"],
        ["P75\xb0 percentile",  f"{p75:.2f}",  "Prob. sotto strike",   f"{pct_neg:.1f}%  \u2717"],
        ["P10\xb0 percentile",  f"{p10:.2f}",  "Dev. std. simulata",   f"{float(np.std(prezzi_sim)):.2f}"],
    ]
    stat_style = TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), SURFACE),
        ("GRID",        (0,0), (-1,-1), 0.3, BORDER),
        ("FONTNAME",    (0,0), (0,-1),  "Helvetica-Bold"),
        ("FONTNAME",    (2,0), (2,-1),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 8),
        ("TEXTCOLOR",   (0,0), (0,-1),  MUTED),
        ("TEXTCOLOR",   (2,0), (2,-1),  MUTED),
        ("TEXTCOLOR",   (1,0), (1,-1),  CYAN),
        ("TEXTCOLOR",   (3,0), (3,0),   GREEN),
        ("TEXTCOLOR",   (3,1), (3,1),   RED),
        ("TEXTCOLOR",   (3,2), (3,2),   WHITE),
        ("PADDING",     (0,0), (-1,-1), 6),
    ])
    story.append(Table(stat_rows, colWidths=col_w4, style=stat_style))
    story.append(Spacer(1, 0.35*cm))

    # ── Gestione della posizione ─────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.3, color=BORDER))
    story.append(Paragraph("Gestione della posizione", s_h2))

    if strategia == "put_scoperta":
        credito_tot = prem * n * mult
        tp_val      = round(credito_tot * 0.50, 0)   # take profit 50%
        sl_val      = round(credito_tot * 2.00, 0)   # stop loss 2x
        tp_premio   = round(prem * 0.50, 4)           # premio a cui riacquistare
        sl_premio   = round(prem * 2.00, 4)
        data_21dte  = (datetime.now() + __import__('datetime').timedelta(days=max(dte-21,0))).strftime("%d/%m/%Y")
        gest_rows = [
            ["Take Profit 50%",   f"Riacquista put a {tp_premio:.2f}",   f"+{tp_val:.2f} \u20ac incassati"],
            ["Stop Loss 2x",      f"Chiudi se put vale {sl_premio:.2f}", f"-{sl_val:.2f} \u20ac perdita"],
            ["Chiudi a 21 DTE",   f"Entro il {data_21dte}",              "Evita rischio Gamma elevato"],
            ["Delta ottimale",    "0.16 \u2013 0.20",                    "84\u201380% prob. di successo"],
            ["Apertura ideale",   "45 DTE",                              "Massima efficienza Theta decay"],
            ["IV Rank minimo",    "> 50 / 100",                          "Regola quantitativa \u2014 premi sufficienti"],
        ]
    else:
        credito_tot = credito * n * mult
        tp_val      = round(credito_tot * 0.50, 0)
        sl_val      = round(credito_tot * 2.00, 0)
        tp_credito  = round(credito * 0.50, 2)
        sl_credito  = round(credito * 2.00, 2)
        data_21dte  = (datetime.now() + __import__('datetime').timedelta(days=max(dte-21,0))).strftime("%d/%m/%Y")
        gest_rows = [
            ["Take Profit 50%",   f"Chiudi spread a {tp_credito:.2f} costo", f"+{tp_val:.2f} \u20ac incassati"],
            ["Stop Loss 2x",      f"Chiudi se spread vale {sl_credito:.2f}", f"-{sl_val:.2f} \u20ac perdita"],
            ["Chiudi a 21 DTE",   f"Entro il {data_21dte}",                  "Evita rischio Gamma elevato"],
            ["Margine bloccato",  f"{params.get('bps_margine_tot', 0):.0f} \u20ac",  f"{params.get('n_contratti',n)} contratti \u00d7 {params.get('bps_margine_c', 0):.0f} \u20ac"],
            ["IV Rank minimo",    "> 30\u201340 / 100",                      "Premi strutturalmente elevati"],
            ["Apertura ideale",   "30\u201345 DTE",                          "Theta decay ottimale"],
        ]

    gest_style = TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), SURFACE),
        ("GRID",          (0,0), (-1,-1), 0.3, BORDER),
        ("FONTNAME",      (0,0), (0,-1),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("TEXTCOLOR",     (0,0), (0,-1),  MUTED),
        ("TEXTCOLOR",     (1,0), (1,-1),  WHITE),
        ("TEXTCOLOR",     (2,0), (2,-1),  CYAN),
        ("PADDING",       (0,0), (-1,-1), 5),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,0), (-1,-1), [SURFACE, colors.HexColor("#0A1828")]),
        # TP verde, SL rosso
        ("TEXTCOLOR",     (2,0), (2,0),   GREEN),
        ("TEXTCOLOR",     (2,1), (2,1),   RED),
    ])
    col_w3 = [total_w*0.26, total_w*0.37, total_w*0.37]
    story.append(Table(gest_rows, colWidths=col_w3, style=gest_style))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    # PAGINA 2 — SCENARIO UNICO spot -10% → +10% (30 righe)
    # ═══════════════════════════════════════════════════════
    prezzi_sc = list(np.linspace(spot * 0.90, spot * 1.10, 30))  # 30 righe

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Scenario Completo: Spot \u221210% \u2192 +10%", ps(
        "sc_title", "Helvetica-Bold", 13, CYAN, TA_LEFT, spaceAfter=2)))
    story.append(Paragraph(
        f"Fascia: <b>{spot*0.90:.2f} \u2013 {spot*1.10:.2f}</b>  \u00b7  30 livelli  \u00b7  "
        f"BS a T residuo: <b>{max(int(T*365*0.5), 1)} gg</b>  \u00b7  IV: <b>{sigma*100:.1f}%</b>",
        ps("sc_sub", "Helvetica", 8, MUTED, TA_LEFT, spaceAfter=4)))
    story.append(HRFlowable(width="100%", thickness=0.5, color=CYAN))
    story.append(Spacer(1, 0.2*cm))

    # Costruisci righe tabella
    if strategia == "put_scoperta":
        header = ["Prezzo", "Val. Put", "P&L / az.", "P&L Tot. (\u20ac)", "Esito"]
    else:
        header = ["Prezzo", "Put Vend.", "Put Comp.", "Spread", "P&L / az.", "P&L Tot. (\u20ac)", "Esito"]

    rows = [header]
    for sp in prezzi_sc:
        if strategia == "put_scoperta":
            vp     = bs_put_price(sp, K, T_residuo, r, sigma)
            pnl_az = round(prem - vp, 2)
            pnl_t  = round(pnl_az * n * mult, 0)
            esito  = "\u2713 Prof." if pnl_t >= 0 else "\u2717 Perd."
            rows.append([f"{sp:.2f}", f"{vp:.2f}", f"{pnl_az:+.2f}", f"{pnl_t:+.2f}", esito])
        else:
            vv     = bs_put_price(sp, K_v, T_residuo, r, sigma)
            vc     = bs_put_price(sp, K_c, T_residuo, r, sigma)
            vspr   = round(vv - vc, 2)
            pnl_az = round(credito - vspr, 2)
            pnl_t  = round(pnl_az * n * mult, 0)
            esito  = "\u2713 Prof." if pnl_t >= 0 else "\u2717 Perd."
            rows.append([f"{sp:.2f}", f"{vv:.2f}", f"{vc:.2f}", f"{vspr:.2f}",
                         f"{pnl_az:+.2f}", f"{pnl_t:+.2f}", esito])

    if strategia == "put_scoperta":
        cw = [total_w*0.19, total_w*0.17, total_w*0.19, total_w*0.22, total_w*0.23]
    else:
        cw = [total_w*0.14, total_w*0.12, total_w*0.12, total_w*0.12,
              total_w*0.14, total_w*0.17, total_w*0.19]

    tbl_style = [
        ("BACKGROUND",    (0,0),  (-1,0),  SURFACE),
        ("FONTNAME",      (0,0),  (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),  (-1,0),  7),
        ("TEXTCOLOR",     (0,0),  (-1,0),  CYAN),
        ("ALIGN",         (0,0),  (-1,0),  "CENTER"),
        ("BOTTOMPADDING", (0,0),  (-1,0),  4),
        ("TOPPADDING",    (0,0),  (-1,0),  4),
        ("FONTNAME",      (0,1),  (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,1),  (-1,-1), 7),
        ("TEXTCOLOR",     (0,1),  (-1,-1), WHITE),
        ("ALIGN",         (1,1),  (-1,-1), "RIGHT"),
        ("ALIGN",         (0,1),  (0,-1),  "CENTER"),
        ("ALIGN",         (-1,1), (-1,-1), "CENTER"),
        ("GRID",          (0,0),  (-1,-1), 0.25, BORDER),
        ("ROWBACKGROUNDS",(0,1),  (-1,-1), [BG, SURFACE]),
        ("TOPPADDING",    (0,1),  (-1,-1), 2),
        ("BOTTOMPADDING", (0,1),  (-1,-1), 2),
        ("TEXTCOLOR",     (0,1),  (0,-1),  CYAN),
        ("FONTNAME",      (0,1),  (0,-1),  "Helvetica-Bold"),
    ]

    for i, row in enumerate(rows[1:], start=1):
        clr_e = GREEN if "\u2713" in row[-1] else RED
        clr_p = GREEN if "+" in row[-2] else RED
        tbl_style.append(("TEXTCOLOR", (-1, i), (-1, i), clr_e))
        tbl_style.append(("FONTNAME",  (-1, i), (-1, i), "Helvetica-Bold"))
        tbl_style.append(("TEXTCOLOR", (-2, i), (-2, i), clr_p))
        tbl_style.append(("FONTNAME",  (-2, i), (-2, i), "Helvetica-Bold"))

    story.append(Table(rows, colWidths=cw, style=TableStyle(tbl_style), repeatRows=1))
    story.append(Spacer(1, 0.3*cm))

    # Break-even: interpolazione lineare sul cambio di segno del P&L Tot nella tabella
    # rows[1:] = righe dati, colonna P&L Tot = indice -2 (penultima, prima di Esito)
    be_str = "n.d."
    for i in range(len(rows) - 2):  # rows[1] = prima riga dati
        row_a = rows[i + 1]
        row_b = rows[i + 2]
        try:
            pnl_a = float(row_a[-2])
            pnl_b = float(row_b[-2])
            s_a   = float(row_a[0])
            s_b   = float(row_b[0])
        except (ValueError, IndexError):
            continue
        if pnl_a * pnl_b < 0:  # cambio di segno preciso
            be = s_a + (s_b - s_a) * (-pnl_a) / (pnl_b - pnl_a)
            be_str = f"{be:.2f}"
            break
        elif pnl_a == 0:
            be_str = f"{s_a:.2f}"
            break

    n_prof = sum(1 for row in rows[1:] if "\u2713" in row[-1])
    if strategia == "put_scoperta":
        perdita_max = f"{-(K - prem)*n*mult:.2f} \u20ac (teorica)"
    else:
        perdita_max = f"{-(K_v-K_c-credito)*n*mult:.2f} \u20ac"

    story.append(Paragraph(
        f"<b>Riepilogo:</b> {n_prof}/30 livelli in profitto, {30-n_prof} in perdita.  "
        f"Break-even: <b>{be_str}</b>  \u00b7  Perdita max: <b>{perdita_max}</b>.",
        s_comment))

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    buf.seek(0)
    return buf.getvalue()



# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════

with st.sidebar:
    # Pulsante cambia strategia
    _strat_labels = {
        "put_scoperta":    "&#9679; Put Scoperta",
        "bull_put_spread": "&#9670; Bull Put Spread",
        "long_call":       "&#9650; Long Call",
        "long_put":        "&#9660; Long Put",
    }
    strat_label = _strat_labels.get(STRATEGIA, STRATEGIA)
    st.markdown(f"<div style='font-family:var(--font-mono);font-size:0.58rem;color:var(--text-muted);letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.4rem'>Strategia attiva</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-family:var(--font-body);font-size:0.9rem;font-weight:600;color:var(--accent-cyan);margin-bottom:0.6rem'>{strat_label}</div>", unsafe_allow_html=True)
    if st.button("&#8635; Cambia strategia", use_container_width=True):
        st.session_state.strategia = None
        st.rerun()
    st.markdown("<hr style='border:none;border-top:1px solid var(--border-subtle);margin:1rem 0'>", unsafe_allow_html=True)

    st.markdown("<div class='sb-section' style='border-top:none;margin-top:0'>Strumento</div>", unsafe_allow_html=True)

    scelta = st.selectbox(
        "Sottostante",
        options=list(TICKER_DISPONIBILI.keys()),
        index=0,
        label_visibility="collapsed",
        help="Seleziona lo strumento. Il VIX viene scaricato in automatico."
    )
    tk = TICKER_DISPONIBILI[scelta]
    if tk == "MANUALE":
        raw = st.text_input("Ticker", value="SPY", label_visibility="collapsed")
        tk  = raw.upper().strip()

    aggiorna = st.button("&#8635;  Aggiorna Tutti i Dati")

    st.markdown("<div class='sb-section'>Parametri Opzione</div>", unsafe_allow_html=True)

    # ── DTE ──
    if "slider_dte" not in st.session_state: st.session_state["slider_dte"] = 45
    if "input_dte" not in st.session_state: st.session_state["input_dte"] = st.session_state["slider_dte"]
    st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>GIORNI ALLA SCADENZA (DTE)</span>", unsafe_allow_html=True)
    col_s, col_n = st.columns([2,1])
    with col_s:
        st.slider("dte_s", 1, 365, key="slider_dte",
            label_visibility="collapsed",
            on_change=lambda: st.session_state.update({"input_dte": st.session_state["slider_dte"]}),
            help="Giorni calendariali alla scadenza. Ottimale: 35-49 giorni.")
    with col_n:
        st.number_input("dte_n", 1, 365, key="input_dte", format="%d",
            label_visibility="collapsed",
            on_change=lambda: st.session_state.update({"slider_dte": int(st.session_state["input_dte"])}))
    dte = int(st.session_state["slider_dte"])

    # ── IV IND ──
    if "slider_iv" not in st.session_state: st.session_state["slider_iv"] = 20.0
    if "input_iv" not in st.session_state: st.session_state["input_iv"] = st.session_state["slider_iv"]
    st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>IV IND (%)</span>", unsafe_allow_html=True)
    col_s, col_n = st.columns([2,1])
    with col_s:
        st.slider("iv_s", 1.0, 150.0, step=0.5, key="slider_iv",
            label_visibility="collapsed",
            on_change=lambda: st.session_state.update({"input_iv": st.session_state["slider_iv"]}),
            help="Volatilità implicita del sottostante — 'IV IND' sul tuo broker. Usato da Black-Scholes per tutti i calcoli.")
    with col_n:
        st.number_input("iv_n", 1.0, 150.0, step=0.5, format="%.2f", key="input_iv",
            label_visibility="collapsed",
            on_change=lambda: st.session_state.update({"slider_iv": float(st.session_state["input_iv"])}))
    if "input_iv" not in st.session_state: st.session_state["input_iv"] = st.session_state["slider_iv"]
    # Aggiorna anche _iv_pct_init per compatibilità con il resto del codice
    st.session_state["_iv_pct_init"] = float(st.session_state["slider_iv"])
    iv_pct = float(st.session_state["slider_iv"])

    # ── IV RANK (solo Put Scoperta / Bull Put Spread) ──
    if "slider_ivr" not in st.session_state: st.session_state["slider_ivr"] = 50.0
    if "input_ivr" not in st.session_state: st.session_state["input_ivr"] = st.session_state["slider_ivr"]
    if STRATEGIA not in ("long_call", "long_put"):
        st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>IV RANK (0–100)</span>", unsafe_allow_html=True)
        col_s, col_n = st.columns([2,1])
        with col_s:
            st.slider("ivr_s", 0.0, 100.0, step=0.5, key="slider_ivr",
                label_visibility="collapsed",
                on_change=lambda: st.session_state.update({"input_ivr": st.session_state["slider_ivr"]}),
                help="Posizione della IV attuale rispetto agli ultimi 12 mesi. Sopra 50 = buon momento per vendere.")
        with col_n:
            st.number_input("ivr_n", 0.0, 100.0, step=0.5, format="%.2f", key="input_ivr",
                label_visibility="collapsed",
                on_change=lambda: st.session_state.update({"slider_ivr": float(st.session_state["input_ivr"])}))
    iv_rank_reale = float(st.session_state["slider_ivr"])

    r_pct = 4.5

    st.markdown("<div class='sb-section'>Posizione & Rischio</div>", unsafe_allow_html=True)

    # ── NUMERO CONTRATTI ──
    if "slider_nc" not in st.session_state: st.session_state["slider_nc"] = 1
    if "input_nc" not in st.session_state: st.session_state["input_nc"] = st.session_state["slider_nc"]
    st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>NUMERO DI CONTRATTI</span>", unsafe_allow_html=True)
    col_s, col_n = st.columns([2,1])
    with col_s:
        st.slider("nc_s", 1, 50, key="slider_nc",
            label_visibility="collapsed",
            on_change=lambda: st.session_state.update({"input_nc": st.session_state["slider_nc"]}),
            help="Quanti contratti vuoi vendere. Ogni contratto copre 100 azioni.")
    with col_n:
        st.number_input("nc_n", 1, 50, key="input_nc", format="%d",
            label_visibility="collapsed",
            on_change=lambda: st.session_state.update({"slider_nc": int(st.session_state["input_nc"])}))
    n_contratti = int(st.session_state["slider_nc"])

    # ── MARGINE BROKER (solo PS) ──
    if STRATEGIA == "put_scoperta":
        if "slider_mp" not in st.session_state: st.session_state["slider_mp"] = 15.0
        if "input_mp" not in st.session_state: st.session_state["input_mp"] = st.session_state["slider_mp"]
        st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>MARGINE BROKER (%)</span>", unsafe_allow_html=True)
        col_s, col_n = st.columns([2,1])
        with col_s:
            st.slider("mp_s", 5.0, 50.0, step=1.0, key="slider_mp",
                label_visibility="collapsed",
                on_change=lambda: st.session_state.update({"input_mp": st.session_state["slider_mp"]}),
                help="% del valore dello strike bloccata come garanzia dal broker. Tipicamente 15-20% per ETF OTM.")
        with col_n:
            st.number_input("mp_n", 5.0, 50.0, step=1.0, format="%.2f", key="input_mp",
                label_visibility="collapsed",
                on_change=lambda: st.session_state.update({"slider_mp": float(st.session_state["input_mp"])}))
        marg_pct = float(st.session_state["slider_mp"])
    else:
        marg_pct = 15.0
    crash = 20.0

    # ── OBIETTIVO STRATEGIA (solo Put Scoperta / Bull Put Spread) ──
    if "slider_pt" not in st.session_state: st.session_state["slider_pt"] = 84.0
    if "input_pt" not in st.session_state: st.session_state["input_pt"] = st.session_state["slider_pt"]
    if STRATEGIA not in ("long_call", "long_put"):
        st.markdown("<div class='sb-section'>Obiettivo Strategia</div>", unsafe_allow_html=True)
        st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>PROBABILITÀ DI SUCCESSO (%)</span>", unsafe_allow_html=True)
        col_s, col_n = st.columns([2,1])
        with col_s:
            st.slider("pt_s", 70.0, 99.0, step=1.0, key="slider_pt",
                label_visibility="collapsed",
                on_change=lambda: st.session_state.update({"input_pt": st.session_state["slider_pt"]}),
                help="84% = Delta 0.16 — ottimale.\n90% = Delta 0.10 — conservativo.\n80% = Delta 0.20 — aggressivo.")
        with col_n:
            st.number_input("pt_n", 70.0, 99.0, step=1.0, format="%.2f", key="input_pt",
                label_visibility="collapsed",
                on_change=lambda: st.session_state.update({"slider_pt": float(st.session_state["input_pt"])}))
    prob_t = float(st.session_state["slider_pt"])

    # Parametri specifici Bull Put Spread
    if STRATEGIA == "bull_put_spread":
        st.markdown("<div class='sb-section'>Parametri Spread</div>", unsafe_allow_html=True)

        # Prezzo put venduta
        st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>PUT VENDUTA — prezzo bid ($)</span>", unsafe_allow_html=True)
        def _sync_pv_slider(): st.session_state["_pv_val"] = st.session_state["slider_pv"]
        def _sync_pv_input():  st.session_state["_pv_val"] = st.session_state["input_pv"]
        if "_pv_val" not in st.session_state: st.session_state["_pv_val"] = 2.50
        cur_pv = float(st.session_state["_pv_val"])
        col_pv_s, col_pv_n = st.columns([2,1])
        with col_pv_s:
            st.slider("pv slider", 0.01, 200.0, min(cur_pv, 200.0), 0.01,
                label_visibility="collapsed", key="slider_pv", on_change=_sync_pv_slider)
        with col_pv_n:
            st.number_input("pv input", 0.01, 200.0, min(cur_pv, 200.0), 0.01,
                label_visibility="collapsed", key="input_pv", format="%.2f", on_change=_sync_pv_input)
        prezzo_put_venduta = float(st.session_state["_pv_val"])

        # Prezzo put comprata
        st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>PUT COMPRATA — prezzo ask ($)</span>", unsafe_allow_html=True)
        def _sync_pc_slider(): st.session_state["_pc_val"] = st.session_state["slider_pc"]
        def _sync_pc_input():  st.session_state["_pc_val"] = st.session_state["input_pc"]
        if "_pc_val" not in st.session_state: st.session_state["_pc_val"] = 1.12
        cur_pc = float(st.session_state["_pc_val"])
        col_pc_s, col_pc_n = st.columns([2,1])
        with col_pc_s:
            st.slider("pc slider", 0.01, 200.0, min(cur_pc, 200.0), 0.01,
                label_visibility="collapsed", key="slider_pc", on_change=_sync_pc_slider)
        with col_pc_n:
            st.number_input("pc input", 0.01, 200.0, min(cur_pc, 200.0), 0.01,
                label_visibility="collapsed", key="input_pc", format="%.2f", on_change=_sync_pc_input)
        prezzo_put_comprata = float(st.session_state["_pc_val"])

        # Larghezza spread
        if "slider_ls" not in st.session_state: st.session_state["slider_ls"] = 10
        if "input_ls" not in st.session_state: st.session_state["input_ls"] = st.session_state["slider_ls"]
        st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>LARGHEZZA SPREAD ($)</span>", unsafe_allow_html=True)
        col_ls_s, col_ls_n = st.columns([2,1])
        with col_ls_s:
            st.slider("ls_s", 1, 100, key="slider_ls",
                label_visibility="collapsed",
                on_change=lambda: st.session_state.update({"input_ls": st.session_state["slider_ls"]}),
                help="Differenza in dollari tra lo strike venduto e quello comprato.")
        with col_ls_n:
            st.number_input("ls_n", 1, 100, key="input_ls", format="%d",
                label_visibility="collapsed",
                on_change=lambda: st.session_state.update({"slider_ls": int(st.session_state["input_ls"])}))
        larghezza_spread = int(st.session_state["slider_ls"])

        credito_reale_bps = max(0.01, round(prezzo_put_venduta - prezzo_put_comprata, 2))
        st.session_state["_credito_bps"] = credito_reale_bps
    else:
        larghezza_spread = None
        credito_reale_bps = None
        prezzo_put_venduta = None
        prezzo_put_comprata = None

    if STRATEGIA == "put_scoperta":
        st.markdown("<div class='sb-section'>Dati Reali dal Broker</div>", unsafe_allow_html=True)


    # ── Greche reali — solo put scoperta ──
    if STRATEGIA == "put_scoperta":
        usa_greche_reali = st.toggle("Usa greche reali",
            help="Attiva per inserire Delta e Theta reali che vedi sul tuo broker.")
        if usa_greche_reali:
            st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>DELTA REALE</span>", unsafe_allow_html=True)
            delta_reale = st.number_input("Delta reale", 0.0, 1.0,
                float(st.session_state.get("_delta_val", 0.20)), 0.01,
                label_visibility="collapsed", key="input_delta", format="%.2f")
            st.session_state["_delta_val"] = delta_reale
            st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>THETA REALE (&euro;/giorno)</span>", unsafe_allow_html=True)
            theta_reale = st.number_input("Theta reale", 0.0, 9999.0,
                float(st.session_state.get("_theta_val", 10.0)), 0.01,
                label_visibility="collapsed", key="input_theta", format="%.2f")
            st.session_state["_theta_val"] = theta_reale
        else:
            delta_reale = None
            theta_reale = None
    else:
        delta_reale = None
        theta_reale = None

    # ── Premio reale — solo put scoperta ──
    if STRATEGIA == "put_scoperta":
        usa_premio_reale = st.toggle("Usa premio reale",
            help="Attiva per inserire il premio reale che vedi sul tuo broker invece di quello calcolato da Black-Scholes.")
        if usa_premio_reale:
            st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>PREMIO REALE (BID) &mdash; &euro;</span>", unsafe_allow_html=True)

            def _sync_slider():
                st.session_state["_pr_val"] = st.session_state["slider_pr"]
            def _sync_input():
                st.session_state["_pr_val"] = st.session_state["input_pr"]

            if "_pr_val" not in st.session_state:
                st.session_state["_pr_val"] = 5.0

            cur = float(st.session_state["_pr_val"])
            col_s, col_n = st.columns([2, 1])
            with col_s:
                st.slider(
                    "Premio (cursore)", 0.01, 500.0, cur, 0.01,
                    label_visibility="collapsed",
                    key="slider_pr",
                    on_change=_sync_slider
                )
            with col_n:
                st.number_input(
                    "Premio (±)", 0.01, 500.0, cur, 0.01,
                    label_visibility="collapsed",
                    key="input_pr",
                    format="%.2f",
                    on_change=_sync_input
                )
            premio_reale = float(st.session_state["_pr_val"])
        else:
            premio_reale = None
    else:
        premio_reale = None


    # ── PULSANTE GENERA PDF (solo Put Scoperta / Bull Put Spread) ──────────────
    if STRATEGIA not in ("long_call", "long_put"):
        st.markdown("<div class='sb-section'>Analisi Scenari</div>", unsafe_allow_html=True)
        genera_pdf_btn = st.button("Genera Report Scenari",
            use_container_width=True,
            help=f"Genera un PDF scaricabile con l'analisi completa della posizione su una fascia -10%/+10% dallo spot, "
                 f"30 livelli di prezzo con valore delle opzioni e P&L calcolato con T residuo = {max(int(st.session_state.get('slider_dte', 45) / 2), 1)} giorni.")
        if "pdf_scenari_bytes" in st.session_state and st.session_state["pdf_scenari_bytes"]:
            st.download_button(
                label="Scarica Report Scenari",
                data=st.session_state["pdf_scenari_bytes"],
                file_name=st.session_state.get("pdf_scenari_fname", "report.pdf"),
                mime="application/pdf",
                use_container_width=True,
            )
    else:
        genera_pdf_btn = False

    # ── Analisi AI (solo Put Scoperta / Bull Put Spread) ──
    if STRATEGIA not in ("long_call", "long_put"):
        st.markdown("<div class='sb-section'>Analisi AI</div>", unsafe_allow_html=True)

        import os as _os
        AI_PWD = _os.environ.get("AI_PASSWORD", "")
        if "ai_sbloccato" not in st.session_state:
            st.session_state["ai_sbloccato"] = False

        if not st.session_state["ai_sbloccato"]:
            st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>PASSWORD</span>", unsafe_allow_html=True)
            pwd_input = st.text_input("pwd", type="password",
                label_visibility="collapsed",
                placeholder="Inserisci password…",
                key="ai_pwd_input")
            if pwd_input:
                if pwd_input == AI_PWD:
                    st.session_state["ai_sbloccato"] = True
                    st.rerun()
                else:
                    st.error("Password errata.")
            genera_ai_btn = st.button("🔒 Genera Report AI",
                use_container_width=True, disabled=True)
        else:
            col_ai, col_lock = st.columns([4, 1])
            with col_lock:
                if st.button("🔓", help="Blocca Report AI", use_container_width=True):
                    st.session_state["ai_sbloccato"] = False
                    st.session_state["ai_pwd_input"] = ""
                    st.rerun()
            genera_ai_btn = st.button("Genera Report AI",
                use_container_width=True,
                help="Invia i parametri della posizione a Claude per un'analisi professionale del sottostante, "
                     "della volatilità e della solidità del trade.")

        if "pdf_ai_bytes" in st.session_state and st.session_state["pdf_ai_bytes"]:
            st.download_button(
                label="Scarica Report AI",
                data=st.session_state["pdf_ai_bytes"],
                file_name=st.session_state.get("pdf_ai_fname", "report_ai.pdf"),
                mime="application/pdf",
                use_container_width=True,
            )
    else:
        genera_ai_btn = False


# ═══════════════════════════════════════════════════════════
# RECUPERO DATI
# ═══════════════════════════════════════════════════════════

if ("dati" not in st.session_state or aggiorna or
        st.session_state.get("tk") != tk):
    with st.spinner(f"&#10227;  Recupero dati per {tk} e VIX…"):
        st.session_state.dati = recupera_dati_mercato(tk)
        st.session_state.tk   = tk

dati = st.session_state.dati
if dati.get("errore"):
    st.error(f"**Errore dati:** {dati['errore']}")
    st.info("💡 Prova con: SPY &middot; QQQ &middot; AAPL &middot; TSLA &middot; MSFT &middot; ^GSPC")
    st.stop()

spot    = dati["prezzo_spot"]
vol_st  = dati["vol_storica"]
iv_rank = iv_rank_reale  # sempre valorizzato dallo slider IV Rank
iv_ind  = iv_pct  # IV IND: direttamente dallo slider omonimo
vix_val    = dati["vix"]
vix_symbol = dati.get("vix_symbol", "^VIX")
vix_label  = "VXN — Paura Nasdaq" if vix_symbol == "^VXN" else "VIX — Paura"
vix_tooltip = ("Il VXN misura la volatilità implicita attesa sul Nasdaq 100 nei prossimi 30 giorni. "
               "Sotto 20 = mercato tranquillo, premi bassi. 20-25 = normale. Sopra 25 = paura elevata, premi gonfiati — ottimo per vendere opzioni."
               if vix_symbol == "^VXN" else
               "Il VIX misura la volatilità implicita attesa sull'S&P 500 nei prossimi 30 giorni. "
               "Sotto 15 = mercato tranquillo, premi bassi. 15-20 = normale. Sopra 20 = paura elevata, premi gonfiati — ottimo per vendere put.")
var     = dati["variazione_gg"]
nome    = dati["nome"]
ts_spot = dati["ts_spot"]
ts_vol  = dati["ts_vol"]
ts_vix  = dati["ts_vix"]
ts_ivr  = dati["ts_ivrank"]

# Preimposta lo slider IV con il VIX aggiornato e ricarica la pagina
if aggiorna and vix_val is not None:
    st.session_state["_iv_pct_init"] = float(vix_val)
    st.rerun()


# ═══════════════════════════════════════════════════════════
# CALCOLI
# ═══════════════════════════════════════════════════════════

T     = dte / 365.0
sigma = iv_pct / 100.0
r     = r_pct / 100.0
K     = strike_target(spot, sigma, T, r, prob_t/100.0)
par   = Par(S=spot, K=K, T=T, r=r, sigma=sigma)
prem_bs = prezzo_put(par)
prem     = premio_reale if premio_reale is not None else prem_bs
prob  = prob_ok(par)
gre   = calc_greche(par)
sema  = calc_semaforo(iv_pct, vol_st, iv_rank, vix_val)
# v5.1 &mdash; calcoli basati su n_contratti scelto dall'utente
mult      = 100                                        # ogni contratto = 100 azioni
mc        = round(K * mult * (marg_pct / 100), 2)     # margine per contratto (&euro;)
marg_tot  = round(n_contratti * mc, 2)                 # margine totale richiesto (&euro;)
ptot      = round(prem * n_contratti * mult, 2)        # incasso totale premi (&euro;)
thday     = round(abs(gre["theta"]) * n_contratti * mult, 2)  # theta totale/giorno (&euro;)
rend      = (ptot / marg_tot * 100) if marg_tot > 0 else 0    # rendimento sul margine (%)
dist      = (spot - K) / spot * 100
sc        = calc_wcs(spot, K, prem, n_contratti, crash)
# sz dict compatibilità (usato nel pannello e nel riepilogo)

# ── CALCOLI BULL PUT SPREAD ──
if STRATEGIA == "bull_put_spread" and larghezza_spread and credito_reale_bps:
    bps_K_venduta  = K                                               # strike put venduta (calcolato)
    bps_K_comprata = K - larghezza_spread                            # strike put comprata
    bps_credito    = credito_reale_bps                               # credito netto per azione
    bps_credito_tot = round(bps_credito * 100 * n_contratti, 2)      # credito totale
    bps_margine_c  = round((larghezza_spread - bps_credito) * 100, 2) # margine per contratto
    bps_margine_tot = round(bps_margine_c * n_contratti, 2)           # margine totale
    bps_be          = bps_K_venduta - bps_credito                     # break-even
    bps_rend        = (bps_credito_tot / bps_margine_tot * 100) if bps_margine_tot > 0 else 0
    bps_rend_ann    = (((1 + bps_rend / 100) ** 12) - 1) * 100
    bps_pct_largh   = (bps_credito / larghezza_spread) * 100
    bps_tp          = round(bps_credito_tot * 0.5, 2)                # take profit al 50%
    bps_sl          = round(bps_credito_tot * 2, 2)                  # stop loss a 2x
    bps_dist_venduta = (spot - bps_K_venduta) / spot * 100
    bps_dist_comprata = (spot - bps_K_comprata) / spot * 100
    # Deviazione standard a scadenza
    bps_sigma_T     = spot * sigma * np.sqrt(T)
    bps_dist_sd     = (spot - bps_K_venduta) / bps_sigma_T if bps_sigma_T > 0 else 0
else:
    bps_K_venduta = bps_K_comprata = bps_credito = bps_credito_tot = None
    bps_margine_c = bps_margine_tot = bps_max_profit = bps_max_loss = None
    bps_be = bps_rend = bps_rend_ann = bps_pct_largh = bps_tp = bps_sl = None
    bps_dist_venduta = bps_dist_comprata = bps_dist_sd = bps_sigma_T = None

# IV Rank badge
ivr_cls   = "alto" if iv_rank >= 50 else "medio" if iv_rank >= 30 else "basso"

# VIX colore
vix_str = fmt(vix_val, 2) if vix_val else "N/D"
# Soglie: VXN storicamente più alto del VIX (soglie +5 punti)
_vix_high = 25 if vix_symbol == "^VXN" else 20
_vix_mid  = 20 if vix_symbol == "^VXN" else 15
vix_cls = "green" if vix_val and vix_val >= _vix_high else "gold" if vix_val and vix_val >= _vix_mid else "red"


# ═══════════════════════════════════════════════════════════
# GENERA PDF SE RICHIESTO
# ═══════════════════════════════════════════════════════════
if genera_pdf_btn:
    pdf_params = {
        "spot": spot, "sigma": sigma, "T": T, "r": r,
        "nome": nome, "dte": dte, "n_contratti": n_contratti,
        "K": K, "prem": prem,
        "bps_K_venduta": bps_K_venduta, "bps_K_comprata": bps_K_comprata,
        "bps_credito": bps_credito,
        "bps_be": bps_be,
        "bps_margine_tot": bps_margine_tot,
        "bps_margine_c": bps_margine_c,
        "prezzo_put_venduta": prezzo_put_venduta if STRATEGIA == "bull_put_spread" else None,
        "prezzo_put_comprata": prezzo_put_comprata if STRATEGIA == "bull_put_spread" else None,
    }
    with st.spinner("Generazione report PDF in corso…"):
        pdf_bytes = genera_pdf_scenari(STRATEGIA, pdf_params)
    if pdf_bytes:
        ticker_clean = tk.replace("^", "").upper()
        fname = f"phinance_scenari_{ticker_clean}_{datetime.now().strftime('%Y%m%d')}.pdf"
        st.session_state["pdf_scenari_bytes"] = pdf_bytes
        st.session_state["pdf_scenari_fname"] = fname
        st.session_state["pdf_ai_bytes"] = None  # reset AI
        st.rerun()
    else:
        st.sidebar.error("Errore nella generazione del PDF. Verifica che reportlab sia installato.")

# ── REPORT AI ──
if genera_ai_btn:
    ai_params = {
        "spot": spot, "nome": nome, "ticker": tk,
        "dte": dte, "sigma": sigma,
        "iv_rank": iv_rank, "vol_st": vol_st,
        "vix": vix_val or 0, "var": var,
        "n_contratti": n_contratti,
    }
    if STRATEGIA == "put_scoperta":
        ai_params.update({"K": K, "prem": prem,
                          "mc": mc, "marg_tot": marg_tot})
    else:
        ai_params.update({
            "bps_K_venduta": bps_K_venduta,
            "bps_K_comprata": bps_K_comprata,
            "bps_credito": bps_credito,
            "bps_margine_tot": bps_margine_tot or 0,
        })
    with st.spinner("Analisi AI in corso…"):
        prompt_ai = costruisci_prompt_ai(STRATEGIA, ai_params, dati)
        testo_ai  = chiama_claude(prompt_ai)
    if testo_ai.startswith("ERRORE"):
        st.sidebar.error(testo_ai)
    else:
        pdf_ai = genera_pdf_ai(testo_ai, nome, tk, STRATEGIA)
        if pdf_ai:
            ticker_clean = tk.replace("^", "").upper()
            fname_ai = f"phinance_ai_{ticker_clean}_{datetime.now().strftime('%Y%m%d')}.pdf"
            st.session_state["pdf_ai_bytes"] = pdf_ai
            st.session_state["pdf_ai_fname"] = fname_ai
            st.session_state["pdf_scenari_bytes"] = None  # reset scenari
            st.rerun()

# ═══════════════════════════════════════════════════════════
# RENDER UI
# ═══════════════════════════════════════════════════════════

# ── HEADER ──
strat_header_label = {
    "put_scoperta":    "Vendita Put Scoperta",
    "bull_put_spread": "Bull Put Spread",
    "long_call":       "Long Call",
    "long_put":        "Long Put",
    "strategy_advisor":"Strategy Advisor",
}.get(STRATEGIA, STRATEGIA)
strat_header_icon = {
    "put_scoperta":    "&#9679;",
    "bull_put_spread": "&#9670;",
    "long_call":       "&#9650;",
    "long_put":        "&#9660;",
    "strategy_advisor":"&#9729;",
}.get(STRATEGIA, "&#9679;")
st.markdown(f"""
<div class="ph-header">
    <div style="display:flex;align-items:center;gap:1.2rem">
        <span class="ph-logo">Phinance</span>
        <div style="width:1px;height:2rem;background:var(--border-medium)"></div>
        <span class="ph-subtitle">{strat_header_icon} {strat_header_label} &middot; Motore Black-Scholes</span>
    </div>
    <div class="ph-header-right">
        <span class="ph-tag">v5.1 &middot; Yahoo Finance &middot; CBOE VIX</span>
        <span style="font-family:var(--font-mono);font-size:0.55rem;color:var(--text-muted);letter-spacing:0.1em">SOLO A SCOPO EDUCATIVO</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── BARRA 4 DATI LIVE &mdash; frecce semantiche ──
# Usiamo delta_color="off" su tutti: Streamlit non aggiunge frecce proprie.
# Freccia e colore nel testo, poi CSS custom colora i delta per posizione.

# Prezzo Spot
if var > 0.05:
    spot_arrow = f"&#9650; +{fmt(var,2)}% oggi"
    spot_cls   = "green"
elif var < -0.05:
    spot_arrow = f"&#9660; {fmt(var,2)}% oggi"
    spot_cls   = "red"
else:
    spot_arrow = f"&#8596; {fmt(var,2)}% oggi"
    spot_cls   = "gold"

# Vol. Storica: alta=verde, media=arancio, bassa=rosso
if vol_st >= 25:
    vol_arrow = "&#9650; Alta &mdash; Premi elevati"
    vol_cls   = "green"
elif vol_st >= 15:
    vol_arrow = "&#8596; Media &mdash; Nella norma"
    vol_cls   = "gold"
else:
    vol_arrow = "&#9660; Bassa &mdash; Premi scarsi"
    vol_cls   = "red"

# IV Rank: alto=verde, medio=arancio, basso=rosso
if iv_rank >= 50:
    ivr_arrow = "&#9650; Alto &mdash; Vendi"
    ivr_cls   = "green"
elif iv_rank >= 30:
    ivr_arrow = "&#8596; Medio &mdash; Valuta"
    ivr_cls   = "gold"
else:
    ivr_arrow = "&#9660; Basso &mdash; Aspetta"
    ivr_cls   = "red"

# VIX: alto=verde, medio=arancio, basso=rosso
if vix_val and vix_val >= _vix_high:
    vix_arrow = "&#9650; Elevato &mdash; Vendi"
    vix_cls   = "green"
elif vix_val and vix_val >= _vix_mid:
    vix_arrow = "&#8596; Normale &mdash; Nella norma"
    vix_cls   = "gold"
elif vix_val:
    vix_arrow = "&#9660; Basso &mdash; Premi scarsi"
    vix_cls   = "red"
else:
    vix_arrow = "Non disponibile"
    vix_cls   = "gold"

# IV IND: per vendita opzioni alto=verde, basso=rosso
if iv_ind >= 30:
    iv_ind_cls   = "green"
    iv_ind_label = "&#9650; Alta &mdash; Vendi"
elif iv_ind >= 20:
    iv_ind_cls   = "gold"
    iv_ind_label = "&#8596; Media &mdash; Valuta"
else:
    iv_ind_cls   = "red"
    iv_ind_label = "&#9660; Bassa &mdash; Aspetta"
iv_ind_fonte = "Da slider IV IND"


st.markdown(f"""
<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0.7rem;margin-bottom:2rem;margin-left:-0.5rem;margin-right:-0.5rem;width:calc(100% + 1rem);box-sizing:border-box">

  <div class="kpi-card kpi-sm" style="animation-delay:0.0s">
    <div class="kpi-eyebrow greek-tooltip">&#9679; Prezzo Spot
        <span class="tip-icon">?</span>
        <div class="tip-box">Prezzo di chiusura pi&ugrave; recente del sottostante selezionato, scaricato in tempo reale. &Egrave; il riferimento base per tutti i calcoli di strike, premio e margine.</div>
    </div>
    <div class="kpi-value {spot_cls}">{fmt(spot,2)}</div>
    <div class="kpi-sub">Aggiornato<br>{ts_spot}</div>
    <div><span class="kpi-badge {spot_cls}">{spot_arrow}</span></div>
  </div>

  <div class="kpi-card kpi-sm" style="animation-delay:0.06s">
    <div class="kpi-eyebrow greek-tooltip">&#9679; Vol. Storica 30gg
        <span class="tip-icon">?</span>
        <div class="tip-box">Volatilità reale del sottostante negli ultimi 30 giorni, annualizzata. Indica quanto si è mosso il prezzo storicamente. Confrontata con la IV: se IV &gt; Vol. Storica significa che le opzioni sono care &mdash; condizione favorevole per vendere.</div>
    </div>
    <div class="kpi-value {vol_cls}">{fmt(vol_st,2)}%</div>
    <div class="kpi-sub">Aggiornato<br>{ts_vol}</div>
    <div><span class="kpi-badge {vol_cls}">{vol_arrow}</span></div>
  </div>

  <div class="kpi-card kpi-sm" style="animation-delay:0.12s">
    <div class="kpi-eyebrow greek-tooltip">&#9679; IV Rank
        <span class="tip-icon">?</span>
        <div class="tip-box">Indica quanto è alta la volatilità implicita attuale rispetto agli ultimi 12 mesi. 0 = minimo storico, 100 = massimo storico. Sopra 50 = buon momento per vendere opzioni (regola quantitativa). Sotto 30 = premi troppo bassi, meglio aspettare.</div>
    </div>
    <div class="kpi-value {ivr_cls}">{fmt(iv_rank,0)} / 100</div>
    <div class="kpi-sub">Aggiornato<br>{ts_ivr}</div>
    <div><span class="kpi-badge {ivr_cls}">{ivr_arrow}</span></div>
  </div>

  <div class="kpi-card kpi-sm" style="animation-delay:0.18s">
    <div class="kpi-eyebrow greek-tooltip">&#9679; {vix_label}
        <span class="tip-icon">?</span>
        <div class="tip-box">{vix_tooltip}</div>
    </div>
    <div class="kpi-value {vix_cls}">{vix_str}</div>
    <div class="kpi-sub">Aggiornato<br>{ts_vix}</div>
    <div><span class="kpi-badge {vix_cls}">{vix_arrow}</span></div>
  </div>

  <div class="kpi-card kpi-sm" style="animation-delay:0.24s">
    <div class="kpi-eyebrow greek-tooltip">&#9679; IV IND
        <span class="tip-icon">?</span>
        <div class="tip-box">IV implicita dello strumento, calcolata sulle sue opzioni quotate. Alta = premi gonfiati, ottimo per vendere. Bassa = aspetta.</div>
    </div>
    <div class="kpi-value {iv_ind_cls}">{fmt(iv_ind,1)}%</div>
    <div class="kpi-sub">{iv_ind_fonte}</div>
    <div><span class="kpi-badge {iv_ind_cls}">{iv_ind_label}</span></div>
  </div>

</div>
""", unsafe_allow_html=True)

# variabili comuni
pn       = sc["lt"]                                        # perdita netta totale (già al netto del premio)
rend_ann = (((1 + rend / 100) ** 12) - 1) * 100           # rendimento annuo composto

# ── SIGNAL BANNER ──
st.markdown(f"""
<div class="signal-banner {sema['c']}">
    <span class="signal-dot {sema['c']}"></span>
    <span class="signal-label">{sema['l']}</span>
    <span class="signal-text">{sema['d']}</span>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# DASHBOARD — PUT SCOPERTA
# ══════════════════════════════════════════════════════════
if STRATEGIA == "put_scoperta":

    # ── KPI CARDS &mdash; 4 colonne ──
    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        st.markdown(f"""
        <div class="kpi-card" style="animation-delay:0.0s">
            <div class="kpi-eyebrow greek-tooltip">&#9679; Strike Consigliato
                <span class="tip-icon">?</span>
                <div class="tip-box">Lo strike viene calcolato automaticamente con Black-Scholes in base alla probabilit&agrave; di successo che imposti nella sidebar. All&apos;84% corrisponde un delta di circa 0,16 &mdash; il punto ottimale per la strategia.</div>
            </div>
            <div class="kpi-value cyan">{fmt(K,2)}</div>
            <div class="kpi-sub">{fmt(dist,2)}% sotto lo spot</div>
            <div><span class="kpi-badge green">OTM TARGET</span></div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        bc = "green" if prob >= 0.90 else "gold" if prob >= 0.80 else "red"
        bt = "Eccellente" if prob >= 0.90 else "Accettabile" if prob >= 0.80 else "Rischiosa"
        vc = "green"  if prob >= 0.90 else "gold" if prob >= 0.80 else "red"
        st.markdown(f"""
        <div class="kpi-card" style="animation-delay:0.06s">
            <div class="kpi-eyebrow greek-tooltip">&#9679; Probabilit&agrave; di Successo
                <span class="tip-icon">?</span>
                <div class="tip-box">Probabilit&agrave; che l&apos;opzione scada OTM e tu incassi il premio intero. Calcolata con Black-Scholes come N(d2). 84% = ottimale per la strategia. Sopra 90% = pi&ugrave; sicuro ma premio molto basso.</div>
            </div>
            <div class="kpi-value {vc}">{fmt(prob*100,2)}%</div>
            <div class="kpi-sub">Scade senza perdite</div>
            <div><span class="kpi-badge {bc}">{bt}</span></div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card" style="animation-delay:0.12s">
            <div class="kpi-eyebrow greek-tooltip">&#9679; Premio Incassato
                <span class="tip-icon">?</span>
                <div class="tip-box">Il premio &egrave; il massimo guadagno possibile &mdash; lo incassi subito alla vendita. Se l&apos;opzione scade OTM tieni tutto. Strategia comune: chiudi al 50% del profitto riacquistando l&apos;opzione a prezzo inferiore.</div>
            </div>
            <div class="kpi-value green">{fmt(prem,2)}</div>
            <div class="kpi-sub">{n_contratti} contratti &rarr; <strong style="color:var(--accent-green)">+{fmt(ptot,0)} &euro;</strong></div>
            <div><span class="kpi-badge green" style="white-space:nowrap">{fmt(rend,2)}% sul margine / mese</span></div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card" style="animation-delay:0.18s">
            <div class="kpi-eyebrow greek-tooltip">&#9679; Margine Richiesto
                <span class="tip-icon">?</span>
                <div class="tip-box">Il margine è la liquidità bloccata come garanzia dal broker. Non è un costo &mdash; rimane tuo &mdash; ma non puoi usarla per altri trade. Il valore è una stima: verifica sempre sul tuo broker prima di operare.</div>
            </div>
            <div class="kpi-value gold">{fmt(marg_tot,2)} &euro;</div>
            <div class="kpi-sub">{fmt(mc,0)} &euro; &times; {n_contratti} contratti</div>
            <div><span class="kpi-badge gold">DA AVERE SUL CONTO</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

    # ── DETTAGLIO POSIZIONE ──
    _s = "background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:var(--radius-xl);padding:0.9rem 1rem;height:110px;max-height:110px;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;cursor:default"
    _v = "font-family:'DM Sans',sans-serif;font-weight:700;letter-spacing:-0.03em;white-space:nowrap;overflow:hidden;text-overflow:clip"
    _e = "font-family:'DM Mono',monospace;font-size:0.55rem;font-weight:500;letter-spacing:0.14em;text-transform:uppercase;color:#3E526A;margin-bottom:0.3rem;white-space:nowrap"
    _b = "font-family:'DM Mono',monospace;font-size:0.6rem;color:#3E526A;white-space:nowrap;overflow:hidden"
    st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--text-secondary)'><span style='color:var(--accent-green);margin-right:0.5rem'>&#9678;</span>Dettaglio Posizione <span style='color:var(--text-muted);font-weight:400'>(margine stimato)</span></span>", unsafe_allow_html=True)
    d1,d2,d3,d4,d5,d6 = st.columns(6, gap="small")
    with d1:
        st.markdown(f'<div style="{_s}"><div style="{_e}">Contratti</div><div style="{_v};font-size:1.2rem;color:var(--accent-cyan)">{n_contratti}</div><div style="{_b}">selezionati</div></div>', unsafe_allow_html=True)
    with d2:
        st.markdown(f'<div style="{_s}"><div style="{_e}">Margine / contratto</div><div style="{_v};font-size:1.2rem;color:var(--accent-cyan)">{fmt(mc,2)} &euro;</div><div style="{_b}">{fmt(marg_pct,0)}% × strike</div></div>', unsafe_allow_html=True)
    with d3:
        st.markdown(f'<div style="{_s}"><div style="{_e}">Margine totale</div><div style="{_v};font-size:1.2rem;color:var(--accent-gold)">{fmt(marg_tot,2)} &euro;</div><div style="{_b}">da avere sul conto</div></div>', unsafe_allow_html=True)
    with d4:
        st.markdown(f'<div style="{_s}"><div style="{_e}">Incasso premi</div><div style="{_v};font-size:1.2rem;color:var(--accent-green)">+{fmt(ptot,2)} &euro;</div><div style="{_b}">{n_contratti} × {fmt(prem,2)} × 100</div></div>', unsafe_allow_html=True)
    with d5:
        st.markdown(f'<div style="{_s}"><div style="{_e}">Theta / giorno</div><div style="{_v};font-size:1.2rem;color:var(--accent-green)">+{fmt(thday,2)} &euro;</div><div style="{_b}">guadagno dal tempo</div></div>', unsafe_allow_html=True)
    with d6:
        st.markdown(f'<div style="{_s}"><div style="{_e}">Rendimento</div><div style="{_v};font-size:1.2rem;color:var(--accent-green)">{fmt(rend,2)}% / mese</div><div style="{_b}">{fmt(rend_ann,2)}% / anno</div></div>', unsafe_allow_html=True)
    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

    # ── GRAFICO P&L INTERATTIVO PUT SCOPERTA ──
    st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--text-secondary)'><span style='color:var(--accent-green);margin-right:0.5rem'>&#9678;</span>Simulatore P&amp;L</span>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)

    _ps_spot   = round(spot, 2)
    _ps_strike = round(K, 2)
    _ps_prem   = round(prem, 2)
    _ps_iv     = round(sigma * 100, 1)
    _ps_dte    = int(dte)
    _ps_maxp   = round(_ps_prem * 100, 2)
    _ps_be     = round(_ps_strike - _ps_prem, 2)
    _ps_dist   = round((_ps_spot - _ps_be) / _ps_spot * 100, 2)
    _ps_margine = round(marg_tot, 2)  # perdita massima = margine bloccato

    st.components.v1.html(f"""
<!DOCTYPE html>
<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'DM Sans', system-ui, sans-serif; }}
  body {{ background: transparent; color: #E2E8F0; }}
  .grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px; }}
  .grid4 {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 8px; margin-bottom: 12px; }}
  .card {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 10px 14px; }}
  .card-label {{ font-size: 11px; color: #8B9FC0; margin-bottom: 3px; letter-spacing: 0.05em; }}
  .card-val {{ font-size: 18px; font-weight: 600; }}
  .green {{ color: #00E5A0; }} .red {{ color: #FF5A5A; }} .cyan {{ color: #00C2FF; }} .gold {{ color: #FFB547; }}
  .slider-row {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 12px 16px; margin-bottom: 12px; display: flex; align-items: center; gap: 14px; }}
  .slider-row label {{ font-size: 11px; color: #8B9FC0; white-space: nowrap; letter-spacing: 0.08em; }}
  .slider-row input[type=range] {{ flex: 1; accent-color: #00C2FF; height: 4px; }}
  .slider-val {{ font-size: 20px; font-weight: 600; color: #00C2FF; min-width: 60px; text-align: right; }}
  .status-grid {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 8px; margin-top: 10px; }}
  .legend {{ display: flex; gap: 16px; margin-bottom: 8px; font-size: 11px; color: #8B9FC0; align-items: center; }}
  .leg-dot {{ width: 12px; height: 3px; display: inline-block; border-radius: 2px; }}
</style>
</head>
<body>

<div class="grid4">
  <div class="card"><div class="card-label">Strike</div><div class="card-val cyan">${_ps_strike}</div></div>
  <div class="card"><div class="card-label">Premio / az.</div><div class="card-val green">+${_ps_prem:.2f}</div></div>
  <div class="card"><div class="card-label">Break-even</div><div class="card-val gold">${_ps_be}</div></div>
  <div class="card"><div class="card-label">Distanza BE</div><div class="card-val">{_ps_dist}%</div></div>
</div>

<div class="slider-row">
  <label>DTE SIMULATI</label>
  <input type="range" id="dteSlider" min="0" max="{_ps_dte}" value="{_ps_dte}" step="1">
  <div class="slider-val"><span id="dteVal">{_ps_dte}</span> <span style="font-size:12px;color:#8B9FC0;">gg</span></div>
</div>

<div class="legend">
  <span><span class="leg-dot" style="background:#00C2FF;"></span> Valore attuale</span>
  <span><span class="leg-dot" style="background:#8B9FC0;border-top:2px dashed #8B9FC0;"></span> A scadenza</span>
  <span><span class="leg-dot" style="background:#FF5A5A;width:2px;height:12px;"></span> Spot ({_ps_spot})</span>
</div>

<div style="position:relative;width:100%;height:300px;">
  <canvas id="psChart"></canvas>
</div>

<div class="status-grid" id="statusBar"></div>

<script>
const SPOT = {_ps_spot};
const STRIKE = {_ps_strike};
const PREM = {_ps_prem};
const IV = {_ps_iv / 100};
const TOTAL_DTE = {_ps_dte};
const R = 0.04;
const MAX_LOSS_FACTOR = 0.40;
const MARGINE = {_ps_margine};  // perdita massima = margine bloccato

function norm(x) {{
  const a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911;
  const sign=x<0?-1:1, t=1/(1+p*Math.abs(x));
  return 0.5*(1+sign*(1-(((((a5*t+a4)*t)+a3)*t+a2)*t+a1)*t*Math.exp(-x*x/2)));
}}

function bsPut(S,K,T,r,sigma) {{
  if(T<=0.0001) return Math.max(K-S,0);
  const d1=(Math.log(S/K)+(r+0.5*sigma*sigma)*T)/(sigma*Math.sqrt(T));
  const d2=d1-sigma*Math.sqrt(T);
  return K*Math.exp(-r*T)*norm(-d2)-S*norm(-d1);
}}

function psPnlCurrent(price, dte) {{
  const T=Math.max(dte,0.1)/365;
  const putVal=bsPut(price,STRIKE,T,R,IV);
  const raw = Math.round((PREM-putVal)*100*100)/100;
  return Math.max(raw, -MARGINE);
}}

function psPnlAtExp(price) {{
  let raw;
  if(price>=STRIKE) raw = Math.round(PREM*100*100)/100;
  else raw = Math.round((PREM-(STRIKE-price))*100*100)/100;
  return Math.max(raw, -MARGINE);
}}

const priceMin = Math.round(STRIKE*(1-MAX_LOSS_FACTOR));
const priceMax = Math.round(SPOT*1.12);
const prices=[];
for(let p=priceMin;p<=priceMax;p+=Math.round((priceMax-priceMin)/60)) prices.push(p);

const spotIdx=prices.findIndex(p=>p>=SPOT);

const chart=new Chart(document.getElementById('psChart'),{{
  type:'line',
  data:{{
    labels:prices.map(p=>'$'+p),
    datasets:[
      {{label:'Valore attuale',data:[],borderColor:'#00C2FF',backgroundColor:'rgba(0,194,255,0.07)',fill:true,pointRadius:0,borderWidth:2.5,tension:0.3}},
      {{label:'A scadenza',data:[],borderColor:'#8B9FC0',backgroundColor:'transparent',fill:false,pointRadius:0,borderWidth:1.5,tension:0,borderDash:[6,4]}}
    ]
  }},
  options:{{
    responsive:true,maintainAspectRatio:false,
    interaction:{{mode:'index',intersect:false}},
    plugins:{{
      legend:{{display:false}},
      tooltip:{{
        backgroundColor:'#0D1520',borderColor:'rgba(0,194,255,0.3)',borderWidth:1,
        titleColor:'#E2E8F0',bodyColor:'#8B9FC0',
        callbacks:{{
          title:ctx=>'SPY a '+ctx[0].label,
          label:ctx=>{{const v=ctx.dataset.data[ctx.dataIndex];if(v===null||v===undefined)return null;return ctx.dataset.label+': '+(v>=0?'+':'')+'€'+v;}}
        }}
      }},
      annotation:{{}}
    }},
    scales:{{
      x:{{ticks:{{autoSkip:true,maxTicksLimit:10,color:'#4A6080',font:{{size:10}}}},grid:{{color:'rgba(255,255,255,0.04)'}}}},
      y:{{
        min: -MARGINE,
        max: Math.round(PREM * 100 * 2.5),
        ticks:{{color:'#4A6080',font:{{size:10}},callback:v=>(v>=0?'+':'')+'€'+v}},
        grid:{{color:'rgba(255,255,255,0.04)'}}
      }}
    }}
  }}
}});

function addSpotAnnotation() {{
  if(spotIdx>=0) {{
    const meta=chart.getDatasetMeta(0);
    chart.options.plugins.annotation={{
      annotations:{{
        spotLine:{{
          type:'line',scaleID:'x',value:prices[spotIdx],borderColor:'rgba(255,90,90,0.7)',borderWidth:1.5,
          label:{{display:true,content:'Spot',backgroundColor:'rgba(255,90,90,0.2)',color:'#FF5A5A',font:{{size:10}}}}
        }}
      }}
    }};
  }}
}}

function updateChart(dte) {{
  chart.data.datasets[0].data=prices.map(p=>psPnlCurrent(p,dte));
  chart.data.datasets[1].data=prices.map(p=>psPnlAtExp(p));
  chart.update('none');
  const spotPnl=psPnlCurrent(SPOT,dte);
  const tp50=Math.round(PREM*100*0.5*100)/100;
  const sl2x=Math.round(PREM*100*2*100)/100;
  const pctD=Math.round((1-dte/TOTAL_DTE)*100);
  document.getElementById('statusBar').innerHTML=`
    <div class="card"><div class="card-label">P&L allo spot</div><div class="card-val ${{spotPnl>=0?'green':'red'}}">${{spotPnl>=0?'+':''}}€${{spotPnl}}</div></div>
    <div class="card"><div class="card-label">Theta decayato</div><div class="card-val">${{pctD}}%</div></div>
    <div class="card"><div class="card-label">Take profit 50%</div><div class="card-val green">+€${{tp50}}</div></div>
    <div class="card"><div class="card-label">Stop loss 2x</div><div class="card-val red">-€${{sl2x}}</div></div>
  `;
}}

document.getElementById('dteSlider').addEventListener('input',function(){{
  document.getElementById('dteVal').textContent=this.value;
  updateChart(parseInt(this.value));
}});

updateChart(TOTAL_DTE);
</script>
</body>
</html>
""", height=530)

    # ── GRAFICO TRADINGVIEW ──
    _tv_map = {"^GSPC": "SP:SPX", "^DJI": "DJ:DJI", "^NDX": "NASDAQ:NDX"}
    tk_tv = _tv_map.get(tk, tk)
    st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--text-secondary)'><span style='color:var(--accent-green);margin-right:0.5rem'>&#9678;</span>Grafico</span>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
    st.components.v1.html(f"""
    <div style="border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,0.06)">
    <div class="tradingview-widget-container" style="height:420px">
      <div id="tradingview_ps" style="height:100%"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "width": "100%",
        "height": 420,
        "symbol": "{tk_tv}",
        "interval": "D",
        "timezone": "Europe/Rome",
        "theme": "dark",
        "style": "1",
        "locale": "it",
        "toolbar_bg": "#080C10",
        "enable_publishing": false,
        "hide_top_toolbar": false,
        "hide_legend": false,
        "save_image": false,
        "container_id": "tradingview_ps",
        "backgroundColor": "#080C10",
        "gridColor": "rgba(255,255,255,0.03)",
      }});
      </script>
    </div>
    </div>
    """, height=430)
    st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

    # ── RIEPILOGO PUT SCOPERTA ──
    st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--text-secondary)'><span style='color:var(--accent-green);margin-right:0.5rem'>&#9678;</span>Riepilogo Operazione</span>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "Parametro": ["Strumento","Prezzo Attuale","Strike Consigliato","Distanza Strike",
                      "Giorni alla Scadenza",
                      "Premio per Contratto","Numero Contratti","Margine per Contratto",
                      "Margine Totale Richiesto","Incasso Totale Premi",
                      "Punto di Pareggio","Theta Giornaliero","Rendimento sul Margine"],
        "Valore":    [nome, fmt(spot,2), fmt(K,2), f"{fmt(dist,2)}% sotto lo spot",
                      f"{dte} gg",
                      f"{fmt(prem,4)}  ({fmt(prem*100,2)} € / contratto 100 azioni)",
                      str(n_contratti), f"{fmt(mc,2)} €",
                      f"{fmt(marg_tot,2)} € (da avere sul conto)",
                      f"+{fmt(ptot,2)} €",
                      fmt(K-prem,2), f"+{fmt(thday,2)} € / giorno",
                      f"{fmt(rend,2)}% / mese  ({fmt(rend_ann,2)}% annuo composto stimato)"],
    }), use_container_width=True, hide_index=True,
        column_config={
            "Parametro": st.column_config.TextColumn(width="medium"),
            "Valore":    st.column_config.TextColumn(width="large"),
        })

# ══════════════════════════════════════════════════════════
# DASHBOARD — BULL PUT SPREAD
# ══════════════════════════════════════════════════════════
elif STRATEGIA == "bull_put_spread" and bps_credito_tot is not None:

    # ── KPI CARDS BPS ──
    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        st.markdown(f"""
        <div class="kpi-card" style="animation-delay:0.0s">
            <div class="kpi-eyebrow greek-tooltip">&#9679; Strike Venduto
                <span class="tip-icon">?</span>
                <div class="tip-box">Lo strike della put che vendi &mdash; calcolato con Black-Scholes in base alla probabilit&agrave; di successo impostata. Incassi il premio pi&ugrave; alto. Se SPY rimane sopra questo strike a scadenza tieni tutto il credito.</div>
            </div>
            <div class="kpi-value cyan">{fmt(bps_K_venduta,2)}</div>
            <div class="kpi-sub">{fmt(bps_dist_venduta,2)}% sotto lo spot</div>
            <div><span class="kpi-badge green">PUT VENDUTA (STO)</span></div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card" style="animation-delay:0.06s">
            <div class="kpi-eyebrow greek-tooltip">&#9679; Strike Comprato
                <span class="tip-icon">?</span>
                <div class="tip-box">Lo strike della put che compri come protezione &mdash; distante {larghezza_spread}$ dalla put venduta. Limita la perdita massima. Se SPY scende sotto questo livello la perdita non aumenta ulteriormente.</div>
            </div>
            <div class="kpi-value gold">{fmt(bps_K_comprata,2)}</div>
            <div class="kpi-sub">{fmt(bps_dist_comprata,2)}% sotto lo spot</div>
            <div><span class="kpi-badge gold">PUT COMPRATA (BTO)</span></div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        cred_cls = "green" if bps_pct_largh >= 33 else "gold" if bps_pct_largh >= 25 else "red"
        st.markdown(f"""
        <div class="kpi-card" style="animation-delay:0.12s">
            <div class="kpi-eyebrow greek-tooltip">&#9679; Credito Netto
                <span class="tip-icon">?</span>
                <div class="tip-box">Il credito netto è la differenza tra il premio incassato e quello pagato. Secondo la regola quantitativa deve essere almeno 1/3 (≈33%) della larghezza dello spread ({larghezza_spread}$) per avere un valore atteso positivo. Sotto il 25% il trade non è efficiente.</div>
            </div>
            <div class="kpi-value {cred_cls}">{fmt(bps_credito,2)}</div>
            <div class="kpi-sub">{n_contratti} contratti &rarr; <strong style="color:var(--accent-green)">+{fmt(bps_credito_tot,0)} &euro;</strong></div>
            <div><span class="kpi-badge {cred_cls}">{fmt(bps_pct_largh,1)}% della larghezza</span></div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card" style="animation-delay:0.18s">
            <div class="kpi-eyebrow greek-tooltip">&#9679; Margine Fisso
                <span class="tip-icon">?</span>
                <div class="tip-box">Il margine del bull put spread &egrave; fisso e predefinito: (larghezza &mdash; credito) &times; 100. Non varia con il prezzo del sottostante. &Egrave; anche la perdita massima teorica assoluta della posizione.</div>
            </div>
            <div class="kpi-value gold">{fmt(bps_margine_tot,2)} &euro;</div>
            <div class="kpi-sub">{fmt(bps_margine_c,2)} &euro; &times; {n_contratti} contratti</div>
            <div><span class="kpi-badge gold" style="white-space:nowrap">FISSO &mdash; RISCHIO DEFINITO</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

    # ── DETTAGLIO POSIZIONE BPS ──
    _s = "background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:var(--radius-xl);padding:0.9rem 1rem;height:110px;max-height:110px;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;cursor:default"
    _v = "font-family:'DM Sans',sans-serif;font-weight:700;letter-spacing:-0.03em;white-space:nowrap;overflow:hidden;text-overflow:clip"
    _e = "font-family:'DM Mono',monospace;font-size:0.55rem;font-weight:500;letter-spacing:0.14em;text-transform:uppercase;color:#3E526A;margin-bottom:0.3rem;white-space:nowrap"
    _b = "font-family:'DM Mono',monospace;font-size:0.6rem;color:#3E526A;white-space:nowrap;overflow:hidden"
    st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--text-secondary)'><span style='color:var(--accent-green);margin-right:0.5rem'>&#9678;</span>Dettaglio Posizione</span>", unsafe_allow_html=True)
    d1,d2,d3,d4,d5 = st.columns(5, gap="small")
    with d1:
        st.markdown(f'<div style="{_s}"><div style="{_e}">Contratti</div><div style="{_v};font-size:1.2rem;color:var(--accent-cyan)">{n_contratti}</div><div style="{_b}">selezionati</div></div>', unsafe_allow_html=True)
    with d2:
        st.markdown(f'<div style="{_s}"><div style="{_e}">Strike venduto</div><div style="{_v};font-size:1.2rem;color:var(--accent-cyan)">{fmt(bps_K_venduta,2)}</div><div style="{_b}">put venduta (STO)</div></div>', unsafe_allow_html=True)
    with d3:
        st.markdown(f'<div style="{_s}"><div style="{_e}">Strike comprato</div><div style="{_v};font-size:1.2rem;color:var(--accent-gold)">{fmt(bps_K_comprata,2)}</div><div style="{_b}">put comprata (BTO)</div></div>', unsafe_allow_html=True)
    with d4:
        cred_col = "var(--accent-green)" if bps_pct_largh >= 33 else "var(--accent-gold)" if bps_pct_largh >= 25 else "var(--accent-red)"
        st.markdown(f'<div style="{_s}"><div style="{_e}">Credito netto</div><div style="{_v};font-size:1.2rem;color:{cred_col}">+{fmt(bps_credito_tot,2)} &euro;</div><div style="{_b}">{fmt(bps_pct_largh,1)}% della larghezza</div></div>', unsafe_allow_html=True)
    with d5:
        st.markdown(f'<div style="{_s}"><div style="{_e}">Margine fisso</div><div style="{_v};font-size:1.2rem;color:var(--accent-gold)">{fmt(bps_margine_tot,2)} &euro;</div><div style="{_b}">rischio definito</div></div>', unsafe_allow_html=True)
    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

    # ── PANNELLO ANALISI SPREAD ──
    sd_label = f"{fmt(bps_dist_sd,2)} SD" if bps_dist_sd else "N/D"
    be_dist  = (spot - bps_be) / spot * 100
    _sa = _s.replace("overflow:hidden", "overflow:visible")
    st.markdown(f"<span style='font-family:var(--font-mono);font-size:0.6rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--text-secondary)'><span style='color:var(--accent-green);margin-right:0.5rem'>&#9670;</span>Analisi Spread &mdash; Bull Put Spread {fmt(bps_K_venduta,0)} / {fmt(bps_K_comprata,0)}</span>", unsafe_allow_html=True)
    a1,a2,a3,a4,a5,a6 = st.columns(6, gap="small")
    with a1:
        st.markdown(f"""<div style="{_sa}"><div style="{_e}" class="greek-tooltip">Larghezza<span class="tip-icon">?</span><div class="tip-box">Differenza in dollari tra lo strike venduto e quello comprato. Determina il rischio massimo per azione: se lo spread scade ITM perdi al massimo questa cifra meno il credito incassato.</div></div><div style="{_v};font-size:1.2rem;color:var(--accent-cyan)">${larghezza_spread}</div><div style="{_b}">tra i due strike</div></div>""", unsafe_allow_html=True)
    with a2:
        st.markdown(f"""<div style="{_sa}"><div style="{_e}" class="greek-tooltip">Break-even<span class="tip-icon">?</span><div class="tip-box">Punto esatto sotto cui inizi a perdere denaro. Calcolato come strike venduto meno il credito incassato per azione. Sopra questo livello a scadenza il trade &egrave; profittevole.</div></div><div style="{_v};font-size:1.2rem;color:var(--accent-cyan)">{fmt(bps_be,2)}</div><div style="{_b}">{fmt(be_dist,2)}% sotto spot</div></div>""", unsafe_allow_html=True)
    with a3:
        st.markdown(f"""<div style="{_sa}"><div style="{_e}" class="greek-tooltip">Distanza SD<span class="tip-icon">?</span><div class="tip-box">Quante deviazioni standard di distanza si trova lo strike venduto rispetto allo spot attuale. Sopra 1 SD = molto OTM, alta probabilit&agrave; di successo. Sotto 0.5 SD = rischioso.</div></div><div style="{_v};font-size:1.2rem;color:var(--accent-cyan)">{sd_label}</div><div style="{_b}">dal strike venduto</div></div>""", unsafe_allow_html=True)
    with a4:
        st.markdown(f"""<div style="{_sa}"><div style="{_e}" class="greek-tooltip">Take Profit 50%<span class="tip-icon">?</span><div class="tip-box">Livello consigliato per chiudere il trade in anticipo. Riacquistando lo spread a met&agrave; del credito incassato si libera il margine e si riduce il rischio residuo. &Egrave; la gestione standard raccomandata dalla ricerca quantitativa.</div></div><div style="{_v};font-size:1.2rem;color:var(--accent-green)">+{fmt(bps_tp,0)} &euro;</div><div style="{_b}">chiudi qui</div></div>""", unsafe_allow_html=True)
    with a5:
        st.markdown(f"""<div style="{_sa}"><div style="{_e}" class="greek-tooltip">Stop Loss 2x<span class="tip-icon">?</span><div class="tip-box">Livello di uscita in perdita: se il costo per chiudere lo spread raggiunge il doppio del credito incassato, esci. Limita la perdita massima gestita a 2 volte il premio ricevuto.</div></div><div style="{_v};font-size:1.2rem;color:var(--accent-red)">-{fmt(bps_sl,0)} &euro;</div><div style="{_b}">perdita max gestita</div></div>""", unsafe_allow_html=True)
    with a6:
        st.markdown(f"""<div style="{_sa}"><div style="{_e}" class="greek-tooltip">Rendimento<span class="tip-icon">?</span><div class="tip-box">Rendimento percentuale sul margine bloccato se il trade va a profitto intero. Calcolato come credito totale diviso margine totale. Non include il costo del capitale nel tempo.</div></div><div style="{_v};font-size:1.2rem;color:var(--accent-green)">{fmt(bps_rend,1)}%</div><div style="{_b}">sul margine / mese</div></div>""", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)


    # ── GRAFICO P&L INTERATTIVO BPS ──
    st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--text-secondary)'><span style='color:var(--accent-green);margin-right:0.5rem'>&#9678;</span>Simulatore P&amp;L</span>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)

    _bps_spot    = round(spot, 2)
    _bps_ks      = round(bps_K_venduta, 2)
    _bps_kl      = round(bps_K_comprata, 2)
    _bps_credit  = round(bps_credito, 4)
    _bps_iv      = round(sigma * 100, 1)
    _bps_dte     = int(dte)
    _bps_width   = round(_bps_ks - _bps_kl, 2)
    _bps_maxp    = round(_bps_credit * 100, 2)
    _bps_maxl    = round((_bps_width - _bps_credit) * 100, 2)
    _bps_be      = round(_bps_ks - _bps_credit, 2)
    _bps_dist    = round((_bps_spot - _bps_be) / _bps_spot * 100, 2)
    _bps_pct_w   = round(_bps_credit / _bps_width * 100, 1)

    st.components.v1.html(f"""
<!DOCTYPE html>
<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
  * {{ box-sizing:border-box;margin:0;padding:0;font-family:'DM Sans',system-ui,sans-serif; }}
  body {{ background:transparent;color:#E2E8F0; }}
  .grid4 {{ display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:12px; }}
  .grid2 {{ display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:12px; }}
  .card {{ background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:10px 14px; }}
  .card-label {{ font-size:11px;color:#8B9FC0;margin-bottom:3px;letter-spacing:0.05em; }}
  .card-val {{ font-size:18px;font-weight:600; }}
  .green {{ color:#00E5A0; }} .red {{ color:#FF5A5A; }} .cyan {{ color:#00C2FF; }} .gold {{ color:#FFB547; }}
  .controls {{ background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:12px 16px;margin-bottom:12px; }}
  .ctrl-row {{ display:flex;align-items:center;gap:14px;margin-bottom:8px; }}
  .ctrl-row:last-child {{ margin-bottom:0; }}
  .ctrl-label {{ font-size:11px;color:#8B9FC0;white-space:nowrap;letter-spacing:0.08em;min-width:90px; }}
  .ctrl-row input[type=range] {{ flex:1;accent-color:#00C2FF;height:4px; }}
  .ctrl-val {{ font-size:16px;font-weight:600;color:#00C2FF;min-width:60px;text-align:right; }}
  .badge {{ display:inline-block;padding:2px 8px;border-radius:20px;font-size:10px;font-weight:600;letter-spacing:0.08em; }}
  .badge-green {{ background:rgba(0,229,160,0.12);color:#00E5A0;border:1px solid rgba(0,229,160,0.25); }}
  .badge-gold {{ background:rgba(255,181,71,0.12);color:#FFB547;border:1px solid rgba(255,181,71,0.25); }}
  .badge-red {{ background:rgba(255,90,90,0.12);color:#FF5A5A;border:1px solid rgba(255,90,90,0.25); }}
  .legend {{ display:flex;gap:16px;margin-bottom:8px;font-size:11px;color:#8B9FC0;align-items:center; }}
  .leg-dot {{ width:12px;height:3px;display:inline-block;border-radius:2px; }}
  .status-grid {{ display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:10px; }}
</style>
</head>
<body>

<div class="grid4">
  <div class="card"><div class="card-label">Strike venduto</div><div class="card-val cyan">${_bps_ks}</div></div>
  <div class="card"><div class="card-label">Strike comprato</div><div class="card-val gold">${_bps_kl}</div></div>
  <div class="card"><div class="card-label">Break-even</div><div class="card-val">${_bps_be}</div></div>
  <div class="card">
    <div class="card-label">Credito / larghezza</div>
    <div class="card-val green">+${_bps_credit}</div>
  </div>
</div>

<div class="grid4">
  <div class="card"><div class="card-label">Max profitto</div><div class="card-val green">+€{_bps_maxp}</div></div>
  <div class="card"><div class="card-label">Max perdita</div><div class="card-val red">-€{_bps_maxl}</div></div>
  <div class="card"><div class="card-label">Distanza BE</div><div class="card-val">{_bps_dist}%</div></div>
  <div class="card"><div class="card-label">Larghezza spread</div><div class="card-val">${_bps_width}</div></div>
</div>

<div class="controls">
  <div class="ctrl-row">
    <span class="ctrl-label">DTE SIMULATI</span>
    <input type="range" id="dteSlider" min="0" max="{_bps_dte}" value="{_bps_dte}" step="1">
    <div class="ctrl-val"><span id="dteVal">{_bps_dte}</span> <span style="font-size:11px;color:#8B9FC0;">gg</span></div>
  </div>
</div>

<div class="legend">
  <span><span class="leg-dot" style="background:#00C2FF;"></span> Valore attuale</span>
  <span><span class="leg-dot" style="background:#8B9FC0;"></span> A scadenza</span>
  <span><span class="leg-dot" style="background:#FF5A5A;width:2px;height:12px;"></span> Spot ({_bps_spot})</span>
</div>

<div style="position:relative;width:100%;height:300px;">
  <canvas id="bpsChart"></canvas>
</div>

<div class="status-grid" id="statusBar"></div>

<script>
const SPOT={_bps_spot}, KS={_bps_ks}, KL={_bps_kl};
const CREDIT={_bps_credit}, WIDTH={_bps_width};
const TOTAL_DTE={_bps_dte}, R=0.04;
let IV={_bps_iv/100};

function norm(x){{
  const a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911;
  const sign=x<0?-1:1,t=1/(1+p*Math.abs(x));
  return 0.5*(1+sign*(1-(((((a5*t+a4)*t)+a3)*t+a2)*t+a1)*t*Math.exp(-x*x/2)));
}}

function bsPut(S,K,T,r,sigma){{
  if(T<=0.0001) return Math.max(K-S,0);
  const d1=(Math.log(S/K)+(r+0.5*sigma*sigma)*T)/(sigma*Math.sqrt(T));
  const d2=d1-sigma*Math.sqrt(T);
  return K*Math.exp(-r*T)*norm(-d2)-S*norm(-d1);
}}

function bpsCurrent(price,dte,iv){{
  const T=Math.max(dte,0.1)/365;
  const ps=bsPut(price,KS,T,R,iv), pl=bsPut(price,KL,T,R,iv);
  return Math.round((CREDIT-(ps-pl))*100*100)/100;
}}

function bpsExp(price){{
  if(price<=KL) return Math.round(-(WIDTH-CREDIT)*100*100)/100;
  if(price<KS)  return Math.round((CREDIT-(KS-price))*100*100)/100;
  return Math.round(CREDIT*100*100)/100;
}}

const pMin=Math.round(KL*0.88), pMax=Math.round(SPOT*1.10);
const prices=[];
for(let p=pMin;p<=pMax;p+=Math.max(1,Math.round((pMax-pMin)/70))) prices.push(p);

const chart=new Chart(document.getElementById('bpsChart'),{{
  type:'line',
  data:{{
    labels:prices.map(p=>'$'+p),
    datasets:[
      {{label:'Valore attuale',data:[],borderColor:'#00C2FF',backgroundColor:'rgba(0,194,255,0.07)',fill:true,pointRadius:0,borderWidth:2.5,tension:0.3}},
      {{label:'A scadenza',data:[],borderColor:'#8B9FC0',backgroundColor:'transparent',fill:false,pointRadius:0,borderWidth:1.5,tension:0,borderDash:[6,4]}}
    ]
  }},
  options:{{
    responsive:true,maintainAspectRatio:false,
    interaction:{{mode:'index',intersect:false}},
    plugins:{{
      legend:{{display:false}},
      tooltip:{{
        backgroundColor:'#0D1520',borderColor:'rgba(0,194,255,0.3)',borderWidth:1,
        titleColor:'#E2E8F0',bodyColor:'#8B9FC0',
        callbacks:{{
          title:ctx=>'SPY a '+ctx[0].label,
          label:ctx=>{{const v=ctx.dataset.data[ctx.dataIndex];if(v===null||v===undefined)return null;return ctx.dataset.label+': '+(v>=0?'+':'')+'€'+v;}}
        }}
      }}
    }},
    scales:{{
      x:{{ticks:{{autoSkip:true,maxTicksLimit:10,color:'#4A6080',font:{{size:10}}}},grid:{{color:'rgba(255,255,255,0.04)'}}}},
      y:{{ticks:{{color:'#4A6080',font:{{size:10}},callback:v=>(v>=0?'+':'')+'€'+v}},grid:{{color:'rgba(255,255,255,0.04)'}}}}
    }}
  }}
}});

function updateChart(dte,iv){{
  chart.data.datasets[0].data=prices.map(p=>bpsCurrent(p,dte,iv));
  chart.data.datasets[1].data=prices.map(p=>bpsExp(p));
  chart.update('none');
  const spotPnl=bpsCurrent(SPOT,dte,iv);
  const tp50=Math.round(CREDIT*100*0.5*100)/100;
  const sl2x=Math.round(CREDIT*100*2*100)/100;
  const pctD=Math.round((1-dte/TOTAL_DTE)*100);
  document.getElementById('statusBar').innerHTML=`
    <div class="card"><div class="card-label">P&L allo spot</div><div class="card-val ${{spotPnl>=0?'green':'red'}}">${{spotPnl>=0?'+':''}}€${{spotPnl}}</div></div>
    <div class="card"><div class="card-label">Theta decayato</div><div class="card-val">${{pctD}}%</div></div>
    <div class="card"><div class="card-label">Take profit 50%</div><div class="card-val green">+€${{tp50}}</div></div>
    <div class="card"><div class="card-label">Stop loss 2x</div><div class="card-val red">-€${{sl2x}}</div></div>
  `;
}}

let curDte=TOTAL_DTE;
document.getElementById('dteSlider').addEventListener('input',function(){{
  curDte=parseInt(this.value);
  document.getElementById('dteVal').textContent=curDte;
  updateChart(curDte,IV);
}});

updateChart(TOTAL_DTE,IV);
</script>
</body>
</html>
""", height=620)

    # ── GRAFICO TRADINGVIEW ──
    _tv_map = {"^GSPC": "SP:SPX", "^DJI": "DJ:DJI", "^NDX": "NASDAQ:NDX"}
    tk_tv = _tv_map.get(tk, tk)
    st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--text-secondary)'><span style='color:var(--accent-green);margin-right:0.5rem'>&#9678;</span>Grafico</span>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
    st.components.v1.html(f"""
    <div style="border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,0.06)">
    <div class="tradingview-widget-container" style="height:420px">
      <div id="tradingview_bps" style="height:100%"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "width": "100%",
        "height": 420,
        "symbol": "{tk_tv}",
        "interval": "D",
        "timezone": "Europe/Rome",
        "theme": "dark",
        "style": "1",
        "locale": "it",
        "toolbar_bg": "#080C10",
        "enable_publishing": false,
        "hide_top_toolbar": false,
        "hide_legend": false,
        "save_image": false,
        "container_id": "tradingview_bps",
        "backgroundColor": "#080C10",
        "gridColor": "rgba(255,255,255,0.03)",
      }});
      </script>
    </div>
    </div>
    """, height=430)
    st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

    # ── RIEPILOGO BPS ──
    st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--text-secondary)'><span style='color:var(--accent-green);margin-right:0.5rem'>&#9678;</span>Riepilogo Operazione</span>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "Parametro": ["Strumento","Prezzo Attuale","Strike Venduto (STO)","Strike Comprato (BTO)",
                      "Larghezza Spread","Giorni alla Scadenza",
                      "Credito Netto per Azione","Numero Contratti",
                      "Margine per Contratto (fisso)","Margine Totale Richiesto",
                      "Credito Totale Incassato","Break-even","Take Profit (50%)",
                      "Stop Loss (2x credito)","Rendimento sul Margine"],
        "Valore":    [nome, fmt(spot,2), fmt(bps_K_venduta,2), fmt(bps_K_comprata,2),
                      f"${larghezza_spread}", f"{dte} gg",
                      f"{fmt(bps_credito,4)} ({fmt(bps_credito*100,2)} € / contratto)",
                      str(n_contratti), f"{fmt(bps_margine_c,0)} €",
                      f"{fmt(bps_margine_tot,0)} € (da avere sul conto)",
                      f"+{fmt(bps_credito_tot,2)} €",
                      fmt(bps_be,2), f"+{fmt(bps_tp,2)} €",
                      f"-{fmt(bps_sl,2)} €",
                      f"{fmt(bps_rend,2)}% / mese  ({fmt(bps_rend_ann,2)}% annuo stimato)"],
    }), use_container_width=True, hide_index=True,
        column_config={
            "Parametro": st.column_config.TextColumn(width="medium"),
            "Valore":    st.column_config.TextColumn(width="large"),
        })

elif STRATEGIA == "bull_put_spread":
    st.info("Inserisci il credito netto e la larghezza dello spread nella sidebar per visualizzare l'analisi.")

# ══════════════════════════════════════════════════════════════
# LONG CALL / LONG PUT — DASHBOARD
# ══════════════════════════════════════════════════════════════
if STRATEGIA in ("long_call", "long_put"):
    is_call    = STRATEGIA == "long_call"
    tipo_label = "Long Call" if is_call else "Long Put"

    import scipy.stats as _si2

    def bs_option(S, K, T, r, sigma, flag):
        if T <= 0.0001:
            return max(S-K, 0) if flag else max(K-S, 0)
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        if flag:
            return float(S*_si2.norm.cdf(d1) - K*np.exp(-r*T)*_si2.norm.cdf(d2))
        else:
            return float(K*np.exp(-r*T)*_si2.norm.cdf(-d2) - S*_si2.norm.cdf(-d1))

    # ── Sidebar ──
    with st.sidebar:
        st.markdown(f"<div class='sb-section'>{tipo_label}</div>", unsafe_allow_html=True)

        # Strike
        if "slider_lo_strike" not in st.session_state:
            st.session_state["slider_lo_strike"] = round(spot * (1.02 if is_call else 0.98))
        if "input_lo_strike" not in st.session_state:
            st.session_state["input_lo_strike"] = st.session_state["slider_lo_strike"]
        st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>STRIKE ($)</span>", unsafe_allow_html=True)
        col_s, col_n = st.columns([2,1])
        _smin, _smax = float(round(spot*0.7)), float(round(spot*1.3))
        with col_s:
            st.slider("lo_str_s", _smin, _smax, key="slider_lo_strike", step=1.0,
                label_visibility="collapsed",
                on_change=lambda: st.session_state.update({"input_lo_strike": st.session_state["slider_lo_strike"]}))
        with col_n:
            st.number_input("lo_str_n", _smin, _smax, key="input_lo_strike", step=1.0, format="%.0f",
                label_visibility="collapsed",
                on_change=lambda: st.session_state.update({"slider_lo_strike": st.session_state["input_lo_strike"]}))
        lo_strike = float(st.session_state["slider_lo_strike"])

        lo_dte = dte  # riusa DTE dalla sidebar globale

        # Premio pagato
        _prem_default = round(bs_option(spot, lo_strike, lo_dte/365, 0.04, iv_pct/100, is_call), 2)
        if "slider_lo_prem" not in st.session_state:
            st.session_state["slider_lo_prem"] = min(_prem_default, 100.0)
        if "input_lo_prem" not in st.session_state:
            st.session_state["input_lo_prem"] = _prem_default
        st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>PREMIO PAGATO ($)</span>", unsafe_allow_html=True)
        col_s, col_n = st.columns([2,1])
        with col_s:
            st.slider("lo_prem_s", 0.01, 100.0, key="slider_lo_prem", step=0.01,
                label_visibility="collapsed",
                on_change=lambda: st.session_state.update({"input_lo_prem": st.session_state["slider_lo_prem"]}))
        with col_n:
            st.number_input("lo_prem_n", 0.01, 500.0, key="input_lo_prem", step=0.01, format="%.2f",
                label_visibility="collapsed",
                on_change=lambda: st.session_state.update({"slider_lo_prem": min(float(st.session_state["input_lo_prem"]), 100.0)}))
        lo_premio    = float(st.session_state["input_lo_prem"])
        lo_contratti = n_contratti

        st.markdown("<div class='sb-section'>Analisi Scenari</div>", unsafe_allow_html=True)
        lo_pdf_btn = st.button("Genera Report Scenari", use_container_width=True)

    # ── Calcoli base ──
    lo_sigma       = iv_pct / 100
    lo_T           = lo_dte / 365
    lo_r           = 0.04
    lo_val_attuale = bs_option(spot, lo_strike, lo_T, lo_r, lo_sigma, is_call)
    lo_pnl_attuale = (lo_val_attuale - lo_premio) * 100 * lo_contratti
    lo_be          = lo_strike + lo_premio if is_call else lo_strike - lo_premio
    lo_max_loss    = lo_premio * 100 * lo_contratti

    # ── KPI Cards (5 compatte, stesso stile PS/BPS) ──
    kpi_pnl_cls = "green" if lo_pnl_attuale >= 0 else "red"
    kpi_pnl_pre = "+" if lo_pnl_attuale >= 0 else ""
    st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card kpi-sm" style="animation-delay:0s">
    <div class="kpi-eyebrow">&#9679; Spot</div>
    <div class="kpi-value cyan">{fmt(spot,2)}</div>
    <div class="kpi-sub">Var. oggi<br><span style="color:var(--{'accent-green' if var>=0 else 'accent-red'})">{var:+.2f}%</span></div>
  </div>
  <div class="kpi-card kpi-sm" style="animation-delay:0.06s">
    <div class="kpi-eyebrow">&#9679; Valore BS</div>
    <div class="kpi-value cyan">{fmt(lo_val_attuale,2)}</div>
    <div class="kpi-sub">Premio pagato<br>{fmt(lo_premio,2)}</div>
  </div>
  <div class="kpi-card kpi-sm" style="animation-delay:0.12s">
    <div class="kpi-eyebrow">&#9679; P&amp;L attuale</div>
    <div class="kpi-value {kpi_pnl_cls}">{kpi_pnl_pre}{fmt(lo_pnl_attuale,0)} $</div>
    <div class="kpi-sub">Su {lo_contratti} contratt{'o' if lo_contratti==1 else 'i'}</div>
  </div>
  <div class="kpi-card kpi-sm" style="animation-delay:0.18s">
    <div class="kpi-eyebrow">&#9679; Break-even</div>
    <div class="kpi-value gold">{fmt(lo_be,2)}</div>
    <div class="kpi-sub">Strike {'+ premio' if is_call else '&minus; premio'}</div>
  </div>
  <div class="kpi-card kpi-sm" style="animation-delay:0.24s">
    <div class="kpi-eyebrow">&#9679; Max perdita</div>
    <div class="kpi-value red">-{fmt(lo_max_loss,0)} $</div>
    <div class="kpi-sub">Premio totale pagato</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Grafico P&L dinamico ──
    st.markdown(f"<div class='section-title'>Simulatore P&amp;L &mdash; {tipo_label}</div>", unsafe_allow_html=True)

    lo_chart_html = f"""
<div style="padding:0.5rem 0;">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;">
    <div>
      <label style="font-size:0.62rem;color:#8B9FC0;letter-spacing:0.1em;font-family:monospace;display:block;margin-bottom:4px;">DTE RESIDUI</label>
      <div style="display:flex;align-items:center;gap:8px;">
        <input type="range" id="dteR" min="0" max="{lo_dte}" value="{lo_dte}" step="1" style="flex:1;">
        <span id="dteRval" style="font-size:1rem;font-weight:600;min-width:32px;text-align:right;color:#E8EDF5;">{lo_dte}</span>
        <span style="font-size:0.68rem;color:#8B9FC0;">gg</span>
      </div>
    </div>
    <div>
      <label style="font-size:0.62rem;color:#8B9FC0;letter-spacing:0.1em;font-family:monospace;display:block;margin-bottom:4px;">IV FUTURA (%)</label>
      <div style="display:flex;align-items:center;gap:8px;">
        <input type="range" id="ivR" min="5" max="80" value="{iv_pct:.0f}" step="1" style="flex:1;">
        <span id="ivRval" style="font-size:1rem;font-weight:600;min-width:32px;text-align:right;color:#E8EDF5;">{iv_pct:.0f}</span>
        <span style="font-size:0.68rem;color:#8B9FC0;">%</span>
      </div>
    </div>
  </div>

  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:0.75rem;">
    <div style="background:#0F1E2E;border-radius:8px;padding:0.5rem 0.75rem;text-align:center;">
      <div style="font-size:0.58rem;color:#8B9FC0;font-family:monospace;letter-spacing:0.08em;">P&L ALLO SPOT</div>
      <div id="pnlSpot" style="font-size:1rem;font-weight:600;margin-top:2px;color:#E8EDF5;">—</div>
    </div>
    <div style="background:#0F1E2E;border-radius:8px;padding:0.5rem 0.75rem;text-align:center;">
      <div style="font-size:0.58rem;color:#8B9FC0;font-family:monospace;letter-spacing:0.08em;">VALORE OPZIONE</div>
      <div id="valOpt" style="font-size:1rem;font-weight:600;margin-top:2px;color:#E8EDF5;">—</div>
    </div>
    <div style="background:#0F1E2E;border-radius:8px;padding:0.5rem 0.75rem;text-align:center;">
      <div style="font-size:0.58rem;color:#8B9FC0;font-family:monospace;letter-spacing:0.08em;">MOLTIPLICATORE</div>
      <div id="moltip" style="font-size:1rem;font-weight:600;margin-top:2px;color:#E8EDF5;">—</div>
    </div>
    <div style="background:#0F1E2E;border-radius:8px;padding:0.5rem 0.75rem;text-align:center;">
      <div style="font-size:0.58rem;color:#8B9FC0;font-family:monospace;letter-spacing:0.08em;">THETA/GG</div>
      <div id="thetaV" style="font-size:1rem;font-weight:600;margin-top:2px;color:#FF5A5A;">—</div>
    </div>
  </div>

  <div style="position:relative;width:100%;height:280px;">
    <canvas id="loChart"></canvas>
  </div>

  <div style="margin-top:1.25rem;">
    <div style="font-size:0.58rem;color:#8B9FC0;font-family:monospace;letter-spacing:0.1em;margin-bottom:0.4rem;">TABELLA SCENARI — P&L PER PREZZO × IV</div>
    <div style="overflow-x:auto;">
      <table id="scenTable" style="width:100%;border-collapse:collapse;font-size:0.7rem;font-family:monospace;"></table>
    </div>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
const IS_CALL   = {'true' if is_call else 'false'};
const SPOT      = {spot:.4f};
const STRIKE    = {lo_strike:.2f};
const PREMIO    = {lo_premio:.4f};
const CONTRATTI = {lo_contratti};
const TOTAL_DTE = {lo_dte};
const R         = 0.04;

function normCDF(x){{
  const a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911;
  const sign=x<0?-1:1;
  const t=1/(1+p*Math.abs(x));
  const y=1-(((((a5*t+a4)*t)+a3)*t+a2)*t+a1)*t*Math.exp(-x*x/2);
  return 0.5*(1+sign*y);
}}

function bsOpt(S,K,T,r,sig){{
  if(T<=0.0001) return IS_CALL?Math.max(S-K,0):Math.max(K-S,0);
  const d1=(Math.log(S/K)+(r+0.5*sig*sig)*T)/(sig*Math.sqrt(T));
  const d2=d1-sig*Math.sqrt(T);
  if(IS_CALL) return S*normCDF(d1)-K*Math.exp(-r*T)*normCDF(d2);
  return K*Math.exp(-r*T)*normCDF(-d2)-S*normCDF(-d1);
}}

function bsTheta(S,K,T,r,sig){{
  if(T<=0.0001) return 0;
  const d1=(Math.log(S/K)+(r+0.5*sig*sig)*T)/(sig*Math.sqrt(T));
  const d2=d1-sig*Math.sqrt(T);
  const nd1=Math.exp(-d1*d1/2)/Math.sqrt(2*Math.PI);
  if(IS_CALL) return (-S*nd1*sig/(2*Math.sqrt(T))-r*K*Math.exp(-r*T)*normCDF(d2))/365;
  return (-S*nd1*sig/(2*Math.sqrt(T))+r*K*Math.exp(-r*T)*normCDF(-d2))/365;
}}

// Prezzi asse X: ±20% in step 1%
const prices=[];
for(let p=-20;p<=20;p++) prices.push(+(SPOT*(1+p/100)).toFixed(2));

const ctx=document.getElementById('loChart');
const chart=new Chart(ctx,{{
  type:'line',
  data:{{
    labels:prices.map(p=>'$'+p.toFixed(0)),
    datasets:[
      {{label:'Valore attuale',data:[],borderColor:'#00C2FF',backgroundColor:'rgba(0,194,255,0.07)',fill:true,pointRadius:0,borderWidth:2,tension:0.25}},
      {{label:'A scadenza',data:[],borderColor:'#555',backgroundColor:'transparent',fill:false,pointRadius:0,borderWidth:1.5,tension:0,borderDash:[5,4]}}
    ]
  }},
  options:{{
    responsive:true,maintainAspectRatio:false,
    animation:false,
    interaction:{{mode:'index',intersect:false}},
    plugins:{{
      legend:{{display:false}},
      tooltip:{{callbacks:{{
        title:ctx=>'SPY: '+ctx[0].label,
        label:ctx=>{{
          const v=ctx.dataset.data[ctx.dataIndex];
          return ctx.dataset.label+': '+(v>=0?'+':'')+'$'+Math.round(v);
        }}
      }}}}
    }},
    scales:{{
      x:{{ticks:{{autoSkip:true,maxTicksLimit:11,color:'#8B9FC0',font:{{size:10}}}},grid:{{color:'rgba(136,135,128,0.12)'}}}},
      y:{{ticks:{{color:'#8B9FC0',font:{{size:10}},callback:v=>(v>=0?'+':'')+'$'+Math.round(v)}},grid:{{color:'rgba(136,135,128,0.12)'}}}}
    }}
  }}
}});

function update(){{
  const dte=parseInt(document.getElementById('dteR').value);
  const ivPct=parseInt(document.getElementById('ivR').value);
  const iv=ivPct/100;
  const T=Math.max(dte/365,0.0001);
  document.getElementById('dteRval').textContent=dte;
  document.getElementById('ivRval').textContent=ivPct;

  // Curva valore attuale
  chart.data.datasets[0].data=prices.map(p=>+((bsOpt(p,STRIKE,T,R,iv)-PREMIO)*100*CONTRATTI).toFixed(1));
  // Curva scadenza
  chart.data.datasets[1].data=prices.map(p=>{{
    const v=IS_CALL?Math.max(p-STRIKE,0):Math.max(STRIKE-p,0);
    return +((v-PREMIO)*100*CONTRATTI).toFixed(1);
  }});
  chart.update('none');

  // KPI live
  const val=bsOpt(SPOT,STRIKE,T,R,iv);
  const pnl=(val-PREMIO)*100*CONTRATTI;
  const molt=PREMIO>0?val/PREMIO:0;
  const theta=bsTheta(SPOT,STRIKE,T,R,iv)*100*CONTRATTI;

  const el=document.getElementById('pnlSpot');
  el.textContent=(pnl>=0?'+':'')+'$'+Math.round(pnl);
  el.style.color=pnl>=0?'#00E5A0':'#FF5A5A';
  document.getElementById('valOpt').textContent='$'+val.toFixed(2);
  const em=document.getElementById('moltip');
  em.textContent=molt.toFixed(2)+'x';
  em.style.color=molt>=1?'#00E5A0':'#FF5A5A';
  document.getElementById('thetaV').textContent='$'+theta.toFixed(2)+'/gg';

  buildTable(dte,iv);
}}

function buildTable(dte,baseIV){{
  const ivLvl=[baseIV*0.6,baseIV*0.8,baseIV,baseIV*1.2,baseIV*1.4];
  const ivLbl=['-40%','-20%','Att.','+20%','+40%'];
  const T=Math.max(dte/365,0.0001);
  const pr=[];
  for(let p=-15;p<=15;p+=5) pr.push(+(SPOT*(1+p/100)).toFixed(2));
  let h='<thead><tr><th style="padding:3px 6px;color:#8B9FC0;text-align:left;border-bottom:1px solid #243550;white-space:nowrap;">Prezzo</th>';
  ivLbl.forEach(l=>h+=`<th style="padding:3px 6px;color:#8B9FC0;text-align:right;border-bottom:1px solid #243550;">${{l}}</th>`);
  h+='</tr></thead><tbody>';
  pr.forEach(p=>{{
    const isSpot=Math.abs(p-SPOT)<SPOT*0.04;
    h+=`<tr style="${{isSpot?'background:rgba(0,194,255,0.04);':''}}"><td style="padding:2px 6px;color:#8B9FC0;white-space:nowrap;">${{p>=SPOT?'▲':'▼'}} ${{p.toFixed(0)}}</td>`;
    ivLvl.forEach(iv=>{{
      const val=bsOpt(p,STRIKE,T,R,iv);
      const pnl=(val-PREMIO)*100*CONTRATTI;
      const bg=pnl>0?`rgba(0,229,160,${{Math.min(pnl/1000,0.3)}})`:`rgba(255,90,90,${{Math.min(Math.abs(pnl)/1000,0.3)}})`;
      const col=pnl>0?'#00E5A0':'#FF5A5A';
      h+=`<td style="padding:2px 6px;text-align:right;background:${{bg}};color:${{col}};font-weight:500;">${{pnl>=0?'+':''}}${{Math.round(pnl)}}</td>`;
    }});
    h+='</tr>';
  }});
  h+='</tbody>';
  document.getElementById('scenTable').innerHTML=h;
}}

document.getElementById('dteR').addEventListener('input',update);
document.getElementById('ivR').addEventListener('input',update);
update();
</script>
"""
    st.components.v1.html(lo_chart_html, height=780, scrolling=False)

    # ── Riepilogo operazione ──
    st.markdown(f"""
<div class="panel">
  <div class="panel-title">Riepilogo Operazione — {tipo_label}</div>
  <div class="kpi-grid" style="grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:0.6rem;margin-top:0.5rem;">
    <div class="tip-box-static"><span class="label">Sottostante</span><span class="val">{nome}</span></div>
    <div class="tip-box-static"><span class="label">Spot</span><span class="val">{fmt(spot,2)}</span></div>
    <div class="tip-box-static"><span class="label">Strike</span><span class="val">{fmt(lo_strike,2)}</span></div>
    <div class="tip-box-static"><span class="label">DTE</span><span class="val">{lo_dte} gg</span></div>
    <div class="tip-box-static"><span class="label">Premio pagato</span><span class="val">{fmt(lo_premio,2)} $ ({fmt(lo_premio*100,2)} € / contratto)</span></div>
    <div class="tip-box-static"><span class="label">Contratti</span><span class="val">{lo_contratti}</span></div>
    <div class="tip-box-static"><span class="label">Costo totale</span><span class="val">{fmt(lo_premio*100*lo_contratti,2)} €</span></div>
    <div class="tip-box-static"><span class="label">Break-even</span><span class="val">{fmt(lo_be,2)}</span></div>
    <div class="tip-box-static"><span class="label">Max perdita</span><span class="val">-{fmt(lo_max_loss,2)} € (premio pagato)</span></div>
    <div class="tip-box-static"><span class="label">IV IND</span><span class="val">{iv_pct:.1f}%</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# STRATEGY ADVISOR — DASHBOARD
# ══════════════════════════════════════════════════════════════
if STRATEGIA == "strategy_advisor":

    # ── Header ──
    st.markdown("""
<div class="ph-header">
  <div style="display:flex;align-items:center;gap:1.2rem">
    <div style="display:flex;flex-direction:column">
      <span style="font-size:1.45rem;font-weight:700;color:var(--accent-cyan);letter-spacing:-0.01em">Strategy Advisor</span>
      <span style="font-size:0.7rem;color:var(--text-muted);letter-spacing:0.12em;text-transform:uppercase;margin-top:1px">Analisi AI Istituzionale &middot; Web Search &middot; Raccomandazione Strategia</span>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:1rem">
    <span class="ph-tag" style="border-color:rgba(0,194,255,0.3);color:rgba(0,194,255,0.7)">&#9679; AI Powered</span>
    <span class="ph-tag">v5.1</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Sidebar Strategy Advisor ──
    with st.sidebar:
        st.markdown("<div class='sb-section'>Strategy Advisor</div>", unsafe_allow_html=True)

        # Selezione ticker
        TICKER_ADVISOR = {
            "NASDAQ 100 (QQQ)":   "QQQ",
            "S&P 500 (SPY)":      "SPY",
            "S&P 500 (^GSPC)":    "^GSPC",
            "Nasdaq 100 (^NDX)":  "^NDX",
            "Dow Jones (^DJI)":   "^DJI",
            "Apple (AAPL)":       "AAPL",
            "Tesla (TSLA)":       "TSLA",
            "NVIDIA (NVDA)":      "NVDA",
            "Microsoft (MSFT)":   "MSFT",
            "Amazon (AMZN)":      "AMZN",
        }
        adv_ticker_nome = st.selectbox("Sottostante", list(TICKER_ADVISOR.keys()), index=1, key="adv_ticker")
        adv_tk = TICKER_ADVISOR[adv_ticker_nome]

        st.markdown("<div class='sb-section'>Parametri Analisi</div>", unsafe_allow_html=True)

        # DTE orizzonte analisi
        adv_dte = st.select_slider("Orizzonte temporale (DTE)",
            options=[14, 21, 30, 45, 60, 90], value=45,
            help="DTE di riferimento per la strategia consigliata")

        # Capitale disponibile
        if "adv_capitale" not in st.session_state: st.session_state["adv_capitale"] = 10000
        st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>CAPITALE DISPONIBILE (€)</span>", unsafe_allow_html=True)
        adv_capitale = st.number_input("adv_cap", 1000, 500000,
            st.session_state["adv_capitale"], 1000,
            label_visibility="collapsed", key="adv_cap_input", format="%d")

        st.markdown("<div class='sb-section'>Avvia Analisi</div>", unsafe_allow_html=True)

        # Password AI
        import os as _os2
        ADV_PWD = _os2.environ.get("AI_PASSWORD", "")
        if "adv_sbloccato" not in st.session_state: st.session_state["adv_sbloccato"] = False

        if not st.session_state["adv_sbloccato"]:
            st.markdown("<span style='font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted);letter-spacing:0.1em'>PASSWORD</span>", unsafe_allow_html=True)
            adv_pwd_input = st.text_input("adv_pwd", type="password",
                label_visibility="collapsed", placeholder="Inserisci password…", key="adv_pwd")
            if adv_pwd_input:
                if adv_pwd_input == ADV_PWD:
                    st.session_state["adv_sbloccato"] = True
                    st.rerun()
                else:
                    st.error("Password errata.")
            adv_btn = st.button("🔒 Avvia Strategy Advisor", use_container_width=True, disabled=True)
        else:
            col_adv, col_lock = st.columns([4,1])
            with col_lock:
                if st.button("🔓", key="adv_lock", help="Blocca", use_container_width=True):
                    st.session_state["adv_sbloccato"] = False
                    st.rerun()
            adv_btn = st.button("Avvia Strategy Advisor", use_container_width=True,
                help="Analizza il sottostante con AI e web search per suggerire la strategia ottimale")

        # Torna alla home
        st.markdown("<div class='sb-section'></div>", unsafe_allow_html=True)
        if st.button("← Torna alla Home", use_container_width=True, key="adv_home"):
            st.session_state.strategia = None
            st.rerun()

    # ── Recupero dati per advisor ──
    if "adv_dati" not in st.session_state or st.session_state.get("adv_tk_cache") != adv_tk:
        with st.spinner(f"Recupero dati per {adv_tk}…"):
            st.session_state["adv_dati"] = recupera_dati_mercato(adv_tk)
            st.session_state["adv_tk_cache"] = adv_tk
    adv_dati = st.session_state["adv_dati"]

    if adv_dati.get("errore"):
        st.error(f"Errore dati: {adv_dati['errore']}")
    else:
        adv_spot   = adv_dati["prezzo_spot"]
        adv_vix    = adv_dati["vix"] or 0
        adv_ivr    = adv_dati["iv_rank"]
        adv_vol    = adv_dati["vol_storica"]
        adv_var    = adv_dati["variazione_gg"]
        adv_nome   = adv_dati["nome"]
        adv_vix_sym= adv_dati.get("vix_symbol", "^VIX")
        adv_vix_lbl= "VXN" if adv_vix_sym == "^VXN" else "VIX"

        # ── KPI snapshot ──
        iv_hv_ratio = round(adv_vix / adv_vol, 2) if adv_vol > 0 else 0
        regime_vol  = "ESTREMA" if adv_vix >= 35 else "ALTA" if adv_vix >= 25 else "MEDIA" if adv_vix >= 18 else "BASSA"
        regime_ivr  = "ALTO" if adv_ivr >= 50 else "MEDIO" if adv_ivr >= 30 else "BASSO"
        vol_col     = "green" if adv_vix >= 25 else "gold" if adv_vix >= 18 else "red"
        ivr_col     = "green" if adv_ivr >= 50 else "gold" if adv_ivr >= 30 else "red"
        var_col     = "green" if adv_var >= 0 else "red"

        st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card kpi-sm">
    <div class="kpi-eyebrow">&#9679; Spot</div>
    <div class="kpi-value cyan">{fmt(adv_spot,2)}</div>
    <div class="kpi-sub">Variazione oggi<br><span style="color:var(--{'accent-green' if adv_var>=0 else 'accent-red'})">{adv_var:+.2f}%</span></div>
  </div>
  <div class="kpi-card kpi-sm">
    <div class="kpi-eyebrow">&#9679; {adv_vix_lbl}</div>
    <div class="kpi-value {vol_col}">{fmt(adv_vix,2)}</div>
    <div class="kpi-sub">Regime volatilità<br>{regime_vol}</div>
  </div>
  <div class="kpi-card kpi-sm">
    <div class="kpi-eyebrow">&#9679; IV Rank</div>
    <div class="kpi-value {ivr_col}">{fmt(adv_ivr,0)}/100</div>
    <div class="kpi-sub">Premio<br>{regime_ivr}</div>
  </div>
  <div class="kpi-card kpi-sm">
    <div class="kpi-eyebrow">&#9679; Vol. Storica 30gg</div>
    <div class="kpi-value cyan">{fmt(adv_vol,1)}%</div>
    <div class="kpi-sub">IV/HV ratio<br>{iv_hv_ratio}x</div>
  </div>
  <div class="kpi-card kpi-sm">
    <div class="kpi-eyebrow">&#9679; DTE Orizzonte</div>
    <div class="kpi-value gold">{adv_dte} gg</div>
    <div class="kpi-sub">Capitale<br>€{adv_capitale:,}</div>
  </div>
</div>
""", unsafe_allow_html=True)

        # ── Pre-classificazione rule-based (mostrata subito) ──
        st.markdown("<div class='section-title'>Pre-Classificazione Rule-Based</div>", unsafe_allow_html=True)

        # Logica rule-based
        if adv_vix >= 35:
            rb_vol = "ESTREMA — mercato in panic selling"
            rb_strat = "Long Put / Bear Put Spread"
            rb_reason = "VIX estremo indica capitolazione — opportunità direzionali ribassiste o protezione"
            rb_conf = "MEDIA"
            rb_cls = "red"
        elif adv_vix >= 25 and adv_ivr >= 50:
            rb_vol = "ALTA con IV Rank elevato — condizioni premium ideali"
            rb_strat = "Iron Condor / Bull Put Spread"
            rb_reason = "IV gonfiata + IV Rank alto = massima efficienza vendita premium"
            rb_conf = "ALTA"
            rb_cls = "green"
        elif adv_vix >= 20 and adv_ivr >= 30:
            rb_vol = "MEDIA-ALTA — condizioni accettabili"
            rb_strat = "Bull Put Spread"
            rb_reason = "IV sufficiente per vendita premium con rischio definito"
            rb_conf = "MEDIA"
            rb_cls = "gold"
        elif adv_vix < 18 and adv_ivr < 30:
            rb_vol = "BASSA — premi insufficienti per vendita"
            rb_strat = "Long Call / Bull Call Spread"
            rb_reason = "IV bassa = opzioni economiche, favorevole per acquisto direzionale"
            rb_conf = "MEDIA"
            rb_cls = "cyan"
        else:
            rb_vol = "NEUTRO — contesto misto"
            rb_strat = "Attendere condizioni migliori"
            rb_reason = "IV Rank e VIX non segnalano un edge chiaro in nessuna direzione"
            rb_conf = "BASSA"
            rb_cls = "gold"

        st.markdown(f"""
<div class="panel" style="border-left:3px solid var(--accent-{'green' if rb_cls=='green' else 'red' if rb_cls=='red' else 'cyan' if rb_cls=='cyan' else 'gold'});">
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;">
    <div>
      <div style="font-size:0.6rem;color:var(--text-muted);font-family:var(--font-mono);letter-spacing:0.12em;margin-bottom:4px">REGIME VOLATILITÀ</div>
      <div style="font-size:0.9rem;font-weight:600;color:var(--text-primary)">{rb_vol}</div>
    </div>
    <div>
      <div style="font-size:0.6rem;color:var(--text-muted);font-family:var(--font-mono);letter-spacing:0.12em;margin-bottom:4px">STRATEGIA RULE-BASED</div>
      <div style="font-size:0.9rem;font-weight:600;color:var(--accent-cyan)">{rb_strat}</div>
    </div>
    <div>
      <div style="font-size:0.6rem;color:var(--text-muted);font-family:var(--font-mono);letter-spacing:0.12em;margin-bottom:4px">CONFIDENZA</div>
      <div style="font-size:0.9rem;font-weight:600;color:var(--{'accent-green' if rb_conf=='ALTA' else 'accent-gold' if rb_conf=='MEDIA' else 'accent-red'})">{rb_conf}</div>
    </div>
  </div>
  <div style="margin-top:0.75rem;font-size:0.8rem;color:var(--text-secondary);font-style:italic">{rb_reason}</div>
</div>
""", unsafe_allow_html=True)

        # ── Analisi AI approfondita ──
        st.markdown("<div class='section-title'>Analisi AI Istituzionale</div>", unsafe_allow_html=True)

        if adv_btn:
            with st.spinner("Strategy Advisor in esecuzione — ricerca web approfondita in corso…"):
                prompt_adv = costruisci_prompt_advisor(adv_tk, adv_nome, adv_dati)
                testo_adv = chiama_claude(prompt_adv)
            st.session_state["adv_risultato"] = testo_adv
            st.session_state["adv_ticker_analizzato"] = adv_tk

        if "adv_risultato" in st.session_state and st.session_state.get("adv_ticker_analizzato") == adv_tk:
            testo = st.session_state["adv_risultato"]
            if testo.startswith("ERRORE"):
                st.error(testo)
            else:
                # Parser sezioni
                import re as _re_adv
                sezioni_adv = _re_adv.split(r'─{5,}', testo)
                sezione_map = {}
                titoli_attesi = [
                    "SINTESI", "REGIME", "SNAPSHOT", "STRATEGIA",
                    "RAGIONAMENTO", "SCENARI", "RISCHI", "NO-TRADE", "NO TRADE"
                ]
                for blocco in sezioni_adv:
                    blocco = blocco.strip()
                    if not blocco: continue
                    prima_riga = blocco.split("\n")[0].strip().upper()
                    for t in titoli_attesi:
                        if t in prima_riga:
                            sezione_map[t] = "\n".join(blocco.split("\n")[1:]).strip()
                            break

                # Render sezioni con styling dedicato
                def render_sezione(titolo_display, chiavi, icon=""):
                    for k in chiavi:
                        if k in sezione_map and sezione_map[k]:
                            contenuto = sezione_map[k]
                            # Pulizia markdown
                            contenuto = _re_adv.sub(r'\*\*(.*?)\*\*', r'\1', contenuto)
                            contenuto = _re_adv.sub(r'#{1,3}\s*', '', contenuto, flags=_re_adv.MULTILINE)
                            linee = [l for l in contenuto.split("\n") if l.strip()]
                            html_contenuto = ""
                            for l in linee:
                                l = l.strip().lstrip("•-–").strip()
                                if not l: continue
                                html_contenuto += f'<p style="margin:0.3rem 0;font-size:0.82rem;color:var(--text-secondary);line-height:1.55">{l}</p>'
                            st.markdown(f"""
<div class="panel" style="margin-bottom:0.8rem;">
  <div style="font-size:0.6rem;color:var(--text-muted);font-family:var(--font-mono);letter-spacing:0.14em;margin-bottom:0.5rem">{icon} {titolo_display}</div>
  {html_contenuto}
</div>""", unsafe_allow_html=True)
                            return
                    st.markdown(f"""
<div class="panel" style="margin-bottom:0.8rem;opacity:0.4;">
  <div style="font-size:0.6rem;color:var(--text-muted);font-family:var(--font-mono);letter-spacing:0.14em">{icon} {titolo_display} — dati non disponibili</div>
</div>""", unsafe_allow_html=True)

                render_sezione("SINTESI ESECUTIVA", ["SINTESI"], "▶")
                render_sezione("REGIME DI MERCATO", ["REGIME"], "◈")

                col_snap, col_strat = st.columns([1, 1])
                with col_snap:
                    render_sezione("SNAPSHOT INDICATORI", ["SNAPSHOT"], "◉")
                with col_strat:
                    render_sezione("STRATEGIA CONSIGLIATA", ["STRATEGIA"], "★")

                render_sezione("RAGIONAMENTO ISTITUZIONALE", ["RAGIONAMENTO"], "◆")
                render_sezione("ANALISI SCENARI", ["SCENARI"], "◐")

                col_r, col_nt = st.columns([1, 1])
                with col_r:
                    render_sezione("RISCHI DA MONITORARE", ["RISCHI"], "⚠")
                with col_nt:
                    render_sezione("CONDIZIONE NO-TRADE", ["NO-TRADE", "NO TRADE"], "⊘")

                # Timestamp analisi
                st.markdown(f"""
<div style="text-align:right;font-size:0.65rem;color:var(--text-muted);font-family:var(--font-mono);margin-top:0.5rem">
  Analisi generata il {datetime.now().strftime('%d/%m/%Y %H:%M')} &middot; {adv_nome} ({adv_tk}) &middot; Spot: {fmt(adv_spot,2)}
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div class="panel" style="text-align:center;padding:2.5rem;opacity:0.6;">
  <div style="font-size:2rem;margin-bottom:0.75rem">&#9729;</div>
  <div style="font-size:0.9rem;color:var(--text-secondary)">Inserisci la password e premi <strong>Avvia Strategy Advisor</strong> per ricevere l'analisi istituzionale completa con web search in tempo reale.</div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="ph-footer">
    <span style="font-size:0.72rem;color:var(--text-secondary);font-weight:500">Phinance</span><br>
    Sistemi Quantitativi per il Trading di Opzioni &middot; v5.1<br>
    Dati: Yahoo Finance &nbsp;&middot;&nbsp; VIX: CBOE &nbsp;&middot;&nbsp; Motore: Black-Scholes<br>
    <span style="color:rgba(255,255,255,0.03);font-size:0.5rem">&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;</span><br>
    Solo a scopo educativo &middot; Non costituisce consulenza finanziaria
</div>
""", unsafe_allow_html=True)
