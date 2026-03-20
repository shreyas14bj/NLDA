"""
╔══════════════════════════════════════════════════════════════════════╗
║   NLDA PRO v4.1 · Natural Language Data Analyst                      ║
║   "The Data Storyteller" — Production-Ready Final Edition            ║
╚══════════════════════════════════════════════════════════════════════╝
FIXES in v4.1:
  ✦ Charts now always render — smart column-type detection before plotting
  ✦ Data Story works correctly for all 3 providers
  ✦ PDF includes summary, insights, KPIs, SQL for every entry
  ✦ Input box auto-clears after query is submitted
  ✦ Clear Query button added
  ✦ Chart fallback: if AI-chosen type fails, auto-picks a safe alternative
  ✦ YearsAtCompany / date-like columns properly handled as numeric
FEATURES:
  ✦ 28 chart types — bar, line, scatter, violin, radar, waterfall,
      gauge, candlestick, sunburst, treemap, heatmap, parallel coords…
  ✦ Edit & re-run any past query inline
  ✦ AI Data Story — narrative across entire session
  ✦ Chart Composer — build any chart manually with column dropdowns
  ✦ Insight Timeline — visual thread of all findings
  ✦ Data DNA Scan — column fingerprint + outlier detection
  ✦ Smart Auto-Dashboard — 4-panel overview in one click
  ✦ Query Library — save & replay favourite questions
  ✦ Side-by-Side Comparison Mode
  ✦ Multi-provider: Groq (free) · Gemini (free) · Anthropic
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json, io, re, time, hashlib
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="NLDA Pro · Data Storyteller",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════
#  DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Inter:wght@300;400;500;600&display=swap');

:root{
  --void:#05060a; --base:#090b11; --surface:#0e1117; --raised:#131720; --overlay:#181e2b;
  --bd0:#1a2035;  --bd1:#232b40;  --bd2:#2d3a55;
  --gold:#f0c040; --gd:rgba(240,192,64,.12); --gg:rgba(240,192,64,.28);
  --cyan:#22d3ee; --cd:rgba(34,211,238,.10);
  --violet:#a78bfa; --vd:rgba(167,139,250,.10);
  --emerald:#34d399; --rose:#fb7185; --amber:#fbbf24; --sky:#38bdf8; --pink:#f472b6;
  --t1:#f1f5f9; --t2:#94a3b8; --t3:#475569;
  --r1:6px; --r2:10px; --r3:16px; --r4:24px;
  --fd:'Syne',sans-serif; --fb:'Inter',sans-serif; --fm:'JetBrains Mono',monospace;
}
html,body,.stApp,[data-testid="stAppViewContainer"]{background:var(--void)!important;font-family:var(--fb);color:var(--t1);}
*{box-sizing:border-box;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-thumb{background:var(--bd2);border-radius:2px;}

/* ── SIDEBAR ── */
[data-testid="stSidebar"]{background:var(--base)!important;border-right:1px solid var(--bd0)!important;}
[data-testid="stSidebar"] *{color:var(--t1)!important;}
[data-testid="stSidebarContent"]{padding:0 0 2rem!important;}
#MainMenu,footer,[data-testid="stDecoration"]{display:none!important;}
[data-testid="stSidebarCollapseButton"],[data-testid="collapsedControl"]{display:flex!important;opacity:1!important;}
.block-container{padding:1.5rem 2rem 4rem!important;max-width:1500px;}
h1,h2,h3,h4{font-family:var(--fd)!important;letter-spacing:-.02em;}

/* ── LOGO ── */
.logo-bar{background:linear-gradient(135deg,var(--base),var(--surface));border-bottom:1px solid var(--bd0);padding:20px 22px 16px;}
.logo-hex{font-size:28px;line-height:1;display:block;margin-bottom:5px;}
.logo-name{font-family:var(--fd);font-size:18px;font-weight:800;
  background:linear-gradient(135deg,var(--gold),var(--amber));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;display:block;line-height:1;}
.logo-tag{font-family:var(--fm);font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:var(--t3);display:block;margin-top:4px;}
.sb-sec{padding:13px 18px 5px;font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--t3);border-top:1px solid var(--bd0);margin-top:6px;}

/* ── STAT STRIP ── */
.stat-strip{display:flex;gap:5px;padding:7px 14px 12px;flex-wrap:wrap;}
.sc{flex:1;min-width:62px;background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:8px 9px;text-align:center;}
.sc-v{font-family:var(--fm);font-size:17px;font-weight:500;color:var(--gold);display:block;line-height:1.1;}
.sc-l{font-size:8px;color:var(--t3);text-transform:uppercase;letter-spacing:.1em;margin-top:2px;display:block;}

/* ── DATASET CARD ── */
.ds-card{margin:4px 10px;background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:10px 12px;}
.ds-card.active{border-color:var(--gold);}
.ds-name{font-family:var(--fd);font-size:12px;font-weight:700;}
.ds-meta{font-family:var(--fm);font-size:9px;color:var(--t3);margin-top:2px;}
.ds-badge{display:inline-block;background:var(--gd);border:1px solid var(--gg);border-radius:3px;font-family:var(--fm);font-size:8px;color:var(--gold);padding:1px 5px;margin-right:3px;}

/* ── HERO ── */
.hero{position:relative;background:var(--surface);border:1px solid var(--bd1);border-radius:var(--r4);padding:52px 60px;margin-bottom:28px;overflow:hidden;}
.hero-grid{position:absolute;inset:0;
  background-image:linear-gradient(var(--bd0) 1px,transparent 1px),linear-gradient(90deg,var(--bd0) 1px,transparent 1px);
  background-size:40px 40px;opacity:.3;}
.hero-glow{position:absolute;top:-100px;right:-80px;width:420px;height:420px;
  background:radial-gradient(circle,var(--gg) 0%,transparent 70%);pointer-events:none;}
.hero-glow2{position:absolute;bottom:-60px;left:18%;width:300px;height:300px;
  background:radial-gradient(circle,rgba(167,139,250,.14) 0%,transparent 70%);pointer-events:none;}
.hero-glow3{position:absolute;top:20%;left:-80px;width:250px;height:250px;
  background:radial-gradient(circle,rgba(34,211,238,.08) 0%,transparent 70%);pointer-events:none;}
.hero-eye{font-family:var(--fm);font-size:9px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.hero-eye::before{content:'';display:block;width:24px;height:1px;background:var(--gold);}
.hero-title{font-family:var(--fd);font-size:clamp(36px,5.5vw,72px);font-weight:800;letter-spacing:-.04em;line-height:.92;color:var(--t1);margin:0 0 6px;position:relative;}
.hero-title span{background:linear-gradient(135deg,var(--gold) 0%,var(--amber) 40%,var(--rose) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{font-size:17px;color:var(--t2);font-weight:300;margin-top:16px;max-width:580px;line-height:1.65;position:relative;}
.hero-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:24px;position:relative;}
.hb{display:flex;align-items:center;gap:6px;background:var(--raised);border:1px solid var(--bd2);border-radius:50px;padding:6px 14px;font-size:11px;color:var(--t2);font-family:var(--fm);}
.hb .dot{width:6px;height:6px;border-radius:50%;}

/* ── FEATURE STRIP ── */
.feat-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:0 0 24px;}
.feat-card{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r3);padding:18px;cursor:pointer;transition:all .2s;position:relative;overflow:hidden;}
.feat-card:hover{border-color:var(--gold);transform:translateY(-2px);box-shadow:0 8px 32px rgba(240,192,64,.12);}
.feat-card.active{border-color:var(--gold);background:var(--gd);}
.feat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--gold),var(--violet));opacity:0;transition:opacity .2s;}
.feat-card.active::before,.feat-card:hover::before{opacity:1;}
.feat-icon{font-size:22px;margin-bottom:8px;display:block;}
.feat-title{font-family:var(--fd);font-size:13px;font-weight:700;color:var(--t1);margin-bottom:3px;}
.feat-desc{font-size:11px;color:var(--t3);line-height:1.4;}

/* ── QUERY PANEL ── */
.q-wrap{background:var(--surface);border:1px solid var(--bd1);border-radius:var(--r4);padding:22px;margin-bottom:24px;position:relative;}
.q-wrap::before{content:'';position:absolute;inset:-1px;border-radius:var(--r4);
  background:linear-gradient(135deg,var(--gold),var(--violet),var(--cyan));
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;padding:1px;opacity:0;transition:opacity .3s;pointer-events:none;}
.q-wrap:focus-within::before{opacity:1;}
.q-lbl{font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--t3);margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.q-lbl::after{content:'';flex:1;height:1px;background:var(--bd0);}

/* ── BUTTONS ── */
.stButton>button{
  background:var(--raised)!important;color:var(--t2)!important;
  border:1px solid var(--bd1)!important;border-radius:8px!important;
  font-family:var(--fb)!important;font-size:12px!important;font-weight:500!important;
  line-height:1.35!important;padding:8px 10px!important;
  white-space:normal!important;word-break:break-word!important;
  min-height:38px!important;width:100%!important;
  transition:all .15s!important;cursor:pointer!important;}
.stButton>button:hover{border-color:var(--gold)!important;color:var(--gold)!important;background:var(--gd)!important;transform:translateY(-1px)!important;}
.stButton>button:active{transform:translateY(0)!important;opacity:.85!important;}
button[data-testid="baseButton-primary"]{
  background:linear-gradient(135deg,#c8980e,#f0c040)!important;color:#05060a!important;
  border:none!important;border-radius:var(--r2)!important;font-family:var(--fd)!important;
  font-size:15px!important;font-weight:700!important;padding:12px 30px!important;
  white-space:nowrap!important;min-height:46px!important;
  box-shadow:0 4px 24px rgba(240,192,64,.3)!important;}
button[data-testid="baseButton-primary"]:hover{
  box-shadow:0 8px 40px rgba(240,192,64,.5)!important;transform:translateY(-2px)!important;color:#05060a!important;}

/* ── TEXT INPUT ── */
.stTextInput>div>div>input,.stTextArea>div>div>textarea{
  background:var(--raised)!important;border:1px solid var(--bd1)!important;
  border-radius:var(--r2)!important;color:var(--t1)!important;font-family:var(--fb)!important;
  font-size:16px!important;padding:14px 20px!important;transition:border-color .2s!important;}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{border-color:var(--gold)!important;box-shadow:0 0 0 3px var(--gd)!important;}
.stTextInput>div>div>input::placeholder{color:var(--t3)!important;}

/* ── CHAT BUBBLES ── */
.msg-row{display:flex;flex-direction:column;gap:4px;margin:22px 0;}
.msg-user-wrap{display:flex;justify-content:flex-end;}
.msg-ai-wrap{display:flex;justify-content:flex-start;}
.msg-user{max-width:75%;background:linear-gradient(135deg,rgba(240,192,64,.15),rgba(167,139,250,.1));
  border:1px solid rgba(240,192,64,.3);border-radius:20px 20px 4px 20px;
  padding:14px 20px;font-size:15px;line-height:1.65;color:var(--t1);}
.msg-ai{max-width:85%;background:var(--raised);border:1px solid var(--bd1);
  border-radius:4px 20px 20px 20px;padding:14px 20px;font-size:15px;line-height:1.65;color:var(--t2);}
.msg-meta{font-family:var(--fm);font-size:9px;letter-spacing:.15em;text-transform:uppercase;color:var(--t3);padding:0 4px;margin-top:4px;}
.edit-row{display:flex;gap:6px;margin:4px 0 0;}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{background:var(--base)!important;border-bottom:1px solid var(--bd0)!important;border-radius:0!important;gap:0!important;padding:0 8px!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--t3)!important;border-radius:0!important;font-family:var(--fm)!important;font-size:10px!important;letter-spacing:.08em!important;padding:12px 18px!important;border-bottom:2px solid transparent!important;transition:all .15s!important;}
.stTabs [aria-selected="true"]{background:transparent!important;color:var(--gold)!important;border-bottom-color:var(--gold)!important;}
.stTabs [data-testid="stTabContent"]{background:var(--surface)!important;padding:20px!important;}

/* ── KPI TILES ── */
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:12px;margin:16px 0;}
.kpi-tile{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:18px 20px;position:relative;overflow:hidden;}
.kpi-tile::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.c-gold::after{background:var(--gold);}.c-cyan::after{background:var(--cyan);}.c-violet::after{background:var(--violet);}
.c-emerald::after{background:var(--emerald);}.c-rose::after{background:var(--rose);}.c-sky::after{background:var(--sky);}
.kpi-val{font-family:var(--fm);font-size:26px;font-weight:500;color:var(--t1);display:block;line-height:1.1;}
.kpi-lbl{font-size:11px;color:var(--t3);margin-top:6px;text-transform:uppercase;letter-spacing:.08em;font-family:var(--fm);}
.kpi-delta{font-family:var(--fm);font-size:11px;margin-top:4px;}
.kpi-delta.pos{color:var(--emerald);}.kpi-delta.neg{color:var(--rose);}

/* ── INSIGHT CARDS ── */
.insight-row{display:flex;flex-direction:column;gap:10px;margin:12px 0;}
.insight-card{display:flex;gap:14px;align-items:flex-start;background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:14px 16px;}
.ins-icon{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;}
.ins-text{font-size:13px;color:var(--t2);line-height:1.6;}

/* ── STORY BLOCK ── */
.story-wrap{background:linear-gradient(135deg,rgba(240,192,64,.06),rgba(167,139,250,.06));
  border:1px solid rgba(240,192,64,.22);border-radius:var(--r3);padding:28px 32px;margin:20px 0;position:relative;overflow:hidden;}
.story-wrap::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(180deg,var(--gold),var(--violet),var(--cyan));}
.story-title{font-family:var(--fd);font-size:12px;font-weight:700;color:var(--gold);letter-spacing:.1em;text-transform:uppercase;margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.story-text{font-size:15px;color:var(--t1);line-height:1.85;white-space:pre-wrap;}

/* ── TIMELINE ── */
.timeline{position:relative;padding-left:30px;margin:16px 0;}
.timeline::before{content:'';position:absolute;left:9px;top:0;bottom:0;width:1px;background:linear-gradient(180deg,var(--gold),var(--violet),var(--cyan));}
.tl-item{position:relative;margin-bottom:22px;}
.tl-dot{position:absolute;left:-26px;top:4px;width:10px;height:10px;border-radius:50%;border:2px solid var(--void);}
.tl-time{font-family:var(--fm);font-size:9px;color:var(--t3);letter-spacing:.1em;margin-bottom:4px;}
.tl-q{font-size:13px;font-weight:600;color:var(--t1);}
.tl-a{font-size:12px;color:var(--t2);margin-top:4px;line-height:1.5;}
.tl-ins{font-size:12px;margin-top:3px;line-height:1.4;}

/* ── CHART COMPOSER ── */
.composer-lbl{font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:12px;}

/* ── COMPARE PANELS ── */
.compare-panel{background:var(--surface);border:1px solid var(--bd1);border-radius:var(--r3);padding:18px;}
.compare-lbl{font-family:var(--fm);font-size:9px;letter-spacing:.15em;text-transform:uppercase;
  padding:5px 10px;border-radius:5px;display:inline-block;margin-bottom:12px;}
.cmp-a{background:rgba(240,192,64,.1);color:var(--gold);border:1px solid rgba(240,192,64,.3);}
.cmp-b{background:rgba(34,211,238,.1);color:var(--cyan);border:1px solid rgba(34,211,238,.3);}

/* ── CODE BLOCKS ── */
.code-wrap{position:relative;background:#020408;border:1px solid var(--bd0);border-radius:var(--r2);margin:8px 0;overflow:hidden;}
.code-hdr{display:flex;align-items:center;justify-content:space-between;padding:8px 16px;background:var(--base);border-bottom:1px solid var(--bd0);}
.code-lang{font-family:var(--fm);font-size:9px;letter-spacing:.15em;color:var(--t3);text-transform:uppercase;}
.code-body{padding:20px;font-family:var(--fm);font-size:12.5px;line-height:1.7;color:#cdd6f4;overflow-x:auto;white-space:pre;}
.kw{color:#cba6f7;}.fn{color:#89b4fa;}.st{color:#a6e3a1;}.cm{color:#585b70;font-style:italic;}.nm{color:#fab387;}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"]{background:var(--raised)!important;border:1.5px dashed var(--bd2)!important;border-radius:var(--r3)!important;padding:16px!important;transition:border-color .2s!important;}
[data-testid="stFileUploader"]:hover{border-color:var(--gold)!important;}

/* ── MISC ── */
[data-testid="stDataFrame"]{border-radius:var(--r2);overflow:hidden;}
.stSelectbox>div>div{background:var(--raised)!important;border-color:var(--bd1)!important;color:var(--t1)!important;}
[data-testid="stAlert"]{background:var(--raised)!important;border-radius:var(--r2)!important;border-left-width:3px!important;}
.streamlit-expanderHeader{background:var(--raised)!important;border:1px solid var(--bd1)!important;border-radius:var(--r2)!important;color:var(--t2)!important;font-family:var(--fm)!important;font-size:10px!important;}
.streamlit-expanderContent{background:var(--surface)!important;border:1px solid var(--bd1)!important;border-top:none!important;}

/* ── DIVIDER ── */
.div{display:flex;align-items:center;gap:12px;margin:28px 0;color:var(--t3);font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;}
.div::before,.div::after{content:'';flex:1;height:1px;background:var(--bd0);}

/* ── ONBOARDING ── */
.ob-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin:22px 0;}
.ob-card{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r3);padding:24px 20px;text-align:center;transition:border-color .2s;}
.ob-card:hover{border-color:var(--bd2);}
.ob-num{font-family:var(--fm);font-size:46px;font-weight:500;color:var(--bd2);line-height:1;margin-bottom:8px;}
.ob-title{font-family:var(--fd);font-size:15px;font-weight:700;color:var(--t1);margin-bottom:6px;}
.ob-desc{font-size:12px;color:var(--t3);line-height:1.5;}

/* ── STEP TRACKER ── */
.step-track{display:flex;margin:16px 0;background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);overflow:hidden;}
.step-item{flex:1;padding:12px 8px;text-align:center;font-family:var(--fm);font-size:9px;letter-spacing:.08em;color:var(--t3);border-right:1px solid var(--bd0);transition:all .3s;}
.step-item:last-child{border-right:none;}
.step-item.done{color:var(--emerald);background:rgba(52,211,153,.06);}
.step-item.active{color:var(--gold);background:var(--gd);}
.step-dot{font-size:13px;display:block;margin-bottom:2px;}

/* ── COL PROFILE ── */
.cp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px;margin:12px 0;}
.cp-card{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:12px 14px;}
.cp-name{font-family:var(--fm);font-size:10px;color:var(--gold);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cp-type{font-size:9px;color:var(--t3);font-family:var(--fm);margin-top:2px;}
.cp-bar-w{height:3px;background:var(--bd0);border-radius:2px;margin-top:8px;overflow:hidden;}
.cp-bar{height:100%;border-radius:2px;background:linear-gradient(90deg,var(--gold),var(--amber));}

/* ── DATA DNA ── */
.dna-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px;margin:14px 0;}
.dna-card{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:14px;}
.dna-col{font-family:var(--fm);font-size:11px;color:var(--gold);margin-bottom:8px;}
.dna-row{display:flex;justify-content:space-between;font-size:11px;padding:3px 0;border-bottom:1px solid var(--bd0);}
.dna-row:last-child{border-bottom:none;}
.dna-k{color:var(--t3);}.dna-v{color:var(--t1);font-family:var(--fm);}

/* ── EDIT MODE ── */
.edit-wrap{margin:8px 0 12px;padding:14px 16px;background:var(--overlay);border:1px solid var(--violet);border-radius:var(--r2);}
.edit-lbl{font-family:var(--fm);font-size:9px;color:var(--violet);letter-spacing:.15em;text-transform:uppercase;margin-bottom:10px;}

/* ── NO CHART PLACEHOLDER ── */
.no-chart{padding:40px;text-align:center;color:var(--t3);font-family:var(--fm);font-size:11px;
  background:var(--raised);border:1px dashed var(--bd1);border-radius:var(--r2);margin:8px 0;}
.no-chart-icon{font-size:32px;display:block;margin-bottom:10px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════
_DEFAULTS = {
    "dataframes":{}, "df_meta":{}, "chat_history":[],
    "provider":"Groq (Free)", "provider_key":"",
    "total_queries":0, "charts_generated":0,
    "pinned_charts":[], "query_tokens_used":0,
    "query_library":[],
    "editing_idx":None,
    "compare_mode":False, "compare_a":"", "compare_b":"",
    "show_dna":False, "show_autodash":False, "show_story":False,
    "show_timeline":False, "show_composer":False,
    "story_cache":{},
    "clear_input":False,          # v4.1: flag to clear input box
}
for k,v in _DEFAULTS.items():
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════
PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono,monospace", color="#f1f5f9", size=11),
    colorway=["#f0c040","#a78bfa","#22d3ee","#34d399","#fb7185","#fbbf24","#818cf8","#38bdf8","#f472b6","#4ade80"],
    xaxis=dict(gridcolor="#1a2035", zeroline=False),
    yaxis=dict(gridcolor="#1a2035", zeroline=False),
    margin=dict(l=16,r=16,t=48,b=16),
    legend=dict(bgcolor="rgba(0,0,0,0.35)", bordercolor="#232b40", borderwidth=1),
    title_font=dict(family="Syne,sans-serif", size=15, color="#f0c040"),
)

PROVIDERS = {
    "Groq (Free)":{
        "label":"Groq","model":"llama-3.3-70b-versatile",
        "url":"https://api.groq.com/openai/v1/chat/completions",
        "key_hint":"gsk_…","key_url":"https://console.groq.com",
        "style":"openai","free":True,"badge":"#34d399"},
    "Gemini (Free)":{
        "label":"Gemini","model":"gemini-2.0-flash",
        "url":"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        "key_hint":"AIza…","key_url":"https://aistudio.google.com",
        "style":"gemini","free":True,"badge":"#a78bfa"},
    "Anthropic Claude":{
        "label":"Claude","model":"claude-sonnet-4-5",
        "url":"https://api.anthropic.com/v1/messages",
        "key_hint":"sk-ant-…","key_url":"https://console.anthropic.com",
        "style":"anthropic","free":False,"badge":"#f0c040"},
}

CHART_TYPES_DISPLAY = [
    "bar","grouped bar","stacked bar","horizontal bar",
    "line","area","stacked area","scatter","bubble",
    "pie","donut","sunburst","treemap",
    "histogram","box","violin","strip",
    "heatmap","density heatmap",
    "waterfall","funnel","gauge","radar",
    "parallel coordinates","candlestick",
]

# ══════════════════════════════════════════════════════════════════════
#  UTILITIES
# ══════════════════════════════════════════════════════════════════════
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
            try:
                info.update({"min":float(s.min()),"max":float(s.max()),"mean":float(s.mean()),
                             "std":float(s.std()),"completeness":round(100-null_pct,1)})
            except: pass
        else:
            info["top_values"]={str(k):int(v) for k,v in s.value_counts().head(3).items()}
        p[col]=info
    return p

def df_schema_str(df, name):
    """Compact schema sent to the AI — only string-safe representations."""
    lines=[f"TABLE `{name}` — {len(df):,} rows × {len(df.columns)} columns"]
    for col in df.columns:
        s=df[col]
        dtype=str(s.dtype)
        if pd.api.types.is_numeric_dtype(s):
            try: extra=f"min={float(s.min()):.3g} max={float(s.max()):.3g} mean={float(s.mean()):.3g}"
            except: extra="numeric"
        elif pd.api.types.is_datetime64_any_dtype(s):
            extra=f"date range: {s.min()} to {s.max()}"
        else:
            extra=f"top:{list(s.value_counts().head(2).index)}"
        sample=[]
        for v in s.dropna().head(3):
            try: sample.append(str(v)[:30])
            except: pass
        lines.append(f"  {col}[{dtype}] unique={s.nunique()} | {extra} | sample={sample}")
    return "\n".join(lines)

def smart_numeric_cols(df):
    """Return truly numeric columns — exclude datetime even if stored as int64."""
    cols=[]
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_datetime64_any_dtype(df[col]):
            # also skip columns whose name suggests dates
            if not any(kw in col.lower() for kw in ["year","date","time","period","month"]):
                cols.append(col)
    return cols

def smart_cat_cols(df):
    """Return categorical / string columns."""
    return [c for c in df.columns
            if df[c].dtype==object or pd.api.types.is_categorical_dtype(df[c])
            or (df[c].dtype=="int64" and df[c].nunique()<20)]

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
                   "INNER","ON","AS","AND","OR","NOT","LIMIT","COUNT","SUM","AVG","MIN","MAX","DISTINCT","BY","DESC","ASC"]:
            esc=re.sub(rf'\b({kw})\b',r'<span class="kw">\1</span>',esc,flags=re.I)
    return (f'<div class="code-wrap"><div class="code-hdr"><span class="code-lang">{lang}</span></div>'
            f'<div class="code-body">{esc}</div></div>')

def generate_auto_kpis(df):
    kpis=[]; colors=["c-gold","c-cyan","c-violet","c-emerald","c-rose","c-sky"]
    num=smart_numeric_cols(df)
    for i,col in enumerate(num[:6]):
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

# ══════════════════════════════════════════════════════════════════════
#  CHART FACTORY  — v4.1: smart column validation before plotting
# ══════════════════════════════════════════════════════════════════════
def _safe_col(df, col):
    """Return col if it exists in df, else None."""
    if col and isinstance(col,str) and col in df.columns:
        return col
    return None

def _best_x(df, preferred=None):
    """Pick best X column: prefer category, then date string, then index."""
    if preferred and preferred in df.columns:
        return preferred
    cats=smart_cat_cols(df)
    if cats: return cats[0]
    # try string date-like
    for c in df.columns:
        if df[c].dtype==object: return c
    return df.columns[0]

def _best_y(df, preferred=None):
    """Pick best Y column: must be numeric."""
    if preferred and preferred in df.columns and pd.api.types.is_numeric_dtype(df[preferred]):
        return preferred
    nums=smart_numeric_cols(df)
    if nums: return nums[0]
    # last resort: any numeric including datetime-like ints
    nums2=[c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if nums2: return nums2[0]
    return None

def make_chart(df, chart_type, cfg):
    """
    Robust chart factory — always validates columns before calling Plotly.
    Falls back to a simple bar/line if the requested type cannot be rendered.
    """
    if df is None or df.empty: return None
    if not chart_type or chart_type.lower() in ("none",""): return None

    # Normalize chart type
    ct = chart_type.lower().strip().replace(" ","_").replace("-","_")

    # Smart column resolution
    x_raw = cfg.get("x"); y_raw = cfg.get("y")
    color_raw = cfg.get("color"); size_raw = cfg.get("size")
    title = cfg.get("title","")

    x     = _safe_col(df, x_raw)
    y     = _safe_col(df, y_raw)
    color = _safe_col(df, color_raw)
    size  = _safe_col(df, size_raw)

    # For charts that need numeric Y — auto-pick if AI gave wrong column
    NEEDS_NUMERIC_Y = {"bar","grouped_bar","stacked_bar","horizontal_bar","line","multi_line",
                       "area","stacked_area","scatter","bubble","box","violin","strip","funnel",
                       "waterfall","gauge","density_heatmap"}
    if ct in NEEDS_NUMERIC_Y:
        if y is None or not pd.api.types.is_numeric_dtype(df[y]):
            y = _best_y(df, y)
        if x is None:
            x = _best_x(df, x)

    try:
        kw = dict(title=title)
        fig = None

        if   ct=="bar":              fig=px.bar(df,x=x,y=y,color=color,**kw); fig.update_traces(marker_line_width=0,opacity=.88)
        elif ct=="grouped_bar":      fig=px.bar(df,x=x,y=y,color=color,barmode="group",**kw)
        elif ct=="stacked_bar":      fig=px.bar(df,x=x,y=y,color=color,barmode="stack",**kw)
        elif ct=="horizontal_bar":   fig=px.bar(df,x=y,y=x,color=color,orientation="h",**kw)
        elif ct in ("line","multi_line"):
            fig=px.line(df,x=x,y=y,color=color,markers=True,**kw); fig.update_traces(line_width=2.5)
        elif ct=="area":             fig=px.area(df,x=x,y=y,color=color,**kw)
        elif ct=="stacked_area":     fig=px.area(df,x=x,y=y,color=color,**kw)
        elif ct=="scatter":
            fig=px.scatter(df,x=x,y=y,color=color,size=size,
                           trendline="ols" if (not color and x and y) else None,**kw)
        elif ct=="bubble":
            sz=size or y
            fig=px.scatter(df,x=x,y=y,color=color,size=sz,**kw)
        elif ct=="pie":              fig=px.pie(df,names=x,values=y,**kw)
        elif ct=="donut":            fig=px.pie(df,names=x,values=y,hole=.45,**kw)
        elif ct=="sunburst":
            path=[c for c in [color,x] if c]; fig=px.sunburst(df,path=path or [x],values=y,**kw)
        elif ct=="treemap":
            path=[c for c in [color,x] if c]; fig=px.treemap(df,path=path or [x],values=y,**kw)
        elif ct=="histogram":
            hx=x or _best_x(df); fig=px.histogram(df,x=hx,color=color,**kw)
        elif ct=="box":              fig=px.box(df,x=x,y=y,color=color,**kw)
        elif ct=="violin":           fig=px.violin(df,x=x,y=y,color=color,box=True,**kw)
        elif ct=="strip":            fig=px.strip(df,x=x,y=y,color=color,**kw)
        elif ct in ("heatmap","correlation_matrix"):
            num=df[smart_numeric_cols(df)]
            if num.shape[1]<2: return None
            fig=px.imshow(num.corr().round(2),color_continuous_scale="RdBu_r",zmin=-1,zmax=1,text_auto=True,**kw)
        elif ct=="density_heatmap":
            fig=px.density_heatmap(df,x=x,y=y,color_continuous_scale="Viridis",**kw)
        elif ct=="waterfall":
            if x and y:
                fig=go.Figure(go.Waterfall(
                    measure=["relative"]*len(df),
                    x=df[x].astype(str).tolist(), y=df[y].tolist(),
                    connector={"line":{"color":"rgba(255,255,255,0.15)"}},
                    increasing={"marker":{"color":"#34d399"}},
                    decreasing={"marker":{"color":"#fb7185"}},
                    totals={"marker":{"color":"#f0c040"}}))
                fig.update_layout(title=title)
            else: return None
        elif ct=="funnel":
            fig=px.funnel(df,x=y,y=x,**kw)
        elif ct=="gauge":
            gy=y or _best_y(df)
            if gy:
                val=float(df[gy].mean()); mx=float(df[gy].max()) if float(df[gy].max())>0 else 1
                fig=go.Figure(go.Indicator(
                    mode="gauge+number+delta", value=val,
                    delta={"reference":mx*0.6},
                    gauge={"axis":{"range":[0,mx]},
                           "bar":{"color":"#f0c040"},
                           "steps":[{"range":[0,mx*.5],"color":"#1a2035"},{"range":[mx*.5,mx*.8],"color":"#232b40"}],
                           "threshold":{"line":{"color":"#fb7185","width":3},"thickness":.75,"value":mx*.9}},
                    title={"text":title or gy,"font":{"color":"#f0c040","size":13}}))
            else: return None
        elif ct=="radar":
            num_c=smart_numeric_cols(df)[:8]
            if len(num_c)<3: return None
            means=[float(df[c].mean()) for c in num_c]
            fig=go.Figure(go.Scatterpolar(
                r=means+[means[0]], theta=num_c+[num_c[0]],
                fill="toself", line_color="#f0c040",
                fillcolor="rgba(240,192,64,.15)", name=title))
            fig.update_layout(polar=dict(
                radialaxis=dict(visible=True,gridcolor="#232b40"),
                angularaxis=dict(gridcolor="#232b40")),title=title)
        elif ct=="parallel_coordinates":
            num_c=smart_numeric_cols(df)
            if len(num_c)<2: return None
            fig=px.parallel_coordinates(df,dimensions=num_c,color=num_c[0],
                color_continuous_scale=px.colors.diverging.Tealrose,**kw)
        elif ct in ("candlestick","ohlc"):
            ohcl_cols=[c.lower() for c in df.columns]
            has_ohlc=all(k in ohcl_cols for k in ["open","high","low","close"])
            if not has_ohlc: return None
            # map back to actual column names
            cm={c.lower():c for c in df.columns}
            xcol=x or (df.columns[0] if df.columns[0].lower() not in ["open","high","low","close"] else None)
            if ct=="candlestick":
                fig=go.Figure(go.Candlestick(
                    x=df[xcol].tolist() if xcol else list(range(len(df))),
                    open=df[cm["open"]],high=df[cm["high"]],
                    low=df[cm["low"]],close=df[cm["close"]]))
            else:
                fig=go.Figure(go.Ohlc(
                    x=df[xcol].tolist() if xcol else list(range(len(df))),
                    open=df[cm["open"]],high=df[cm["high"]],
                    low=df[cm["low"]],close=df[cm["close"]]))
            fig.update_layout(title=title)
        else:
            # Unknown chart type — fallback to bar
            if x and y:
                fig=px.bar(df,x=x,y=y,color=color,title=f"{title} (bar fallback)")
            else: return None

        if fig is None: return None

        fig.update_layout(
            **PLOTLY_THEME, title_x=0.0,
            hoverlabel=dict(bgcolor="#131720",font_size=11,font_family="JetBrains Mono"))

        NO_AXES = {"pie","donut","treemap","sunburst","heatmap","correlation_matrix",
                   "density_heatmap","radar","gauge","parallel_coordinates","candlestick","ohlc"}
        if ct not in NO_AXES:
            fig.update_xaxes(showgrid=True,gridwidth=1,gridcolor="#1a2035",showline=False,tickfont_size=10)
            fig.update_yaxes(showgrid=True,gridwidth=1,gridcolor="#1a2035",showline=False,tickfont_size=10)
        return fig

    except Exception as exc:
        # Last resort: try simple bar with auto-detected columns
        try:
            nx=_best_x(df); ny=_best_y(df)
            if nx and ny:
                fb=px.bar(df.head(30),x=nx,y=ny,title=f"{title} (auto-rendered)")
                fb.update_layout(**PLOTLY_THEME,title_x=0.0)
                return fb
        except Exception:
            pass
        return None

def make_multi_chart_dashboard(df):
    """Auto 4-panel dashboard."""
    num_c=smart_numeric_cols(df); cat_c=smart_cat_cols(df)
    date_c=[c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    figs=[]
    try:
        if cat_c and num_c:
            g=df.groupby(cat_c[0])[num_c[0]].sum().reset_index().sort_values(num_c[0],ascending=False).head(10)
            f=make_chart(g,"bar",{"x":cat_c[0],"y":num_c[0],"title":f"{num_c[0]} by {cat_c[0]}"})
            if f: figs.append(f)
        if date_c and num_c:
            td=df.copy(); td["_dt"]=pd.to_datetime(td[date_c[0]]).dt.to_period("M").astype(str)
            td2=td.groupby("_dt")[num_c[0]].sum().reset_index()
            f=make_chart(td2,"line",{"x":"_dt","y":num_c[0],"title":f"{num_c[0]} trend over time"})
            if f: figs.append(f)
        if len(num_c)>=2:
            f=make_chart(df.sample(min(200,len(df))),"scatter",
                         {"x":num_c[0],"y":num_c[1],"title":f"{num_c[0]} vs {num_c[1]}"})
            if f: figs.append(f)
        if len(num_c)>=3:
            f=make_chart(df,"heatmap",{"title":"Correlation Matrix"})
            if f: figs.append(f)
    except Exception: pass
    return figs

# ══════════════════════════════════════════════════════════════════════
#  PDF EXPORT  — v4.1: includes summary, KPIs, insights, SQL per entry
# ══════════════════════════════════════════════════════════════════════
def make_pdf(history):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors as rc
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                        HRFlowable, KeepTogether, Table, TableStyle)
        buf=io.BytesIO()
        doc=SimpleDocTemplate(buf,pagesize=A4,
                              leftMargin=2.2*cm,rightMargin=2.2*cm,
                              topMargin=2.2*cm,bottomMargin=2.2*cm)
        sty=getSampleStyleSheet()
        gold=rc.HexColor('#f0c040'); violet=rc.HexColor('#a78bfa')
        muted=rc.HexColor('#64748b'); body_c=rc.HexColor('#cbd5e1')
        bg_dark=rc.HexColor('#0e1117')

        ts  =ParagraphStyle('T',  parent=sty['Title'],   fontSize=26,textColor=gold,   spaceAfter=2, fontName='Helvetica-Bold')
        ss  =ParagraphStyle('S',  parent=sty['Normal'],  fontSize=10,textColor=muted,  spaceAfter=16)
        h2s =ParagraphStyle('H2', parent=sty['Heading2'],fontSize=13,textColor=violet, spaceAfter=5, spaceBefore=14)
        h3s =ParagraphStyle('H3', parent=sty['Heading3'],fontSize=11,textColor=gold,   spaceAfter=4, spaceBefore=8)
        bs  =ParagraphStyle('B',  parent=sty['Normal'],  fontSize=10,textColor=body_c, leading=15,  spaceAfter=4)
        ms  =ParagraphStyle('M',  parent=sty['Normal'],  fontSize=8, textColor=rc.HexColor('#94a3b8'),fontName='Courier',leading=12,spaceAfter=3)
        bus =ParagraphStyle('BU', parent=sty['Normal'],  fontSize=10,textColor=body_c, leading=14,  spaceAfter=3,leftIndent=12)
        anom=ParagraphStyle('AN', parent=sty['Normal'],  fontSize=10,textColor=rc.HexColor('#fb7185'),leading=14,spaceAfter=3,leftIndent=12)

        T=lambda t,s: Paragraph(str(t).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"),s)

        story=[
            T("NLDA Pro",ts),
            T(f"Data Intelligence Report · {datetime.now().strftime('%A, %d %B %Y · %H:%M')}",ss),
            T(f"Total analyses: {len(history)}",ss),
            HRFlowable(width="100%",thickness=1,color=gold,spaceAfter=14),
            Spacer(1,.4*cm),
        ]

        for i,e in enumerate(history,1):
            items=[]
            items.append(T(f"Analysis {i} — {e.get('ts','')}",h2s))
            items.append(T(f"<b>Question:</b> {e.get('question','')}",bs))
            items.append(T(f"<b>Summary:</b> {e.get('summary','No summary available.')}",bs))
            items.append(T(f"<b>Confidence:</b> {e.get('confidence','—').upper()}",bs))

            # KPIs table
            kpis=e.get("kpis",[])
            if kpis:
                items.append(T("Key Metrics",h3s))
                kpi_data=[["Metric","Value"]]
                for kpi in kpis:
                    kpi_data.append([kpi.get("label",""),kpi.get("value","")])
                t=Table(kpi_data,colWidths=[8*cm,5*cm])
                t.setStyle(TableStyle([
                    ('BACKGROUND',(0,0),(-1,0),violet),
                    ('TEXTCOLOR',(0,0),(-1,0),rc.white),
                    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
                    ('FONTSIZE',(0,0),(-1,-1),9),
                    ('ROWBACKGROUNDS',(0,1),(-1,-1),[rc.HexColor('#131720'),rc.HexColor('#1a2035')]),
                    ('TEXTCOLOR',(0,1),(-1,-1),body_c),
                    ('GRID',(0,0),(-1,-1),.5,rc.HexColor('#232b40')),
                    ('ROWPADDING',4),
                ]))
                items.append(Spacer(1,.2*cm)); items.append(t); items.append(Spacer(1,.3*cm))

            # Insights
            insights=e.get("insights",[])
            if insights:
                items.append(T("Key Insights",h3s))
                for ins in insights:
                    items.append(T(f"• {ins}",bus))

            # Anomalies
            anomalies=e.get("anomalies",[])
            if anomalies:
                items.append(T("Anomalies Detected",h3s))
                for an in anomalies:
                    items.append(T(f"⚠ {an}",anom))

            # SQL
            if e.get("sql_query","").strip():
                items.append(T("SQL Query",h3s))
                for line in e["sql_query"].split("\n"):
                    items.append(T(line or " ",ms))

            # Reasoning
            if e.get("reasoning","").strip():
                items.append(T("AI Reasoning",h3s))
                items.append(T(e["reasoning"],bs))

            items.append(Spacer(1,.2*cm))
            items.append(HRFlowable(width="100%",thickness=.5,color=rc.HexColor('#1a2035'),spaceAfter=6))
            story.append(KeepTogether(items))

        doc.build(story)
        return buf.getvalue()
    except ImportError:
        return b""
    except Exception as exc:
        return b""

# ══════════════════════════════════════════════════════════════════════
#  HTTP LAYER  — encoding-safe for all providers
# ══════════════════════════════════════════════════════════════════════
def _http_post(url, headers, payload):
    import http.client, urllib.parse, ssl
    body=json.dumps(payload,ensure_ascii=False).encode("utf-8")
    safe_h={str(k): str(v).encode("ascii",errors="replace").decode("ascii")
            for k,v in headers.items()}
    safe_h["Content-Type"]  ="application/json; charset=utf-8"
    safe_h["Content-Length"]=str(len(body))
    p=urllib.parse.urlparse(url)
    host=p.netloc; path=p.path+(f"?{p.query}" if p.query else "")
    ctx=ssl.create_default_context()
    conn=(http.client.HTTPSConnection(host,timeout=90,context=ctx)
          if p.scheme=="https" else http.client.HTTPConnection(host,timeout=90))
    try:
        conn.request("POST",path,body=body,headers=safe_h)
        r=conn.getresponse(); rb=r.read().decode("utf-8",errors="replace")
    finally: conn.close()
    try: data=json.loads(rb)
    except json.JSONDecodeError: raise RuntimeError(f"HTTP {r.status}: non-JSON — {rb[:300]}")
    if r.status not in (200,201):
        msg=(data.get("error",{}).get("message") or data.get("message") or rb[:400])
        raise RuntimeError(f"API error {r.status}: {msg}")
    return data

def _call_openai(url, key, model, system, question):
    d=_http_post(url,{"Authorization":f"Bearer {key}"},
        {"model":model,
         "messages":[{"role":"system","content":system},{"role":"user","content":question}],
         "max_tokens":3500,"temperature":.1,"response_format":{"type":"json_object"}})
    return d["choices"][0]["message"]["content"]

def _call_gemini(url, key, system, question):
    prompt=f"{system}\n\nUser question: {question}\n\nRespond with ONLY a valid JSON object."
    d=_http_post(f"{url}?key={key}",{},
        {"contents":[{"role":"user","parts":[{"text":prompt}]}],
         "generationConfig":{"temperature":.1,"maxOutputTokens":3500}})
    try: return d["candidates"][0]["content"]["parts"][0]["text"]
    except(KeyError,IndexError): raise RuntimeError(f"Unexpected Gemini response: {str(d)[:300]}")

def _call_anthropic(url, key, model, system, question):
    d=_http_post(url,{"x-api-key":key,"anthropic-version":"2023-06-01"},
        {"model":model,"max_tokens":3500,"system":system,
         "messages":[{"role":"user","content":question}]})
    st.session_state.query_tokens_used+=d.get("usage",{}).get("input_tokens",0)+d.get("usage",{}).get("output_tokens",0)
    return d["content"][0]["text"]

def _parse_raw(raw):
    """Strip markdown fences and parse JSON robustly."""
    raw=re.sub(r'^```(?:json)?\s*','',raw.strip())
    raw=re.sub(r'\s*```$','',raw)
    try: return json.loads(raw)
    except json.JSONDecodeError:
        m=re.search(r'\{.*\}',raw,re.DOTALL)
        if m:
            try: return json.loads(m.group())
            except: pass
        raise RuntimeError(f"Could not parse AI JSON response:\n{raw[:500]}")

def _route(system, question):
    """Route to the selected provider. Returns raw text."""
    provider=st.session_state.get("provider","Groq (Free)")
    key=st.session_state.get("provider_key","").strip()
    if not key:
        raise RuntimeError(f"No API key for {provider}. Add it in the sidebar → AI Provider.")
    cfg=PROVIDERS[provider]
    style=cfg["style"]
    if   style=="openai":    return _call_openai(cfg["url"],key,cfg["model"],system,question)
    elif style=="gemini":    return _call_gemini(cfg["url"],key,system,question)
    elif style=="anthropic": return _call_anthropic(cfg["url"],key,cfg["model"],system,question)
    raise RuntimeError(f"Unknown provider style: {style}")

# ══════════════════════════════════════════════════════════════════════
#  AI SYSTEM PROMPTS
# ══════════════════════════════════════════════════════════════════════
ANALYSIS_SYSTEM = """You are NLDA Pro — a world-class data analyst AI.

