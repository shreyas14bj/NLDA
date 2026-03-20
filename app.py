"""
╔══════════════════════════════════════════════════════════════════╗
║          NLDA PRO · Natural Language Data Analyst                ║
║          Ultimate Elite Edition — v3.0                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json, io, os, re, time, hashlib, textwrap
from datetime import datetime
from collections import defaultdict
import warnings
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="NLDA Pro · Elite Data Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "NLDA Pro — Elite Natural Language Data Intelligence Platform"}
)

# ═══════════════════════════════════════════════════════════════════
#  DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════════════
STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Inter:wght@300;400;500;600&display=swap');

/* ── TOKENS ── */
:root {
    --void:       #05060a;
    --base:       #090b11;
    --surface:    #0e1117;
    --raised:     #131720;
    --overlay:    #181e2b;
    --border-dim: #1a2035;
    --border:     #232b40;
    --border-hi:  #2d3a55;

    --gold:       #f0c040;
    --gold-dim:   rgba(240,192,64,0.12);
    --gold-glow:  rgba(240,192,64,0.25);
    --cyan:       #22d3ee;
    --cyan-dim:   rgba(34,211,238,0.10);
    --violet:     #a78bfa;
    --violet-dim: rgba(167,139,250,0.10);
    --emerald:    #34d399;
    --rose:       #fb7185;
    --amber:      #fbbf24;

    --text-1:     #f1f5f9;
    --text-2:     #94a3b8;
    --text-3:     #475569;

    --radius-sm:  6px;
    --radius-md:  10px;
    --radius-lg:  16px;
    --radius-xl:  24px;

    --font-display: 'Syne', sans-serif;
    --font-body:    'Inter', sans-serif;
    --font-mono:    'JetBrains Mono', monospace;
}

/* ── RESET & BASE ── */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: var(--void) !important;
    font-family: var(--font-body);
    color: var(--text-1);
}
* { box-sizing: border-box; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 2px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--base) !important;
    border-right: 1px solid var(--border-dim) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0; }
[data-testid="stSidebar"] * { color: var(--text-1) !important; }
[data-testid="stSidebarContent"] { padding: 0 !important; }

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }
.block-container { padding: 1.5rem 2rem 4rem !important; max-width: 1400px; }

/* ── TYPOGRAPHY ── */
h1, h2, h3, h4 { font-family: var(--font-display) !important; letter-spacing: -0.02em; }

/* ── LOGO BANNER ── */
.nlda-logo-bar {
    background: linear-gradient(135deg, var(--base) 0%, var(--surface) 100%);
    border-bottom: 1px solid var(--border-dim);
    padding: 20px 24px 16px;
    margin: -1px -1px 0;
}
.nlda-logo-hex {
    font-size: 28px;
    line-height: 1;
    display: block;
    margin-bottom: 6px;
}
.nlda-logo-name {
    font-family: var(--font-display);
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, var(--gold) 0%, var(--amber) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: block;
    line-height: 1;
}
.nlda-logo-tag {
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-3);
    display: block;
    margin-top: 4px;
}

/* ── SIDEBAR SECTION HEADERS ── */
.sb-section {
    padding: 14px 20px 6px;
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-3);
    border-top: 1px solid var(--border-dim);
    margin-top: 8px;
}
.sb-section:first-of-type { border-top: none; }

/* ── STAT CHIPS (sidebar) ── */
.stat-strip {
    display: flex;
    gap: 6px;
    padding: 8px 16px 12px;
    flex-wrap: wrap;
}
.stat-chip {
    flex: 1; min-width: 70px;
    background: var(--raised);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 8px 10px;
    text-align: center;
}
.stat-chip-val {
    font-family: var(--font-mono);
    font-size: 18px;
    font-weight: 500;
    color: var(--gold);
    display: block;
    line-height: 1.1;
}
.stat-chip-lbl {
    font-size: 9px;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 2px;
    display: block;
}

/* ── DATASET CARDS (sidebar) ── */
.ds-card {
    margin: 4px 12px;
    background: var(--raised);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 10px 12px;
    cursor: pointer;
    transition: border-color 0.15s;
}
.ds-card.active { border-color: var(--gold); }
.ds-card-name {
    font-family: var(--font-display);
    font-size: 13px;
    font-weight: 700;
    color: var(--text-1);
}
.ds-card-meta {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-3);
    margin-top: 3px;
}
.ds-badge {
    display: inline-block;
    background: var(--gold-dim);
    border: 1px solid var(--gold-glow);
    border-radius: 4px;
    font-family: var(--font-mono);
    font-size: 9px;
    color: var(--gold);
    padding: 1px 5px;
    margin-right: 4px;
}

/* ── HERO ── */
.hero-wrap {
    position: relative;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    padding: 48px 56px;
    margin-bottom: 28px;
    overflow: hidden;
}
.hero-grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(var(--border-dim) 1px, transparent 1px),
        linear-gradient(90deg, var(--border-dim) 1px, transparent 1px);
    background-size: 40px 40px;
    opacity: 0.4;
}
.hero-glow {
    position: absolute;
    top: -80px; right: -80px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, var(--gold-glow) 0%, transparent 70%);
    pointer-events: none;
}
.hero-glow2 {
    position: absolute;
    bottom: -60px; left: 20%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(167,139,250,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.hero-eyebrow::before {
    content: '';
    display: block;
    width: 24px; height: 1px;
    background: var(--gold);
}
.hero-title {
    font-family: var(--font-display);
    font-size: clamp(36px, 5vw, 68px);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 0.95;
    color: var(--text-1);
    margin: 0 0 6px;
    position: relative;
}
.hero-title span {
    background: linear-gradient(135deg, var(--gold) 0%, var(--amber) 50%, var(--rose) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 17px;
    color: var(--text-2);
    font-weight: 300;
    margin-top: 14px;
    max-width: 560px;
    line-height: 1.6;
    position: relative;
}
.hero-badges {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 24px;
    position: relative;
}
.hero-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--raised);
    border: 1px solid var(--border-hi);
    border-radius: 50px;
    padding: 6px 14px;
    font-size: 12px;
    color: var(--text-2);
    font-family: var(--font-mono);
}
.hero-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
}

/* ── QUERY FORTRESS ── */
.query-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    padding: 24px;
    margin-bottom: 28px;
    position: relative;
}
.query-wrap::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: var(--radius-xl);
    background: linear-gradient(135deg, var(--gold), var(--violet), var(--cyan));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    padding: 1px;
    opacity: 0;
    transition: opacity 0.3s;
    pointer-events: none;
}
.query-wrap:focus-within::before { opacity: 1; }

.query-label {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-3);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.query-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border-dim);
}

/* ── ALL BUTTONS base reset ── */
.stButton > button {
    background: var(--raised) !important;
    color: var(--text-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 50px !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    padding: 6px 14px !important;
    transition: all 0.15s !important;
    letter-spacing: 0.02em !important;
    white-space: nowrap !important;
    cursor: pointer !important;
    pointer-events: auto !important;
}
.stButton > button:hover {
    border-color: var(--gold) !important;
    color: var(--gold) !important;
    background: var(--gold-dim) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
    opacity: 0.85 !important;
}

/* Primary analyze button — wraps a div.analyze-btn around the st.button */
div[data-testid="stButton"].analyze-btn > button,
.analyze-btn .stButton > button {
    background: linear-gradient(135deg, #c8980e, #f0c040) !important;
    color: #05060a !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-display) !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    padding: 12px 32px !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 4px 24px var(--gold-glow) !important;
}
div[data-testid="stButton"].analyze-btn > button:hover,
.analyze-btn .stButton > button:hover {
    box-shadow: 0 8px 40px var(--gold-glow) !important;
    transform: translateY(-2px) !important;
    color: #05060a !important;
    background: linear-gradient(135deg, #c8980e, #f0c040) !important;
}

/* Streamlit type="primary" button */
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #c8980e, #f0c040) !important;
    color: #05060a !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    padding: 12px 32px !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 4px 24px rgba(240,192,64,0.25) !important;
}
button[data-testid="baseButton-primary"]:hover {
    box-shadow: 0 8px 40px rgba(240,192,64,0.4) !important;
    transform: translateY(-2px) !important;
    color: #05060a !important;
    background: linear-gradient(135deg, #c8980e, #f0c040) !important;
}

/* ── TEXT INPUT ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--raised) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-1) !important;
    font-family: var(--font-body) !important;
    font-size: 16px !important;
    padding: 16px 20px !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-dim) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--text-3) !important; }

/* ── CHAT MESSAGES ── */
.msg-row { display: flex; flex-direction: column; gap: 4px; margin: 24px 0; }
.msg-user-wrap { display: flex; justify-content: flex-end; }
.msg-ai-wrap   { display: flex; justify-content: flex-start; }

.msg-user {
    max-width: 72%;
    background: linear-gradient(135deg, rgba(240,192,64,0.15) 0%, rgba(167,139,250,0.10) 100%);
    border: 1px solid rgba(240,192,64,0.3);
    border-radius: 20px 20px 4px 20px;
    padding: 14px 20px;
    font-size: 15px;
    line-height: 1.6;
    color: var(--text-1);
}
.msg-ai {
    max-width: 82%;
    background: var(--raised);
    border: 1px solid var(--border);
    border-radius: 4px 20px 20px 20px;
    padding: 14px 20px;
    font-size: 15px;
    line-height: 1.6;
    color: var(--text-2);
}
.msg-meta {
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-3);
    padding: 0 4px;
    margin-top: 4px;
}

/* ── RESULT PANEL ── */
.result-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    margin: 12px 0 28px;
}
.result-tab-bar {
    display: flex;
    background: var(--base);
    border-bottom: 1px solid var(--border-dim);
    padding: 0 6px;
    gap: 2px;
    overflow-x: auto;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--base) !important;
    border-bottom: 1px solid var(--border-dim) !important;
    border-radius: 0 !important;
    gap: 0 !important;
    padding: 0 8px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-3) !important;
    border-radius: 0 !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: 0.08em !important;
    padding: 12px 18px !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.15s !important;
}
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: var(--gold) !important;
    border-bottom-color: var(--gold) !important;
}
.stTabs [data-testid="stTabContent"] {
    background: var(--surface) !important;
    padding: 20px !important;
}

/* ── METRIC TILES ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin: 16px 0;
}
.kpi-tile {
    background: var(--raised);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}
.kpi-tile::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.kpi-tile.c-gold::after  { background: var(--gold); }
.kpi-tile.c-cyan::after  { background: var(--cyan); }
.kpi-tile.c-violet::after{ background: var(--violet); }
.kpi-tile.c-emerald::after{ background: var(--emerald); }
.kpi-tile.c-rose::after  { background: var(--rose); }

.kpi-val {
    font-family: var(--font-mono);
    font-size: 26px;
    font-weight: 500;
    color: var(--text-1);
    display: block;
    line-height: 1.1;
}
.kpi-lbl {
    font-size: 11px;
    color: var(--text-3);
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-family: var(--font-mono);
}
.kpi-delta {
    font-family: var(--font-mono);
    font-size: 11px;
    margin-top: 4px;
}
.kpi-delta.pos { color: var(--emerald); }
.kpi-delta.neg { color: var(--rose); }

/* ── INSIGHT CARDS ── */
.insight-row { display: flex; flex-direction: column; gap: 10px; margin: 12px 0; }
.insight-card {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    background: var(--raised);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px 16px;
}
.insight-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}
.insight-icon.gold   { background: var(--gold-dim);   }
.insight-icon.cyan   { background: var(--cyan-dim);   }
.insight-icon.violet { background: var(--violet-dim); }
.insight-text {
    font-size: 13px;
    color: var(--text-2);
    line-height: 1.6;
}

/* ── FOLLOW-UP BUTTONS ── */
.followup-wrap { margin-top: 20px; }
.followup-label {
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.2em;
    color: var(--text-3);
    text-transform: uppercase;
    margin-bottom: 10px;
}

/* ── CODE BLOCKS ── */
.code-wrap {
    position: relative;
    background: #020408;
    border: 1px solid var(--border-dim);
    border-radius: var(--radius-md);
    margin: 8px 0;
    overflow: hidden;
}
.code-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 16px;
    background: var(--base);
    border-bottom: 1px solid var(--border-dim);
}
.code-lang {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.15em;
    color: var(--text-3);
    text-transform: uppercase;
}
.code-body {
    padding: 20px;
    font-family: var(--font-mono);
    font-size: 12.5px;
    line-height: 1.7;
    color: #cdd6f4;
    overflow-x: auto;
    white-space: pre;
}
/* Syntax highlights */
.kw  { color: #cba6f7; }  /* keyword */
.fn  { color: #89b4fa; }  /* function */
.st  { color: #a6e3a1; }  /* string */
.cm  { color: #585b70; font-style: italic; }  /* comment */
.nm  { color: #fab387; }  /* number */
.op  { color: #89dceb; }  /* operator */

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: var(--raised) !important;
    border: 1.5px dashed var(--border-hi) !important;
    border-radius: var(--radius-lg) !important;
    padding: 16px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--gold) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border-radius: var(--radius-md); overflow: hidden; }
.stDataFrame { background: var(--raised) !important; }

/* ── SELECT / RADIO ── */
.stSelectbox > div > div {
    background: var(--raised) !important;
    border-color: var(--border) !important;
    color: var(--text-1) !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: var(--raised) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-2) !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: 0.05em !important;
}
.streamlit-expanderContent {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
}

/* ── DIVIDER ── */
.fancy-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 28px 0;
    color: var(--text-3);
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}
.fancy-divider::before, .fancy-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border-dim);
}

/* ── ONBOARDING STEPS ── */
.onboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin: 24px 0;
}
.onboard-card {
    background: var(--raised);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 24px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.onboard-card:hover { border-color: var(--border-hi); }
.onboard-num {
    font-family: var(--font-mono);
    font-size: 48px;
    font-weight: 500;
    color: var(--border-hi);
    line-height: 1;
    margin-bottom: 8px;
}
.onboard-title {
    font-family: var(--font-display);
    font-size: 16px;
    font-weight: 700;
    color: var(--text-1);
    margin-bottom: 8px;
}
.onboard-desc { font-size: 13px; color: var(--text-3); line-height: 1.5; }

/* ── TOAST / ALERT OVERRIDES ── */
[data-testid="stAlert"] {
    background: var(--raised) !important;
    border-radius: var(--radius-md) !important;
    border-left-width: 3px !important;
}

/* ── PROGRESS BAR ── */
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--gold), var(--amber)) !important;
}

/* ── LOADING SHIMMER ── */
@keyframes shimmer {
    0%   { background-position: -600px 0; }
    100% { background-position:  600px 0; }
}
.shimmer {
    background: linear-gradient(90deg, var(--raised) 25%, var(--overlay) 50%, var(--raised) 75%);
    background-size: 600px 100%;
    animation: shimmer 1.4s infinite;
    border-radius: var(--radius-sm);
    height: 14px;
    margin: 6px 0;
}

/* ── ANALYSIS STEP TRACKER ── */
.step-track {
    display: flex;
    gap: 0;
    margin: 16px 0;
    background: var(--raised);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    overflow: hidden;
}
.step-item {
    flex: 1;
    padding: 12px 8px;
    text-align: center;
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.08em;
    color: var(--text-3);
    border-right: 1px solid var(--border-dim);
    transition: all 0.3s;
}
.step-item:last-child { border-right: none; }
.step-item.done  { color: var(--emerald); background: rgba(52,211,153,0.06); }
.step-item.active { color: var(--gold);   background: var(--gold-dim); }
.step-dot { font-size: 14px; display: block; margin-bottom: 2px; }

/* ── COLUMN PROFILE ── */
.col-profile-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
    margin: 12px 0;
}
.col-card {
    background: var(--raised);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 12px 14px;
}
.col-card-name {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--gold);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.col-card-type {
    font-size: 10px;
    color: var(--text-3);
    font-family: var(--font-mono);
    margin-top: 2px;
}
.col-mini-bar-wrap {
    height: 4px;
    background: var(--border-dim);
    border-radius: 2px;
    margin-top: 8px;
    overflow: hidden;
}
.col-mini-bar {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--gold), var(--amber));
}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════════
_defaults = {
    "dataframes": {},
    "df_meta": {},           # stores column stats per df
    "chat_history": [],
    "api_key": "",
    "total_queries": 0,
    "charts_generated": 0,
    "pinned_charts": [],     # list of saved chart figures
    "conversation": [],      # multi-turn conversation list for context
    "active_tab": "chat",
    "query_tokens_used": 0,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════════
#  UTILITIES
# ═══════════════════════════════════════════════════════════════════
COLORS = {
    "plotly": ["#f0c040","#a78bfa","#22d3ee","#34d399","#fb7185","#fbbf24","#818cf8","#38bdf8"],
    "plotly_bg": "rgba(0,0,0,0)",
    "paper_bg": "rgba(0,0,0,0)",
    "font_color": "#f1f5f9",
    "grid": "#1a2035",
}
PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor=COLORS["paper_bg"],
    plot_bgcolor=COLORS["plotly_bg"],
    font=dict(family="JetBrains Mono, monospace", color=COLORS["font_color"], size=12),
    colorway=COLORS["plotly"],
    xaxis=dict(gridcolor=COLORS["grid"], zeroline=False),
    yaxis=dict(gridcolor=COLORS["grid"], zeroline=False),
    margin=dict(l=20, r=20, t=48, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0.4)", bordercolor="#232b40", borderwidth=1),
    title_font=dict(family="Syne, sans-serif", size=16, color="#f0c040"),
)

def fmt(n, decimals=2):
    try:
        decimals = int(decimals)
    except (ValueError, TypeError):
        decimals = 0
    if not isinstance(n, (int, float, np.integer, np.floating)):
        return str(n)
    try:
        if np.isnan(float(n)): return "—"
    except Exception:
        return str(n)
    n = float(n)
    if abs(n) >= 1_000_000_000: return f"{n/1e9:.{decimals}f}B"
    if abs(n) >= 1_000_000:     return f"{n/1e6:.{decimals}f}M"
    if abs(n) >= 1_000:         return f"{n/1e3:.{decimals}f}K"
    if isinstance(n, float):    return f"{n:.{decimals}f}"
    return f"{int(n):,}"

def col_profile(df: pd.DataFrame) -> dict:
    """Rich per-column statistics."""
    profile = {}
    for col in df.columns:
        s = df[col]
        dtype = str(s.dtype)
        nulls = int(s.isna().sum())
        null_pct = round(nulls / len(s) * 100, 1)
        unique = int(s.nunique())
        info = {"dtype": dtype, "nulls": nulls, "null_pct": null_pct, "unique": unique}
        if pd.api.types.is_numeric_dtype(s):
            info.update({
                "min": float(s.min()), "max": float(s.max()),
                "mean": float(s.mean()), "median": float(s.median()),
                "std": float(s.std()),
                "completeness": round((1 - null_pct/100) * 100, 1),
            })
        else:
            top = s.value_counts().head(3).to_dict()
            info["top_values"] = {str(k): int(v) for k, v in top.items()}
        profile[col] = info
    return profile

def df_schema_str(df: pd.DataFrame, name: str) -> str:
    lines = [f"TABLE `{name}` — {len(df):,} rows × {len(df.columns)} columns"]
    for col in df.columns:
        s = df[col]
        dtype = str(s.dtype)
        n_unique = s.nunique()
        samples = s.dropna().head(4).tolist()
        if pd.api.types.is_numeric_dtype(s):
            extra = f"min={s.min():.2g} max={s.max():.2g} mean={s.mean():.2g}"
        else:
            extra = f"top: {list(s.value_counts().head(2).index)}"
        lines.append(f"  {col} [{dtype}] unique={n_unique} | {extra} | sample={samples}")
    return "\n".join(lines)

def code_html(code: str, lang: str = "python") -> str:
    """Render a styled code block (basic keyword highlighting)."""
    escaped = (code
               .replace("&", "&amp;")
               .replace("<", "&lt;")
               .replace(">", "&gt;"))
    if lang == "python":
        kws = ["import","from","def","return","if","else","elif","for","in",
               "not","and","or","True","False","None","with","as","class","lambda"]
        for kw in kws:
            escaped = re.sub(rf'\b({kw})\b', r'<span class="kw">\1</span>', escaped)
        escaped = re.sub(r'(#[^\n]*)', r'<span class="cm">\1</span>', escaped)
        escaped = re.sub(r'\b(\d+\.?\d*)\b', r'<span class="nm">\1</span>', escaped)
        escaped = re.sub(r'(\"[^\"]*\"|\'[^\']*\')', r'<span class="st">\1</span>', escaped)
    elif lang == "sql":
        kws = ["SELECT","FROM","WHERE","GROUP BY","ORDER BY","HAVING","JOIN",
               "LEFT","RIGHT","INNER","ON","AS","AND","OR","NOT","LIMIT",
               "COUNT","SUM","AVG","MIN","MAX","DISTINCT","BY","DESC","ASC"]
        for kw in kws:
            escaped = re.sub(rf'\b({kw})\b', r'<span class="kw">\1</span>', escaped, flags=re.I)
    return f"""
