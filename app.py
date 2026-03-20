"""
╔══════════════════════════════════════════════════════════════════╗
║   NLDA PRO v4.0 · Natural Language Data Analyst                  ║
║   "The Data Storyteller"                                         ║
╚══════════════════════════════════════════════════════════════════╝
NEW in v4.0:
  ✦ 18 chart types (candlestick, radar, waterfall, gauge, sunburst,
      parallel coords, violin, density heatmap, bubble, gantt, +more)
  ✦ Edit/re-run any past query inline
  ✦ Data Storytelling — AI writes a narrative arc across ALL analyses
  ✦ Chart Composer — manually build any chart with drag-and-drop cols
  ✦ Insight Timeline — visual thread connecting every finding
  ✦ Data DNA — automatic column fingerprint & outlier scanner
  ✦ Query Memory — save favourite queries to a library
  ✦ Live Comparison Mode — run 2 queries side by side
  ✦ Smart Auto-Dashboard — one click full analysis of entire dataset
  ✦ Multi-provider: Groq (free) · Gemini (free) · Anthropic
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json, io, re, time, hashlib, math
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="NLDA Pro · Data Storyteller",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
#  DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Inter:wght@300;400;500;600&display=swap');

:root{
  --void:#05060a;--base:#090b11;--surface:#0e1117;--raised:#131720;--overlay:#181e2b;
  --bd0:#1a2035;--bd1:#232b40;--bd2:#2d3a55;
  --gold:#f0c040;--gd:rgba(240,192,64,.12);--gg:rgba(240,192,64,.28);
  --cyan:#22d3ee;--cd:rgba(34,211,238,.10);
  --violet:#a78bfa;--vd:rgba(167,139,250,.10);
  --emerald:#34d399;--rose:#fb7185;--amber:#fbbf24;--sky:#38bdf8;--pink:#f472b6;
  --t1:#f1f5f9;--t2:#94a3b8;--t3:#475569;
  --r1:6px;--r2:10px;--r3:16px;--r4:24px;
  --fd:'Syne',sans-serif;--fb:'Inter',sans-serif;--fm:'JetBrains Mono',monospace;
}
html,body,.stApp,[data-testid="stAppViewContainer"]{background:var(--void)!important;font-family:var(--fb);color:var(--t1);}
*{box-sizing:border-box;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-thumb{background:var(--bd2);border-radius:2px;}

/* SIDEBAR */
[data-testid="stSidebar"]{background:var(--base)!important;border-right:1px solid var(--bd0)!important;}
[data-testid="stSidebar"] *{color:var(--t1)!important;}
[data-testid="stSidebarContent"]{padding:0 0 2rem!important;}
#MainMenu,footer,[data-testid="stDecoration"]{display:none!important;}
[data-testid="stSidebarCollapseButton"],[data-testid="collapsedControl"]{display:flex!important;opacity:1!important;}
.block-container{padding:1.5rem 2rem 4rem!important;max-width:1500px;}
h1,h2,h3,h4{font-family:var(--fd)!important;letter-spacing:-.02em;}

/* LOGO */
.logo-bar{background:linear-gradient(135deg,var(--base),var(--surface));border-bottom:1px solid var(--bd0);padding:18px 22px 14px;}
.logo-hex{font-size:26px;line-height:1;display:block;margin-bottom:5px;}
.logo-name{font-family:var(--fd);font-size:17px;font-weight:800;background:linear-gradient(135deg,var(--gold),var(--amber));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;display:block;line-height:1;}
.logo-tag{font-family:var(--fm);font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:var(--t3);display:block;margin-top:3px;}

/* SIDEBAR SECTIONS */
.sb-sec{padding:12px 18px 5px;font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--t3);border-top:1px solid var(--bd0);margin-top:6px;}

/* STAT STRIP */
.stat-strip{display:flex;gap:5px;padding:6px 14px 10px;flex-wrap:wrap;}
.sc{flex:1;min-width:60px;background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:7px 8px;text-align:center;}
.sc-v{font-family:var(--fm);font-size:16px;font-weight:500;color:var(--gold);display:block;line-height:1.1;}
.sc-l{font-size:8px;color:var(--t3);text-transform:uppercase;letter-spacing:.1em;margin-top:1px;display:block;}

/* DS CARD */
.ds-card{margin:3px 10px;background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:9px 11px;}
.ds-card.active{border-color:var(--gold);}
.ds-name{font-family:var(--fd);font-size:12px;font-weight:700;}
.ds-meta{font-family:var(--fm);font-size:9px;color:var(--t3);margin-top:2px;}
.ds-badge{display:inline-block;background:var(--gd);border:1px solid var(--gg);border-radius:3px;font-family:var(--fm);font-size:8px;color:var(--gold);padding:1px 4px;margin-right:3px;}

/* HERO */
.hero{position:relative;background:var(--surface);border:1px solid var(--bd1);border-radius:var(--r4);padding:44px 52px;margin-bottom:24px;overflow:hidden;}
.hero-grid{position:absolute;inset:0;background-image:linear-gradient(var(--bd0) 1px,transparent 1px),linear-gradient(90deg,var(--bd0) 1px,transparent 1px);background-size:40px 40px;opacity:.35;}
.hero-glow{position:absolute;top:-80px;right:-60px;width:360px;height:360px;background:radial-gradient(circle,var(--gg) 0%,transparent 70%);pointer-events:none;}
.hero-glow2{position:absolute;bottom:-50px;left:15%;width:280px;height:280px;background:radial-gradient(circle,rgba(167,139,250,.12) 0%,transparent 70%);pointer-events:none;}
.hero-eye{font-family:var(--fm);font-size:9px;letter-spacing:.25em;text-transform:uppercase;color:var(--gold);margin-bottom:10px;display:flex;align-items:center;gap:7px;}
.hero-eye::before{content:'';display:block;width:20px;height:1px;background:var(--gold);}
.hero-title{font-family:var(--fd);font-size:clamp(32px,5vw,64px);font-weight:800;letter-spacing:-.04em;line-height:.95;color:var(--t1);margin:0 0 5px;position:relative;}
.hero-title span{background:linear-gradient(135deg,var(--gold) 0%,var(--amber) 50%,var(--rose) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{font-size:16px;color:var(--t2);font-weight:300;margin-top:12px;max-width:540px;line-height:1.6;position:relative;}
.hero-badges{display:flex;gap:7px;flex-wrap:wrap;margin-top:20px;position:relative;}
.hb{display:flex;align-items:center;gap:5px;background:var(--raised);border:1px solid var(--bd2);border-radius:50px;padding:5px 12px;font-size:11px;color:var(--t2);font-family:var(--fm);}
.hb .dot{width:5px;height:5px;border-radius:50%;}

/* QUERY PANEL */
.q-wrap{background:var(--surface);border:1px solid var(--bd1);border-radius:var(--r4);padding:20px;margin-bottom:24px;position:relative;}
.q-wrap::before{content:'';position:absolute;inset:-1px;border-radius:var(--r4);background:linear-gradient(135deg,var(--gold),var(--violet),var(--cyan));-webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;padding:1px;opacity:0;transition:opacity .3s;pointer-events:none;}
.q-wrap:focus-within::before{opacity:1;}
.q-lbl{font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--t3);margin-bottom:12px;display:flex;align-items:center;gap:7px;}
.q-lbl::after{content:'';flex:1;height:1px;background:var(--bd0);}

/* BUTTONS */
.stButton>button{background:var(--raised)!important;color:var(--t2)!important;border:1px solid var(--bd1)!important;border-radius:7px!important;font-family:var(--fb)!important;font-size:12px!important;font-weight:500!important;line-height:1.35!important;padding:7px 10px!important;white-space:normal!important;word-break:break-word!important;min-height:36px!important;width:100%!important;transition:all .15s!important;cursor:pointer!important;}
.stButton>button:hover{border-color:var(--gold)!important;color:var(--gold)!important;background:var(--gd)!important;transform:translateY(-1px)!important;}
.stButton>button:active{transform:translateY(0)!important;opacity:.85!important;}
button[data-testid="baseButton-primary"]{background:linear-gradient(135deg,#c8980e,#f0c040)!important;color:#05060a!important;border:none!important;border-radius:var(--r2)!important;font-family:var(--fd)!important;font-size:14px!important;font-weight:700!important;padding:11px 28px!important;letter-spacing:.01em!important;white-space:nowrap!important;min-height:44px!important;box-shadow:0 4px 20px rgba(240,192,64,.25)!important;}
button[data-testid="baseButton-primary"]:hover{box-shadow:0 8px 36px rgba(240,192,64,.4)!important;transform:translateY(-2px)!important;color:#05060a!important;}
button[data-testid="baseButton-secondary"]{background:var(--overlay)!important;color:var(--cyan)!important;border:1px solid var(--cyan)!important;border-radius:var(--r2)!important;font-family:var(--fb)!important;font-size:12px!important;font-weight:600!important;padding:8px 18px!important;min-height:36px!important;}

/* TEXT INPUT */
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:var(--raised)!important;border:1px solid var(--bd1)!important;border-radius:var(--r2)!important;color:var(--t1)!important;font-family:var(--fb)!important;font-size:15px!important;padding:14px 18px!important;transition:border-color .2s!important;}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{border-color:var(--gold)!important;box-shadow:0 0 0 3px var(--gd)!important;}
.stTextInput>div>div>input::placeholder{color:var(--t3)!important;}

/* CHAT BUBBLES */
.msg-row{display:flex;flex-direction:column;gap:3px;margin:20px 0;}
.msg-user-wrap{display:flex;justify-content:flex-end;}
.msg-ai-wrap{display:flex;justify-content:flex-start;}
.msg-user{max-width:74%;background:linear-gradient(135deg,rgba(240,192,64,.14),rgba(167,139,250,.09));border:1px solid rgba(240,192,64,.28);border-radius:18px 18px 4px 18px;padding:13px 18px;font-size:15px;line-height:1.6;color:var(--t1);}
.msg-ai{max-width:84%;background:var(--raised);border:1px solid var(--bd1);border-radius:4px 18px 18px 18px;padding:13px 18px;font-size:15px;line-height:1.6;color:var(--t2);}
.msg-meta{font-family:var(--fm);font-size:8px;letter-spacing:.15em;text-transform:uppercase;color:var(--t3);padding:0 3px;margin-top:3px;}

/* TABS */
.stTabs [data-baseweb="tab-list"]{background:var(--base)!important;border-bottom:1px solid var(--bd0)!important;border-radius:0!important;gap:0!important;padding:0 6px!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--t3)!important;border-radius:0!important;font-family:var(--fm)!important;font-size:10px!important;letter-spacing:.08em!important;padding:11px 16px!important;border-bottom:2px solid transparent!important;transition:all .15s!important;}
.stTabs [aria-selected="true"]{background:transparent!important;color:var(--gold)!important;border-bottom-color:var(--gold)!important;}
.stTabs [data-testid="stTabContent"]{background:var(--surface)!important;padding:18px!important;}

/* KPI TILES */
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:14px 0;}
.kpi-tile{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:16px 18px;position:relative;overflow:hidden;}
.kpi-tile::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.c-gold::after{background:var(--gold);}.c-cyan::after{background:var(--cyan);}.c-violet::after{background:var(--violet);}.c-emerald::after{background:var(--emerald);}.c-rose::after{background:var(--rose);}.c-sky::after{background:var(--sky);}.c-pink::after{background:var(--pink);}
.kpi-val{font-family:var(--fm);font-size:24px;font-weight:500;color:var(--t1);display:block;line-height:1.1;}
.kpi-lbl{font-size:10px;color:var(--t3);margin-top:5px;text-transform:uppercase;letter-spacing:.08em;font-family:var(--fm);}
.kpi-delta{font-family:var(--fm);font-size:10px;margin-top:3px;}
.kpi-delta.pos{color:var(--emerald);}.kpi-delta.neg{color:var(--rose);}

/* INSIGHT CARDS */
.insight-row{display:flex;flex-direction:column;gap:8px;margin:10px 0;}
.insight-card{display:flex;gap:12px;align-items:flex-start;background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:12px 14px;}
.ins-icon{width:30px;height:30px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;}
.ins-text{font-size:13px;color:var(--t2);line-height:1.6;}

/* STORY BLOCK */
.story-wrap{background:linear-gradient(135deg,rgba(240,192,64,.05),rgba(167,139,250,.05));border:1px solid rgba(240,192,64,.2);border-radius:var(--r3);padding:24px 28px;margin:20px 0;position:relative;overflow:hidden;}
.story-wrap::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(180deg,var(--gold),var(--violet));}
.story-title{font-family:var(--fd);font-size:13px;font-weight:700;color:var(--gold);letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px;}
.story-text{font-size:15px;color:var(--t1);line-height:1.8;}
.story-chapter{font-family:var(--fd);font-size:11px;color:var(--violet);letter-spacing:.1em;text-transform:uppercase;margin:16px 0 6px;}

/* TIMELINE */
.timeline{position:relative;padding-left:28px;margin:16px 0;}
.timeline::before{content:'';position:absolute;left:8px;top:0;bottom:0;width:1px;background:linear-gradient(180deg,var(--gold),var(--violet),var(--cyan));}
.tl-item{position:relative;margin-bottom:20px;}
.tl-dot{position:absolute;left:-24px;top:4px;width:10px;height:10px;border-radius:50%;background:var(--gold);border:2px solid var(--void);}
.tl-time{font-family:var(--fm);font-size:9px;color:var(--t3);letter-spacing:.1em;margin-bottom:3px;}
.tl-q{font-size:13px;font-weight:600;color:var(--t1);}
.tl-a{font-size:12px;color:var(--t2);margin-top:3px;line-height:1.5;}

/* CHART COMPOSER */
.composer-wrap{background:var(--surface);border:1px solid var(--bd1);border-radius:var(--r3);padding:20px;margin:16px 0;}
.composer-title{font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:14px;}

/* COMPARE MODE */
.compare-wrap{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:16px 0;}
.compare-panel{background:var(--surface);border:1px solid var(--bd1);border-radius:var(--r3);padding:16px;overflow:hidden;}
.compare-label{font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;padding:6px 10px;border-radius:5px;display:inline-block;margin-bottom:10px;}
.compare-a{background:rgba(240,192,64,.1);color:var(--gold);border:1px solid rgba(240,192,64,.3);}
.compare-b{background:rgba(34,211,238,.1);color:var(--cyan);border:1px solid rgba(34,211,238,.3);}

/* CODE BLOCKS */
.code-wrap{position:relative;background:#020408;border:1px solid var(--bd0);border-radius:var(--r2);margin:7px 0;overflow:hidden;}
.code-hdr{display:flex;align-items:center;justify-content:space-between;padding:7px 14px;background:var(--base);border-bottom:1px solid var(--bd0);}
.code-lang{font-family:var(--fm);font-size:9px;letter-spacing:.15em;color:var(--t3);text-transform:uppercase;}
.code-body{padding:18px;font-family:var(--fm);font-size:12px;line-height:1.7;color:#cdd6f4;overflow-x:auto;white-space:pre;}
.kw{color:#cba6f7;}.fn{color:#89b4fa;}.st{color:#a6e3a1;}.cm{color:#585b70;font-style:italic;}.nm{color:#fab387;}

/* FILE UPLOADER */
[data-testid="stFileUploader"]{background:var(--raised)!important;border:1.5px dashed var(--bd2)!important;border-radius:var(--r3)!important;padding:14px!important;}

/* MISC */
[data-testid="stDataFrame"]{border-radius:var(--r2);overflow:hidden;}
.stSelectbox>div>div{background:var(--raised)!important;border-color:var(--bd1)!important;color:var(--t1)!important;}
[data-testid="stAlert"]{background:var(--raised)!important;border-radius:var(--r2)!important;border-left-width:3px!important;}
.stTabs{margin-top:0!important;}

/* DIVIDER */
.div{display:flex;align-items:center;gap:10px;margin:24px 0;color:var(--t3);font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;}
.div::before,.div::after{content:'';flex:1;height:1px;background:var(--bd0);}

/* ONBOARDING */
.ob-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:20px 0;}
.ob-card{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r3);padding:22px 18px;text-align:center;transition:border-color .2s;}
.ob-card:hover{border-color:var(--bd2);}
.ob-num{font-family:var(--fm);font-size:42px;font-weight:500;color:var(--bd2);line-height:1;margin-bottom:7px;}
.ob-title{font-family:var(--fd);font-size:15px;font-weight:700;color:var(--t1);margin-bottom:6px;}
.ob-desc{font-size:12px;color:var(--t3);line-height:1.5;}

/* STEP TRACKER */
.step-track{display:flex;margin:14px 0;background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);overflow:hidden;}
.step-item{flex:1;padding:11px 7px;text-align:center;font-family:var(--fm);font-size:9px;letter-spacing:.08em;color:var(--t3);border-right:1px solid var(--bd0);transition:all .3s;}
.step-item:last-child{border-right:none;}
.step-item.done{color:var(--emerald);background:rgba(52,211,153,.06);}
.step-item.active{color:var(--gold);background:var(--gd);}
.step-dot{font-size:13px;display:block;margin-bottom:2px;}

/* COL PROFILE */
.cp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(185px,1fr));gap:9px;margin:10px 0;}
.cp-card{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:11px 13px;}
.cp-name{font-family:var(--fm);font-size:10px;color:var(--gold);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cp-type{font-size:9px;color:var(--t3);font-family:var(--fm);margin-top:2px;}
.cp-bar-w{height:3px;background:var(--bd0);border-radius:2px;margin-top:7px;overflow:hidden;}
.cp-bar{height:100%;border-radius:2px;background:linear-gradient(90deg,var(--gold),var(--amber));}

/* DATA DNA */
.dna-wrap{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin:14px 0;}
.dna-card{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:14px;}
.dna-col{font-family:var(--fm);font-size:11px;color:var(--gold);margin-bottom:6px;}
.dna-row{display:flex;justify-content:space-between;font-size:11px;padding:2px 0;border-bottom:1px solid var(--bd0);}
.dna-row:last-child{border-bottom:none;}
.dna-k{color:var(--t3);}
.dna-v{color:var(--t1);font-family:var(--fm);}

/* QUERY LIBRARY */
.ql-item{display:flex;align-items:center;gap:8px;background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:9px 12px;margin:5px 0;cursor:pointer;transition:border-color .15s;}
.ql-item:hover{border-color:var(--gold);}
.ql-icon{color:var(--gold);font-size:12px;flex-shrink:0;}
.ql-text{font-size:12px;color:var(--t2);flex:1;}

/* EDIT BADGE */
.edit-badge{display:inline-flex;align-items:center;gap:4px;background:rgba(167,139,250,.12);border:1px solid rgba(167,139,250,.3);border-radius:4px;font-family:var(--fm);font-size:9px;color:var(--violet);padding:2px 7px;margin-left:8px;cursor:pointer;}

/* EXPANDER */
.streamlit-expanderHeader{background:var(--raised)!important;border:1px solid var(--bd1)!important;border-radius:var(--r2)!important;color:var(--t2)!important;font-family:var(--fm)!important;font-size:10px!important;}
.streamlit-expanderContent{background:var(--surface)!important;border:1px solid var(--bd1)!important;border-top:none!important;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════
_D = {
    "dataframes":{}, "df_meta":{}, "chat_history":[], "api_key":"",
    "total_queries":0, "charts_generated":0, "pinned_charts":[],
    "query_tokens_used":0,
    "provider":"Groq (Free)", "provider_key":"",
    "query_library":[],          # saved favourite queries
    "editing_idx":None,          # index of entry being edited
    "compare_mode":False,        # side-by-side compare
    "compare_a":"", "compare_b":"",
    "story_expanded":False,
    "auto_dash_done":False,
}
for k,v in _D.items():
    if k not in st.session_state: st.session_state[k]=v

# ═══════════════════════════════════════════════════════════════
#  CONSTANTS & THEME
# ═══════════════════════════════════════════════════════════════
PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono, monospace", color="#f1f5f9", size=11),
    colorway=["#f0c040","#a78bfa","#22d3ee","#34d399","#fb7185","#fbbf24","#818cf8","#38bdf8","#f472b6","#4ade80"],
    xaxis=dict(gridcolor="#1a2035", zeroline=False),
    yaxis=dict(gridcolor="#1a2035", zeroline=False),
    margin=dict(l=16, r=16, t=44, b=16),
    legend=dict(bgcolor="rgba(0,0,0,0.4)", bordercolor="#232b40", borderwidth=1),
    title_font=dict(family="Syne, sans-serif", size=15, color="#f0c040"),
)

CHART_TYPES = [
    "bar","grouped bar","stacked bar","horizontal bar",
    "line","multi-line","area","stacked area",
    "scatter","bubble","dot plot",
    "pie","donut","sunburst","treemap",
    "histogram","box","violin","strip",
    "heatmap","density heatmap","correlation matrix",
    "waterfall","funnel","gauge",
    "radar","parallel coordinates",
    "candlestick","ohlc",
    "none"
]

PROVIDERS = {
    "Groq (Free)":{"label":"Groq","model":"llama-3.3-70b-versatile",
      "url":"https://api.groq.com/openai/v1/chat/completions",
      "key_hint":"gsk_…","key_url":"https://console.groq.com","style":"openai","free":True,"badge_color":"#34d399"},
    "Gemini (Free)":{"label":"Gemini","model":"gemini-2.0-flash",
      "url":"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
      "key_hint":"AIza…","key_url":"https://aistudio.google.com","style":"gemini","free":True,"badge_color":"#a78bfa"},
    "Anthropic Claude":{"label":"Claude","model":"claude-sonnet-4-5",
      "url":"https://api.anthropic.com/v1/messages",
      "key_hint":"sk-ant-…","key_url":"https://console.anthropic.com","style":"anthropic","free":False,"badge_color":"#f0c040"},
}

# ═══════════════════════════════════════════════════════════════
#  UTILITIES
# ═══════════════════════════════════════════════════════════════
def fmt(n, d=2):
    try: d=int(d)
    except: d=0
    if not isinstance(n,(int,float,np.integer,np.floating)): return str(n)
    try:
        if np.isnan(float(n)): return "—"
    except: return str(n)
    n=float(n)
    if abs(n)>=1e9: return f"{n/1e9:.{d}f}B"
    if abs(n)>=1e6: return f"{n/1e6:.{d}f}M"
    if abs(n)>=1e3: return f"{n/1e3:.{d}f}K"
    return f"{n:.{d}f}"

def col_profile(df):
    p={}
    for col in df.columns:
        s=df[col]; nulls=int(s.isna().sum()); null_pct=round(nulls/max(len(s),1)*100,1)
        info={"dtype":str(s.dtype),"nulls":nulls,"null_pct":null_pct,"unique":int(s.nunique())}
        if pd.api.types.is_numeric_dtype(s):
            info.update({"min":float(s.min()),"max":float(s.max()),"mean":float(s.mean()),
                         "std":float(s.std()),"completeness":round(100-null_pct,1)})
        else:
            info["top_values"]={str(k):int(v) for k,v in s.value_counts().head(3).items()}
        p[col]=info
    return p

def df_schema_str(df, name):
    lines=[f"TABLE `{name}` — {len(df):,} rows × {len(df.columns)} columns"]
    for col in df.columns:
        s=df[col]
        extra=(f"min={s.min():.2g} max={s.max():.2g} mean={s.mean():.2g}"
               if pd.api.types.is_numeric_dtype(s) else f"top:{list(s.value_counts().head(2).index)}")
        lines.append(f"  {col}[{s.dtype}] unique={s.nunique()} {extra} sample={s.dropna().head(3).tolist()}")
    return "\n".join(lines)

def code_html(code, lang="python"):
    esc=code.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    if lang=="python":
        for kw in ["import","from","def","return","if","else","elif","for","in",
                   "not","and","or","True","False","None","with","as","class","lambda"]:
            esc=re.sub(rf'\b({kw})\b',r'<span class="kw">\1</span>',esc)
        esc=re.sub(r'(#[^\n]*)','<span class="cm">\\1</span>',esc)
        esc=re.sub(r'\b(\d+\.?\d*)\b','<span class="nm">\\1</span>',esc)
        esc=re.sub(r'("([^"]*)")'  ,'<span class="st">\\1</span>',esc)
    elif lang=="sql":
        for kw in ["SELECT","FROM","WHERE","GROUP BY","ORDER BY","HAVING","JOIN","LEFT","RIGHT",
                   "INNER","ON","AS","AND","OR","NOT","LIMIT","COUNT","SUM","AVG","MIN","MAX",
                   "DISTINCT","BY","DESC","ASC"]:
            esc=re.sub(rf'\b({kw})\b',r'<span class="kw">\1</span>',esc,flags=re.I)
    return (f'<div class="code-wrap"><div class="code-hdr"><span class="code-lang">{lang}</span></div>'
            f'<div class="code-body">{esc}</div></div>')

def generate_auto_kpis(df):
    kpis,colors=[],["c-gold","c-cyan","c-violet","c-emerald","c-rose","c-sky"]
    for i,col in enumerate(df.select_dtypes(include="number").columns[:6]):
        val=df[col].sum() if len(df)>1 else df[col].iloc[0]
        kpis.append({"label":col.replace("_"," ").title(),"value":fmt(val),"color":colors[i%6]})
    return kpis

def generate_demo_datasets():
    np.random.seed(42); n=300
    dates=pd.date_range("2022-01-01",periods=n,freq="D")
    regions=["North America","Europe","Asia-Pacific","Latin America","Middle East"]
    products=["Enterprise Suite","Pro Plan","Starter","Add-ons","Services"]
    reps=[f"Rep {chr(65+i)}" for i in range(8)]
    sales=pd.DataFrame({
        "date":dates,"region":np.random.choice(regions,n),"product":np.random.choice(products,n),
        "sales_rep":np.random.choice(reps,n),"revenue":np.random.lognormal(8.2,.7,n).round(2),
        "units_sold":np.random.randint(1,120,n),"marketing_spend":np.random.lognormal(6.,.5,n).round(2),
        "cac":np.random.lognormal(5.5,.4,n).round(2),"churn_rate":np.random.uniform(.01,.18,n).round(4),
        "nps":np.random.randint(1,11,n),"cost":np.random.lognormal(7.5,.6,n).round(2),
    })
    sales["profit"]=(sales["revenue"]-sales["cost"]).round(2)
    sales["profit_margin"]=(sales["profit"]/sales["revenue"]*100).round(2)
    sales["month"]=sales["date"].dt.to_period("M").astype(str)
    sales["quarter"]=sales["date"].dt.to_period("Q").astype(str)
    n2=60
    try:    me=pd.date_range("2022-01-01",periods=n2,freq="ME")
    except: me=pd.date_range("2022-01-01",periods=n2,freq="M")
    mkt=pd.DataFrame({
        "month":me.strftime("%Y-%m"),
        "channel":np.random.choice(["Paid Search","Social","Email","Content","Events","Referral"],n2),
        "spend":np.random.lognormal(7.,.6,n2).round(2),"impressions":np.random.randint(5000,200000,n2),
        "clicks":np.random.randint(100,8000,n2),"conversions":np.random.randint(5,500,n2),
        "revenue_attr":np.random.lognormal(8.,.8,n2).round(2),
    })
    mkt["cpc"]=(mkt["spend"]/mkt["clicks"].clip(1)).round(2)
    mkt["roas"]=(mkt["revenue_attr"]/mkt["spend"]).round(3)
    mkt["ctr_pct"]=(mkt["clicks"]/mkt["impressions"]*100).round(2)
    return {"sales_data":sales,"marketing_data":mkt}

# ═══════════════════════════════════════════════════════════════
#  CHART FACTORY  — 28 chart types
# ═══════════════════════════════════════════════════════════════
def make_chart(df, chart_type, cfg):
    if df is None or df.empty or chart_type=="none": return None
    x=cfg.get("x"); y=cfg.get("y"); color=cfg.get("color")
    size=cfg.get("size"); title=cfg.get("title",""); orient=cfg.get("orientation","v")
    try:
        kw=dict(title=title)
        ct=chart_type.lower().replace(" ","_")

        if   ct=="bar":              fig=px.bar(df,x=x,y=y,color=color,**kw); fig.update_traces(marker_line_width=0,opacity=.9)
        elif ct=="grouped_bar":      fig=px.bar(df,x=x,y=y,color=color,barmode="group",**kw)
        elif ct=="stacked_bar":      fig=px.bar(df,x=x,y=y,color=color,barmode="stack",**kw)
        elif ct=="horizontal_bar":   fig=px.bar(df,x=y,y=x,color=color,orientation="h",**kw)
        elif ct=="line":             fig=px.line(df,x=x,y=y,color=color,markers=True,**kw); fig.update_traces(line_width=2.5)
        elif ct=="multi_line":       fig=px.line(df,x=x,y=y,color=color,markers=True,**kw)
        elif ct=="area":             fig=px.area(df,x=x,y=y,color=color,**kw)
        elif ct=="stacked_area":     fig=px.area(df,x=x,y=y,color=color,groupnorm="",**kw)
        elif ct=="scatter":          fig=px.scatter(df,x=x,y=y,color=color,size=size,trendline="ols" if not color else None,**kw)
        elif ct=="bubble":           fig=px.scatter(df,x=x,y=y,color=color,size=size or y,**kw)
        elif ct=="dot_plot":         fig=px.strip(df,x=x,y=y,color=color,**kw)
        elif ct=="pie":              fig=px.pie(df,names=x,values=y,**kw)
        elif ct=="donut":            fig=px.pie(df,names=x,values=y,hole=.45,**kw)
        elif ct=="sunburst":
            path=[c for c in [color,x] if c]; fig=px.sunburst(df,path=path or [x],values=y,**kw)
        elif ct=="treemap":
            path=[c for c in [color,x] if c]; fig=px.treemap(df,path=path or [x],values=y,**kw)
        elif ct=="histogram":        fig=px.histogram(df,x=x,color=color,**kw)
        elif ct=="box":              fig=px.box(df,x=x,y=y,color=color,**kw)
        elif ct=="violin":           fig=px.violin(df,x=x,y=y,color=color,box=True,**kw)
        elif ct=="strip":            fig=px.strip(df,x=x,y=y,color=color,**kw)
        elif ct=="heatmap":
            num=df.select_dtypes(include="number")
            if num.shape[1]<2: return None
            fig=px.imshow(num.corr().round(3),color_continuous_scale="RdBu_r",zmin=-1,zmax=1,text_auto=True,**kw)
        elif ct=="density_heatmap":  fig=px.density_heatmap(df,x=x,y=y,**kw)
        elif ct=="correlation_matrix":
            num=df.select_dtypes(include="number")
            if num.shape[1]<2: return None
            fig=px.imshow(num.corr().round(3),color_continuous_scale="RdBu_r",zmin=-1,zmax=1,text_auto=True,**kw)
        elif ct=="waterfall":
            if x and y and x in df.columns and y in df.columns:
                fig=go.Figure(go.Waterfall(name="",orientation="v",
                    measure=["relative"]*len(df),x=df[x].astype(str),y=df[y],
                    connector={"line":{"color":"rgba(255,255,255,0.2)"}},
                    increasing={"marker":{"color":"#34d399"}},
                    decreasing={"marker":{"color":"#fb7185"}},
                    totals={"marker":{"color":"#f0c040"}}))
                fig.update_layout(title=title)
            else: return None
        elif ct=="funnel":           fig=px.funnel(df,x=y,y=x,**kw)
        elif ct=="gauge":
            if y and y in df.columns:
                val=float(df[y].mean()); mx=float(df[y].max())
                fig=go.Figure(go.Indicator(mode="gauge+number+delta",value=val,
                    delta={"reference":mx*0.6},
                    gauge={"axis":{"range":[0,mx]},
                           "bar":{"color":"#f0c040"},
                           "steps":[{"range":[0,mx*0.5],"color":"#1a2035"},{"range":[mx*0.5,mx*0.8],"color":"#232b40"}],
                           "threshold":{"line":{"color":"#fb7185","width":3},"thickness":.75,"value":mx*0.9}},
                    title={"text":title,"font":{"color":"#f0c040"}}))
            else: return None
        elif ct=="radar":
            num_cols=df.select_dtypes(include="number").columns.tolist()[:8]
            if len(num_cols)<3: return None
            means=df[num_cols].mean().tolist()
            fig=go.Figure(go.Scatterpolar(r=means+[means[0]],theta=num_cols+[num_cols[0]],
                fill="toself",line_color="#f0c040",fillcolor="rgba(240,192,64,.15)",name=title))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True,gridcolor="#232b40"),
                                         angularaxis=dict(gridcolor="#232b40")),title=title)
        elif ct=="parallel_coordinates":
            num_cols=df.select_dtypes(include="number").columns.tolist()
            if len(num_cols)<2: return None
            fig=px.parallel_coordinates(df,dimensions=num_cols,color=num_cols[0],
                color_continuous_scale=px.colors.diverging.Tealrose,**kw)
        elif ct in ("candlestick","ohlc"):
            if all(c in df.columns for c in ["open","high","low","close"]):
                xcol=x or (df.columns[0] if df.columns[0] not in ["open","high","low","close"] else None)
                if ct=="candlestick":
                    fig=go.Figure(go.Candlestick(x=df[xcol] if xcol else df.index,
                        open=df["open"],high=df["high"],low=df["low"],close=df["close"]))
                else:
                    fig=go.Figure(go.Ohlc(x=df[xcol] if xcol else df.index,
                        open=df["open"],high=df["high"],low=df["low"],close=df["close"]))
                fig.update_layout(title=title)
            else: return None
        else: return None

        fig.update_layout(**PLOTLY_THEME,title_x=0.,
                          hoverlabel=dict(bgcolor="#131720",font_size=11,font_family="JetBrains Mono"))
        if ct not in ("pie","donut","treemap","sunburst","heatmap","correlation_matrix",
                      "density_heatmap","radar","gauge","parallel_coordinates","candlestick","ohlc"):
            fig.update_xaxes(showgrid=True,gridwidth=1,gridcolor="#1a2035",showline=False,tickfont_size=10)
            fig.update_yaxes(showgrid=True,gridwidth=1,gridcolor="#1a2035",showline=False,tickfont_size=10)
        return fig
    except Exception: return None

def make_multi_chart_dashboard(df):
    """Auto-generate a 2×2 dashboard of charts from a dataframe."""
    num_cols=df.select_dtypes(include="number").columns.tolist()
    cat_cols=df.select_dtypes(include=["object","category"]).columns.tolist()
    date_cols=[c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    figs=[]
    try:
        if len(num_cols)>=2 and cat_cols:
            f=make_chart(df.groupby(cat_cols[0])[num_cols[0]].sum().reset_index(),
                         "bar",{"x":cat_cols[0],"y":num_cols[0],"title":f"{num_cols[0]} by {cat_cols[0]}"}); figs.append(f)
        if date_cols and num_cols:
            td=df.copy(); td["_dt"]=pd.to_datetime(td[date_cols[0]]).dt.to_period("M").astype(str)
            td2=td.groupby("_dt")[num_cols[0]].sum().reset_index()
            f=make_chart(td2,"line",{"x":"_dt","y":num_cols[0],"title":f"{num_cols[0]} over time"}); figs.append(f)
        if len(num_cols)>=2:
            f=make_chart(df,"scatter",{"x":num_cols[0],"y":num_cols[1],"title":f"{num_cols[0]} vs {num_cols[1]}"}); figs.append(f)
        if len(num_cols)>=3:
            f=make_chart(df,"heatmap",{"title":"Correlation Matrix"}); figs.append(f)
    except Exception: pass
    return [f for f in figs if f is not None]

def make_pdf(history):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors as rc
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
        buf=io.BytesIO()
        doc=SimpleDocTemplate(buf,pagesize=A4,leftMargin=2.2*cm,rightMargin=2.2*cm,topMargin=2*cm,bottomMargin=2*cm)
        sty=getSampleStyleSheet()
        gold=rc.HexColor('#f0c040'); violet=rc.HexColor('#a78bfa'); muted=rc.HexColor('#475569')
        T=lambda t,s:Paragraph(t,s)
        ts =ParagraphStyle('T', parent=sty['Title'],  fontSize=24,textColor=gold,  spaceAfter=4, fontName='Helvetica-Bold')
        ss =ParagraphStyle('S', parent=sty['Normal'], fontSize=10,textColor=muted, spaceAfter=14)
        h2s=ParagraphStyle('H2',parent=sty['Heading2'],fontSize=13,textColor=violet,spaceAfter=5,spaceBefore=12)
        bs =ParagraphStyle('B', parent=sty['Normal'], fontSize=10,textColor=rc.HexColor('#cbd5e1'),leading=14,spaceAfter=4)
        ms =ParagraphStyle('M', parent=sty['Normal'], fontSize=8, textColor=rc.HexColor('#94a3b8'),fontName='Courier',leading=12,spaceAfter=3)
        bus=ParagraphStyle('BU',parent=sty['Normal'], fontSize=10,textColor=rc.HexColor('#cbd5e1'),leading=13,spaceAfter=2,leftIndent=10)
        story=[T("NLDA Pro",ts),T(f"Data Intelligence Report · {datetime.now().strftime('%d %b %Y %H:%M')}",ss),
               HRFlowable(width="100%",thickness=1,color=gold,spaceAfter=12),Spacer(1,.3*cm)]
        for i,e in enumerate(history,1):
            items=[T(f"Analysis {i}",h2s),T(f"<b>Q:</b> {e['question']}",bs),T(f"<b>A:</b> {e.get('summary','')}",bs)]
            for ins in e.get("insights",[]): items.append(T(f"• {ins}",bus))
            if e.get("sql_query"):
                items.append(T("SQL:",h2s))
                for line in e["sql_query"].split("\n"): items.append(T(line or " ",ms))
            items.append(HRFlowable(width="100%",thickness=.5,color=rc.HexColor('#1a2035'),spaceAfter=5))
            story.append(KeepTogether(items))
        doc.build(story); return buf.getvalue()
    except ImportError: return b""

# ═══════════════════════════════════════════════════════════════
#  HTTP + MULTI-PROVIDER AI
# ═══════════════════════════════════════════════════════════════
def _http_post(url, headers, payload):
    import http.client, urllib.parse, ssl
    body_bytes=json.dumps(payload,ensure_ascii=False).encode("utf-8")
    safe_h={str(k):str(v).encode("ascii",errors="replace").decode("ascii") for k,v in headers.items()}
    safe_h["Content-Type"]="application/json; charset=utf-8"
    safe_h["Content-Length"]=str(len(body_bytes))
    p=urllib.parse.urlparse(url)
    host=p.netloc; path=p.path+(f"?{p.query}" if p.query else "")
    ctx=ssl.create_default_context()
    conn=(http.client.HTTPSConnection(host,timeout=90,context=ctx)
          if p.scheme=="https" else http.client.HTTPConnection(host,timeout=90))
    try:
        conn.request("POST",path,body=body_bytes,headers=safe_h)
        resp=conn.getresponse(); rb=resp.read().decode("utf-8",errors="replace")
    finally: conn.close()
    try: data=json.loads(rb)
    except json.JSONDecodeError: raise RuntimeError(f"HTTP {resp.status}: non-JSON — {rb[:300]}")
    if resp.status not in(200,201):
        msg=(data.get("error",{}).get("message") or data.get("message") or rb[:400])
        raise RuntimeError(f"API error {resp.status}: {msg}")
    return data

def _call_openai_compat(url,api_key,model,system,question):
    d=_http_post(url,{"Authorization":f"Bearer {api_key}"},
        {"model":model,"messages":[{"role":"system","content":system},{"role":"user","content":question}],
         "max_tokens":3500,"temperature":.1,"response_format":{"type":"json_object"}})
    return d["choices"][0]["message"]["content"]

def _call_gemini(url,api_key,system,question):
    prompt=f"{system}\n\nUser question: {question}\n\nRespond with ONLY a valid JSON object."
    d=_http_post(f"{url}?key={api_key}",{},
        {"contents":[{"role":"user","parts":[{"text":prompt}]}],
         "generationConfig":{"temperature":.1,"maxOutputTokens":3500}})
    try: return d["candidates"][0]["content"]["parts"][0]["text"]
    except(KeyError,IndexError): raise RuntimeError(f"Unexpected Gemini response: {str(d)[:300]}")

def _call_anthropic(url,api_key,model,system,question):
    d=_http_post(url,{"x-api-key":api_key,"anthropic-version":"2023-06-01"},
        {"model":model,"max_tokens":3500,"system":system,"messages":[{"role":"user","content":question}]})
    usage=d.get("usage",{})
    st.session_state.query_tokens_used+=usage.get("input_tokens",0)+usage.get("output_tokens",0)
    return d["content"][0]["text"]

def _parse_raw(raw):
    raw=re.sub(r'^```(?:json)?\s*','',raw.strip()); raw=re.sub(r'\s*```$','',raw)
    try: return json.loads(raw)
    except json.JSONDecodeError:
        m=re.search(r'\{.*\}',raw,re.DOTALL)
        if m: return json.loads(m.group())
        raise RuntimeError(f"Could not parse AI JSON response:\n{raw[:500]}")

SYSTEM_PROMPT="""You are NLDA Pro — an elite AI data analyst. You produce precise, data-backed analysis.