Datasets available:
{schemas}

Recent conversation:
{context}

Answer the user's question. Respond with ONLY a valid JSON object (no markdown, no extra text):

{{
  "summary": "1-2 crisp sentences referencing ACTUAL numbers from the data",
  "pandas_code": "pandas code — use df (single table) or dfs['name'] (multi-table). MUST store final result in result_df. pd/np/datetime available. No imports. No file I/O.",
  "sql_query": "equivalent SQL SELECT statement (complete, runnable)",
  "chart_type": "one of: bar | grouped bar | stacked bar | horizontal bar | line | area | scatter | bubble | pie | donut | sunburst | treemap | histogram | box | violin | heatmap | density heatmap | waterfall | funnel | gauge | radar | parallel coordinates | candlestick | none",
  "chart_config": {{
    "x": "exact column name for X axis, or null",
    "y": "exact column name for Y axis — MUST be a numeric column",
    "color": "exact column name for color grouping, or null",
    "size": "exact column name for bubble size, or null",
    "title": "descriptive chart title"
  }},
  "kpis": [
    {{"label": "short metric name", "value": "pre-formatted string e.g. $1.2M", "delta": "+12.3% vs prior or null"}}
  ],
  "insights": [
    "Specific insight with exact number e.g. North America leads with $4.2M",
    "Second insight with exact number",
    "Third actionable insight"
  ],
  "anomalies": ["Describe any statistical outlier with specific value, or empty list []"],
  "follow_up_questions": ["Smart follow-up question 1?", "Question 2?", "Question 3?"],
  "confidence": "high | medium | low",
  "reasoning": "Brief description of your analytical approach"
}}