<div class="code-wrap">
  <div class="code-header">
    <span class="code-lang">{lang}</span>
  </div>
  <div class="code-body">{escaped}</div>
</div>"""

# ═══════════════════════════════════════════════════════════════════
#  CLAUDE API
# ═══════════════════════════════════════════════════════════════════
SYSTEM_PROMPT_TEMPLATE = """You are NLDA Pro — an elite AI data analyst embedded in a premium analytics platform.

The user has uploaded these datasets:

{schemas}

CONVERSATION CONTEXT (last {n_ctx} exchanges):
{context}

Your task: answer the user's natural-language question with precision and insight.

RESPOND with ONLY a valid JSON object — no markdown fences, no preamble:

{{
  "summary": "Crisp 1-2 sentence answer referencing actual data values",
  "pandas_code": "Python/pandas code. Use `df` for single table or `dfs['name']` for multi-table. Store final result in `result_df`. No imports needed — pd, np, datetime available.",
  "sql_query": "Equivalent SQL SELECT (use table names matching dataset names, all lowercase)",
  "chart_type": "bar|line|scatter|pie|histogram|heatmap|box|area|treemap|funnel|none",
  "chart_config": {{
    "x": "column_name or null",
    "y": "column_name or null",
    "color": "column_name or null",
    "size": "column_name or null",
    "facet": "column_name or null",
    "title": "Descriptive chart title",
    "orientation": "v or h"
  }},
  "kpis": [
    {{"label": "Metric name", "value": "Formatted value", "delta": "+12.3% vs last period or null"}}
  ],
  "insights": [
    "Specific data-backed insight with actual numbers",
    "Another insight revealing a pattern or anomaly",
    "Actionable recommendation based on the data"
  ],
  "anomalies": ["Any surprising finding or outlier worth flagging"],
  "follow_up_questions": ["3 smart follow-up questions the user should ask next"],
  "confidence": "high|medium|low",
  "reasoning": "Brief explanation of your analytical approach"
}}