Datasets:
{schemas}

Conversation context:
{context}

Respond with ONLY a valid JSON object (no markdown fences, no extra text):

{{
  "summary": "1-2 crisp sentences referencing ACTUAL numbers from the data",
  "pandas_code": "pandas code — use df (single) or dfs['name'] (multi-table). Store final result in result_df. pd/np/datetime available. No imports.",
  "sql_query": "equivalent SQL SELECT statement",
  "chart_type": "one of: bar|grouped bar|stacked bar|horizontal bar|line|area|scatter|bubble|pie|donut|sunburst|treemap|histogram|box|violin|heatmap|density heatmap|waterfall|funnel|gauge|radar|parallel coordinates|candlestick|none",
  "chart_config": {{"x":"col or null","y":"col or null","color":"col or null","size":"col or null","title":"descriptive title","orientation":"v or h"}},
  "kpis": [{{"label":"short label","value":"formatted value string","delta":"+X.X% vs prior or null"}}],
  "insights": ["specific insight with exact numbers","second insight","third insight"],
  "anomalies": ["outlier or anomaly description, or empty list"],
  "follow_up_questions": ["smart follow-up q1?","q2?","q3?"],
  "confidence": "high|medium|low",
  "reasoning": "brief description of your analytical approach"
}}

Rules:
- pandas_code: no file I/O, no subprocess, no __import__
- kpis: 2-5 items max, values as formatted strings  
- insights must cite real numbers (e.g. "$1.2M", "34%", "top region: Europe")
- chart_type "none" only when the query is purely textual with no data result
"""

STORY_PROMPT="""You are a data storyteller. You have access to these AI analysis results from a data session:

{analyses}

Write a compelling data story (3-5 paragraphs) that:
1. Opens with the single biggest finding ("The headline")
2. Explains the underlying patterns and why they matter
3. Identifies the key tension or surprise in the data
4. Closes with a clear strategic recommendation

Write in plain English, like an insightful analyst presenting to a CEO. 
Reference specific numbers. Use story structure: setup, conflict, resolution.
Return ONLY the story text — no JSON, no headers, no markdown.
"""

def call_ai(question, schemas, history, extra_system=""):
    provider_name=st.session_state.get("provider","Groq (Free)")
    api_key=st.session_state.get("provider_key","").strip()
    if not api_key:
        raise RuntimeError(f"No API key for {provider_name}. Add it in the sidebar → Configuration.")
    cfg=PROVIDERS[provider_name]
    ctx="\n".join(f"Q:{h['question']}\nA:{h.get('summary','')}" for h in history[-4:]) or "(none)"
    system=SYSTEM_PROMPT.format(schemas=schemas,context=ctx)+(f"\n{extra_system}" if extra_system else "")
    raw={"openai":_call_openai_compat,"gemini":_call_gemini,"anthropic":_call_anthropic}[cfg["style"]](
        cfg["url"],api_key,cfg.get("model",""),system,question) if cfg["style"]!="gemini" else \
        _call_gemini(cfg["url"],api_key,system,question)
    return _parse_raw(raw)

def call_story(analyses_text):
    provider_name=st.session_state.get("provider","Groq (Free)")
    api_key=st.session_state.get("provider_key","").strip()
    if not api_key: return "Add an API key to generate a data story."
    cfg=PROVIDERS[provider_name]
    system=STORY_PROMPT.format(analyses=analyses_text)
    question="Write the data story now."
    try:
        if   cfg["style"]=="openai":    return _call_openai_compat(cfg["url"],api_key,cfg["model"],system,question)
        elif cfg["style"]=="gemini":    return _call_gemini(cfg["url"],api_key,system,question)
        elif cfg["style"]=="anthropic": return _call_anthropic(cfg["url"],api_key,cfg["model"],system,question)
    except Exception as e: return f"Story generation error: {e}"

def safe_exec(code, dfs):
    env={"pd":pd,"np":np,"datetime":datetime,
         "dfs":dfs,"df":list(dfs.values())[0] if dfs else pd.DataFrame(),"result_df":None}
    try:
        exec(compile(code,"<nlda>","exec"),env)
        res=env.get("result_df")
        if res is not None and not isinstance(res,pd.DataFrame):
            res=pd.DataFrame({"result":[res]})
        return res,None
    except Exception as e: return None,str(e)

# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div class="logo-bar">
        <span class="logo-hex">⬡</span>
        <span class="logo-name">NLDA Pro</span>
        <span class="logo-tag">Data Storyteller · v4.0</span>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">AI Provider</div>', unsafe_allow_html=True)
    provider=st.selectbox("Provider",list(PROVIDERS.keys()),
        index=list(PROVIDERS.keys()).index(st.session_state.get("provider","Groq (Free)")),
        key="provider_select")
    st.session_state["provider"]=provider
    pcfg=PROVIDERS[provider]
    bc=pcfg["badge_color"]
    fl="● FREE tier" if pcfg["free"] else "● Paid — requires credits"
    st.markdown(f'<div style="font-family:var(--fm);font-size:9px;color:{bc};padding:1px 0 6px 1px">{fl} · {pcfg["model"]}</div>',unsafe_allow_html=True)
    kv=st.text_input(f"{pcfg['label']} Key",type="password",
                     value=st.session_state.get("provider_key",""),
                     placeholder=pcfg["key_hint"],
                     help=f"Get free key at {pcfg['key_url']}")
    if kv: st.session_state["provider_key"]=kv
    st.markdown(f'<div style="font-size:10px;color:var(--t3);padding:1px 0 3px">🔑 <a href="{pcfg["key_url"]}" target="_blank" style="color:var(--gold)">{pcfg["key_url"].replace("https://","")}</a></div>',unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">Session</div>', unsafe_allow_html=True)
    total_rows=sum(len(d) for d in st.session_state.dataframes.values())
    st.markdown(f"""<div class="stat-strip">
        <div class="sc"><span class="sc-v">{st.session_state.total_queries}</span><span class="sc-l">Queries</span></div>
        <div class="sc"><span class="sc-v">{st.session_state.charts_generated}</span><span class="sc-l">Charts</span></div>
        <div class="sc"><span class="sc-v">{len(st.session_state.dataframes)}</span><span class="sc-l">Tables</span></div>
        <div class="sc"><span class="sc-v">{fmt(total_rows,0)}</span><span class="sc-l">Rows</span></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">Data Sources</div>', unsafe_allow_html=True)
    uploaded=st.file_uploader("Upload CSV/Excel",type=["csv","xlsx","xls"],
                              accept_multiple_files=True,label_visibility="collapsed")
    if uploaded:
        for uf in uploaded:
            nm=re.sub(r'\s+','_',uf.name.rsplit(".",1)[0].lower())
            if nm not in st.session_state.dataframes:
                try:
                    df=pd.read_csv(uf) if uf.name.endswith(".csv") else pd.read_excel(uf)
                    for col in df.columns:
                        if any(kw in col.lower() for kw in ["date","time","period","month","year"]):
                            try: df[col]=pd.to_datetime(df[col])
                            except: pass
                    st.session_state.dataframes[nm]=df
                    st.session_state.df_meta[nm]=col_profile(df)
                    st.success(f"✓ {nm}")
                except Exception as e: st.error(f"Error: {e}")

    for dname,ddf in list(st.session_state.dataframes.items()):
        nc=len(ddf.select_dtypes(include="number").columns)
        st.markdown(f"""<div class="ds-card active">
            <div class="ds-name">{dname}</div>
            <div class="ds-meta"><span class="ds-badge">{len(ddf):,}r</span><span class="ds-badge">{len(ddf.columns)}c</span><span class="ds-badge">{nc}num</span></div>
        </div>""", unsafe_allow_html=True)
        if st.button(f"✕ {dname}",key=f"rm_{dname}"):
            del st.session_state.dataframes[dname]; st.session_state.df_meta.pop(dname,None); st.rerun()

    st.markdown('<div class="sb-sec">Quick Start</div>', unsafe_allow_html=True)
    if st.button("⚡ Load Demo Data",use_container_width=True,key="sb_demo"):
        for k,v in generate_demo_datasets().items():
            st.session_state.dataframes[k]=v; st.session_state.df_meta[k]=col_profile(v)
        st.rerun()

    # Query Library
    if st.session_state.query_library:
        st.markdown('<div class="sb-sec">Query Library</div>', unsafe_allow_html=True)
        for qi,q in enumerate(st.session_state.query_library[:8]):
            if st.button(f"📚 {q[:36]}…" if len(q)>36 else f"📚 {q}",key=f"ql_{qi}"):
                st.session_state["prefill"]=q; st.rerun()
        if st.button("🗑 Clear Library",key="clr_lib"):
            st.session_state.query_library=[]; st.rerun()

    if st.session_state.chat_history:
        st.markdown('<div class="sb-sec">Export</div>', unsafe_allow_html=True)
        if st.button("📄 PDF Report",use_container_width=True,key="pdf_btn"):
            pdf=make_pdf(st.session_state.chat_history)
            if pdf:
                st.download_button("⬇ Download",pdf,
                    file_name=f"nlda_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",key="dl_pdf")
            else: st.info("pip install reportlab")
        if st.button("🗑 Clear Session",use_container_width=True,key="clr_btn"):
            for k,v in _D.items(): st.session_state[k]=v
            st.rerun()