CRITICAL RULES:
1. chart_config.y MUST be a numeric column name that actually exists in the data
2. pandas_code MUST store final result in result_df variable
3. kpis: 2-5 items maximum, values as formatted strings
4. insights: minimum 2, must cite real numbers from the actual data
5. chart_type "none" only if the query needs no visualization
"""

STORY_SYSTEM = """You are a world-class data storyteller and business analyst.

You have access to these analysis results from a data session:
{analyses}

Write a compelling data story in 4 paragraphs:

Paragraph 1 — THE HEADLINE: Open with the single most important finding. Make it punchy. Use exact numbers.

Paragraph 2 — THE PATTERN: Explain the underlying trend or relationship driving this headline. What does the data reveal about how variables connect?

Paragraph 3 — THE SURPRISE: What is the most unexpected or counter-intuitive finding? What would a naive observer have predicted vs what the data actually shows?

Paragraph 4 — THE RECOMMENDATION: Close with 2-3 concrete, specific, actionable recommendations backed by the data. What should leadership do Monday morning?

Style: Write like a senior analyst presenting to a CEO. Direct, confident, data-driven. No bullet points. No headers. Just four powerful paragraphs.
Return ONLY the story text — no JSON, no markdown, no headers."""

def call_ai(question, schemas, history, extra=""):
    ctx="\n".join(f"Q:{h['question']}\nA:{h.get('summary','')}" for h in history[-4:]) or "(none)"
    system=ANALYSIS_SYSTEM.format(schemas=schemas,context=ctx)
    if extra: system+=f"\n\nAdditional context: {extra}"
    raw=_route(system,question)
    return _parse_raw(raw)

def call_story(analyses_text):
    """Generate data story — handles all providers correctly."""
    system=STORY_SYSTEM.format(analyses=analyses_text)
    question="Write the data story now based on the analyses above."
    try:
        provider=st.session_state.get("provider","Groq (Free)")
        key=st.session_state.get("provider_key","").strip()
        if not key: return "Add an API key in the sidebar to generate a data story."
        cfg=PROVIDERS[provider]
        style=cfg["style"]
        # For story we want plain text, not JSON — use a plain call
        if style=="openai":
            d=_http_post(cfg["url"],{"Authorization":f"Bearer {key}"},
                {"model":cfg["model"],
                 "messages":[{"role":"system","content":system},{"role":"user","content":question}],
                 "max_tokens":1500,"temperature":.7})
            return d["choices"][0]["message"]["content"]
        elif style=="gemini":
            prompt=f"{system}\n\n{question}"
            d=_http_post(f"{cfg['url']}?key={key}",{},
                {"contents":[{"role":"user","parts":[{"text":prompt}]}],
                 "generationConfig":{"temperature":.7,"maxOutputTokens":1500}})
            return d["candidates"][0]["content"]["parts"][0]["text"]
        elif style=="anthropic":
            d=_http_post(cfg["url"],{"x-api-key":key,"anthropic-version":"2023-06-01"},
                {"model":cfg["model"],"max_tokens":1500,"system":system,
                 "messages":[{"role":"user","content":question}]})
            return d["content"][0]["text"]
    except Exception as e:
        return f"Story generation error: {e}"

def safe_exec(code, dfs):
    env={"pd":pd,"np":np,"datetime":datetime,
         "dfs":dfs,"df":list(dfs.values())[0] if dfs else pd.DataFrame(),
         "result_df":None}
    try:
        exec(compile(code,"<nlda>","exec"),env)
        res=env.get("result_df")
        if res is not None and not isinstance(res,pd.DataFrame):
            try: res=pd.DataFrame({"result":[res]})
            except: res=None
        return res,None
    except Exception as e:
        return None,str(e)

# ══════════════════════════════════════════════════════════════════════
#  HELPER: run a query and return entry dict
# ══════════════════════════════════════════════════════════════════════
def run_query(question, prog_placeholder=None):
    schemas="\n\n".join(df_schema_str(df,n) for n,df in st.session_state.dataframes.items())
    STEPS=["PARSE","AI CALL","EXECUTE","VISUALIZE"]

    def show(active):
        if prog_placeholder is None: return
        items="".join(
            f'<div class="step-item {"done" if STEPS.index(s)<STEPS.index(active) else "active" if s==active else ""}"><span class="step-dot">{"✓" if STEPS.index(s)<STEPS.index(active) else "⬡"}</span>{s}</div>'
            for s in STEPS)
        prog_placeholder.markdown(f'<div class="step-track">{items}</div>',unsafe_allow_html=True)

    show("PARSE"); show("AI CALL")
    result=call_ai(question,schemas,st.session_state.chat_history)
    show("EXECUTE")
    rdf,err=None,None
    if result.get("pandas_code"):
        rdf,err=safe_exec(result["pandas_code"],st.session_state.dataframes)
    show("VISUALIZE")
    fig=None; ctype=result.get("chart_type","none")
    if ctype and ctype.lower()!="none" and rdf is not None and not rdf.empty:
        fig=make_chart(rdf,ctype,result.get("chart_config",{}))
        if fig: st.session_state.charts_generated+=1
    if prog_placeholder: prog_placeholder.empty()

    provider_label=PROVIDERS[st.session_state.get("provider","Groq (Free)")]["label"]
    return {
        "id":     hashlib.md5(f"{question}{time.time()}".encode()).hexdigest()[:10],
        "ts":     datetime.now().strftime("%H:%M"),
        "question":    question,
        "summary":     result.get("summary",""),
        "pandas_code": result.get("pandas_code",""),
        "sql_query":   result.get("sql_query",""),
        "chart_type":  ctype,
        "chart_config":result.get("chart_config",{}),
        "kpis":        result.get("kpis",[]),
        "insights":    result.get("insights",[]),
        "anomalies":   result.get("anomalies",[]),
        "follow_up_questions":result.get("follow_up_questions",[]),
        "confidence":  result.get("confidence","high"),
        "reasoning":   result.get("reasoning",""),
        "result_df":   rdf,
        "exec_error":  err,
        "fig":         fig,
        "provider":    provider_label,
    }

# ══════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div class="logo-bar">
        <span class="logo-hex">⬡</span>
        <span class="logo-name">NLDA Pro</span>
        <span class="logo-tag">The Data Storyteller · v4.1</span>
    </div>""", unsafe_allow_html=True)

    # ── AI Provider ──
    st.markdown('<div class="sb-sec">AI Provider</div>', unsafe_allow_html=True)
    provider=st.selectbox("Provider",list(PROVIDERS.keys()),
        index=list(PROVIDERS.keys()).index(st.session_state.get("provider","Groq (Free)")),
        key="provider_select")
    st.session_state["provider"]=provider
    pc=PROVIDERS[provider]
    fl="● FREE tier" if pc["free"] else "● Paid — requires credits"
    st.markdown(f'<div style="font-family:var(--fm);font-size:9px;color:{pc["badge"]};padding:2px 0 6px 1px">{fl} · {pc["model"]}</div>',unsafe_allow_html=True)
    kv=st.text_input(f"{pc['label']} API Key",type="password",
                     value=st.session_state.get("provider_key",""),
                     placeholder=pc["key_hint"],
                     help=f"Get a free key at {pc['key_url']}")
    if kv: st.session_state["provider_key"]=kv
    st.markdown(f'<div style="font-size:10px;color:var(--t3);padding:2px 0 4px">🔑 <a href="{pc["key_url"]}" target="_blank" style="color:var(--gold)">{pc["key_url"].replace("https://","")}</a></div>',unsafe_allow_html=True)

    # ── Session stats ──
    st.markdown('<div class="sb-sec">Session</div>', unsafe_allow_html=True)
    tr=sum(len(d) for d in st.session_state.dataframes.values())
    st.markdown(f"""<div class="stat-strip">
        <div class="sc"><span class="sc-v">{st.session_state.total_queries}</span><span class="sc-l">Queries</span></div>
        <div class="sc"><span class="sc-v">{st.session_state.charts_generated}</span><span class="sc-l">Charts</span></div>
        <div class="sc"><span class="sc-v">{len(st.session_state.dataframes)}</span><span class="sc-l">Tables</span></div>
        <div class="sc"><span class="sc-v">{fmt(tr,0)}</span><span class="sc-l">Rows</span></div>
    </div>""", unsafe_allow_html=True)

    # ── Data upload ──
    st.markdown('<div class="sb-sec">Data Sources</div>', unsafe_allow_html=True)
    uploaded=st.file_uploader("Upload CSV / Excel",type=["csv","xlsx","xls"],
                              accept_multiple_files=True,label_visibility="collapsed")
    if uploaded:
        for uf in uploaded:
            nm=re.sub(r'\s+','_',uf.name.rsplit(".",1)[0].lower())
            if nm not in st.session_state.dataframes:
                try:
                    df_up=pd.read_csv(uf) if uf.name.endswith(".csv") else pd.read_excel(uf)
                    for col in df_up.columns:
                        if any(kw in col.lower() for kw in ["date","time","period","month","year"]):
                            try: df_up[col]=pd.to_datetime(df_up[col])
                            except: pass
                    st.session_state.dataframes[nm]=df_up
                    st.session_state.df_meta[nm]=col_profile(df_up)
                    st.success(f"✓ {nm} ({len(df_up):,} rows)")
                except Exception as e: st.error(f"Error: {e}")

    for dn,dd in list(st.session_state.dataframes.items()):
        nc=len(smart_numeric_cols(dd))
        st.markdown(f"""<div class="ds-card active">
            <div class="ds-name">{dn}</div>
            <div class="ds-meta">
                <span class="ds-badge">{len(dd):,} rows</span>
                <span class="ds-badge">{len(dd.columns)} cols</span>
                <span class="ds-badge">{nc} numeric</span>
            </div>
        </div>""", unsafe_allow_html=True)
        if st.button(f"✕ Remove {dn}",key=f"rm_{dn}"):
            del st.session_state.dataframes[dn]; st.session_state.df_meta.pop(dn,None); st.rerun()

    st.markdown('<div class="sb-sec">Quick Start</div>', unsafe_allow_html=True)
    if st.button("⚡ Load Demo Datasets",use_container_width=True,key="sb_demo"):
        for k,v in generate_demo_datasets().items():
            st.session_state.dataframes[k]=v; st.session_state.df_meta[k]=col_profile(v)
        st.rerun()

    # ── Query Library ──
    if st.session_state.query_library:
        st.markdown('<div class="sb-sec">📚 Query Library</div>', unsafe_allow_html=True)
        for qi,q in enumerate(st.session_state.query_library[:8]):
            lbl=f"{q[:32]}…" if len(q)>32 else q
            if st.button(lbl,key=f"ql_{qi}"):
                st.session_state["_prefill"]=q; st.rerun()
        if st.button("🗑 Clear Library",key="clr_lib"):
            st.session_state.query_library=[]; st.rerun()

    # ── Export ──
    if st.session_state.chat_history:
        st.markdown('<div class="sb-sec">Export</div>', unsafe_allow_html=True)
        if st.button("📄 PDF Intelligence Report",use_container_width=True,key="pdf_btn"):
            with st.spinner("Generating PDF…"):
                pdf=make_pdf(st.session_state.chat_history)
            if pdf:
                st.download_button("⬇ Download PDF",pdf,
                    file_name=f"nlda_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",key="dl_pdf")
            else:
                st.info("Install reportlab: `pip install reportlab`")
        if st.button("🗑 Clear Session",use_container_width=True,key="clr_btn"):
            for k,v in _DEFAULTS.items(): st.session_state[k]=v
            st.rerun()