Rules:
- pandas_code: safe only, no file I/O, no subprocess, no __import__
- kpis: 2-4 items max, values pre-formatted as strings
- insights: minimum 2, reference actual numbers from the data
- chart_type "none" when query is purely textual
- Be specific — generic answers are not acceptable
"""

def call_claude(question: str, schemas: str, api_key: str, history: list) -> dict:
    import urllib.request
    import urllib.error

    # Build context string from recent history
    ctx_items = history[-4:] if len(history) > 4 else history
    ctx_str = "\n".join(
        f"Q: {h['question']}\nA: {h.get('summary','')}"
        for h in ctx_items
    ) or "(no prior context)"

    system = SYSTEM_PROMPT_TEMPLATE.format(
        schemas=schemas,
        n_ctx=len(ctx_items),
        context=ctx_str
    )
    payload = json.dumps({
        "model": "claude-haiku-4-5",
        "max_tokens": 3000,
        "system": system,
        "messages": [{"role": "user", "content": question}]
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        # Read the actual error body from Anthropic for a clear message
        error_body = e.read().decode("utf-8", errors="replace")
        try:
            error_json = json.loads(error_body)
            msg = error_json.get("error", {}).get("message", error_body)
        except Exception:
            msg = error_body
        raise RuntimeError(f"Anthropic API error {e.code}: {msg}") from None

    raw = body["content"][0]["text"].strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    result = json.loads(raw)

    # Token accounting
    usage = body.get("usage", {})
    st.session_state.query_tokens_used += usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
    return result

def safe_exec(code: str, dfs: dict) -> tuple[pd.DataFrame | None, str | None]:
    """Execute code in sandbox. Returns (result_df, error_message)."""
    env = {
        "pd": pd, "np": np,
        "dfs": dfs,
        "df": list(dfs.values())[0] if dfs else pd.DataFrame(),
        "result_df": None,
        "datetime": datetime,
    }
    try:
        exec(compile(code, "<nlda_code>", "exec"), env)
        res = env.get("result_df")
        if res is not None and not isinstance(res, pd.DataFrame):
            res = pd.DataFrame({"result": [res]})
        return res, None
    except Exception as e:
        return None, str(e)

def make_chart(df: pd.DataFrame, chart_type: str, cfg: dict) -> go.Figure | None:
    if df is None or df.empty or chart_type == "none":
        return None
    x, y = cfg.get("x"), cfg.get("y")
    color = cfg.get("color")
    size  = cfg.get("size")
    title = cfg.get("title", "")
    orient = cfg.get("orientation", "v")

    try:
        kwargs = dict(title=title)
        if chart_type == "bar":
            fig = px.bar(df, x=x, y=y, color=color, orientation=orient,
                         barmode="group" if color else "relative", **kwargs)
            fig.update_traces(marker_line_width=0, opacity=0.9)
        elif chart_type == "line":
            fig = px.line(df, x=x, y=y, color=color, markers=True, **kwargs)
            fig.update_traces(line_width=2.5)
        elif chart_type == "area":
            fig = px.area(df, x=x, y=y, color=color, **kwargs)
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x, y=y, color=color, size=size,
                             trendline="ols" if not color else None, **kwargs)
        elif chart_type == "pie":
            fig = px.pie(df, names=x, values=y, hole=0.42, **kwargs)
        elif chart_type == "histogram":
            fig = px.histogram(df, x=x, color=color, **kwargs)
        elif chart_type == "heatmap":
            num = df.select_dtypes(include="number")
            if num.shape[1] < 2:
                return None
            corr = num.corr().round(3)
            fig = px.imshow(corr, color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                            text_auto=True, **kwargs)
        elif chart_type == "box":
            fig = px.box(df, x=x, y=y, color=color, **kwargs)
        elif chart_type == "treemap":
            path_cols = [c for c in [color, x] if c]
            fig = px.treemap(df, path=path_cols or [x], values=y, **kwargs)
        elif chart_type == "funnel":
            fig = px.funnel(df, x=y, y=x, **kwargs)
        else:
            return None

        fig.update_layout(**PLOTLY_THEME)
        fig.update_layout(
            title_x=0.0,
            hoverlabel=dict(bgcolor="#131720", font_size=12, font_family="JetBrains Mono"),
        )
        # Clean up edges
        if chart_type not in ("pie", "treemap"):
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COLORS["grid"],
                             showline=False, tickfont=dict(size=11))
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS["grid"],
                             showline=False, tickfont=dict(size=11))
        return fig
    except Exception as e:
        return None

def generate_auto_kpis(df: pd.DataFrame) -> list[dict]:
    """Auto-generate KPI tiles from a result dataframe."""
    kpis = []
    num_cols = df.select_dtypes(include="number").columns.tolist()
    colors = ["c-gold", "c-cyan", "c-violet", "c-emerald"]
    for i, col in enumerate(num_cols[:4]):
        kpis.append({
            "label": col.replace("_", " ").title(),
            "value": fmt(df[col].sum() if len(df) > 1 else df[col].iloc[0]),
            "color": colors[i % len(colors)],
        })
    return kpis

def make_pdf(history: list) -> bytes:
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                        HRFlowable, Table, TableStyle, KeepTogether)
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                leftMargin=2.2*cm, rightMargin=2.2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        gold   = colors.HexColor('#f0c040')
        violet = colors.HexColor('#a78bfa')
        muted  = colors.HexColor('#475569')

        T = lambda txt, s: Paragraph(txt, s)
        title_s  = ParagraphStyle('T', parent=styles['Title'],  fontSize=26, textColor=gold,     spaceAfter=4, fontName='Helvetica-Bold')
        sub_s    = ParagraphStyle('S', parent=styles['Normal'], fontSize=11, textColor=muted,     spaceAfter=16)
        h2_s     = ParagraphStyle('H2',parent=styles['Heading2'],fontSize=14,textColor=violet,   spaceAfter=6, spaceBefore=14)
        body_s   = ParagraphStyle('B', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#cbd5e1'), leading=15, spaceAfter=5)
        mono_s   = ParagraphStyle('M', parent=styles['Normal'], fontSize=9,  textColor=colors.HexColor('#94a3b8'), fontName='Courier', leading=13, spaceAfter=4)
        bullet_s = ParagraphStyle('BU',parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#cbd5e1'), leading=14, spaceAfter=3, leftIndent=12)

        story = [
            T("NLDA Pro", title_s),
            T(f"Intelligence Report · {datetime.now().strftime('%A, %d %B %Y · %H:%M')}", sub_s),
            T(f"Total queries: {len(history)}  ·  Session analyses", sub_s),
            HRFlowable(width="100%", thickness=1, color=gold, spaceAfter=14),
            Spacer(1, 0.3*cm),
        ]
        for i, e in enumerate(history, 1):
            items = [
                T(f"Analysis {i}", h2_s),
                T(f"<b>Question:</b> {e['question']}", body_s),
                T(f"<b>Summary:</b> {e.get('summary','')}", body_s),
            ]
            for ins in e.get("insights", []):
                items.append(T(f"• {ins}", bullet_s))
            sql = e.get("sql_query", "")
            if sql:
                items.append(T("SQL Query:", h2_s))
                for line in sql.split("\n"):
                    items.append(T(line or " ", mono_s))
            items.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#1a2035'), spaceAfter=6))
            story.append(KeepTogether(items))
        doc.build(story)
        return buf.getvalue()
    except ImportError:
        return b""

def generate_demo_datasets() -> dict:
    np.random.seed(42)
    n = 300
    dates = pd.date_range("2022-01-01", periods=n, freq="D")
    regions = ["North America","Europe","Asia-Pacific","Latin America","Middle East"]
    products = ["Enterprise Suite","Pro Plan","Starter","Add-ons","Services"]
    reps = [f"Rep {chr(65+i)}" for i in range(8)]

    sales = pd.DataFrame({
        "date":           dates,
        "region":         np.random.choice(regions, n),
        "product":        np.random.choice(products, n),
        "sales_rep":      np.random.choice(reps, n),
        "revenue":        np.random.lognormal(8.2, 0.7, n).round(2),
        "units_sold":     np.random.randint(1, 120, n),
        "marketing_spend":np.random.lognormal(6.0, 0.5, n).round(2),
        "cac":            np.random.lognormal(5.5, 0.4, n).round(2),
        "churn_rate":     np.random.uniform(0.01, 0.18, n).round(4),
        "nps":            np.random.randint(1, 11, n),
        "cost":           np.random.lognormal(7.5, 0.6, n).round(2),
    })
    sales["profit"]        = (sales["revenue"] - sales["cost"]).round(2)
    sales["profit_margin"] = (sales["profit"] / sales["revenue"] * 100).round(2)
    sales["month"]         = sales["date"].dt.to_period("M").astype(str)
    sales["quarter"]       = sales["date"].dt.to_period("Q").astype(str)

    n2 = 60
    try:
        # pandas >= 2.2 uses "ME"; older uses "M"
        month_ends = pd.date_range("2022-01-01", periods=n2, freq="ME")
    except ValueError:
        month_ends = pd.date_range("2022-01-01", periods=n2, freq="M")
    mkt = pd.DataFrame({
        "month":         month_ends.strftime("%Y-%m"),
        "channel":       np.random.choice(["Paid Search","Social","Email","Content","Events","Referral"], n2),
        "spend":         np.random.lognormal(7.0, 0.6, n2).round(2),
        "impressions":   np.random.randint(5000, 200000, n2),
        "clicks":        np.random.randint(100, 8000, n2),
        "conversions":   np.random.randint(5, 500, n2),
        "revenue_attr":  np.random.lognormal(8.0, 0.8, n2).round(2),
    })
    mkt["cpc"]     = (mkt["spend"] / mkt["clicks"].clip(1)).round(2)
    mkt["roas"]    = (mkt["revenue_attr"] / mkt["spend"]).round(3)
    mkt["ctr_pct"] = (mkt["clicks"] / mkt["impressions"] * 100).round(2)

    return {"sales_data": sales, "marketing_data": mkt}

# ═══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="nlda-logo-bar">
        <span class="nlda-logo-hex">⬡</span>
        <span class="nlda-logo-name">NLDA Pro</span>
        <span class="nlda-logo-tag">Elite Data Intelligence · v3.0</span>
    </div>
    """, unsafe_allow_html=True)

    # API Key
    st.markdown('<div class="sb-section">Configuration</div>', unsafe_allow_html=True)
    with st.container():
        api_key_input = st.text_input(
            "Anthropic API Key",
            type="password",
            value=st.session_state.api_key,
            placeholder="sk-ant-api03-…",
            help="Your key is stored only in this session"
        )
        if api_key_input:
            st.session_state.api_key = api_key_input

    # Model selector (display only — always Sonnet 4)
    st.selectbox("Model", ["claude-haiku-4-5 (free tier)", "claude-sonnet-4-5 (paid)", "claude-opus-4-5 (paid)"], index=0)

    # Stats strip
    st.markdown('<div class="sb-section">Session Metrics</div>', unsafe_allow_html=True)
    total_rows = sum(len(df) for df in st.session_state.dataframes.values())
    total_cols = sum(len(df.columns) for df in st.session_state.dataframes.values())
    st.markdown(f"""
    <div class="stat-strip">
        <div class="stat-chip">
            <span class="stat-chip-val">{st.session_state.total_queries}</span>
            <span class="stat-chip-lbl">Queries</span>
        </div>
        <div class="stat-chip">
            <span class="stat-chip-val">{st.session_state.charts_generated}</span>
            <span class="stat-chip-lbl">Charts</span>
        </div>
        <div class="stat-chip">
            <span class="stat-chip-val">{len(st.session_state.dataframes)}</span>
            <span class="stat-chip-lbl">Datasets</span>
        </div>
        <div class="stat-chip">
            <span class="stat-chip-val">{fmt(total_rows, 0)}</span>
            <span class="stat-chip-lbl">Rows</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upload
    st.markdown('<div class="sb-section">Data Sources</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload CSV / Excel",
        type=["csv", "xlsx", "xls"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    if uploaded:
        for uf in uploaded:
            name = uf.name.rsplit(".", 1)[0].lower().replace(" ", "_")
            if name not in st.session_state.dataframes:
                try:
                    df = pd.read_csv(uf) if uf.name.endswith(".csv") else pd.read_excel(uf)
                    # Auto-detect and parse date columns
                    for col in df.columns:
                        if any(kw in col.lower() for kw in ["date","time","period","month","year"]):
                            try:
                                df[col] = pd.to_datetime(df[col])
                            except:
                                pass
                    st.session_state.dataframes[name] = df
                    st.session_state.df_meta[name] = col_profile(df)
                    st.success(f"✓ {name}")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Dataset list
    if st.session_state.dataframes:
        for dname, ddf in list(st.session_state.dataframes.items()):
            ncols = len(ddf.columns)
            nrows = len(ddf)
            num_cols = ddf.select_dtypes(include="number").columns.tolist()
            st.markdown(f"""
            <div class="ds-card active">
                <div class="ds-card-name">{dname}</div>
                <div class="ds-card-meta">
                    <span class="ds-badge">{nrows:,} rows</span>
                    <span class="ds-badge">{ncols} cols</span>
                    <span class="ds-badge">{len(num_cols)} numeric</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"✕ Remove {dname}", key=f"rm_{dname}"):
                del st.session_state.dataframes[dname]
                st.session_state.df_meta.pop(dname, None)
                st.rerun()

    # Demo datasets
    st.markdown('<div class="sb-section">Quick Start</div>', unsafe_allow_html=True)
    if st.button("⚡  Load Demo Datasets", use_container_width=True, key="sidebar_demo"):
        demo = generate_demo_datasets()
        for k, v in demo.items():
            st.session_state.dataframes[k] = v
            st.session_state.df_meta[k] = col_profile(v)
        st.rerun()

    # Export
    if st.session_state.chat_history:
        st.markdown('<div class="sb-section">Export</div>', unsafe_allow_html=True)
        if st.button("📄  Export PDF Intelligence Report", use_container_width=True):
            pdf = make_pdf(st.session_state.chat_history)
            if pdf:
                st.download_button(
                    "⬇  Download PDF",
                    pdf,
                    file_name=f"nlda_pro_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf"
                )
            else:
                st.info("Install reportlab: `pip install reportlab`")

        if st.button("🗑  Clear Session", use_container_width=True):
            for k, v in _defaults.items():
                st.session_state[k] = v
            st.rerun()