# ═══════════════════════════════════════════════════════════════
#  MAIN PANEL
# ═══════════════════════════════════════════════════════════════
st.markdown("""<div class="hero">
    <div class="hero-grid"></div><div class="hero-glow"></div><div class="hero-glow2"></div>
    <div class="hero-eye">The Data Storyteller · v4.0</div>
    <h1 class="hero-title">Your data has a story.<br><span>Let's find it.</span></h1>
    <p class="hero-sub">Ask anything in plain English — get 28 chart types, AI storytelling, edit history, side-by-side comparison, and insights that no other platform generates.</p>
    <div class="hero-badges">
        <div class="hb"><div class="dot" style="background:#34d399"></div>28 chart types</div>
        <div class="hb"><div class="dot" style="background:#f0c040"></div>AI storytelling</div>
        <div class="hb"><div class="dot" style="background:#a78bfa"></div>Edit any query</div>
        <div class="hb"><div class="dot" style="background:#22d3ee"></div>Compare mode</div>
        <div class="hb"><div class="dot" style="background:#fb7185"></div>Data DNA scan</div>
        <div class="hb"><div class="dot" style="background:#f472b6"></div>Auto-dashboard</div>
    </div>
</div>""", unsafe_allow_html=True)

# ── Onboarding ──────────────────────────────────────────────────
if not st.session_state.dataframes:
    st.markdown("""<div class="ob-grid">
        <div class="ob-card"><div class="ob-num">01</div><div class="ob-title">Upload Data</div><div class="ob-desc">CSV or Excel. Multiple files supported — reference them in the same query.</div></div>
        <div class="ob-card"><div class="ob-num">02</div><div class="ob-title">Ask Anything</div><div class="ob-desc">Plain English. AI understands intent. Edit any past question and re-run.</div></div>
        <div class="ob-card"><div class="ob-num">03</div><div class="ob-title">28 Chart Types</div><div class="ob-desc">Bar, line, scatter, violin, radar, waterfall, gauge, candlestick & more.</div></div>
        <div class="ob-card"><div class="ob-num">04</div><div class="ob-title">AI Storytelling</div><div class="ob-desc">One click turns your whole session into a narrative analysis report.</div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,c3=st.columns([1,2,1])
    with c2:
        if st.button("⚡ Try it — Load Demo Datasets",use_container_width=True,key="ob_demo"):
            for k,v in generate_demo_datasets().items():
                st.session_state.dataframes[k]=v; st.session_state.df_meta[k]=col_profile(v)
            st.rerun()
    st.stop()

# ═══════════════════════════════════════════════════════════════
# DATA LOADED
# ═══════════════════════════════════════════════════════════════

# ── Feature strip ──────────────────────────────────────────────
feat_cols=st.columns(5)
with feat_cols[0]:
    if st.button("🔬 Data DNA Scan",use_container_width=True,key="dna_btn"):
        st.session_state["show_dna"]=not st.session_state.get("show_dna",False)
with feat_cols[1]:
    if st.button("🚀 Auto-Dashboard",use_container_width=True,key="auto_dash"):
        st.session_state["show_autodash"]=not st.session_state.get("show_autodash",False)
with feat_cols[2]:
    if st.button("⚔ Compare Mode",use_container_width=True,key="cmp_toggle"):
        st.session_state.compare_mode=not st.session_state.compare_mode
with feat_cols[3]:
    if st.button("📖 Data Story",use_container_width=True,key="story_btn"):
        st.session_state.story_expanded=not st.session_state.story_expanded
with feat_cols[4]:
    with st.expander("🗃 Dataset Explorer",expanded=False):
        pass  # placeholder — real content below

# ── Dataset Explorer ───────────────────────────────────────────
with st.expander("🗃  Dataset Explorer & Column Profiles",expanded=False):
    ds_tabs=st.tabs([f"  {n}  " for n in st.session_state.dataframes])
    for tab,(dname,ddf) in zip(ds_tabs,st.session_state.dataframes.items()):
        with tab:
            nc=ddf.select_dtypes(include="number").columns.tolist()
            c1,c2,c3,c4,c5=st.columns(5)
            c1.metric("Rows",f"{len(ddf):,}"); c2.metric("Cols",len(ddf.columns))
            c3.metric("Numeric",len(nc)); c4.metric("Null%",f"{ddf.isna().mean().mean()*100:.1f}%")
            c5.metric("Memory",f"{ddf.memory_usage(deep=True).sum()/1024:.0f}KB")
            profile=st.session_state.df_meta.get(dname,col_profile(ddf))
            html="".join(f'<div class="cp-card"><div class="cp-name">{col}</div>'
                f'<div class="cp-type">{info["dtype"].replace("float64","float").replace("int64","int").replace("object","str")} · {info["unique"]} unique</div>'
                f'<div class="cp-bar-w"><div class="cp-bar" style="width:{info.get("completeness",100-info.get("null_pct",0))}%"></div></div></div>'
                for col,info in list(profile.items())[:16])
            st.markdown(f'<div class="cp-grid">{html}</div>',unsafe_allow_html=True)
            st.dataframe(ddf.head(30),use_container_width=True,height=230)

# ── DATA DNA SCAN ──────────────────────────────────────────────
if st.session_state.get("show_dna",False):
    st.markdown('<div class="div">Data DNA — Column Fingerprints & Outlier Detection</div>',unsafe_allow_html=True)
    for dname,ddf in st.session_state.dataframes.items():
        st.markdown(f"**{dname}**")
        num_cols=ddf.select_dtypes(include="number").columns.tolist()
        cards=""
        for col in num_cols[:12]:
            s=ddf[col].dropna()
            q1,q3=s.quantile(.25),s.quantile(.75); iqr=q3-q1
            outliers=int(((s<q1-1.5*iqr)|(s>q3+1.5*iqr)).sum())
            skew=float(s.skew()); kurt=float(s.kurt())
            cards+=(f'<div class="dna-card"><div class="dna-col">{col}</div>'
                f'<div class="dna-row"><span class="dna-k">Mean</span><span class="dna-v">{fmt(s.mean())}</span></div>'
                f'<div class="dna-row"><span class="dna-k">Std</span><span class="dna-v">{fmt(s.std())}</span></div>'
                f'<div class="dna-row"><span class="dna-k">Skew</span><span class="dna-v" style="color:{"#fb7185" if abs(skew)>1 else "#34d399"}">{skew:.2f}</span></div>'
                f'<div class="dna-row"><span class="dna-k">Outliers</span><span class="dna-v" style="color:{"#fb7185" if outliers>0 else "#34d399"}">{outliers}</span></div>'
                f'<div class="dna-row"><span class="dna-k">Kurtosis</span><span class="dna-v">{kurt:.2f}</span></div>'
                f'</div>')
        if cards: st.markdown(f'<div class="dna-wrap">{cards}</div>',unsafe_allow_html=True)

# ── AUTO-DASHBOARD ─────────────────────────────────────────────
if st.session_state.get("show_autodash",False):
    st.markdown('<div class="div">Auto-Dashboard — Full Dataset Overview</div>',unsafe_allow_html=True)
    for dname,ddf in st.session_state.dataframes.items():
        st.markdown(f"**{dname}** — auto-generated from {len(ddf):,} rows")
        figs=make_multi_chart_dashboard(ddf)
        if figs:
            cols=st.columns(min(2,len(figs)))
            for i,fig in enumerate(figs):
                with cols[i%2]: st.plotly_chart(fig,use_container_width=True,key=f"ad_{dname}_{i}")
        else: st.info("Not enough numeric/date columns for auto-dashboard.")

# ── DATA STORY ─────────────────────────────────────────────────
if st.session_state.story_expanded and st.session_state.chat_history:
    st.markdown('<div class="div">AI Data Story — Narrative Analysis</div>',unsafe_allow_html=True)
    analyses_text="\n\n".join(
        f"Q: {e['question']}\nA: {e.get('summary','')}\nInsights: {'; '.join(e.get('insights',[]))}"
        for e in st.session_state.chat_history[-8:])
    story_key=hashlib.md5(analyses_text.encode()).hexdigest()[:8]
    cached=st.session_state.get(f"story_{story_key}")
    if not cached:
        with st.spinner("✍ Writing your data story…"):
            cached=call_story(analyses_text)
            st.session_state[f"story_{story_key}"]=cached
    st.markdown(f"""<div class="story-wrap">
        <div class="story-title">✦ The Data Story</div>
        <div class="story-text">{cached.replace(chr(10),'<br>')}</div>
    </div>""",unsafe_allow_html=True)

# ── INSIGHT TIMELINE ───────────────────────────────────────────
if len(st.session_state.chat_history)>=2:
    with st.expander("⏱  Insight Timeline — Visual thread of all findings",expanded=False):
        colors=["#f0c040","#a78bfa","#22d3ee","#34d399","#fb7185","#fbbf24"]
        tl_html='<div class="timeline">'
        for i,e in enumerate(st.session_state.chat_history):
            dot_color=colors[i%len(colors)]
            ins=e.get("insights",[""])[0][:80] if e.get("insights") else ""
            tl_html+=(f'<div class="tl-item"><div class="tl-dot" style="background:{dot_color}"></div>'
                f'<div class="tl-time">{e.get("ts","")} · Query {i+1}</div>'
                f'<div class="tl-q">{e["question"]}</div>'
                f'<div class="tl-a">{e.get("summary","")[:120]}</div>'
                f'{"<div class=tl-a style=color:"+dot_color+">↳ "+ins+"</div>" if ins else ""}'
                f'</div>')
        tl_html+='</div>'
        st.markdown(tl_html,unsafe_allow_html=True)

# ── CHART COMPOSER ─────────────────────────────────────────────
with st.expander("🎨  Chart Composer — Build any chart manually",expanded=False):
    dnames=list(st.session_state.dataframes.keys())
    if dnames:
        st.markdown('<div class="composer-title">Chart Composer</div>',unsafe_allow_html=True)
        cc1,cc2,cc3,cc4,cc5,cc6=st.columns(6)
        with cc1: comp_ds=st.selectbox("Dataset",dnames,key="comp_ds")
        comp_df=st.session_state.dataframes[comp_ds]
        all_cols=["(none)"]+list(comp_df.columns)
        with cc2: comp_chart=st.selectbox("Chart type",[c for c in CHART_TYPES if c!="none"],key="comp_ct")
        with cc3: comp_x=st.selectbox("X axis",all_cols,key="comp_x")
        with cc4: comp_y=st.selectbox("Y axis",all_cols,key="comp_y")
        with cc5: comp_color=st.selectbox("Color",all_cols,key="comp_col")
        with cc6: comp_title=st.text_input("Title","My Chart",key="comp_title")
        if st.button("🎨 Render Chart",key="comp_render"):
            cfg_c={"x":None if comp_x=="(none)" else comp_x,
                   "y":None if comp_y=="(none)" else comp_y,
                   "color":None if comp_color=="(none)" else comp_color,
                   "title":comp_title}
            f=make_chart(comp_df,comp_chart,cfg_c)
            if f: st.plotly_chart(f,use_container_width=True,key="comp_fig")
            else: st.warning("Could not render this chart — check your column selections.")

# ═══════════════════════════════════════════════════════════════
#  CHAT HISTORY
# ═══════════════════════════════════════════════════════════════
if st.session_state.chat_history:
    st.markdown('<div class="div">Analysis History</div>',unsafe_allow_html=True)

    for idx,entry in enumerate(st.session_state.chat_history):
        # ── Edit mode ─────────────────────────────────────────
        is_editing=(st.session_state.editing_idx==idx)

        # User bubble + edit controls
        edit_html=f'<span class="edit-badge" title="Edit this query">✎ edit</span>'
        st.markdown(f"""<div class="msg-row">
            <div class="msg-user-wrap">
                <div class="msg-user">{entry['question']}{edit_html if not is_editing else ''}</div>
            </div>
            <div class="msg-meta" style="text-align:right">You · {entry.get('ts','')}</div>
        </div>""",unsafe_allow_html=True)

        ecol1,ecol2,ecol3=st.columns([1,1,8])
        with ecol1:
            if st.button("✎ Edit",key=f"edit_{idx}"):
                st.session_state.editing_idx=idx
                st.session_state["prefill"]=entry["question"]
                st.rerun()
        with ecol2:
            if st.button("🗑 Del",key=f"del_{idx}"):
                st.session_state.chat_history.pop(idx); st.rerun()

        # Edit box (shown inline when editing)
        if is_editing:
            st.markdown('<div style="margin:6px 0 10px;padding:12px;background:var(--overlay);border:1px solid var(--violet);border-radius:10px">',unsafe_allow_html=True)
            st.markdown('<div style="font-family:var(--fm);font-size:9px;color:var(--violet);letter-spacing:.15em;text-transform:uppercase;margin-bottom:8px">Editing query — modify and re-run</div>',unsafe_allow_html=True)
            edited_q=st.text_input("Edit query",value=entry["question"],key=f"eq_{idx}",label_visibility="collapsed")
            ec1,ec2,ec3=st.columns([1,1,4])
            with ec1:
                if st.button("▶ Re-run",key=f"rerun_{idx}",type="primary"):
                    st.session_state["rerun_query"]=edited_q
                    st.session_state["rerun_idx"]=idx
                    st.session_state.editing_idx=None
                    st.rerun()
            with ec2:
                if st.button("✕ Cancel",key=f"cancel_{idx}"):
                    st.session_state.editing_idx=None; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

        # AI bubble
        conf=entry.get("confidence","high")
        cc={"high":"#34d399","medium":"#fbbf24","low":"#fb7185"}.get(conf,"#34d399")
        prov=entry.get("provider","AI")
        st.markdown(f"""<div class="msg-row">
            <div class="msg-ai-wrap">
                <div class="msg-ai">
                    <span style="font-family:var(--fm);font-size:8px;letter-spacing:.15em;color:{cc};text-transform:uppercase;display:block;margin-bottom:5px">
                        ⬡ NLDA · {prov} · {conf} confidence
                    </span>
                    {entry.get('summary','Analysis complete.')}
                </div>
            </div>
            <div class="msg-meta">{entry.get('ts','')}</div>
        </div>""",unsafe_allow_html=True)

        # KPI tiles
        _rdf=entry.get("result_df"); _kpis=entry.get("kpis") or []
        if not _kpis and _rdf is not None and not _rdf.empty: _kpis=generate_auto_kpis(_rdf)
        if _kpis:
            cc2=["c-gold","c-cyan","c-violet","c-emerald","c-rose","c-sky"]
            tiles=""
            for i,kpi in enumerate(_kpis[:6]):
                c=kpi.get("color",cc2[i%6]); dh=""
                if kpi.get("delta"):
                    cls="pos" if "+" in str(kpi["delta"]) else "neg"
                    dh=f'<div class="kpi-delta {cls}">{kpi["delta"]}</div>'
                tiles+=f'<div class="kpi-tile {c}"><span class="kpi-val">{kpi["value"]}</span><span class="kpi-lbl">{kpi["label"]}</span>{dh}</div>'
            st.markdown(f'<div class="kpi-grid">{tiles}</div>',unsafe_allow_html=True)

        # Result tabs (7 tabs)
        rt=st.tabs(["📊 Charts","📋 Table","💡 Insights","🔎 SQL","🐍 Code","🧠 Reasoning","➕ More Charts"])

        with rt[0]:  # Primary chart
            if entry.get("fig"):
                pc,_=st.columns([1,7])
                with pc:
                    if st.button("📌 Pin",key=f"pin_{entry['id']}"):
                        st.session_state.pinned_charts.append(entry["fig"]); st.success("Pinned!")
                st.plotly_chart(entry["fig"],use_container_width=True,key=f"fig_{entry['id']}")
                # Save to library
                sc,_=st.columns([1,7])
                with sc:
                    if st.button("📚 Save Q",key=f"saveq_{entry['id']}"):
                        if entry["question"] not in st.session_state.query_library:
                            st.session_state.query_library.append(entry["question"]); st.success("Saved!")
            else:
                st.markdown('<div style="padding:28px;text-align:center;color:#475569;font-family:JetBrains Mono,monospace;font-size:11px">No chart for this query — try asking for a specific chart type</div>',unsafe_allow_html=True)

        with rt[1]:  # Table + downloads
            rdf=entry.get("result_df")
            if rdf is not None and not rdf.empty:
                st.dataframe(rdf,use_container_width=True,height=280)
                d1,d2,_=st.columns([1,1,4])
                with d1: st.download_button("⬇ CSV",rdf.to_csv(index=False).encode(),file_name=f"nlda_{entry['id']}.csv",mime="text/csv",key=f"csv_{entry['id']}")
                with d2:
                    try:
                        xl=io.BytesIO()
                        with pd.ExcelWriter(xl,engine="openpyxl") as xw: rdf.to_excel(xw,index=False)
                        st.download_button("⬇ Excel",xl.getvalue(),file_name=f"nlda_{entry['id']}.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",key=f"xl_{entry['id']}")
                    except: pass
            else: st.info("No tabular result.")

        with rt[2]:  # Insights + anomalies + follow-ups
            cards=""
            icons=["★","◆","▲","●","◉","✦"]; icls=["gold","cyan","violet","emerald","rose","sky"]
            for i,ins in enumerate(entry.get("insights",[])):
                cards+=f'<div class="insight-card"><div class="ins-icon" style="background:var(--{icls[i%6]}d)">{icons[i%6]}</div><div class="ins-text">{ins}</div></div>'
            for a in entry.get("anomalies",[]):
                cards+=f'<div class="insight-card"><div class="ins-icon" style="background:var(--vd)">⚠</div><div class="ins-text" style="color:#fb7185"><strong>Anomaly:</strong> {a}</div></div>'
            if cards: st.markdown(f'<div class="insight-row">{cards}</div>',unsafe_allow_html=True)
            fqs=entry.get("follow_up_questions",[])
            if fqs:
                st.markdown('<div style="font-family:var(--fm);font-size:9px;color:var(--t3);letter-spacing:.2em;text-transform:uppercase;margin:12px 0 8px">Suggested next questions</div>',unsafe_allow_html=True)
                fq_cols=st.columns(len(fqs))
                for col,q in zip(fq_cols,fqs):
                    with col:
                        if st.button(f"↗ {q}",key=f"fq_{entry['id']}_{q[:16]}"):
                            st.session_state["prefill"]=q; st.rerun()

        with rt[3]:  # SQL
            sql=entry.get("sql_query","")
            if sql: st.markdown(code_html(sql,"sql"),unsafe_allow_html=True)
            else:   st.info("No SQL generated.")

        with rt[4]:  # Python code
            pyc=entry.get("pandas_code",""); err=entry.get("exec_error","")
            if pyc: st.markdown(code_html(pyc,"python"),unsafe_allow_html=True)
            if err: st.error(f"Exec note: {err}")

        with rt[5]:  # Reasoning
            r=entry.get("reasoning","")
            if r: st.markdown(f'<div style="background:var(--raised);border:1px solid var(--bd1);border-radius:9px;padding:14px 18px;font-size:13px;color:#94a3b8;line-height:1.7"><span style="font-family:var(--fm);font-size:8px;color:#475569;letter-spacing:.15em;text-transform:uppercase;display:block;margin-bottom:8px">AI Reasoning</span>{r}</div>',unsafe_allow_html=True)

        with rt[6]:  # More Charts — render alternative chart types on same data
            rdf2=entry.get("result_df")
            if rdf2 is not None and not rdf2.empty:
                num_c=rdf2.select_dtypes(include="number").columns.tolist()
                cat_c=rdf2.select_dtypes(include=["object","category"]).columns.tolist()
                alt_charts=[]
                if cat_c and num_c:
                    for ct in ["bar","horizontal bar","grouped bar","pie","donut","radar","treemap","sunburst","funnel"]:
                        f=make_chart(rdf2,ct,{"x":cat_c[0],"y":num_c[0],"title":f"{ct.title()} — {num_c[0]} by {cat_c[0]}"})
                        if f: alt_charts.append((ct,f))
                if len(num_c)>=2:
                    for ct in ["scatter","bubble","heatmap","parallel coordinates","violin","box"]:
                        f=make_chart(rdf2,ct,{"x":num_c[0],"y":num_c[1],"title":f"{ct.title()}"})
                        if f: alt_charts.append((ct,f))
                if num_c:
                    for ct in ["histogram","gauge","waterfall"]:
                        f=make_chart(rdf2,ct,{"x":cat_c[0] if cat_c else None,"y":num_c[0],"title":ct.title()})
                        if f: alt_charts.append((ct,f))
                if alt_charts:
                    st.markdown(f'<div style="font-family:var(--fm);font-size:9px;color:var(--t3);letter-spacing:.15em;text-transform:uppercase;margin-bottom:8px">{len(alt_charts)} alternative chart views on same data</div>',unsafe_allow_html=True)
                    ac_sel=st.selectbox("Select chart",[(ct,i) for i,(ct,_) in enumerate(alt_charts)],
                                        format_func=lambda x:x[0].title(),key=f"ac_{entry['id']}")
                    _,ac_i=ac_sel
                    st.plotly_chart(alt_charts[ac_i][1],use_container_width=True,key=f"ac_fig_{entry['id']}_{ac_i}")
                else: st.info("Not enough column types for alternative charts.")
            else: st.info("No result data to visualize.")

        st.markdown('<div style="margin:6px 0;border-top:1px solid #1a2035"></div>',unsafe_allow_html=True)

# ── Pinned Charts ──────────────────────────────────────────────
if st.session_state.pinned_charts:
    st.markdown('<div class="div">Pinned Charts Dashboard</div>',unsafe_allow_html=True)
    pc=st.columns(min(2,len(st.session_state.pinned_charts)))
    for i,fig in enumerate(st.session_state.pinned_charts):
        with pc[i%2]: st.plotly_chart(fig,use_container_width=True,key=f"pin_{i}")
    if st.button("Clear Pins",key="clr_pins"): st.session_state.pinned_charts=[]; st.rerun()

# ═══════════════════════════════════════════════════════════════
#  COMPARE MODE
# ═══════════════════════════════════════════════════════════════
if st.session_state.compare_mode:
    st.markdown('<div class="div">⚔ Side-by-Side Comparison Mode</div>',unsafe_allow_html=True)
    cm1,cm2=st.columns(2)
    with cm1:
        st.markdown('<span class="compare-label compare-a">Query A</span>',unsafe_allow_html=True)
        qa=st.text_input("Query A",value=st.session_state.compare_a,placeholder="First question…",key="qa_in",label_visibility="collapsed")
        st.session_state.compare_a=qa
    with cm2:
        st.markdown('<span class="compare-label compare-b">Query B</span>',unsafe_allow_html=True)
        qb=st.text_input("Query B",value=st.session_state.compare_b,placeholder="Second question…",key="qb_in",label_visibility="collapsed")
        st.session_state.compare_b=qb
    if st.button("⚔ Run Both Queries",key="cmp_run",type="primary"):
        if qa.strip() and qb.strip():
            schemas="\n\n".join(df_schema_str(df,n) for n,df in st.session_state.dataframes.items())
            with st.spinner("Running comparison…"):
                try:
                    ra=call_ai(qa.strip(),schemas,st.session_state.chat_history)
                    rb=call_ai(qb.strip(),schemas,st.session_state.chat_history)
                    st.session_state["cmp_results"]=(qa,qb,ra,rb)
                except Exception as e: st.error(str(e))
    if st.session_state.get("cmp_results"):
        qa,qb,ra,rb=st.session_state["cmp_results"]
        schemas="\n\n".join(df_schema_str(df,n) for n,df in st.session_state.dataframes.items())
        cr1,cr2=st.columns(2)
        for col,q,r,lab in [(cr1,qa,ra,"A"),(cr2,qb,rb,"B")]:
            with col:
                cls="compare-a" if lab=="A" else "compare-b"
                st.markdown(f'<div class="compare-panel"><div class="compare-label {cls}">Result {lab} — {q[:40]}</div>',unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:13px;color:var(--t2);margin-bottom:10px">{r.get("summary","")}</div>',unsafe_allow_html=True)
                rdf_c,_=safe_exec(r.get("pandas_code",""),st.session_state.dataframes)
                if rdf_c is not None and not rdf_c.empty:
                    fig_c=make_chart(rdf_c,r.get("chart_type","bar"),r.get("chart_config",{}))
                    if fig_c: st.plotly_chart(fig_c,use_container_width=True,key=f"cmp_{lab}")
                    st.dataframe(rdf_c.head(10),use_container_width=True)
                st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  QUERY INPUT
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="div">New Analysis</div>',unsafe_allow_html=True)

CHIPS=["Top 10 by revenue","Monthly trend","Correlation heatmap",
       "Profit by region","ROAS by channel","Revenue vs spend",
       "Violin distribution","Waterfall by quarter"]
prefill=st.session_state.pop("prefill","")
chip_cols=st.columns(len(CHIPS))
for i,(col,sug) in enumerate(zip(chip_cols,CHIPS)):
    with col:
        if st.button(sug,key=f"chip_{i}"): prefill=sug

st.markdown('<div class="q-wrap">',unsafe_allow_html=True)
st.markdown('<div class="q-lbl">Natural Language Query</div>',unsafe_allow_html=True)
query=st.text_input("q",value=prefill,
    placeholder='e.g. "Show a violin chart of revenue distribution by region with outliers highlighted"',
    label_visibility="collapsed",key="main_q")
qc1,qc2,qc3=st.columns([2,1,5])
with qc1: run=st.button("⬡  Analyze",use_container_width=True,key="run_btn",type="primary")
with qc2: adv=st.checkbox("Deep",value=False,help="More thorough analysis")
st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  HANDLE EDIT RE-RUN
# ═══════════════════════════════════════════════════════════════
if st.session_state.get("rerun_query"):
    rerun_q=st.session_state.pop("rerun_query")
    rerun_idx=st.session_state.pop("rerun_idx",None)
    schemas="\n\n".join(df_schema_str(df,n) for n,df in st.session_state.dataframes.items())
    prog=st.empty()
    STEPS=["PARSE","AI CALL","EXECUTE","VISUALIZE"]
    def show_step(a):
        items="".join(
            f'<div class="step-item {"done" if STEPS.index(s)<STEPS.index(a) else "active" if s==a else ""}"><span class="step-dot">{"✓" if STEPS.index(s)<STEPS.index(a) else "⬡"}</span>{s}</div>'
            for s in STEPS)
        prog.markdown(f'<div class="step-track">{items}</div>',unsafe_allow_html=True)
    show_step("PARSE"); show_step("AI CALL")
    try: result=call_ai(rerun_q,schemas,st.session_state.chat_history)
    except Exception as e: prog.empty(); st.error(str(e)); st.stop()
    show_step("EXECUTE")
    rdf,err=None,None
    if result.get("pandas_code"): rdf,err=safe_exec(result["pandas_code"],st.session_state.dataframes)
    show_step("VISUALIZE")
    fig=None; ctype=result.get("chart_type","none")
    if ctype!="none" and rdf is not None and not rdf.empty:
        fig=make_chart(rdf,ctype,result.get("chart_config",{}))
        if fig: st.session_state.charts_generated+=1
    prog.empty()
    new_entry={"id":hashlib.md5(f"{rerun_q}{time.time()}".encode()).hexdigest()[:10],
               "ts":datetime.now().strftime("%H:%M"),"question":rerun_q,
               "summary":result.get("summary",""),"pandas_code":result.get("pandas_code",""),
               "sql_query":result.get("sql_query",""),"chart_type":ctype,
               "chart_config":result.get("chart_config",{}),"kpis":result.get("kpis",[]),
               "insights":result.get("insights",[]),"anomalies":result.get("anomalies",[]),
               "follow_up_questions":result.get("follow_up_questions",[]),
               "confidence":result.get("confidence","high"),"reasoning":result.get("reasoning",""),
               "result_df":rdf,"exec_error":err,"fig":fig,
               "provider":PROVIDERS[st.session_state.get("provider","Groq (Free)")]["label"]}
    if rerun_idx is not None: st.session_state.chat_history[rerun_idx]=new_entry
    else: st.session_state.chat_history.append(new_entry)
    st.session_state.total_queries+=1; st.rerun()

# ═══════════════════════════════════════════════════════════════
#  ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════════
if run and query.strip():
    if not st.session_state.get("provider_key","").strip():
        pcfg2=PROVIDERS[st.session_state.get("provider","Groq (Free)")]
        st.error(f"⚠ No API key for {st.session_state.get('provider','Groq (Free)')}. "
                 f"Get a free key at [{pcfg2['key_url']}]({pcfg2['key_url']}) and paste it in the sidebar.")
        st.stop()

    schemas="\n\n".join(df_schema_str(df,n) for n,df in st.session_state.dataframes.items())
    prog=st.empty()
    STEPS=["PARSE","AI CALL","EXECUTE","VISUALIZE"]
    def show_step(a):
        items="".join(
            f'<div class="step-item {"done" if STEPS.index(s)<STEPS.index(a) else "active" if s==a else ""}"><span class="step-dot">{"✓" if STEPS.index(s)<STEPS.index(a) else "⬡"}</span>{s}</div>'
            for s in STEPS)
        prog.markdown(f'<div class="step-track">{items}</div>',unsafe_allow_html=True)

    show_step("PARSE"); show_step("AI CALL")
    extra=""
    if adv: extra="The user wants deep, thorough analysis. Provide maximum detail in insights."
    try: result=call_ai(query.strip(),schemas,st.session_state.chat_history,extra)
    except RuntimeError as e: prog.empty(); st.error(str(e)); st.stop()
    except json.JSONDecodeError as e: prog.empty(); st.error(f"JSON parse error — try rephrasing. ({e})"); st.stop()
    except Exception as e: prog.empty(); st.error(f"Unexpected error: {e}"); st.stop()

    show_step("EXECUTE")
    rdf,err=None,None
    if result.get("pandas_code"): rdf,err=safe_exec(result["pandas_code"],st.session_state.dataframes)

    show_step("VISUALIZE")
    fig=None; ctype=result.get("chart_type","none")
    if ctype!="none" and rdf is not None and not rdf.empty:
        fig=make_chart(rdf,ctype,result.get("chart_config",{}))
        if fig: st.session_state.charts_generated+=1
    prog.empty()

    eid=hashlib.md5(f"{query}{time.time()}".encode()).hexdigest()[:10]
    st.session_state.chat_history.append({
        "id":eid,"ts":datetime.now().strftime("%H:%M"),"question":query.strip(),
        "summary":result.get("summary",""),"pandas_code":result.get("pandas_code",""),
        "sql_query":result.get("sql_query",""),"chart_type":ctype,
        "chart_config":result.get("chart_config",{}),"kpis":result.get("kpis",[]),
        "insights":result.get("insights",[]),"anomalies":result.get("anomalies",[]),
        "follow_up_questions":result.get("follow_up_questions",[]),
        "confidence":result.get("confidence","high"),"reasoning":result.get("reasoning",""),
        "result_df":rdf,"exec_error":err,"fig":fig,
        "provider":PROVIDERS[st.session_state.get("provider","Groq (Free)")]["label"]
    })
    st.session_state.total_queries+=1; st.rerun()