# ══════════════════════════════════════════════════════════════════════
#  MAIN PANEL
# ══════════════════════════════════════════════════════════════════════

# ── Hero ──
st.markdown("""<div class="hero">
    <div class="hero-grid"></div>
    <div class="hero-glow"></div><div class="hero-glow2"></div><div class="hero-glow3"></div>
    <div class="hero-eye">The Data Storyteller · v4.1 · Production Edition</div>
    <h1 class="hero-title">Your data has<br><span>a story to tell.</span></h1>
    <p class="hero-sub">
        Ask anything in plain English — get 25+ chart types, AI-powered narrative analysis,
        edit history, side-by-side comparison, and insights that no other platform generates.
    </p>
    <div class="hero-badges">
        <div class="hb"><div class="dot" style="background:#34d399"></div>25+ chart types</div>
        <div class="hb"><div class="dot" style="background:#f0c040"></div>AI storytelling</div>
        <div class="hb"><div class="dot" style="background:#a78bfa"></div>Edit any query</div>
        <div class="hb"><div class="dot" style="background:#22d3ee"></div>Compare mode</div>
        <div class="hb"><div class="dot" style="background:#fb7185"></div>Data DNA</div>
        <div class="hb"><div class="dot" style="background:#f472b6"></div>Auto-dashboard</div>
        <div class="hb"><div class="dot" style="background:#fbbf24"></div>PDF export</div>
    </div>
</div>""", unsafe_allow_html=True)