# ═══════════════════════════════════════════════════════════════════
#  MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════

# ── Hero ──────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-grid"></div>
    <div class="hero-glow"></div>
    <div class="hero-glow2"></div>
    <div class="hero-eyebrow">Elite Data Intelligence Platform</div>
    <h1 class="hero-title">
        Ask anything.<br>
        <span>Understand everything.</span>
    </h1>
    <p class="hero-sub">
        Upload your data, ask in plain English — get SQL, executable code,
        interactive charts, and expert-level insights in seconds.
    </p>
    <div class="hero-badges">
        <div class="hero-badge"><div class="dot" style="background:#34d399"></div>Claude Sonnet 4</div>
        <div class="hero-badge"><div class="dot" style="background:#f0c040"></div>Multi-table joins</div>
        <div class="hero-badge"><div class="dot" style="background:#a78bfa"></div>8 chart types</div>
        <div class="hero-badge"><div class="dot" style="background:#22d3ee"></div>PDF export</div>
        <div class="hero-badge"><div class="dot" style="background:#fb7185"></div>Context-aware</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Onboarding (no data) ──────────────────────────────────────────
if not st.session_state.dataframes:
    st.markdown("""
    <div class="onboard-grid">
        <div class="onboard-card">
            <div class="onboard-num">01</div>
            <div class="onboard-title">Upload Data</div>
            <div class="onboard-desc">Drag CSV or Excel files into the sidebar. Multiple files supported — join them with natural language.</div>
        </div>
        <div class="onboard-card">
            <div class="onboard-num">02</div>
            <div class="onboard-title">Ask Anything</div>
            <div class="onboard-desc">Type any question in plain English. The AI understands intent, not just keywords.</div>
        </div>
        <div class="onboard-card">
            <div class="onboard-num">03</div>
            <div class="onboard-title">Explore Insights</div>
            <div class="onboard-desc">Get charts, SQL, Python code, KPIs, and expert insights — all in one click.</div>
        </div>
        <div class="onboard-card">
            <div class="onboard-num">04</div>
            <div class="onboard-title">Export Report</div>
            <div class="onboard-desc">Download a professional PDF intelligence report of your entire analysis session.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Inline demo button so user doesn't have to find sidebar
    st.markdown("<br>", unsafe_allow_html=True)
    demo_col1, demo_col2, demo_col3 = st.columns([1, 2, 1])
    with demo_col2:
        if st.button("⚡  Try it now — Load Demo Datasets", use_container_width=True, key="onboard_demo"):
            demo = generate_demo_datasets()
            for k, v in demo.items():
                st.session_state.dataframes[k] = v
                st.session_state.df_meta[k] = col_profile(v)
            st.rerun()
    st.stop()

# ─────────────────────────────────────────────────────────────────
# From here on, data is guaranteed to be loaded
# ─────────────────────────────────────────────────────────────────

# ── Dataset explorer ──────────────────────────────────────────────
with st.expander("🗃  Dataset Explorer & Column Profiles", expanded=False):
    if st.session_state.dataframes:
        ds_tabs = st.tabs([f"  {n}  " for n in st.session_state.dataframes])
        for tab, (dname, ddf) in zip(ds_tabs, st.session_state.dataframes.items()):
            with tab:
                num_cols = ddf.select_dtypes(include="number").columns.tolist()
                # KPI row
                c1,c2,c3,c4,c5 = st.columns(5)
                c1.metric("Rows",      f"{len(ddf):,}")
                c2.metric("Columns",   len(ddf.columns))
                c3.metric("Numeric",   len(num_cols))
                c4.metric("Null %",    f"{ddf.isna().mean().mean()*100:.1f}%")
                c5.metric("Memory",    f"{ddf.memory_usage(deep=True).sum()/1024:.0f} KB")

                # Column profile cards
                profile = st.session_state.df_meta.get(dname, col_profile(ddf))
                cards_html = ""
                for col, info in list(profile.items())[:16]:
                    completeness = info.get("completeness", 100 - info.get("null_pct", 0))
                    dtype_short = info["dtype"].replace("float64","float").replace("int64","int").replace("object","str")
                    cards_html += f"""
                    <div class="col-card">
                        <div class="col-card-name">{col}</div>
                        <div class="col-card-type">{dtype_short} · {info['unique']} unique</div>
                        <div class="col-mini-bar-wrap">
                            <div class="col-mini-bar" style="width:{completeness}%"></div>
                        </div>
                    </div>"""
                st.markdown(f'<div class="col-profile-grid">{cards_html}</div>', unsafe_allow_html=True)
                st.dataframe(ddf.head(30), use_container_width=True, height=240)

# ── Chat history ──────────────────────────────────────────────────
if st.session_state.chat_history:
    st.markdown('<div class="fancy-divider">Analysis History</div>', unsafe_allow_html=True)

    for entry in st.session_state.chat_history:
        # User message
        st.markdown(f"""
        <div class="msg-row">
            <div class="msg-user-wrap">
                <div class="msg-user">{entry['question']}</div>
            </div>
            <div class="msg-meta" style="text-align:right">You · {entry.get('ts','')}</div>
        </div>
        """, unsafe_allow_html=True)

        # AI response summary
        confidence = entry.get("confidence","high")
        conf_color = {"high":"#34d399","medium":"#fbbf24","low":"#fb7185"}.get(confidence,"#34d399")
        st.markdown(f"""
        <div class="msg-row">
            <div class="msg-ai-wrap">
                <div class="msg-ai">
                    <span style="font-family:var(--font-mono);font-size:9px;
                                 letter-spacing:0.15em;color:{conf_color};
                                 text-transform:uppercase;display:block;margin-bottom:6px">
                        ⬡ NLDA Pro · {confidence} confidence
                    </span>
                    {entry.get('summary','Analysis complete.')}
                </div>
            </div>
            <div class="msg-meta">NLDA · {entry.get('ts','')}</div>
        </div>
        """, unsafe_allow_html=True)

        # KPI tiles
        _rdf = entry.get("result_df")
        _kpis_from_claude = entry.get("kpis") or []
        if _kpis_from_claude:
            kpis = _kpis_from_claude
        elif _rdf is not None and not _rdf.empty:
            kpis = generate_auto_kpis(_rdf)
        else:
            kpis = []
        if kpis:
            colors_cycle = ["c-gold","c-cyan","c-violet","c-emerald","c-rose"]
            tiles = ""
            for i, kpi in enumerate(kpis[:5]):
                c = kpi.get("color", colors_cycle[i % len(colors_cycle)])
                delta_html = ""
                if kpi.get("delta"):
                    is_pos = "+" in str(kpi["delta"])
                    cls = "pos" if is_pos else "neg"
                    delta_html = f'<div class="kpi-delta {cls}">{kpi["delta"]}</div>'
                tiles += f"""
                <div class="kpi-tile {c}">
                    <span class="kpi-val">{kpi["value"]}</span>
                    <span class="kpi-lbl">{kpi["label"]}</span>
                    {delta_html}
                </div>"""
            st.markdown(f'<div class="kpi-grid">{tiles}</div>', unsafe_allow_html=True)

        # Results tabs
        result_tabs = st.tabs([
            "  📊 Chart  ",
            "  📋 Table  ",
            "  💡 Insights  ",
            "  🔎 SQL  ",
            "  🐍 Code  ",
            "  🧠 Reasoning  ",
        ])

        with result_tabs[0]:
            if entry.get("fig"):
                pin_col, _ = st.columns([1, 5])
                with pin_col:
                    if st.button("📌 Pin Chart", key=f"pin_{entry['id']}"):
                        st.session_state.pinned_charts.append(entry["fig"])
                        st.success("Chart pinned!")
                st.plotly_chart(entry["fig"], use_container_width=True, key=f"fig_{entry['id']}")
            else:
                st.markdown("""
                <div style="padding:32px;text-align:center;color:#475569;
                             font-family:'JetBrains Mono',monospace;font-size:12px">
                    No chart generated for this query
                </div>""", unsafe_allow_html=True)

        with result_tabs[1]:
            rdf = entry.get("result_df")
            if rdf is not None and not rdf.empty:
                st.dataframe(rdf, use_container_width=True, height=320)
                dl1, dl2, _ = st.columns([1, 1, 4])
                with dl1:
                    st.download_button(
                        "⬇ CSV",
                        rdf.to_csv(index=False).encode(),
                        file_name=f"nlda_{entry['id']}.csv",
                        mime="text/csv",
                        key=f"csv_{entry['id']}"
                    )
                with dl2:
                    try:
                        xl_buf = io.BytesIO()
                        with pd.ExcelWriter(xl_buf, engine="openpyxl") as xw:
                            rdf.to_excel(xw, index=False)
                        st.download_button(
                            "⬇ Excel",
                            xl_buf.getvalue(),
                            file_name=f"nlda_{entry['id']}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"xl_{entry['id']}"
                        )
                    except:
                        pass
            else:
                st.info("No tabular result for this query.")

        with result_tabs[2]:
            insights = entry.get("insights", [])
            anomalies = entry.get("anomalies", [])
            icons = ["★", "◆", "▲", "●", "◉"]
            icon_classes = ["gold","cyan","violet","emerald","rose"]
            cards = ""
            for i, ins in enumerate(insights):
                ic = icons[i % len(icons)]
                cls = icon_classes[i % len(icon_classes)]
                cards += f"""
                <div class="insight-card">
                    <div class="insight-icon {cls}">{ic}</div>
                    <div class="insight-text">{ins}</div>
                </div>"""
            if anomalies:
                for a in anomalies:
                    cards += f"""
                    <div class="insight-card">
                        <div class="insight-icon rose">⚠</div>
                        <div class="insight-text"><strong>Anomaly:</strong> {a}</div>
                    </div>"""
            st.markdown(f'<div class="insight-row">{cards}</div>', unsafe_allow_html=True)

            fqs = entry.get("follow_up_questions", [])
            if fqs:
                st.markdown('<div class="followup-label">Suggested next questions</div>', unsafe_allow_html=True)
                fq_cols = st.columns(len(fqs))
                for col, q in zip(fq_cols, fqs):
                    with col:
                        if st.button(f"↗ {q}", key=f"fq_{entry['id']}_{q[:18]}"):
                            st.session_state["prefill"] = q
                            st.rerun()

        with result_tabs[3]:
            sql = entry.get("sql_query","")
            if sql:
                st.markdown(code_html(sql, "sql"), unsafe_allow_html=True)
            else:
                st.info("No SQL generated.")

        with result_tabs[4]:
            pyc = entry.get("pandas_code","")
            err = entry.get("exec_error","")
            if pyc:
                st.markdown(code_html(pyc, "python"), unsafe_allow_html=True)
            if err:
                st.error(f"Execution note: {err}")

        with result_tabs[5]:
            reasoning = entry.get("reasoning","")
            if reasoning:
                st.markdown(f"""
                <div style="background:var(--raised);border:1px solid var(--border);
                             border-radius:10px;padding:16px 20px;
                             font-size:13px;color:#94a3b8;line-height:1.7">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:9px;
                                 color:#475569;letter-spacing:0.15em;
                                 text-transform:uppercase;display:block;margin-bottom:10px">
                        AI Reasoning Chain
                    </span>
                    {reasoning}
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

# ── Pinned charts dashboard ───────────────────────────────────────
if st.session_state.pinned_charts:
    st.markdown('<div class="fancy-divider">Pinned Charts Dashboard</div>', unsafe_allow_html=True)
    cols = st.columns(min(2, len(st.session_state.pinned_charts)))
    for i, fig in enumerate(st.session_state.pinned_charts):
        with cols[i % 2]:
            st.plotly_chart(fig, use_container_width=True, key=f"pinned_{i}")
    if st.button("Clear Pinned Charts"):
        st.session_state.pinned_charts = []
        st.rerun()

# ═══════════════════════════════════════════════════════════════════
#  QUERY INPUT
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="fancy-divider">New Analysis</div>', unsafe_allow_html=True)

SUGGESTIONS = [
    "Top 10 by revenue",
    "Monthly revenue trend",
    "Correlation heatmap",
    "Profit by region (bar)",
    "Marketing ROAS by channel",
    "Revenue vs marketing spend scatter",
    "Quarterly cohort breakdown",
    "Anomalies & outliers",
]

prefill = st.session_state.pop("prefill", "")

# Suggestion chips
chip_cols = st.columns(len(SUGGESTIONS))
for i, (col, sug) in enumerate(zip(chip_cols, SUGGESTIONS)):
    with col:
        if st.button(sug, key=f"chip_{i}"):
            prefill = sug

st.markdown('<div class="query-wrap">', unsafe_allow_html=True)
st.markdown("""
<div class="query-label">Natural Language Query</div>
""", unsafe_allow_html=True)

query = st.text_input(
    "query",
    value=prefill,
    placeholder='Ask anything — e.g. "Which region has the highest profit margin over the last 3 months?"',
    label_visibility="collapsed",
    key="main_query_input"
)

a_col, b_col, c_col = st.columns([2, 1, 5])
with a_col:
    run = st.button("⬡  Analyze", use_container_width=True, key="run_btn",
                    type="primary")

with b_col:
    adv_mode = st.checkbox("Deep mode", value=False, help="More detailed analysis, slightly slower")

st.markdown('</div>', unsafe_allow_html=True)  # close query-wrap

# ═══════════════════════════════════════════════════════════════════
#  ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════════════
if run and query.strip():
    if not st.session_state.api_key:
        st.error("⚠ Please add your Anthropic API key in the sidebar.")
        st.stop()

    schemas = "\n\n".join(
        df_schema_str(df, name)
        for name, df in st.session_state.dataframes.items()
    )

    # Multi-step progress UI
    progress_placeholder = st.empty()
    with progress_placeholder.container():
        st.markdown("""
        <div class="step-track">
            <div class="step-item active">
                <span class="step-dot">⬡</span>PARSING
            </div>
            <div class="step-item">
                <span class="step-dot">○</span>CLAUDE
            </div>
            <div class="step-item">
                <span class="step-dot">○</span>EXECUTE
            </div>
            <div class="step-item">
                <span class="step-dot">○</span>VISUALIZE
            </div>
        </div>""", unsafe_allow_html=True)

    # Step 1: Call Claude
    progress_placeholder.empty()
    with progress_placeholder.container():
        st.markdown("""
        <div class="step-track">
            <div class="step-item done"><span class="step-dot">✓</span>PARSED</div>
            <div class="step-item active"><span class="step-dot">⬡</span>CLAUDE</div>
            <div class="step-item"><span class="step-dot">○</span>EXECUTE</div>
            <div class="step-item"><span class="step-dot">○</span>VISUALIZE</div>
        </div>""", unsafe_allow_html=True)

    try:
        result = call_claude(query.strip(), schemas, st.session_state.api_key,
                             st.session_state.chat_history)
    except json.JSONDecodeError as e:
        progress_placeholder.empty()
        st.error(f"**JSON parse error** — Claude returned malformed JSON. Try rephrasing your question. ({e})")
        st.stop()
    except RuntimeError as e:
        progress_placeholder.empty()
        st.error(f"**{e}**")
        st.stop()
    except Exception as e:
        progress_placeholder.empty()
        st.error(f"**Unexpected error:** {e}")
        st.stop()

    # Step 2: Execute code
    progress_placeholder.empty()
    with progress_placeholder.container():
        st.markdown("""
        <div class="step-track">
            <div class="step-item done"><span class="step-dot">✓</span>PARSED</div>
            <div class="step-item done"><span class="step-dot">✓</span>CLAUDE</div>
            <div class="step-item active"><span class="step-dot">⬡</span>EXECUTE</div>
            <div class="step-item"><span class="step-dot">○</span>VISUALIZE</div>
        </div>""", unsafe_allow_html=True)

    result_df, exec_err = None, None
    if result.get("pandas_code"):
        result_df, exec_err = safe_exec(result["pandas_code"], st.session_state.dataframes)

    # Step 3: Chart
    progress_placeholder.empty()
    with progress_placeholder.container():
        st.markdown("""
        <div class="step-track">
            <div class="step-item done"><span class="step-dot">✓</span>PARSED</div>
            <div class="step-item done"><span class="step-dot">✓</span>CLAUDE</div>
            <div class="step-item done"><span class="step-dot">✓</span>EXECUTED</div>
            <div class="step-item active"><span class="step-dot">⬡</span>VISUALIZE</div>
        </div>""", unsafe_allow_html=True)

    fig = None
    ctype = result.get("chart_type", "none")
    if ctype != "none" and result_df is not None and not result_df.empty:
        fig = make_chart(result_df, ctype, result.get("chart_config", {}))
        if fig:
            st.session_state.charts_generated += 1

    progress_placeholder.empty()

    # Save entry
    eid = hashlib.md5(f"{query}{time.time()}".encode()).hexdigest()[:10]
    ts  = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append({
        "id": eid,
        "ts": ts,
        "question":    query.strip(),
        "summary":     result.get("summary",""),
        "pandas_code": result.get("pandas_code",""),
        "sql_query":   result.get("sql_query",""),
        "chart_type":  ctype,
        "chart_config":result.get("chart_config",{}),
        "kpis":        result.get("kpis", []),
        "insights":    result.get("insights", []),
        "anomalies":   result.get("anomalies", []),
        "follow_up_questions": result.get("follow_up_questions", []),
        "confidence":  result.get("confidence", "high"),
        "reasoning":   result.get("reasoning", ""),
        "result_df":   result_df,
        "exec_error":  exec_err,
        "fig":         fig,
    })
    st.session_state.total_queries += 1
    st.rerun()