# ── Onboarding (no data) ──
if not st.session_state.dataframes:
    st.markdown("""<div class="ob-grid">
        <div class="ob-card"><div class="ob-num">01</div><div class="ob-title">Upload Data</div><div class="ob-desc">CSV or Excel. Multiple files. Auto date parsing.</div></div>
        <div class="ob-card"><div class="ob-num">02</div><div class="ob-title">Ask Anything</div><div class="ob-desc">Plain English. AI understands intent. Edit past queries and re-run.</div></div>
        <div class="ob-card"><div class="ob-num">03</div><div class="ob-title">25+ Chart Types</div><div class="ob-desc">Bar, violin, radar, waterfall, gauge, sunburst, candlestick & more.</div></div>
        <div class="ob-card"><div class="ob-num">04</div><div class="ob-title">AI Storytelling</div><div class="ob-desc">One click: CEO-ready narrative analysis of your entire session.</div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,c3=st.columns([1,2,1])
    with c2:
        if st.button("⚡ Try it — Load Demo Datasets",use_container_width=True,key="ob_demo"):
            for k,v in generate_demo_datasets().items():
                st.session_state.dataframes[k]=v; st.session_state.df_meta[k]=col_profile(v)
            st.rerun()
    st.stop()

# ══════════════════════════════════════════════════════════════════════
#  DATA LOADED — FEATURE STRIP
# ══════════════════════════════════════════════════════════════════════
feat_cols=st.columns(6)
feats=[
    ("🔬","Data DNA","Column fingerprints & outlier scan","show_dna"),
    ("🚀","Auto-Dashboard","4-panel overview in one click","show_autodash"),
    ("⚔","Compare Mode","Run 2 queries side by side","compare_mode"),
    ("📖","Data Story","AI narrative analysis","show_story"),
    ("⏱","Timeline","Visual thread of all findings","show_timeline"),
    ("🎨","Chart Composer","Build any chart manually","show_composer"),
]
for col,(icon,title,desc,key) in zip(feat_cols,feats):
    with col:
        active=st.session_state.get(key,False)
        if st.button(f"{icon} {title}",key=f"feat_{key}",
                     help=desc):
            st.session_state[key]=not active; st.rerun()

st.markdown("<div style='height:4px'></div>",unsafe_allow_html=True)

# ── Dataset Explorer ──
with st.expander("🗃  Dataset Explorer & Column Profiles",expanded=False):
    if st.session_state.dataframes:
        dstabs=st.tabs([f"  {n}  " for n in st.session_state.dataframes])
        for tab,(dn,dd) in zip(dstabs,st.session_state.dataframes.items()):
            with tab:
                nc=smart_numeric_cols(dd); cc=smart_cat_cols(dd)
                c1,c2,c3,c4,c5=st.columns(5)
                c1.metric("Rows",f"{len(dd):,}"); c2.metric("Columns",len(dd.columns))
                c3.metric("Numeric",len(nc)); c4.metric("Null%",f"{dd.isna().mean().mean()*100:.1f}%")
                c5.metric("Memory",f"{dd.memory_usage(deep=True).sum()/1024:.0f}KB")
                prof=st.session_state.df_meta.get(dn,col_profile(dd))
                html=""
                for col,info in list(prof.items())[:16]:
                    comp=info.get("completeness",round(100-info.get("null_pct",0),1))
                    dt=info["dtype"].replace("float64","float").replace("int64","int").replace("object","str")
                    html+=f'<div class="cp-card"><div class="cp-name">{col}</div><div class="cp-type">{dt} · {info["unique"]} unique</div><div class="cp-bar-w"><div class="cp-bar" style="width:{comp}%"></div></div></div>'
                st.markdown(f'<div class="cp-grid">{html}</div>',unsafe_allow_html=True)
                st.dataframe(dd.head(30),use_container_width=True,height=240)

# ── DATA DNA ──
if st.session_state.get("show_dna"):
    st.markdown('<div class="div">🔬 Data DNA — Column Fingerprints</div>',unsafe_allow_html=True)
    for dn,dd in st.session_state.dataframes.items():
        st.markdown(f"**{dn}**")
        nc=smart_numeric_cols(dd)
        if not nc:
            st.info("No numeric columns found."); continue
        cards=""
        for col in nc[:12]:
            s=dd[col].dropna()
            if len(s)==0: continue
            q1,q3=s.quantile(.25),s.quantile(.75); iqr=q3-q1
            out=int(((s<q1-1.5*iqr)|(s>q3+1.5*iqr)).sum())
            skw=float(s.skew()); kurt=float(s.kurt())
            skw_color="#fb7185" if abs(skw)>1 else "#34d399"
            out_color="#fb7185" if out>0 else "#34d399"
            cards+=(f'<div class="dna-card"><div class="dna-col">{col}</div>'
                f'<div class="dna-row"><span class="dna-k">Mean</span><span class="dna-v">{fmt(float(s.mean()))}</span></div>'
                f'<div class="dna-row"><span class="dna-k">Std dev</span><span class="dna-v">{fmt(float(s.std()))}</span></div>'
                f'<div class="dna-row"><span class="dna-k">Skewness</span><span class="dna-v" style="color:{skw_color}">{skw:.2f}</span></div>'
                f'<div class="dna-row"><span class="dna-k">Kurtosis</span><span class="dna-v">{kurt:.2f}</span></div>'
                f'<div class="dna-row"><span class="dna-k">IQR outliers</span><span class="dna-v" style="color:{out_color}">{out}</span></div>'
                f'</div>')
        st.markdown(f'<div class="dna-grid">{cards}</div>',unsafe_allow_html=True)

# ── AUTO DASHBOARD ──
if st.session_state.get("show_autodash"):
    st.markdown('<div class="div">🚀 Auto-Dashboard — Full Dataset Overview</div>',unsafe_allow_html=True)
    for dn,dd in st.session_state.dataframes.items():
        st.markdown(f"**{dn}** — {len(dd):,} rows")
        figs=make_multi_chart_dashboard(dd)
        if figs:
            cols=st.columns(min(2,len(figs)))
            for i,fg in enumerate(figs):
                with cols[i%2]: st.plotly_chart(fg,use_container_width=True,key=f"ad_{dn}_{i}")
        else:
            st.info("Not enough numeric/date columns for auto-dashboard on this dataset.")

# ── COMPARE MODE ──
if st.session_state.get("compare_mode"):
    st.markdown('<div class="div">⚔ Side-by-Side Comparison Mode</div>',unsafe_allow_html=True)
    cm1,cm2=st.columns(2)
    with cm1:
        st.markdown('<span class="compare-lbl cmp-a">Query A</span>',unsafe_allow_html=True)
        qa=st.text_input("Query A",value=st.session_state.compare_a,
                         placeholder="First question…",key="qa_in",label_visibility="collapsed")
        st.session_state.compare_a=qa
    with cm2:
        st.markdown('<span class="compare-lbl cmp-b">Query B</span>',unsafe_allow_html=True)
        qb=st.text_input("Query B",value=st.session_state.compare_b,
                         placeholder="Second question…",key="qb_in",label_visibility="collapsed")
        st.session_state.compare_b=qb
    if st.button("⚔ Run Both Queries",key="cmp_run",type="primary"):
        if qa.strip() and qb.strip():
            prog2=st.empty()
            with st.spinner("Running A…"):
                try: ra=run_query(qa.strip())
                except Exception as e: st.error(str(e)); ra=None
            with st.spinner("Running B…"):
                try: rb=run_query(qb.strip())
                except Exception as e: st.error(str(e)); rb=None
            if ra and rb:
                st.session_state["cmp_results"]=(qa,qb,ra,rb)
    if st.session_state.get("cmp_results"):
        qa2,qb2,ra2,rb2=st.session_state["cmp_results"]
        cr1,cr2=st.columns(2)
        for col,q,r,lab,cls in [(cr1,qa2,ra2,"A","cmp-a"),(cr2,qb2,rb2,"B","cmp-b")]:
            with col:
                st.markdown(f'<div class="compare-panel"><span class="compare-lbl {cls}">Result {lab}</span><br><b style="font-size:12px">{q[:50]}</b><br><div style="font-size:13px;color:var(--t2);margin:8px 0">{r.get("summary","")}</div>',unsafe_allow_html=True)
                if r.get("fig"):
                    st.plotly_chart(r["fig"],use_container_width=True,key=f"cmp_{lab}_fig")
                elif r.get("result_df") is not None and not r["result_df"].empty:
                    st.dataframe(r["result_df"].head(10),use_container_width=True)
                st.markdown('</div>',unsafe_allow_html=True)

# ── DATA STORY ──
if st.session_state.get("show_story"):
    st.markdown('<div class="div">📖 AI Data Story — Narrative Analysis</div>',unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.info("Run some queries first, then come back to generate the story.")
    else:
        def _fmt_entry(i, e):
            kpi_str="; ".join(str(k.get("label",""))+"="+str(k.get("value","")) for k in e.get("kpis",[]))
            return (f"Analysis {i+1}\nQuestion: {e['question']}\n"
                    f"Answer: {e.get('summary','')}\n"
                    f"Key insights: {'; '.join(e.get('insights',[]))}\n"
                    f"KPIs: {kpi_str}")
        analyses="\n\n".join(_fmt_entry(i,e) for i,e in enumerate(st.session_state.chat_history[-8:]))
        story_key=hashlib.md5(analyses.encode()).hexdigest()[:8]
        cached=st.session_state.story_cache.get(story_key)
        if cached is None:
            with st.spinner("✍ Writing your data story…"):
                cached=call_story(analyses)
                st.session_state.story_cache[story_key]=cached
        st.markdown(f"""<div class="story-wrap">
            <div class="story-title">✦ The Data Story — {len(st.session_state.chat_history)} analyses</div>
            <div class="story-text">{cached}</div>
        </div>""",unsafe_allow_html=True)
        if st.button("🔄 Regenerate Story",key="regen_story"):
            st.session_state.story_cache.pop(story_key,None); st.rerun()

# ── INSIGHT TIMELINE ──
if st.session_state.get("show_timeline") and len(st.session_state.chat_history)>=1:
    st.markdown('<div class="div">⏱ Insight Timeline</div>',unsafe_allow_html=True)
    colors=["#f0c040","#a78bfa","#22d3ee","#34d399","#fb7185","#fbbf24","#f472b6","#38bdf8"]
    tl='<div class="timeline">'
    for i,e in enumerate(st.session_state.chat_history):
        dc=colors[i%len(colors)]
        ins=e.get("insights",[""])[0][:90] if e.get("insights") else ""
        tl+=(f'<div class="tl-item">'
             f'<div class="tl-dot" style="background:{dc}"></div>'
             f'<div class="tl-time">Query {i+1} · {e.get("ts","")}</div>'
             f'<div class="tl-q">{e["question"]}</div>'
             f'<div class="tl-a">{e.get("summary","")[:100]}</div>'
             f'{"<div class=tl-ins style=color:"+dc+">↳ "+ins+"</div>" if ins else ""}'
             f'</div>')
    tl+='</div>'
    st.markdown(tl,unsafe_allow_html=True)

# ── CHART COMPOSER ──
if st.session_state.get("show_composer"):
    st.markdown('<div class="div">🎨 Chart Composer — Build Any Chart Manually</div>',unsafe_allow_html=True)
    dnames=list(st.session_state.dataframes.keys())
    if dnames:
        cc1,cc2,cc3,cc4,cc5,cc6=st.columns(6)
        with cc1: cds=st.selectbox("Dataset",dnames,key="comp_ds")
        cdf=st.session_state.dataframes[cds]
        allc=["(none)"]+list(cdf.columns)
        with cc2: cct=st.selectbox("Chart type",CHART_TYPES_DISPLAY,key="comp_ct")
        with cc3: cx=st.selectbox("X axis",allc,key="comp_x")
        with cc4: cy=st.selectbox("Y axis",allc,key="comp_y")
        with cc5: ccol=st.selectbox("Color by",allc,key="comp_col")
        with cc6: ctitle=st.text_input("Title","My Chart",key="comp_title")
        if st.button("🎨 Render",key="comp_go",type="primary"):
            fc={"x":None if cx=="(none)" else cx,
                "y":None if cy=="(none)" else cy,
                "color":None if ccol=="(none)" else ccol,
                "title":ctitle}
            fg=make_chart(cdf,cct,fc)
            if fg: st.plotly_chart(fg,use_container_width=True,key="comp_fig")
            else:  st.warning("Could not render — try different column selections or chart type.")

# ══════════════════════════════════════════════════════════════════════
#  CHAT HISTORY
# ══════════════════════════════════════════════════════════════════════
if st.session_state.chat_history:
    st.markdown('<div class="div">Analysis History</div>',unsafe_allow_html=True)

    for idx,entry in enumerate(st.session_state.chat_history):
        is_editing=(st.session_state.editing_idx==idx)

        # ── User message ──
        st.markdown(f"""<div class="msg-row">
            <div class="msg-user-wrap">
                <div class="msg-user">{entry['question']}</div>
            </div>
            <div class="msg-meta" style="text-align:right">You · {entry.get('ts','')} · via {entry.get('provider','AI')}</div>
        </div>""",unsafe_allow_html=True)

        # Edit / Delete / Save controls
        ec1,ec2,ec3,ec4=st.columns([1,1,1,7])
        with ec1:
            if st.button("✎ Edit",key=f"edit_{idx}"):
                st.session_state.editing_idx=idx
                st.session_state["_prefill"]=entry["question"]
                st.rerun()
        with ec2:
            if st.button("🗑 Del",key=f"del_{idx}"):
                st.session_state.chat_history.pop(idx); st.rerun()
        with ec3:
            if st.button("📚 Save",key=f"save_{idx}"):
                if entry["question"] not in st.session_state.query_library:
                    st.session_state.query_library.append(entry["question"])
                    st.success("Saved to library!")

        # ── Edit box ──
        if is_editing:
            st.markdown('<div class="edit-wrap"><div class="edit-lbl">✎ Edit this query and re-run</div>',unsafe_allow_html=True)
            eq=st.text_input("Edited query",value=entry["question"],key=f"eq_{idx}",label_visibility="collapsed")
            er1,er2,er3=st.columns([1,1,5])
            with er1:
                if st.button("▶ Re-run",key=f"rerun_{idx}",type="primary"):
                    prog_ph=st.empty()
                    try:
                        new_e=run_query(eq.strip(),prog_ph)
                        st.session_state.chat_history[idx]=new_e
                        st.session_state.editing_idx=None
                        st.session_state.total_queries+=1
                        st.rerun()
                    except Exception as ex:
                        prog_ph.empty(); st.error(str(ex))
            with er2:
                if st.button("✕ Cancel",key=f"cancel_{idx}"):
                    st.session_state.editing_idx=None; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

        # ── AI response ──
        conf=entry.get("confidence","high")
        cc={"high":"#34d399","medium":"#fbbf24","low":"#fb7185"}.get(conf,"#34d399")
        st.markdown(f"""<div class="msg-row">
            <div class="msg-ai-wrap">
                <div class="msg-ai">
                    <span style="font-family:var(--fm);font-size:8px;letter-spacing:.15em;color:{cc};text-transform:uppercase;display:block;margin-bottom:6px">
                        ⬡ NLDA Pro · {entry.get('provider','AI')} · {conf} confidence
                    </span>
                    {entry.get('summary','Analysis complete.')}
                </div>
            </div>
            <div class="msg-meta">{entry.get('ts','')}</div>
        </div>""",unsafe_allow_html=True)

        # ── KPI tiles ──
        _rdf=entry.get("result_df"); _kpis=entry.get("kpis") or []
        if not _kpis and _rdf is not None and not _rdf.empty:
            _kpis=generate_auto_kpis(_rdf)
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

        # ── Result tabs ──
        rt=st.tabs(["📊 Chart","📋 Table","💡 Insights","🔎 SQL","🐍 Code","🧠 Reasoning","➕ Alt Charts"])

        with rt[0]:  # CHART
            if entry.get("fig"):
                pc2,_=st.columns([1,8])
                with pc2:
                    if st.button("📌 Pin chart",key=f"pin_{entry['id']}"):
                        st.session_state.pinned_charts.append(entry["fig"]); st.success("Pinned!")
                st.plotly_chart(entry["fig"],use_container_width=True,key=f"fig_{entry['id']}")
            else:
                st.markdown(f"""<div class="no-chart">
                    <span class="no-chart-icon">📊</span>
                    No chart rendered for this query.<br>
                    Try asking: "show as a bar chart" or use the <b>Alt Charts</b> tab to pick a chart type.
                </div>""",unsafe_allow_html=True)

        with rt[1]:  # TABLE
            rdf=entry.get("result_df")
            if rdf is not None and not rdf.empty:
                st.dataframe(rdf,use_container_width=True,height=300)
                dl1,dl2,_=st.columns([1,1,5])
                with dl1:
                    st.download_button("⬇ CSV",rdf.to_csv(index=False).encode(),
                                       file_name=f"nlda_{entry['id']}.csv",mime="text/csv",key=f"csv_{entry['id']}")
                with dl2:
                    try:
                        xl=io.BytesIO()
                        with pd.ExcelWriter(xl,engine="openpyxl") as xw: rdf.to_excel(xw,index=False)
                        st.download_button("⬇ Excel",xl.getvalue(),
                                           file_name=f"nlda_{entry['id']}.xlsx",
                                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                           key=f"xl_{entry['id']}")
                    except: pass
            else:
                st.info("No tabular data for this query.")

        with rt[2]:  # INSIGHTS
            cards=""
            icons=["★","◆","▲","●","◉","✦"]; icls=["#gd","#cd","#vd","rgba(52,211,153,.1)","rgba(251,113,133,.1)","rgba(56,189,248,.1)"]
            bg_colors=["rgba(240,192,64,.1)","rgba(34,211,238,.1)","rgba(167,139,250,.1)",
                       "rgba(52,211,153,.1)","rgba(251,113,133,.1)","rgba(56,189,248,.1)"]
            for i,ins in enumerate(entry.get("insights",[])):
                bg=bg_colors[i%len(bg_colors)]
                cards+=f'<div class="insight-card"><div class="ins-icon" style="background:{bg}">{icons[i%len(icons)]}</div><div class="ins-text">{ins}</div></div>'
            for an in entry.get("anomalies",[]):
                cards+=f'<div class="insight-card"><div class="ins-icon" style="background:rgba(251,113,133,.15)">⚠</div><div class="ins-text" style="color:#fb7185"><strong>Anomaly:</strong> {an}</div></div>'
            if cards: st.markdown(f'<div class="insight-row">{cards}</div>',unsafe_allow_html=True)
            else:     st.info("No insights generated.")
            fqs=entry.get("follow_up_questions",[])
            if fqs:
                st.markdown('<div style="font-family:var(--fm);font-size:9px;color:var(--t3);letter-spacing:.2em;text-transform:uppercase;margin:14px 0 8px">Suggested next questions</div>',unsafe_allow_html=True)
                fq_c=st.columns(len(fqs))
                for col,q in zip(fq_c,fqs):
                    with col:
                        if st.button(f"↗ {q}",key=f"fq_{entry['id']}_{q[:16]}"):
                            st.session_state["_prefill"]=q; st.rerun()

        with rt[3]:  # SQL
            sql=entry.get("sql_query","").strip()
            if sql: st.markdown(code_html(sql,"sql"),unsafe_allow_html=True)
            else:   st.info("No SQL generated for this query.")

        with rt[4]:  # CODE
            pyc=entry.get("pandas_code","").strip(); err=entry.get("exec_error","")
            if pyc: st.markdown(code_html(pyc,"python"),unsafe_allow_html=True)
            if err: st.error(f"Code execution note: {err}")
            if not pyc: st.info("No Python code generated.")

        with rt[5]:  # REASONING
            r=entry.get("reasoning","").strip()
            if r:
                st.markdown(f'<div style="background:var(--raised);border:1px solid var(--bd1);border-radius:10px;padding:16px 20px;font-size:13px;color:#94a3b8;line-height:1.75"><span style="font-family:var(--fm);font-size:8px;color:#475569;letter-spacing:.15em;text-transform:uppercase;display:block;margin-bottom:10px">⬡ AI Reasoning Chain</span>{r}</div>',unsafe_allow_html=True)
            else: st.info("No reasoning available.")

        with rt[6]:  # ALT CHARTS
            rdf2=entry.get("result_df")
            if rdf2 is not None and not rdf2.empty:
                nc2=smart_numeric_cols(rdf2); cc3=smart_cat_cols(rdf2)
                alt_options=[]
                if cc3 and nc2:
                    for ctype in ["bar","horizontal bar","pie","donut","radar","treemap","sunburst","funnel"]:
                        alt_options.append((ctype,{"x":cc3[0],"y":nc2[0],"title":f"{ctype.title()} — {nc2[0]} by {cc3[0]}"}))
                if len(nc2)>=2:
                    for ctype in ["scatter","bubble","box","violin","heatmap","parallel coordinates","density heatmap"]:
                        alt_options.append((ctype,{"x":nc2[0],"y":nc2[1],"title":f"{ctype.title()}"}))
                if nc2:
                    for ctype in ["histogram","gauge","waterfall"]:
                        alt_options.append((ctype,{"x":cc3[0] if cc3 else None,"y":nc2[0],"title":ctype.title()}))
                if alt_options:
                    sel=st.selectbox("Choose alternative chart",
                                     [ct for ct,_ in alt_options],
                                     key=f"altsel_{entry['id']}")
                    sel_cfg=next(cfg for ct,cfg in alt_options if ct==sel)
                    afig=make_chart(rdf2,sel,sel_cfg)
                    if afig: st.plotly_chart(afig,use_container_width=True,key=f"alt_{entry['id']}_{sel}")
                    else:    st.warning(f"'{sel}' chart could not be rendered — try another type.")
                else:
                    st.info("Not enough column types for alternative charts.")
            else:
                st.info("No result data to visualize.")

        st.markdown('<div style="margin:8px 0 4px;border-top:1px solid #1a2035"></div>',unsafe_allow_html=True)

# ── Pinned Charts ──
if st.session_state.pinned_charts:
    st.markdown('<div class="div">📌 Pinned Charts Dashboard</div>',unsafe_allow_html=True)
    pcols=st.columns(min(2,len(st.session_state.pinned_charts)))
    for i,fg in enumerate(st.session_state.pinned_charts):
        with pcols[i%2]: st.plotly_chart(fg,use_container_width=True,key=f"pin_{i}")
    if st.button("Clear All Pins",key="clr_pins"):
        st.session_state.pinned_charts=[]; st.rerun()

# ══════════════════════════════════════════════════════════════════════
#  QUERY INPUT  — v4.1: clears after submit, has Clear button
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="div">New Analysis</div>',unsafe_allow_html=True)

# Suggestion chips
CHIPS=["Top 10 by revenue","Monthly revenue trend","Correlation heatmap",
       "Profit by region (bar)","ROAS by channel","Revenue vs spend (scatter)",
       "Violin distribution","Waterfall by quarter"]

prefill=st.session_state.pop("_prefill","")

# If clear_input flag is set, force-reset the input key
if st.session_state.get("clear_input"):
    st.session_state.clear_input=False
    st.session_state["_query_value"]=""
    prefill=""

chip_cols=st.columns(len(CHIPS))
for i,(col,sug) in enumerate(zip(chip_cols,CHIPS)):
    with col:
        if st.button(sug,key=f"chip_{i}"): prefill=sug

st.markdown('<div class="q-wrap">',unsafe_allow_html=True)
st.markdown('<div class="q-lbl">Natural Language Query</div>',unsafe_allow_html=True)

# Use a key tied to a session counter so we can force-reset it
input_key=f"main_q_{st.session_state.get('query_counter',0)}"
query=st.text_input(
    "q", value=prefill,
    placeholder='e.g. "Show profit by region as a horizontal bar chart" or "What are the top 5 products by revenue?"',
    label_visibility="collapsed",
    key=input_key)

qc1,qc2,qc3,qc4=st.columns([2,1,1,4])
with qc1: run=st.button("⬡  Analyze",use_container_width=True,key="run_btn",type="primary")
with qc2: deep=st.checkbox("Deep",value=False,help="More thorough analysis")
with qc3:
    # ── CLEAR QUERY BUTTON ── (new in v4.1)
    if st.button("✕ Clear",key="clear_q"):
        st.session_state["query_counter"]=st.session_state.get("query_counter",0)+1
        st.rerun()
st.markdown('</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  ANALYSIS ENGINE
# ══════════════════════════════════════════════════════════════════════
if run and query.strip():
    if not st.session_state.get("provider_key","").strip():
        pname=st.session_state.get("provider","Groq (Free)")
        pcfg=PROVIDERS[pname]
        st.error(f"⚠ No API key for **{pname}**. "
                 f"Get a free key at [{pcfg['key_url']}]({pcfg['key_url']}) and paste it in the sidebar.")
        st.stop()

    prog=st.empty()
    try:
        entry=run_query(query.strip(),prog)
    except RuntimeError as e:
        prog.empty(); st.error(str(e)); st.stop()
    except json.JSONDecodeError as e:
        prog.empty(); st.error(f"JSON parse error — try rephrasing your question. ({e})"); st.stop()
    except Exception as e:
        prog.empty(); st.error(f"Unexpected error: {e}"); st.stop()

    st.session_state.chat_history.append(entry)
    st.session_state.total_queries+=1
    # ── Clear input after successful query ── (v4.1 fix)
    st.session_state["query_counter"]=st.session_state.get("query_counter",0)+1
    st.rerun()
