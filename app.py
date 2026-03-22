"""
╔═══════════════════════════════════════════════════════════════════╗
║  NLDA PRO  Business Data Intelligence Platform                 ║
║  "The Data Storyteller" — Ultimate Edition                        ║
╠═══════════════════════════════════════════════════════════════════╣
║  FIXED in v5.0:                                                   ║
║  1. Visual Insights — AI-powered mini-charts per insight, smart   ║
║     column validation, insight quality scoring, trend indicators  ║
║  2. PDF — rich formatted report with chart images (kaleido),      ║
║     professional layout, story section, KPI tables               ║
║  3. Chart Composer — industry preset templates (Sales, Finance,   ║
║     Marketing, HR, Operations), smart column auto-mapping         ║
║  4. Storytelling — deep 6-paragraph story of ENTIRE dataset,      ║
║     not just recent queries. Includes patterns, anomalies,        ║
║     correlations, seasonal trends, recommendations                ║
║  5. Per-query story — every single analysis gets its own          ║
║     mini-narrative explaining what the chart means                ║
╚═══════════════════════════════════════════════════════════════════╝
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json, io, re, time, hashlib, textwrap
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NLDA Pro · Business Data Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────
#  DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Inter:wght@300;400;500;600&display=swap');
:root{
  --void:#05060a;--base:#090b11;--surface:#0e1117;--raised:#131720;--overlay:#181e2b;
  --bd0:#1a2035;--bd1:#232b40;--bd2:#2d3a55;
  --gold:#f0c040;--gd:rgba(240,192,64,.12);--gg:rgba(240,192,64,.3);
  --cyan:#22d3ee;--cd:rgba(34,211,238,.1);
  --violet:#a78bfa;--vd:rgba(167,139,250,.1);
  --emerald:#34d399;--rose:#fb7185;--amber:#fbbf24;--sky:#38bdf8;--pink:#f472b6;
  --t1:#f1f5f9;--t2:#94a3b8;--t3:#475569;
  --r1:6px;--r2:10px;--r3:16px;--r4:24px;
  --fd:'Syne',sans-serif;--fb:'Inter',sans-serif;--fm:'JetBrains Mono',monospace;
}
html,body,.stApp,[data-testid="stAppViewContainer"]{background:var(--void)!important;font-family:var(--fb);color:var(--t1);}
*{box-sizing:border-box;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-thumb{background:var(--bd2);border-radius:2px;}
[data-testid="stSidebar"]{background:var(--base)!important;border-right:1px solid var(--bd0)!important;}
[data-testid="stSidebar"] *{color:var(--t1)!important;}
[data-testid="stSidebarContent"]{padding:0 0 2rem!important;}
#MainMenu,footer,[data-testid="stDecoration"]{display:none!important;}
[data-testid="stSidebarCollapseButton"],[data-testid="collapsedControl"]{display:flex!important;opacity:1!important;}
.block-container{padding:1.5rem 2rem 4rem!important;max-width:1500px;}
h1,h2,h3,h4{font-family:var(--fd)!important;letter-spacing:-.02em;}
/* LOGO */
.logo-bar{background:linear-gradient(135deg,var(--base),var(--surface));border-bottom:1px solid var(--bd0);padding:20px 22px 16px;}
.logo-hex{font-size:28px;line-height:1;display:block;margin-bottom:5px;}
.logo-name{font-family:var(--fd);font-size:18px;font-weight:800;background:linear-gradient(135deg,var(--gold),var(--amber));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;display:block;line-height:1;}
.logo-tag{font-family:var(--fm);font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:var(--t3);display:block;margin-top:4px;}
.sb-sec{padding:13px 18px 5px;font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--t3);border-top:1px solid var(--bd0);margin-top:6px;}
/* STAT STRIP */
.stat-strip{display:flex;gap:5px;padding:7px 14px 12px;flex-wrap:wrap;}
.sc{flex:1;min-width:62px;background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:8px 9px;text-align:center;}
.sc-v{font-family:var(--fm);font-size:17px;font-weight:500;color:var(--gold);display:block;line-height:1.1;}
.sc-l{font-size:8px;color:var(--t3);text-transform:uppercase;letter-spacing:.1em;margin-top:2px;display:block;}
/* DS CARD */
.ds-card{margin:4px 10px;background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:10px 12px;}
.ds-card.active{border-color:var(--gold);}
.ds-name{font-family:var(--fd);font-size:12px;font-weight:700;}
.ds-meta{font-family:var(--fm);font-size:9px;color:var(--t3);margin-top:2px;}
.ds-badge{display:inline-block;background:var(--gd);border:1px solid var(--gg);border-radius:3px;font-family:var(--fm);font-size:8px;color:var(--gold);padding:1px 5px;margin-right:3px;}
/* HERO */
.hero{position:relative;background:var(--surface);border:1px solid var(--bd1);border-radius:var(--r4);padding:52px 60px;margin-bottom:28px;overflow:hidden;}
.hero-grid{position:absolute;inset:0;background-image:linear-gradient(var(--bd0) 1px,transparent 1px),linear-gradient(90deg,var(--bd0) 1px,transparent 1px);background-size:40px 40px;opacity:.3;}
.hero-glow{position:absolute;top:-100px;right:-80px;width:420px;height:420px;background:radial-gradient(circle,var(--gg) 0%,transparent 70%);pointer-events:none;}
.hero-glow2{position:absolute;bottom:-60px;left:18%;width:300px;height:300px;background:radial-gradient(circle,rgba(167,139,250,.14) 0%,transparent 70%);pointer-events:none;}
.hero-glow3{position:absolute;top:20%;left:-80px;width:250px;height:250px;background:radial-gradient(circle,rgba(34,211,238,.08) 0%,transparent 70%);pointer-events:none;}
.hero-eye{font-family:var(--fm);font-size:9px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.hero-eye::before{content:'';display:block;width:24px;height:1px;background:var(--gold);}
.hero-title{font-family:var(--fd);font-size:clamp(36px,5.5vw,72px);font-weight:800;letter-spacing:-.04em;line-height:.92;color:var(--t1);margin:0 0 6px;position:relative;}
.hero-title span{background:linear-gradient(135deg,var(--gold) 0%,var(--amber) 40%,var(--rose) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{font-size:17px;color:var(--t2);font-weight:300;margin-top:16px;max-width:580px;line-height:1.65;position:relative;}
.hero-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:24px;position:relative;}
.hb{display:flex;align-items:center;gap:6px;background:var(--raised);border:1px solid var(--bd2);border-radius:50px;padding:6px 14px;font-size:11px;color:var(--t2);font-family:var(--fm);}
.hb .dot{width:6px;height:6px;border-radius:50%;}
/* QUERY PANEL */
.q-wrap{background:var(--surface);border:1px solid var(--bd1);border-radius:var(--r4);padding:22px;margin-bottom:24px;position:relative;}
.q-wrap::before{content:'';position:absolute;inset:-1px;border-radius:var(--r4);background:linear-gradient(135deg,var(--gold),var(--violet),var(--cyan));-webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;padding:1px;opacity:0;transition:opacity .3s;pointer-events:none;}
.q-wrap:focus-within::before{opacity:1;}
.q-lbl{font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--t3);margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.q-lbl::after{content:'';flex:1;height:1px;background:var(--bd0);}
/* BUTTONS */
.stButton>button{background:var(--raised)!important;color:var(--t2)!important;border:1px solid var(--bd1)!important;border-radius:8px!important;font-family:var(--fb)!important;font-size:12px!important;font-weight:500!important;line-height:1.35!important;padding:8px 10px!important;white-space:normal!important;word-break:break-word!important;min-height:38px!important;width:100%!important;transition:all .15s!important;cursor:pointer!important;}
.stButton>button:hover{border-color:var(--gold)!important;color:var(--gold)!important;background:var(--gd)!important;transform:translateY(-1px)!important;}
.stButton>button:active{transform:translateY(0)!important;opacity:.85!important;}
button[data-testid="baseButton-primary"]{background:linear-gradient(135deg,#c8980e,#f0c040)!important;color:#05060a!important;border:none!important;border-radius:var(--r2)!important;font-family:var(--fd)!important;font-size:15px!important;font-weight:700!important;padding:12px 30px!important;white-space:nowrap!important;min-height:46px!important;box-shadow:0 4px 24px rgba(240,192,64,.3)!important;}
button[data-testid="baseButton-primary"]:hover{box-shadow:0 8px 40px rgba(240,192,64,.5)!important;transform:translateY(-2px)!important;color:#05060a!important;}

/* PRESET PILL BUTTONS — fixed height, never wrap */
.preset-pill-row{display:flex;gap:10px;flex-wrap:nowrap;overflow-x:auto;padding:4px 2px 12px;scrollbar-width:thin;scrollbar-color:var(--bd2) transparent;}
.preset-pill-row::-webkit-scrollbar{height:4px;}
.preset-pill-row::-webkit-scrollbar-thumb{background:var(--bd2);border-radius:2px;}
.preset-pill{flex:0 0 auto;display:flex;align-items:center;gap:8px;
  background:var(--raised);border:1px solid var(--bd1);border-radius:50px;
  padding:10px 18px;cursor:pointer;transition:all .18s;
  font-family:var(--fb);font-size:12px;font-weight:600;
  color:var(--t2);white-space:nowrap;user-select:none;}
.preset-pill:hover{border-color:var(--gold);color:var(--gold);background:var(--gd);transform:translateY(-2px);box-shadow:0 4px 16px rgba(240,192,64,.15);}
.preset-pill.active{border-color:var(--gold);color:var(--gold);background:var(--gd);box-shadow:0 0 0 2px rgba(240,192,64,.2);}
.preset-pill .pill-icon{font-size:16px;line-height:1;}
.preset-pill .pill-label{letter-spacing:.01em;}
/* TEXT INPUT */
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:var(--raised)!important;border:1px solid var(--bd1)!important;border-radius:var(--r2)!important;color:var(--t1)!important;font-family:var(--fb)!important;font-size:16px!important;padding:14px 20px!important;transition:border-color .2s!important;}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{border-color:var(--gold)!important;box-shadow:0 0 0 3px var(--gd)!important;}
.stTextInput>div>div>input::placeholder{color:var(--t3)!important;}
/* CHAT */
.msg-row{display:flex;flex-direction:column;gap:4px;margin:22px 0;}
.msg-user-wrap{display:flex;justify-content:flex-end;}
.msg-ai-wrap{display:flex;justify-content:flex-start;}
.msg-user{max-width:75%;background:linear-gradient(135deg,rgba(240,192,64,.15),rgba(167,139,250,.1));border:1px solid rgba(240,192,64,.3);border-radius:20px 20px 4px 20px;padding:14px 20px;font-size:15px;line-height:1.65;color:var(--t1);}
.msg-ai{max-width:85%;background:var(--raised);border:1px solid var(--bd1);border-radius:4px 20px 20px 20px;padding:14px 20px;font-size:15px;line-height:1.65;color:var(--t2);}
.msg-meta{font-family:var(--fm);font-size:9px;letter-spacing:.15em;text-transform:uppercase;color:var(--t3);padding:0 4px;margin-top:4px;}
/* TABS */
.stTabs [data-baseweb="tab-list"]{background:var(--base)!important;border-bottom:1px solid var(--bd0)!important;border-radius:0!important;gap:0!important;padding:0 8px!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--t3)!important;border-radius:0!important;font-family:var(--fm)!important;font-size:10px!important;letter-spacing:.08em!important;padding:12px 18px!important;border-bottom:2px solid transparent!important;transition:all .15s!important;}
.stTabs [aria-selected="true"]{background:transparent!important;color:var(--gold)!important;border-bottom-color:var(--gold)!important;}
.stTabs [data-testid="stTabContent"]{background:var(--surface)!important;padding:20px!important;}
/* KPI TILES */
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:12px;margin:16px 0;}
.kpi-tile{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:18px 20px;position:relative;overflow:hidden;}
.kpi-tile::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.c-gold::after{background:var(--gold);}.c-cyan::after{background:var(--cyan);}.c-violet::after{background:var(--violet);}
.c-emerald::after{background:var(--emerald);}.c-rose::after{background:var(--rose);}.c-sky::after{background:var(--sky);}
.kpi-val{font-family:var(--fm);font-size:26px;font-weight:500;color:var(--t1);display:block;line-height:1.1;}
.kpi-lbl{font-size:11px;color:var(--t3);margin-top:6px;text-transform:uppercase;letter-spacing:.08em;font-family:var(--fm);}
.kpi-delta{font-family:var(--fm);font-size:11px;margin-top:4px;}
.kpi-delta.pos{color:var(--emerald);}.kpi-delta.neg{color:var(--rose);}
/* INSIGHT CARDS v5 — richer */
.insight-row{display:flex;flex-direction:column;gap:10px;margin:12px 0;}
.insight-card{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:16px;position:relative;overflow:hidden;}
.insight-card::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;}
.ins-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;}
.ins-title{font-family:var(--fd);font-size:12px;font-weight:700;color:var(--t1);}
.ins-badge{font-family:var(--fm);font-size:9px;padding:2px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:.08em;}
.ins-text{font-size:13px;color:var(--t2);line-height:1.65;}
.ins-trend{display:flex;align-items:center;gap:6px;margin-top:8px;font-family:var(--fm);font-size:10px;}
.trend-up{color:var(--emerald);}.trend-down{color:var(--rose);}.trend-flat{color:var(--t3);}
.anomaly-card{background:rgba(251,113,133,.06);border:1px solid rgba(251,113,133,.25);border-radius:var(--r2);padding:14px 16px;margin:6px 0;display:flex;gap:12px;align-items:flex-start;}
.anomaly-icon{font-size:18px;flex-shrink:0;}
.anomaly-text{font-size:13px;color:var(--rose);line-height:1.6;}
/* STORY */
.story-wrap{background:linear-gradient(135deg,rgba(240,192,64,.04),rgba(167,139,250,.04));border:1px solid rgba(240,192,64,.2);border-radius:var(--r3);padding:30px 36px;margin:20px 0;position:relative;overflow:hidden;}
.story-wrap::before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(180deg,var(--gold),var(--violet),var(--cyan));}
.story-eyebrow{font-family:var(--fm);font-size:9px;letter-spacing:.25em;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.story-headline{font-family:var(--fd);font-size:18px;font-weight:800;color:var(--t1);margin-bottom:16px;line-height:1.2;}
.story-body{font-size:15px;color:var(--t1);line-height:1.9;}
.story-body p{margin:0 0 16px;}
.story-body p:last-child{margin:0;}
.story-chapter{font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--violet);margin:20px 0 8px;display:flex;align-items:center;gap:8px;}
.story-chapter::after{content:'';flex:1;height:1px;background:var(--bd0);}
/* QUERY STORY */
.qstory-wrap{background:var(--overlay);border:1px solid var(--bd1);border-radius:var(--r2);padding:16px 20px;margin:12px 0;}
.qstory-lbl{font-family:var(--fm);font-size:8px;letter-spacing:.2em;text-transform:uppercase;color:var(--violet);margin-bottom:8px;}
.qstory-text{font-size:13px;color:var(--t2);line-height:1.75;}
/* COMPOSER */
.composer-wrap{background:var(--surface);border:1px solid var(--bd1);border-radius:var(--r3);padding:20px;margin:16px 0;}
.preset-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin:12px 0;}
.preset-card{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:12px;cursor:pointer;transition:all .15s;text-align:center;}
.preset-card:hover{border-color:var(--gold);transform:translateY(-1px);}
.preset-icon{font-size:20px;display:block;margin-bottom:5px;}
.preset-name{font-family:var(--fd);font-size:11px;font-weight:700;color:var(--t1);}
.preset-desc{font-size:10px;color:var(--t3);margin-top:2px;}
/* CODE */
.code-wrap{position:relative;background:#020408;border:1px solid var(--bd0);border-radius:var(--r2);margin:8px 0;overflow:hidden;}
.code-hdr{display:flex;align-items:center;justify-content:space-between;padding:8px 16px;background:var(--base);border-bottom:1px solid var(--bd0);}
.code-lang{font-family:var(--fm);font-size:9px;letter-spacing:.15em;color:var(--t3);text-transform:uppercase;}
.code-body{padding:20px;font-family:var(--fm);font-size:12.5px;line-height:1.7;color:#cdd6f4;overflow-x:auto;white-space:pre;}
.kw{color:#cba6f7;}.st{color:#a6e3a1;}.cm{color:#585b70;font-style:italic;}.nm{color:#fab387;}
/* MISC */
[data-testid="stFileUploader"]{background:var(--raised)!important;border:1.5px dashed var(--bd2)!important;border-radius:var(--r3)!important;padding:16px!important;}
[data-testid="stFileUploader"]:hover{border-color:var(--gold)!important;}
[data-testid="stDataFrame"]{border-radius:var(--r2);overflow:hidden;}
.stSelectbox>div>div{background:var(--raised)!important;border-color:var(--bd1)!important;color:var(--t1)!important;}
[data-testid="stAlert"]{background:var(--raised)!important;border-radius:var(--r2)!important;border-left-width:3px!important;}
.streamlit-expanderHeader{background:var(--raised)!important;border:1px solid var(--bd1)!important;border-radius:var(--r2)!important;color:var(--t2)!important;font-family:var(--fm)!important;font-size:10px!important;}
.streamlit-expanderContent{background:var(--surface)!important;border:1px solid var(--bd1)!important;border-top:none!important;}
.div{display:flex;align-items:center;gap:12px;margin:28px 0;color:var(--t3);font-family:var(--fm);font-size:9px;letter-spacing:.2em;text-transform:uppercase;}
.div::before,.div::after{content:'';flex:1;height:1px;background:var(--bd0);}
/* ONBOARDING */
.ob-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin:22px 0;}
.ob-card{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r3);padding:24px 20px;text-align:center;transition:border-color .2s;}
.ob-card:hover{border-color:var(--bd2);}
.ob-num{font-family:var(--fm);font-size:46px;font-weight:500;color:var(--bd2);line-height:1;margin-bottom:8px;}
.ob-title{font-family:var(--fd);font-size:15px;font-weight:700;color:var(--t1);margin-bottom:6px;}
.ob-desc{font-size:12px;color:var(--t3);line-height:1.5;}
/* STEP TRACKER */
.step-track{display:flex;margin:16px 0;background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);overflow:hidden;}
.step-item{flex:1;padding:12px 8px;text-align:center;font-family:var(--fm);font-size:9px;letter-spacing:.08em;color:var(--t3);border-right:1px solid var(--bd0);transition:all .3s;}
.step-item:last-child{border-right:none;}
.step-item.done{color:var(--emerald);background:rgba(52,211,153,.06);}
.step-item.active{color:var(--gold);background:var(--gd);}
.step-dot{font-size:13px;display:block;margin-bottom:2px;}
/* COL PROFILE */
.cp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px;margin:12px 0;}
.cp-card{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:12px 14px;}
.cp-name{font-family:var(--fm);font-size:10px;color:var(--gold);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cp-type{font-size:9px;color:var(--t3);font-family:var(--fm);margin-top:2px;}
.cp-bar-w{height:3px;background:var(--bd0);border-radius:2px;margin-top:8px;overflow:hidden;}
.cp-bar{height:100%;border-radius:2px;background:linear-gradient(90deg,var(--gold),var(--amber));}
/* DNA */
.dna-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px;margin:14px 0;}
.dna-card{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:14px;}
.dna-col{font-family:var(--fm);font-size:11px;color:var(--gold);margin-bottom:8px;}
.dna-row{display:flex;justify-content:space-between;font-size:11px;padding:3px 0;border-bottom:1px solid var(--bd0);}
.dna-row:last-child{border-bottom:none;}
.dna-k{color:var(--t3);}.dna-v{color:var(--t1);font-family:var(--fm);}
/* EDIT */
.edit-wrap{margin:8px 0 12px;padding:14px 16px;background:var(--overlay);border:1px solid var(--violet);border-radius:var(--r2);}
.edit-lbl{font-family:var(--fm);font-size:9px;color:var(--violet);letter-spacing:.15em;text-transform:uppercase;margin-bottom:10px;}
/* COMPARE */
.compare-panel{background:var(--surface);border:1px solid var(--bd1);border-radius:var(--r3);padding:18px;}
.compare-lbl{font-family:var(--fm);font-size:9px;letter-spacing:.15em;text-transform:uppercase;padding:5px 10px;border-radius:5px;display:inline-block;margin-bottom:12px;}
.cmp-a{background:rgba(240,192,64,.1);color:var(--gold);border:1px solid rgba(240,192,64,.3);}
.cmp-b{background:rgba(34,211,238,.1);color:var(--cyan);border:1px solid rgba(34,211,238,.3);}
/* TIMELINE */
.timeline{position:relative;padding-left:30px;margin:16px 0;}
.timeline::before{content:'';position:absolute;left:9px;top:0;bottom:0;width:1px;background:linear-gradient(180deg,var(--gold),var(--violet),var(--cyan));}
.tl-item{position:relative;margin-bottom:22px;}
.tl-dot{position:absolute;left:-26px;top:4px;width:10px;height:10px;border-radius:50%;border:2px solid var(--void);}
.tl-time{font-family:var(--fm);font-size:9px;color:var(--t3);letter-spacing:.1em;margin-bottom:4px;}
.tl-q{font-size:13px;font-weight:600;color:var(--t1);}
.tl-a{font-size:12px;color:var(--t2);margin-top:4px;line-height:1.5;}
.no-chart{padding:40px;text-align:center;color:var(--t3);font-family:var(--fm);font-size:11px;background:var(--raised);border:1px dashed var(--bd1);border-radius:var(--r2);margin:8px 0;}

/* POWER BI DASHBOARD */
.pbi-wrap{background:var(--base);border:1px solid var(--bd1);border-radius:var(--r3);padding:0;overflow:hidden;margin-bottom:28px;}
.pbi-header{background:linear-gradient(135deg,#0f172a,#1e1b4b);padding:20px 28px 16px;border-bottom:1px solid var(--bd1);display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:12px;}
.pbi-title{font-family:var(--fd);font-size:20px;font-weight:800;color:var(--t1);}
.pbi-subtitle{font-family:var(--fm);font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:var(--t3);margin-top:3px;}
.pbi-stamp{font-family:var(--fm);font-size:9px;color:var(--t3);}
.pbi-kpi-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:1px;background:var(--bd0);border-bottom:1px solid var(--bd0);}
.pbi-kpi{background:var(--surface);padding:16px 20px;position:relative;overflow:hidden;}
.pbi-kpi::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;}
.pbi-kpi-icon{font-size:18px;margin-bottom:6px;display:block;}
.pbi-kpi-val{font-family:var(--fm);font-size:22px;font-weight:500;color:var(--t1);display:block;line-height:1.1;}
.pbi-kpi-lbl{font-size:10px;color:var(--t3);text-transform:uppercase;letter-spacing:.07em;font-family:var(--fm);margin-top:4px;display:block;}
.pbi-kpi-avg{font-family:var(--fm);font-size:9px;color:var(--t3);margin-top:2px;}
.pbi-kpi-delta{font-family:var(--fm);font-size:10px;margin-top:3px;display:flex;align-items:center;gap:3px;}
.pbi-kpi-delta.up{color:var(--emerald);}.pbi-kpi-delta.dn{color:var(--rose);}
.pbi-chart-grid{padding:20px;display:grid;gap:16px;}
.pbi-chart-tile{background:var(--raised);border:1px solid var(--bd1);border-radius:var(--r2);padding:0;overflow:hidden;}
.pbi-chart-label{font-family:var(--fm);font-size:9px;letter-spacing:.15em;text-transform:uppercase;color:var(--t3);padding:10px 14px 0;}
.pbi-footer{background:var(--base);border-top:1px solid var(--bd0);padding:10px 28px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;}
.pbi-footer-text{font-family:var(--fm);font-size:9px;color:var(--t3);}
.pbi-divider{height:1px;background:var(--bd0);margin:0 20px;}</style>"""
st.markdown(CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────
_D = {
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
    "query_counter":0,
    "story_show_raw":False,
    "comp_preset_fig":None,
    "comp_preset_name":"",
    "comp_preset_desc":"",
    "comp_preset_query":"",
}
for k,v in _D.items():
    if k not in st.session_state: st.session_state[k]=v

# ─────────────────────────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────────────────────────
PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono,monospace", color="#f1f5f9", size=11),
    colorway=["#f0c040","#a78bfa","#22d3ee","#34d399","#fb7185","#fbbf24","#818cf8","#38bdf8","#f472b6","#4ade80"],
    xaxis=dict(gridcolor="#1a2035", zeroline=False),
    yaxis=dict(gridcolor="#1a2035", zeroline=False),
    margin=dict(l=16,r=16,t=48,b=16),
    legend=dict(bgcolor="rgba(0,0,0,0.35)", bordercolor="#232b40", borderwidth=1),
    title_font=dict(family="Syne,sans-serif", size=14, color="#f0c040"),
)
PROVIDERS = {
    "Groq (Free)":{"label":"Groq","model":"llama-3.3-70b-versatile",
        "url":"https://api.groq.com/openai/v1/chat/completions",
        "key_hint":"gsk_…","key_url":"https://console.groq.com","style":"openai","free":True,"badge":"#34d399"},
    "Gemini (Free)":{"label":"Gemini","model":"gemini-2.0-flash",
        "url":"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        "key_hint":"AIza…","key_url":"https://aistudio.google.com","style":"gemini","free":True,"badge":"#a78bfa"},
    "Anthropic Claude":{"label":"Claude","model":"claude-sonnet-4-5",
        "url":"https://api.anthropic.com/v1/messages",
        "key_hint":"sk-ant-…","key_url":"https://console.anthropic.com","style":"anthropic","free":False,"badge":"#f0c040"},
}

# Industry chart presets for Chart Composer
INDUSTRY_PRESETS = {
    "Sales Performance": {
        "icon":"💰", "desc":"Revenue, units, growth",
        "chart":"bar", "x_pref":["region","product","sales_rep","category"],
        "y_pref":["revenue","sales","amount","total"], "color_pref":["product","category","region"],
    },
    "Trend Analysis": {
        "icon":"📈", "desc":"Time series, forecasts",
        "chart":"line", "x_pref":["date","month","quarter","period","week"],
        "y_pref":["revenue","sales","count","value"], "color_pref":["product","category","region"],
    },
    "Distribution": {
        "icon":"🔔", "desc":"Spread, outliers, shape",
        "chart":"violin", "x_pref":["category","region","department","segment"],
        "y_pref":["revenue","salary","score","value"], "color_pref":["category","department"],
    },
    "Part-of-Whole": {
        "icon":"🍕", "desc":"Shares, proportions",
        "chart":"donut", "x_pref":["region","product","category","channel"],
        "y_pref":["revenue","count","amount","sales"], "color_pref":None,
    },
    "Correlation": {
        "icon":"🔗", "desc":"Relationships between metrics",
        "chart":"scatter", "x_pref":["marketing_spend","cost","cac","spend"],
        "y_pref":["revenue","profit","sales","roas"], "color_pref":["region","category"],
    },
    "Marketing ROI": {
        "icon":"📣", "desc":"Channel, spend, attribution",
        "chart":"bar", "x_pref":["channel","campaign","medium","source"],
        "y_pref":["roas","revenue_attr","conversions","ctr_pct"], "color_pref":["channel"],
    },
    "HR Analytics": {
        "icon":"👥", "desc":"Headcount, tenure, performance",
        "chart":"box", "x_pref":["department","level","role","team"],
        "y_pref":["salary","tenure","score","rating"], "color_pref":["department","level"],
    },
    "Operations": {
        "icon":"⚙", "desc":"Efficiency, throughput, quality",
        "chart":"heatmap", "x_pref":None, "y_pref":None, "color_pref":None,
    },
    "Funnel / Pipeline": {
        "icon":"🎯", "desc":"Conversion stages",
        "chart":"funnel", "x_pref":["stage","status","step"],
        "y_pref":["count","amount","revenue"], "color_pref":None,
    },
    "Geographic": {
        "icon":"🌍", "desc":"Region, country, market",
        "chart":"horizontal bar", "x_pref":["region","country","market","territory"],
        "y_pref":["revenue","sales","profit","count"], "color_pref":["region"],
    },
}

# ─────────────────────────────────────────────────────────────────────
#  UTILITIES
# ─────────────────────────────────────────────────────────────────────
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

def smart_numeric_cols(df):
    """Return truly numeric cols, skip datetime-stored-as-int and date-named cols."""
    out=[]
    for c in df.columns:
        if not pd.api.types.is_numeric_dtype(df[c]): continue
        if pd.api.types.is_datetime64_any_dtype(df[c]): continue
        if any(k in c.lower() for k in ["year","date","time","period","month","week"]): continue
        out.append(c)
    return out

def smart_cat_cols(df):
    out=[]
    for c in df.columns:
        if df[c].dtype==object or pd.api.types.is_categorical_dtype(df[c]):
            out.append(c)
        elif df[c].dtype in ("int32","int64") and df[c].nunique()<=20:
            out.append(c)
    return out

def _safe_col(df,col):
    return col if col and isinstance(col,str) and col in df.columns else None

def _best_x(df, pref=None):
    if pref and pref in df.columns: return pref
    cats=smart_cat_cols(df)
    if cats: return cats[0]
    for c in df.columns:
        if df[c].dtype==object: return c
    return df.columns[0] if len(df.columns) else None

def _best_y(df, pref=None):
    if pref and pref in df.columns and pd.api.types.is_numeric_dtype(df[pref]): return pref
    nums=smart_numeric_cols(df)
    if nums: return nums[0]
    nums2=[c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    return nums2[0] if nums2 else None

def _pick_col(df, preferences):
    """Pick first matching column from a preference list."""
    if not preferences: return None
    cols_lower={c.lower():c for c in df.columns}
    for p in preferences:
        if p.lower() in cols_lower: return cols_lower[p.lower()]
        for c in df.columns:
            if p.lower() in c.lower(): return c
    return None

def col_profile(df):
    p={}
    for col in df.columns:
        s=df[col]; nulls=int(s.isna().sum()); null_pct=round(nulls/max(len(s),1)*100,1)
        info={"dtype":str(s.dtype),"nulls":nulls,"null_pct":null_pct,"unique":int(s.nunique())}
        if pd.api.types.is_numeric_dtype(s):
            try: info.update({"min":float(s.min()),"max":float(s.max()),"mean":float(s.mean()),
                              "std":float(s.std()),"completeness":round(100-null_pct,1)})
            except: pass
        else:
            info["top_values"]={str(k):int(v) for k,v in s.value_counts().head(3).items()}
        p[col]=info
    return p

def df_schema_str(df, name):
    lines=[f"TABLE `{name}` — {len(df):,} rows x {len(df.columns)} columns"]
    for col in df.columns:
        s=df[col]; dtype=str(s.dtype)
        if pd.api.types.is_numeric_dtype(s):
            try: extra=f"min={float(s.min()):.3g} max={float(s.max()):.3g} mean={float(s.mean()):.3g}"
            except: extra="numeric"
        elif pd.api.types.is_datetime64_any_dtype(s):
            extra=f"date range: {s.min()} to {s.max()}"
        else:
            extra=f"top:{list(s.value_counts().head(2).index)}"
        sample=[str(v)[:25] for v in s.dropna().head(3)]
        lines.append(f"  {col}[{dtype}] unique={s.nunique()} | {extra} | sample={sample}")
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
                   "INNER","ON","AS","AND","OR","NOT","LIMIT","COUNT","SUM","AVG","MIN","MAX","DISTINCT","BY","DESC","ASC"]:
            esc=re.sub(rf'\b({kw})\b',r'<span class="kw">\1</span>',esc,flags=re.I)
    return f'<div class="code-wrap"><div class="code-hdr"><span class="code-lang">{lang}</span></div><div class="code-body">{esc}</div></div>'

def generate_auto_kpis(df):
    kpis=[]; colors=["c-gold","c-cyan","c-violet","c-emerald","c-rose","c-sky"]
    for i,col in enumerate(smart_numeric_cols(df)[:6]):
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

# ─────────────────────────────────────────────────────────────────────
#  CHART CONSTANTS  — must be defined before make_chart
# ─────────────────────────────────────────────────────────────────────
NEEDS_NUMERIC_Y = {
    "bar","grouped_bar","stacked_bar","horizontal_bar","line","multi_line",
    "area","stacked_area","scatter","bubble","box","violin","strip",
    "funnel","waterfall","gauge","density_heatmap"
}

# 20-color high-contrast palette for distinct series
COLORS = [
    "#f0c040","#22d3ee","#a78bfa","#34d399","#fb7185","#fbbf24",
    "#38bdf8","#f472b6","#4ade80","#818cf8","#fdba74","#67e8f9",
    "#c084fc","#86efac","#fca5a5","#fde68a","#7dd3fc","#f9a8d4",
    "#6ee7b7","#a5b4fc"
]

# Dashboard palette (slightly different order for variety)
DASH_COLORS = [
    "#f0c040","#22d3ee","#a78bfa","#34d399","#fb7185",
    "#fbbf24","#38bdf8","#f472b6","#4ade80","#818cf8",
    "#fdba74","#67e8f9","#c084fc","#86efac","#fca5a5"
]

# ─────────────────────────────────────────────────────────────────────
#  CHART FACTORY  — 25+ types, smart column validation, rich colors
# ─────────────────────────────────────────────────────────────────────
def make_chart(df, chart_type, cfg):
    if df is None or df.empty: return None
    if not chart_type or chart_type.lower().strip() in ("none",""): return None
    ct=chart_type.lower().strip().replace(" ","_").replace("-","_")
    x=_safe_col(df,cfg.get("x")); y=_safe_col(df,cfg.get("y"))
    color=_safe_col(df,cfg.get("color")); size=_safe_col(df,cfg.get("size"))
    title=cfg.get("title","")
    if ct in NEEDS_NUMERIC_Y:
        if y is None or not pd.api.types.is_numeric_dtype(df[y]): y=_best_y(df,y)
        if x is None: x=_best_x(df,x)

    try:
        kw=dict(title=title); fig=None

        def color_map(df_col):
            """Generate discrete color map for a categorical column."""
            if df_col is None or df_col not in df.columns: return {}
            vals=df[df_col].dropna().unique().tolist()
            return {v:COLORS[i%len(COLORS)] for i,v in enumerate(vals)}

        cmap = color_map(color) if color else None

        if ct=="bar":
            if color:
                fig=px.bar(df,x=x,y=y,color=color,barmode="group",
                           color_discrete_map=cmap,**kw)
            else:
                # Color each bar differently
                fig=px.bar(df,x=x,y=y,color=x,
                           color_discrete_sequence=COLORS,**kw)
            fig.update_traces(marker_line_width=0,opacity=.9)
        elif ct=="grouped_bar":
            fig=px.bar(df,x=x,y=y,color=color,barmode="group",
                       color_discrete_map=cmap,color_discrete_sequence=COLORS,**kw)
        elif ct=="stacked_bar":
            fig=px.bar(df,x=x,y=y,color=color,barmode="stack",
                       color_discrete_map=cmap,color_discrete_sequence=COLORS,**kw)
        elif ct=="horizontal_bar":
            if color:
                fig=px.bar(df,x=y,y=x,color=color,orientation="h",
                           color_discrete_map=cmap,color_discrete_sequence=COLORS,**kw)
            else:
                fig=px.bar(df,x=y,y=x,color=x,orientation="h",
                           color_discrete_sequence=COLORS,**kw)
        elif ct in ("line","multi_line"):
            fig=px.line(df,x=x,y=y,color=color,markers=True,
                        color_discrete_map=cmap,color_discrete_sequence=COLORS,**kw)
            fig.update_traces(line_width=2.5)
        elif ct=="area":
            fig=px.area(df,x=x,y=y,color=color,
                        color_discrete_map=cmap,color_discrete_sequence=COLORS,**kw)
        elif ct=="stacked_area":
            fig=px.area(df,x=x,y=y,color=color,
                        color_discrete_map=cmap,color_discrete_sequence=COLORS,**kw)
        elif ct=="scatter":
            fig=px.scatter(df,x=x,y=y,color=color,size=size,
                           color_discrete_map=cmap,color_discrete_sequence=COLORS,
                           color_continuous_scale="Viridis",
                           trendline="ols" if (not color and x and y) else None,**kw)
        elif ct=="bubble":
            fig=px.scatter(df,x=x,y=y,color=color,size=size or y,
                           color_discrete_sequence=COLORS,
                           color_continuous_scale="Plasma",**kw)
        elif ct=="pie":
            fig=px.pie(df,names=x,values=y,
                       color_discrete_sequence=COLORS,**kw)
            fig.update_traces(textposition="inside",textinfo="percent+label",
                              marker_line_width=2,marker_line_color="#05060a")
        elif ct=="donut":
            fig=px.pie(df,names=x,values=y,hole=.45,
                       color_discrete_sequence=COLORS,**kw)
            fig.update_traces(textposition="inside",textinfo="percent+label",
                              marker_line_width=2,marker_line_color="#05060a")
        elif ct=="sunburst":
            path=[c for c in [color,x] if c]
            fig=px.sunburst(df,path=path or [x],values=y,
                            color_discrete_sequence=COLORS,**kw)
        elif ct=="treemap":
            path=[c for c in [color,x] if c]
            fig=px.treemap(df,path=path or [x],values=y,
                           color_discrete_sequence=COLORS,**kw)
        elif ct=="histogram":
            fig=px.histogram(df,x=x or _best_x(df),color=color,
                             color_discrete_map=cmap,color_discrete_sequence=COLORS,
                             opacity=0.85,**kw)
            fig.update_traces(marker_line_width=0.5,marker_line_color="#131720")
        elif ct=="box":
            fig=px.box(df,x=x,y=y,color=color,
                       color_discrete_map=cmap,color_discrete_sequence=COLORS,**kw)
        elif ct=="violin":
            fig=px.violin(df,x=x,y=y,color=color,box=True,
                          color_discrete_map=cmap,color_discrete_sequence=COLORS,**kw)
        elif ct=="strip":
            fig=px.strip(df,x=x,y=y,color=color,
                         color_discrete_sequence=COLORS,**kw)
        elif ct in ("heatmap","correlation_matrix"):
            num=df[smart_numeric_cols(df)]
            if num.shape[1]<2: return None
            fig=px.imshow(num.corr().round(2),
                          color_continuous_scale=["#fb7185","#131720","#22d3ee"],
                          zmin=-1,zmax=1,text_auto=True,**kw)
        elif ct=="density_heatmap":
            fig=px.density_heatmap(df,x=x,y=y,
                                   color_continuous_scale="Viridis",**kw)
        elif ct=="waterfall":
            if x and y:
                fig=go.Figure(go.Waterfall(
                    measure=["relative"]*len(df),
                    x=df[x].astype(str).tolist(),y=df[y].tolist(),
                    connector={"line":{"color":"rgba(255,255,255,0.15)"}},
                    increasing={"marker":{"color":"#34d399"}},
                    decreasing={"marker":{"color":"#fb7185"}},
                    totals={"marker":{"color":"#f0c040"}}))
                fig.update_layout(title=title)
            else: return None
        elif ct=="funnel":
            fig=px.funnel(df,x=y,y=x,
                          color_discrete_sequence=COLORS,**kw)
        elif ct=="gauge":
            gy=y or _best_y(df)
            if gy:
                val=float(df[gy].mean()); mx=max(float(df[gy].max()),0.001)
                fig=go.Figure(go.Indicator(
                    mode="gauge+number+delta",value=val,
                    delta={"reference":mx*0.6},
                    gauge={"axis":{"range":[0,mx]},"bar":{"color":"#f0c040"},
                           "steps":[{"range":[0,mx*.33],"color":"#fb7185"},
                                    {"range":[mx*.33,mx*.66],"color":"#fbbf24"},
                                    {"range":[mx*.66,mx],"color":"#34d399"}],
                           "threshold":{"line":{"color":"#fb7185","width":3},
                                        "thickness":.75,"value":mx*.9}},
                    title={"text":title or gy,"font":{"color":"#f0c040","size":13}}))
            else: return None
        elif ct=="radar":
            num_c=smart_numeric_cols(df)[:8]
            if len(num_c)<3: return None
            means=[float(df[c].mean()) for c in num_c]
            fig=go.Figure(go.Scatterpolar(
                r=means+[means[0]],theta=num_c+[num_c[0]],
                fill="toself",line_color="#f0c040",
                fillcolor="rgba(240,192,64,.2)",name=title))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True,gridcolor="#232b40"),
                           angularaxis=dict(gridcolor="#232b40")),title=title)
        elif ct=="parallel_coordinates":
            num_c=smart_numeric_cols(df)
            if len(num_c)<2: return None
            fig=px.parallel_coordinates(df,dimensions=num_c,color=num_c[0],
                color_continuous_scale=["#f0c040","#22d3ee","#a78bfa"],**kw)
        elif ct in ("candlestick","ohlc"):
            ohcl={c.lower():c for c in df.columns}
            if not all(k in ohcl for k in ["open","high","low","close"]): return None
            xcol=x or (df.columns[0] if df.columns[0].lower() not in ["open","high","low","close"] else None)
            if ct=="candlestick":
                fig=go.Figure(go.Candlestick(
                    x=df[xcol].tolist() if xcol else list(range(len(df))),
                    open=df[ohcl["open"]],high=df[ohcl["high"]],
                    low=df[ohcl["low"]],close=df[ohcl["close"]],
                    increasing_line_color="#34d399",decreasing_line_color="#fb7185"))
            else:
                fig=go.Figure(go.Ohlc(
                    x=df[xcol].tolist() if xcol else list(range(len(df))),
                    open=df[ohcl["open"]],high=df[ohcl["high"]],
                    low=df[ohcl["low"]],close=df[ohcl["close"]]))
            fig.update_layout(title=title)
        else:
            if x and y:
                fig=px.bar(df,x=x,y=y,color=x,
                           color_discrete_sequence=COLORS,title=f"{title} (auto-bar)")
            else: return None

        if fig is None: return None
        fig.update_layout(**PLOTLY_THEME,title_x=0.,
                          hoverlabel=dict(bgcolor="#131720",font_size=11,font_family="JetBrains Mono"))
        NO_AXES={"pie","donut","treemap","sunburst","heatmap","correlation_matrix",
                 "density_heatmap","radar","gauge","parallel_coordinates","candlestick","ohlc"}
        if ct not in NO_AXES:
            fig.update_xaxes(showgrid=True,gridwidth=1,gridcolor="#1a2035",showline=False,tickfont_size=10)
            fig.update_yaxes(showgrid=True,gridwidth=1,gridcolor="#1a2035",showline=False,tickfont_size=10)
        return fig
    except Exception:
        try:
            nx=_best_x(df); ny=_best_y(df)
            if nx and ny:
                fb=px.bar(df.head(30),x=nx,y=ny,color=nx,
                          color_discrete_sequence=COLORS,title=f"{title} (fallback)")
                fb.update_layout(**PLOTLY_THEME,title_x=0.)
                return fb
        except Exception: pass
        return None


# ─────────────────────────────────────────────────────────────────────
#  POWER BI STYLE DASHBOARD
# ─────────────────────────────────────────────────────────────────────

def make_powerbi_dashboard(df, dataset_name):
    nc  = smart_numeric_cols(df)
    cc  = smart_cat_cols(df)
    dc  = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]

    kpi_icons = ["💰","📈","🎯","⚡","🔥","💡"]
    kpi_tiles = []
    for i, col in enumerate(nc[:6]):
        s = df[col].dropna()
        half = len(s)//2
        delta_pct = None
        if half > 0 and s.iloc[:half].mean() != 0:
            delta_pct = round((s.iloc[half:].mean()-s.iloc[:half].mean())/abs(s.iloc[:half].mean())*100,1)
        kpi_tiles.append({
            "label": col.replace("_"," ").title(), "value": fmt(s.sum()), "avg": fmt(s.mean()),
            "delta": f"{'+' if (delta_pct or 0)>=0 else ''}{delta_pct}%" if delta_pct is not None else None,
            "color": DASH_COLORS[i%len(DASH_COLORS)], "icon": kpi_icons[i%len(kpi_icons)],
        })

    charts = []
    def _add(label, fn):
        """Try to build a chart; add it only if it succeeds."""
        try:
            f = fn()
            if f is not None:
                charts.append((label, f))
        except Exception:
            pass

    # 1 ── Colored vertical bar (top categories)
    if cc and nc:
        cat, num = cc[0], nc[0]
        def _c1():
            g = df.groupby(cat)[num].sum().reset_index().sort_values(num, ascending=False).head(10)
            fig = px.bar(g, x=cat, y=num, color=cat,
                         color_discrete_sequence=DASH_COLORS,
                         title=f"Top {cat.replace('_',' ').title()} by {num.replace('_',' ').title()}",
                         text_auto=".2s")
            fig.update_traces(marker_line_width=0, opacity=.92,
                              textfont_size=10, textposition="outside", cliponaxis=False)
            fig.update_layout(**PLOTLY_THEME, title_x=0., showlegend=False)
            fig.update_xaxes(showgrid=False, tickfont_size=10)
            fig.update_yaxes(showgrid=True, gridcolor="#1a2035", tickfont_size=10)
            return fig
        _add("Top Performers", _c1)

    # 2 ── Dual-axis trend line
    if dc and nc:
        def _c2():
            td = df.copy()
            td["_p"] = pd.to_datetime(td[dc[0]]).dt.to_period("M").astype(str)
            td2 = td.groupby("_p")[nc[0]].agg(["sum","mean"]).reset_index()
            td2.columns = ["Period","Total","Average"]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=td2["Period"], y=td2["Total"], name="Total",
                line=dict(color="#f0c040", width=3), fill="tozeroy",
                fillcolor="rgba(240,192,64,.07)", mode="lines+markers",
                marker=dict(size=6, color="#f0c040")))
            fig.add_trace(go.Scatter(x=td2["Period"], y=td2["Average"], name="Monthly Avg",
                line=dict(color="#22d3ee", width=2, dash="dot"), mode="lines"))
            fig.update_layout(**PLOTLY_THEME,
                title=f"{nc[0].replace('_',' ').title()} — Trend & Average",
                title_x=0., legend=dict(orientation="h", y=1.12, x=0))
            fig.update_xaxes(showgrid=False, tickfont_size=9, tickangle=-35)
            fig.update_yaxes(showgrid=True, gridcolor="#1a2035", tickfont_size=10)
            return fig
        _add("Trend Over Time", _c2)

    # 3 ── Donut with center annotation
    if cc and nc:
        def _c3():
            g2 = df.groupby(cc[0])[nc[0]].sum().reset_index()
            total = g2[nc[0]].sum()
            fig = px.pie(g2, names=cc[0], values=nc[0], hole=.52,
                         color_discrete_sequence=DASH_COLORS,
                         title=f"Share of {nc[0].replace('_',' ').title()}")
            fig.update_traces(textposition="outside", textinfo="percent+label",
                              marker_line_width=3, marker_line_color="#05060a",
                              pull=[0.04]*len(g2))
            fig.update_layout(**PLOTLY_THEME, title_x=0., showlegend=False,
                annotations=[dict(text=f"<b>{fmt(total)}</b><br>Total", x=0.5, y=0.5,
                                  font_size=13, font_color="#f0c040", showarrow=False)])
            return fig
        _add("Market Share", _c3)

    # 4 ── Scatter correlation
    if len(nc) >= 2:
        def _c4():
            sample = df.sample(min(300, len(df)), random_state=42)
            col_arg = cc[0] if cc else None
            fig = px.scatter(sample, x=nc[0], y=nc[1], color=col_arg,
                             color_discrete_sequence=DASH_COLORS,
                             trendline="ols" if not col_arg else None,
                             opacity=0.72,
                             title=f"{nc[0].replace('_',' ').title()} vs {nc[1].replace('_',' ').title()}")
            fig.update_traces(marker=dict(size=7, line_width=0))
            fig.update_layout(**PLOTLY_THEME, title_x=0.)
            return fig
        _add("Correlation Scatter", _c4)

    # 5 ── Correlation heatmap
    if len(nc) >= 3:
        def _c5():
            corr = df[nc[:10]].corr().round(2)
            fig = px.imshow(corr, color_continuous_scale=["#fb7185","#0e1117","#22d3ee"],
                            zmin=-1, zmax=1, text_auto=True, title="Metric Correlation Matrix")
            fig.update_layout(**PLOTLY_THEME, title_x=0.)
            return fig
        _add("Correlation Matrix", _c5)

    # 6 ── Box distribution
    if cc and nc:
        def _c6():
            fig = px.box(df, x=cc[0], y=nc[0], color=cc[0],
                         color_discrete_sequence=DASH_COLORS, notched=True,
                         title=f"Distribution — {nc[0].replace('_',' ').title()} by {cc[0].replace('_',' ').title()}")
            fig.update_traces(marker_size=3, line_width=1.5)
            fig.update_layout(**PLOTLY_THEME, title_x=0., showlegend=False)
            return fig
        _add("Distribution (Box)", _c6)

    # 7 ── Stacked bar (2 categories)
    if len(cc) >= 2 and nc:
        def _c7():
            g3 = df.groupby([cc[0], cc[1]])[nc[0]].sum().reset_index()
            fig = px.bar(g3, x=cc[0], y=nc[0], color=cc[1], barmode="stack",
                         color_discrete_sequence=DASH_COLORS,
                         title=f"{nc[0].replace('_',' ').title()} by {cc[0].replace('_',' ').title()} & {cc[1].replace('_',' ').title()}")
            fig.update_traces(marker_line_width=0)
            fig.update_layout(**PLOTLY_THEME, title_x=0., legend=dict(orientation="h", y=1.12))
            return fig
        _add("Stacked Breakdown", _c7)

    # 8 ── Horizontal ranked bar
    if cc and nc:
        def _c8():
            g4 = df.groupby(cc[0])[nc[0]].sum().reset_index().sort_values(nc[0], ascending=True).tail(10)
            fig = px.bar(g4, x=nc[0], y=cc[0], orientation="h", color=nc[0],
                         color_continuous_scale=["#1a2035","#f0c040"],
                         title=f"Rankings — {nc[0].replace('_',' ').title()}", text_auto=".2s")
            fig.update_traces(marker_line_width=0, textfont_size=10)
            fig.update_layout(**PLOTLY_THEME, title_x=0., showlegend=False, coloraxis_showscale=False)
            return fig
        _add("Rankings", _c8)

    # 9 ── Grouped multi-metric bar
    if len(nc) >= 2 and cc:
        def _c9():
            g5 = df.groupby(cc[0])[nc[:3]].sum().reset_index()
            gm = g5.melt(id_vars=cc[0], var_name="Metric", value_name="Value")
            fig = px.bar(gm, x=cc[0], y="Value", color="Metric", barmode="group",
                         color_discrete_sequence=DASH_COLORS,
                         title=f"Multi-Metric Comparison by {cc[0].replace('_',' ').title()}")
            fig.update_traces(marker_line_width=0, opacity=.88)
            fig.update_layout(**PLOTLY_THEME, title_x=0., legend=dict(orientation="h", y=1.12))
            return fig
        _add("Multi-Metric", _c9)

    # 10 ── Area trend (by category over time)
    if dc and nc:
        def _c10():
            td = df.copy()
            td["_p"] = pd.to_datetime(td[dc[0]]).dt.to_period("M").astype(str)
            if cc:
                td3 = td.groupby(["_p", cc[0]])[nc[0]].sum().reset_index()
                fig = px.area(td3, x="_p", y=nc[0], color=cc[0],
                              color_discrete_sequence=DASH_COLORS,
                              title=f"Cumulative {nc[0].replace('_',' ').title()} by {cc[0].replace('_',' ').title()}")
            else:
                td3 = td.groupby("_p")[nc[0]].sum().reset_index()
                fig = px.area(td3, x="_p", y=nc[0],
                              color_discrete_sequence=DASH_COLORS,
                              title=f"Cumulative {nc[0].replace('_',' ').title()}")
            fig.update_layout(**PLOTLY_THEME, title_x=0., legend=dict(orientation="h", y=1.12))
            fig.update_xaxes(showgrid=False, tickfont_size=9, tickangle=-35)
            fig.update_yaxes(showgrid=True, gridcolor="#1a2035", tickfont_size=10)
            return fig
        _add("Area Trend", _c10)

    # 11 ── Violin distribution
    if cc and nc:
        def _c11():
            fig = px.violin(df, x=cc[0], y=nc[0], color=cc[0], box=True,
                            color_discrete_sequence=DASH_COLORS,
                            title=f"Shape of {nc[0].replace('_',' ').title()} by {cc[0].replace('_',' ').title()}")
            fig.update_layout(**PLOTLY_THEME, title_x=0., showlegend=False)
            return fig
        _add("Violin Distribution", _c11)

    # 12 ── Treemap hierarchy
    if cc and nc:
        def _c12():
            path = [cc[0], cc[1]] if len(cc) >= 2 else [cc[0]]
            fig = px.treemap(df, path=path, values=nc[0], color=nc[0],
                             color_continuous_scale=["#1a2035","#f0c040","#fb7185"],
                             title=f"Treemap — {nc[0].replace('_',' ').title()} Hierarchy")
            fig.update_layout(**PLOTLY_THEME, title_x=0.)
            return fig
        _add("Treemap", _c12)

    # 13 ── Histogram with box marginal
    if nc:
        def _c13():
            fig = px.histogram(df, x=nc[0],
                               color=cc[0] if cc else None,
                               color_discrete_sequence=DASH_COLORS,
                               marginal="box", opacity=0.82, nbins=30,
                               title=f"Distribution — {nc[0].replace('_',' ').title()}")
            fig.update_traces(marker_line_width=0.5, marker_line_color="#131720")
            fig.update_layout(**PLOTLY_THEME, title_x=0.)
            return fig
        _add("Histogram", _c13)

    # 14 ── Bubble chart
    if len(nc) >= 3:
        def _c14():
            sample = df.sample(min(200, len(df)), random_state=42)
            fig = px.scatter(sample, x=nc[0], y=nc[1], size=nc[2],
                             color=cc[0] if cc else nc[2],
                             color_discrete_sequence=DASH_COLORS,
                             color_continuous_scale="Viridis",
                             opacity=0.75, size_max=40,
                             title=f"Bubble — {nc[0]} vs {nc[1]} (size: {nc[2]})")
            fig.update_layout(**PLOTLY_THEME, title_x=0.)
            return fig
        _add("Bubble Chart", _c14)

    return {"kpis": kpi_tiles, "charts": charts}



def make_insight_chart(df, insight_text, idx):
    """Small supporting chart per insight."""
    if df is None or df.empty: return None
    nc=smart_numeric_cols(df); cc=smart_cat_cols(df)
    try:
        if cc and nc:
            g=df.groupby(cc[0])[nc[0]].mean().reset_index().sort_values(nc[0],ascending=False).head(8)
            fig=px.bar(g,x=cc[0],y=nc[0],color=cc[0],
                       color_discrete_sequence=DASH_COLORS,
                       title=f"Supporting: {nc[0]} by {cc[0]}")
            fig.update_layout(**PLOTLY_THEME,title_x=0.,height=250,margin=dict(l=8,r=8,t=40,b=8),showlegend=False)
            fig.update_traces(marker_line_width=0,opacity=.88)
            fig.update_xaxes(showgrid=False,tickfont_size=9)
            fig.update_yaxes(showgrid=True,gridcolor="#1a2035",tickfont_size=9)
            return fig
        elif len(nc)>=2:
            fig=px.scatter(df.sample(min(100,len(df))),x=nc[0],y=nc[1],
                           color_discrete_sequence=DASH_COLORS,
                           title=f"{nc[0]} vs {nc[1]}")
            fig.update_layout(**PLOTLY_THEME,title_x=0.,height=250,margin=dict(l=8,r=8,t=40,b=8))
            return fig
    except Exception: pass
    return None

# ─────────────────────────────────────────────────────────────────────
#  PDF HELPERS
# ─────────────────────────────────────────────────────────────────────
def _st(t):
    """Sanitize text for ReportLab latin-1 fonts."""
    if not isinstance(t, str): t = str(t)
    t = (t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
          .replace("\u2019","'").replace("\u2018","'")
          .replace("\u201c",'"').replace("\u201d",'"')
          .replace("\u2014","--").replace("\u2013","-")
          .replace("\u2022","*").replace("\u25cf","*")
          .replace("\u2605","*").replace("\u25c6","*")
          .replace("\u2b21","o").replace("\u26a1","!")
          .replace("\u1f4b0","$").replace("\u1f4c8","^"))
    return t.encode("latin-1","replace").decode("latin-1")

def _check_rl():
    try: import reportlab; return True
    except ImportError: raise RuntimeError("Install reportlab: pip install reportlab")

def _check_kaleido():
    try: import kaleido; return True
    except ImportError: return False

def _rl_imports():
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors as rc
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    HRFlowable, KeepTogether, Table, TableStyle,
                                    PageBreak, Image as RLImage)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    return (A4, landscape, getSampleStyleSheet, ParagraphStyle, cm, rc,
            SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether,
            Table, TableStyle, PageBreak, RLImage, TA_CENTER, TA_LEFT, TA_RIGHT)

def _fig_to_image(fig, rl_image_cls, width_cm=14, height_cm=7, cm_unit=None):
    """Convert a Plotly figure to a ReportLab Image flowable."""
    if fig is None: return None
    try:
        import kaleido
        cm_ = cm_unit or 1
        img_bytes = fig.to_image(format="png", width=900, height=500, scale=2)
        img_io    = io.BytesIO(img_bytes)
        return rl_image_cls(img_io, width=width_cm*cm_, height=height_cm*cm_)
    except Exception:
        return None

def _common_styles(sty, rc, ParagraphStyle):
    """Return shared paragraph styles dict."""
    GOLD   = rc.HexColor("#996600");  VIOLET = rc.HexColor("#5b21b6")
    BLUE   = rc.HexColor("#1e40af");  GREEN  = rc.HexColor("#166534")
    RED    = rc.HexColor("#991b1b");  GRAY   = rc.HexColor("#374151")
    LTGRAY = rc.HexColor("#f3f4f6"); MDGRAY = rc.HexColor("#d1d5db")
    DKGRAY = rc.HexColor("#6b7280"); WHITE  = rc.white
    def S(n,**kw): return ParagraphStyle(n,parent=sty["Normal"],**kw)
    styles = dict(
        GOLD=GOLD, VIOLET=VIOLET, BLUE=BLUE, GREEN=GREEN, RED=RED,
        GRAY=GRAY, LTGRAY=LTGRAY, MDGRAY=MDGRAY, DKGRAY=DKGRAY, WHITE=WHITE,
        cover_s   = S("cov", fontSize=36, textColor=WHITE, fontName="Helvetica-Bold", leading=42),
        sub2_s    = S("sub2",fontSize=16, textColor=WHITE, fontName="Helvetica-Bold", leading=20),
        sub_s     = S("sub",  fontSize=11, textColor=DKGRAY, spaceAfter=6),
        h2_s      = S("h2",  fontSize=14, textColor=BLUE,  fontName="Helvetica-Bold", spaceAfter=6,  spaceBefore=18),
        h3_s      = S("h3",  fontSize=11, textColor=VIOLET,fontName="Helvetica-Bold", spaceAfter=4,  spaceBefore=10),
        h4_s      = S("h4",  fontSize=10, textColor=GRAY,  fontName="Helvetica-Bold", spaceAfter=3,  spaceBefore=6),
        body_s    = S("body",fontSize=10, textColor=GRAY,  leading=15, spaceAfter=5),
        bullet_s  = S("bul", fontSize=10, textColor=GRAY,  leading=14, spaceAfter=3, leftIndent=16, firstLineIndent=-10),
        anomaly_s = S("an",  fontSize=10, textColor=RED,   leading=14, spaceAfter=3, leftIndent=16, firstLineIndent=-10),
        mono_s    = S("mon", fontSize=8,  textColor=DKGRAY,fontName="Courier", leading=12, spaceAfter=2, leftIndent=10),
        story_s   = S("stry",fontSize=11, textColor=GRAY,  leading=18, spaceAfter=12),
        conf_hi   = S("chi", fontSize=9,  textColor=GREEN, fontName="Helvetica-Bold", spaceAfter=4),
        conf_med  = S("cme", fontSize=9,  textColor=rc.HexColor("#92400e"), fontName="Helvetica-Bold", spaceAfter=4),
        conf_low  = S("clo", fontSize=9,  textColor=RED,   fontName="Helvetica-Bold", spaceAfter=4),
        # Dashboard-specific
        ds_title_s= S("dst", fontSize=18, textColor=WHITE, fontName="Helvetica-Bold", leading=22),
        ds_sub_s  = S("dss", fontSize=10, textColor=rc.HexColor("#94a3b8"), leading=14),
        kpi_val_s = S("kpv", fontSize=22, textColor=GOLD,  fontName="Helvetica-Bold", leading=26),
        kpi_lbl_s = S("kpl", fontSize=9,  textColor=DKGRAY,fontName="Helvetica",      leading=12),
        chart_lbl_s=S("chl", fontSize=9,  textColor=DKGRAY,fontName="Helvetica-Bold", leading=12, spaceBefore=6),
        section_s = S("sec", fontSize=13, textColor=BLUE,  fontName="Helvetica-Bold", leading=16, spaceBefore=14, spaceAfter=6),
    )
    return styles

def _cover_page(elements, title, subtitle, meta_lines, st_obj, cm, HRFlowable,
                Table, TableStyle, Paragraph, Spacer, styles, HAS_KALEIDO):
    GOLD=styles["GOLD"]; VIOLET=styles["VIOLET"]; MDGRAY=styles["MDGRAY"]
    DKGRAY=styles["DKGRAY"]
    def P(t,s): return Paragraph(_st(str(t)),s)
    def HR(thick=0.8,clr=MDGRAY,sp=8): return HRFlowable(width="100%",thickness=thick,color=clr,spaceAfter=sp)

    elements.append(Spacer(1, 2.2*cm))
    for txt, styl, bg in [(title, styles["cover_s"], GOLD), (subtitle, styles["sub2_s"], VIOLET)]:
        tbl = Table([[P(txt, styl)]], colWidths=[16*cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),bg),
            ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
            ("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14),
        ]))
        elements.append(tbl)
        elements.append(Spacer(1, 0.25*cm))
    elements.append(Spacer(1, 0.8*cm))
    elements.append(HR(1.0, GOLD, 10))
    elements.append(Spacer(1, 0.3*cm))
    for line in meta_lines:
        elements.append(P(line, styles["sub_s"]))
    if not HAS_KALEIDO:
        elements.append(Spacer(1, 0.3*cm))
        note_p = Paragraph(_st(
            "Charts not embedded — install kaleido (pip install kaleido) to include chart images."),
            styles["sub_s"])
        elements.append(note_p)
    elements.append(Spacer(1, 0.5*cm))
    elements.append(HR(0.5, MDGRAY, 16))


# ── REPORT 1: Query Analysis PDF ─────────────────────────────────────
def make_pdf(history):
    _check_rl()
    (A4, landscape, getSampleStyleSheet, ParagraphStyle, cm, rc,
     SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether,
     Table, TableStyle, PageBreak, RLImage, TA_CENTER, TA_LEFT, TA_RIGHT) = _rl_imports()

    HAS_KALEIDO = _check_kaleido()
    sty   = getSampleStyleSheet()
    styles = _common_styles(sty, rc, ParagraphStyle)
    BLUE=styles["BLUE"]; VIOLET=styles["VIOLET"]; GRAY=styles["GRAY"]
    LTGRAY=styles["LTGRAY"]; MDGRAY=styles["MDGRAY"]; WHITE=styles["WHITE"]
    RED=styles["RED"]; GREEN=styles["GREEN"]

    def P(t, s): return Paragraph(_st(str(t)), s)
    def HR(thick=0.8, clr=MDGRAY, sp=8): return HRFlowable(width="100%", thickness=thick, color=clr, spaceAfter=sp)

    def kpi_table(kpis):
        if not kpis: return []
        data = [["Metric", "Value", "Change"]]
        for k in kpis:
            data.append([_st(k.get("label","")), _st(k.get("value","")), _st(k.get("delta","—") or "—")])
        t = Table(data, colWidths=[7*cm, 3.5*cm, 3.5*cm], repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),VIOLET),("TEXTCOLOR",(0,0),(-1,0),WHITE),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,0),9),
            ("ALIGN",(0,0),(-1,0),"CENTER"),
            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,1),(-1,-1),9),
            ("TEXTCOLOR",(0,1),(-1,-1),GRAY),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
            ("GRID",(0,0),(-1,-1),0.4,MDGRAY),("LINEBELOW",(0,0),(-1,0),1.2,VIOLET),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LTGRAY]),
        ]))
        return [Spacer(1,.15*cm), t, Spacer(1,.3*cm)]

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2.2*cm, bottomMargin=2.2*cm,
                            title="NLDA Pro Intelligence Report")
    elements = []
    meta = [
        f"Generated: {datetime.now().strftime('%A, %d %B %Y at %H:%M')}",
        f"Total analyses: {len(history)}",
        f"AI Provider: {history[-1].get('provider','—') if history else '—'}",
    ]
    _cover_page(elements, "NLDA Pro", "Query Analysis Report",
                meta, None, cm, HRFlowable, Table, TableStyle,
                Paragraph, Spacer, styles, HAS_KALEIDO)

    # Session overview table
    if history:
        total_kpis = sum(len(e.get("kpis",[])) for e in history)
        total_ins  = sum(len(e.get("insights",[])) for e in history)
        sd = [["Metric","Value"],
              ["Analyses", str(len(history))],
              ["KPIs extracted", str(total_kpis)],
              ["Insights generated", str(total_ins)],
              ["Charts generated", str(sum(1 for e in history if e.get("fig")))]]
        st_tbl = Table(sd, colWidths=[8*cm, 5*cm])
        st_tbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),BLUE),("TEXTCOLOR",(0,0),(-1,0),WHITE),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),10),
            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("TEXTCOLOR",(0,1),(-1,-1),GRAY),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LTGRAY]),
            ("GRID",(0,0),(-1,-1),0.4,MDGRAY),("LINEBELOW",(0,0),(-1,0),1,BLUE),
            ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
            ("LEFTPADDING",(0,0),(-1,-1),10),
        ]))
        elements.append(P("Session Overview", styles["h2_s"]))
        elements.append(st_tbl)
        elements.append(Spacer(1,.4*cm))

    elements.append(PageBreak())

    # Per-analysis sections
    for i, e in enumerate(history, 1):
        items = []
        items.append(P(f"Analysis {i}  —  {e.get('ts','')}", styles["h2_s"]))
        items.append(HR(0.5, rc.HexColor("#bfdbfe"), 4))

        q_tbl = Table([[P(f"Question: {e.get('question','')}", styles["h3_s"])]], colWidths=[14*cm])
        q_tbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),rc.HexColor("#eff6ff")),
            ("LEFTPADDING",(0,0),(-1,-1),12),("TOPPADDING",(0,0),(-1,-1),8),
            ("BOTTOMPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),12),
            ("BOX",(0,0),(-1,-1),1,rc.HexColor("#93c5fd")),
        ]))
        items.append(q_tbl); items.append(Spacer(1,.2*cm))

        items.append(P("Summary", styles["h3_s"]))
        items.append(P(e.get("summary","No summary."), styles["body_s"]))

        conf   = e.get("confidence","high").lower()
        conf_s = {"high":styles["conf_hi"],"medium":styles["conf_med"],"low":styles["conf_low"]}.get(conf, styles["conf_hi"])
        items.append(P(f"AI Confidence: {conf.upper()}", conf_s))

        if e.get("kpis"):
            items.append(P("Key Performance Indicators", styles["h3_s"]))
            items.extend(kpi_table(e["kpis"]))

        # Chart image
        if e.get("fig"):
            items.append(P("Chart Visualization", styles["h3_s"]))
            img = _fig_to_image(e["fig"], RLImage, 13, 6.5, cm)
            if img:
                items.append(img); items.append(Spacer(1,.2*cm))

        if e.get("query_story","").strip():
            items.append(P("Analysis Story (Plain English)", styles["h3_s"]))
            for para in e["query_story"].split("\n\n"):
                if para.strip(): items.append(P(para, styles["story_s"]))

        if e.get("insights"):
            items.append(P("Key Insights", styles["h3_s"]))
            for ins in e["insights"]:
                items.append(P(f"* {ins}", styles["bullet_s"]))

        if e.get("anomalies"):
            items.append(P("Anomalies Detected", styles["h3_s"]))
            for an in e["anomalies"]:
                items.append(P(f"[!] {an}", styles["anomaly_s"]))

        if e.get("sql_query","").strip():
            items.append(P("SQL Query", styles["h3_s"]))
            for line in e["sql_query"].split("\n"):
                items.append(P(line or " ", styles["mono_s"]))

        if e.get("reasoning","").strip():
            items.append(P("AI Reasoning", styles["h4_s"]))
            items.append(P(e["reasoning"], styles["body_s"]))

        items.append(Spacer(1,.3*cm))
        items.append(HR(0.8, MDGRAY, 10))
        elements.append(KeepTogether(items[:6]))
        for item in items[6:]: elements.append(item)

    doc.build(elements)
    return buf.getvalue()


# ── REPORT 2: Dashboard PDF ───────────────────────────────────────────
# NOTE: The full make_dashboard_pdf is defined later in the file.
# A forward-reference shim is not needed — Python resolves at call time.




# ─────────────────────────────────────────────────────────────────────
#  FULL DASHBOARD PDF EXPORT
# ─────────────────────────────────────────────────────────────────────
def make_dashboard_pdf(datasets_dict, dashboard_data_by_name, story_text="", history=None):
    """Complete PDF: cover + dataset stats + ALL dashboard charts + story + query analyses."""
    history = history or []
    try: import reportlab
    except ImportError: raise RuntimeError("Install reportlab: pip install reportlab")

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors as rc
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    HRFlowable, KeepTogether, Table, TableStyle,
                                    PageBreak, Image as RLImage)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    try: import kaleido; HAS_K=True
    except ImportError: HAS_K=False

    buf=io.BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,leftMargin=1.8*cm,rightMargin=1.8*cm,
                          topMargin=2*cm,bottomMargin=2*cm,
                          title="NLDA Pro Full Intelligence Report")
    sty=getSampleStyleSheet()

    GOLD=rc.HexColor("#996600"); VIOLET=rc.HexColor("#5b21b6"); BLUE=rc.HexColor("#1e40af")
    GREEN=rc.HexColor("#166534"); RED=rc.HexColor("#991b1b"); GRAY=rc.HexColor("#374151")
    LTGRAY=rc.HexColor("#f3f4f6"); MDGRAY=rc.HexColor("#d1d5db"); DKGRAY=rc.HexColor("#6b7280")
    WHITE=rc.white; TEAL=rc.HexColor("#0d9488"); AMBER=rc.HexColor("#b45309")

    def S(n,**kw): return ParagraphStyle(n,parent=sty["Normal"],**kw)
    def P(t,s):    return Paragraph(_st(str(t)),s)
    def HR(th=0.8,cl=MDGRAY,sp=8): return HRFlowable(width="100%",thickness=th,color=cl,spaceAfter=sp)

    h2_s  =S("h2", fontSize=14,textColor=BLUE,  fontName="Helvetica-Bold",spaceAfter=6, spaceBefore=16)
    h3_s  =S("h3", fontSize=11,textColor=VIOLET, fontName="Helvetica-Bold",spaceAfter=4, spaceBefore=10)
    h4_s  =S("h4", fontSize=10,textColor=TEAL,   fontName="Helvetica-Bold",spaceAfter=3, spaceBefore=6)
    sub_s =S("sub",fontSize=11,textColor=DKGRAY, spaceAfter=5)
    body_s=S("body",fontSize=10,textColor=GRAY,  leading=15,spaceAfter=4)
    bul_s =S("bul",fontSize=10,textColor=GRAY,   leading=14,spaceAfter=3,leftIndent=14,firstLineIndent=-8)
    anom_s=S("an", fontSize=10,textColor=RED,    leading=14,spaceAfter=3,leftIndent=14,firstLineIndent=-8)
    mono_s=S("mon",fontSize=8, textColor=DKGRAY, fontName="Courier",leading=12,spaceAfter=2,leftIndent=8)
    story_s=S("st",fontSize=11,textColor=GRAY,   leading=18,spaceAfter=12)
    note_s=S("nt", fontSize=9, textColor=DKGRAY, fontName="Helvetica-Oblique",spaceAfter=4)
    chap_s=S("cp", fontSize=10,textColor=VIOLET, fontName="Helvetica-Bold",spaceAfter=4,spaceBefore=10)
    conf_map={"high":S("ch",fontSize=9,textColor=GREEN,fontName="Helvetica-Bold",spaceAfter=3),
              "medium":S("cm",fontSize=9,textColor=AMBER,fontName="Helvetica-Bold",spaceAfter=3),
              "low":   S("cl",fontSize=9,textColor=RED,  fontName="Helvetica-Bold",spaceAfter=3)}

    def img_from_fig(fig,w=15*cm,h=7.5*cm):
        if not HAS_K or fig is None: return []
        try:
            img_bytes=fig.to_image(format="png",width=1100,height=550,scale=1.5)
            return [RLImage(io.BytesIO(img_bytes),width=w,height=h),Spacer(1,0.2*cm)]
        except Exception: return []

    def kpi_row(kpis):
        if not kpis: return []
        cols=min(3,len(kpis))
        all_rows=[]
        for row_kpis in [kpis[i:i+cols] for i in range(0,len(kpis),cols)]:
            row_cells=[]
            for k in row_kpis:
                cell=f"{k['icon']} {k['label']}\n{k['value']}"
                if k.get("delta"): cell+=f"\n{k['delta']}"
                row_cells.append(P(cell,S(f"kc",fontSize=10,textColor=BLUE,fontName="Helvetica-Bold",leading=14)))
            while len(row_cells)<cols: row_cells.append(Paragraph("",sty["Normal"]))
            all_rows.append(row_cells)
        t=Table(all_rows,colWidths=[16.4*cm/cols]*cols)
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),LTGRAY),("GRID",(0,0),(-1,-1),0.4,MDGRAY),
            ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
            ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        return [t,Spacer(1,0.3*cm)]

    def stat_table(df):
        nc2=smart_numeric_cols(df)
        if not nc2: return []
        data=[["Column","Total","Mean","Min","Max","Std"]]
        for col in nc2[:8]:
            s=df[col].dropna()
            data.append([_st(col.replace("_"," ").title()),_st(fmt(float(s.sum()))),
                         _st(fmt(float(s.mean()))),_st(fmt(float(s.min()))),
                         _st(fmt(float(s.max()))),_st(fmt(float(s.std())))])
        cw=[5*cm,2.2*cm,2.2*cm,2.2*cm,2.2*cm,2.2*cm]
        t=Table(data,colWidths=cw,repeatRows=1)
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),VIOLET),("TEXTCOLOR",(0,0),(-1,0),WHITE),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8),
            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("TEXTCOLOR",(0,1),(-1,-1),GRAY),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LTGRAY]),
            ("GRID",(0,0),(-1,-1),0.3,MDGRAY),("LINEBELOW",(0,0),(-1,0),1,VIOLET),
            ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
            ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
            ("ALIGN",(1,0),(-1,-1),"CENTER")]))
        return [t,Spacer(1,0.3*cm)]

    elems=[]

    # ── COVER ──────────────────────────────────────────────────────────
    elems.append(Spacer(1,2.5*cm))
    def colored_bar(text,font_size,bg_color,font_color=WHITE,font_name="Helvetica-Bold"):
        d=[[P(text,S(f"b{font_size}",fontSize=font_size,textColor=font_color,
                     fontName=font_name,leading=font_size+6))]]
        t=Table(d,colWidths=[16.4*cm])
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg_color),
            ("LEFTPADDING",(0,0),(-1,-1),18),("TOPPADDING",(0,0),(-1,-1),14),
            ("BOTTOMPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),18)]))
        return t
    elems.append(colored_bar("NLDA Pro",38,GOLD))
    elems.append(Spacer(1,0.3*cm))
    elems.append(colored_bar("Full Intelligence Report — Dashboard & Analysis",15,VIOLET))
    elems.append(Spacer(1,1.2*cm))
    elems.append(HR(1.0,GOLD,10))
    elems.append(Spacer(1,0.4*cm))
    elems.append(P(f"Generated: {datetime.now().strftime('%A, %d %B %Y at %H:%M')}",sub_s))
    elems.append(P(f"Datasets: {', '.join(datasets_dict.keys())}",sub_s))
    total_dash_charts=sum(len(d.get("charts",[])) for d in dashboard_data_by_name.values())
    elems.append(P(f"Dashboard charts: {total_dash_charts}  |  Query analyses: {len(history)}",sub_s))
    if not HAS_K:
        elems.append(P("Tip: pip install kaleido to embed chart images in this PDF.",note_s))
    elems.append(Spacer(1,0.5*cm)); elems.append(HR(0.5,MDGRAY,16))

    cov_data=[["Metric","Value"],
              ["Total dataset rows",f"{sum(len(d) for d in datasets_dict.values()):,}"],
              ["Dashboard charts",str(total_dash_charts)],
              ["Query analyses",str(len(history))],
              ["KPIs extracted",str(sum(len(e.get("kpis",[])) for e in history))],
              ["Insights generated",str(sum(len(e.get("insights",[])) for e in history))]]
    ct=Table(cov_data,colWidths=[9*cm,7*cm])
    ct.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),BLUE),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),10),
        ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("TEXTCOLOR",(0,1),(-1,-1),GRAY),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LTGRAY]),("GRID",(0,0),(-1,-1),0.4,MDGRAY),
        ("LINEBELOW",(0,0),(-1,0),1,BLUE),("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(0,0),(-1,-1),10)]))
    elems.append(ct)
    elems.append(PageBreak())

    # ── PART I: DASHBOARD ─────────────────────────────────────────────
    elems.append(P("Part I — Auto-Dashboard",h2_s)); elems.append(HR(1.0,GOLD,12))
    for dn,dd in datasets_dict.items():
        dash=dashboard_data_by_name.get(dn,{}); kpis=dash.get("kpis",[]); dcharts=dash.get("charts",[])
        nc2=smart_numeric_cols(dd); cc2=smart_cat_cols(dd)
        elems.append(P(f"Dataset: {dn.replace('_',' ').title()}",h2_s))
        elems.append(P(f"{len(dd):,} rows · {len(dd.columns)} cols · {len(nc2)} numeric · {len(cc2)} categorical",sub_s))
        elems.append(HR(0.5,rc.HexColor("#bfdbfe"),6))
        elems.append(P("Numeric Statistics",h3_s)); elems.extend(stat_table(dd))
        if kpis: elems.append(P("Key Performance Indicators",h3_s)); elems.extend(kpi_row(kpis))
        if dcharts:
            elems.append(P(f"Dashboard Charts ({len(dcharts)} total)",h3_s))
            if not HAS_K: elems.append(P("[Install kaleido: pip install kaleido]",note_s))
            for ci,(label,fig) in enumerate(dcharts):
                elems.append(P(f"{ci+1}. {label}",chap_s))
                imgs=img_from_fig(fig,w=15*cm,h=7*cm)
                elems.extend(imgs if imgs else [P("[Chart not embedded — install kaleido]",note_s)])
                elems.append(Spacer(1,0.3*cm))
        elems.append(PageBreak())

    # ── PART II: DATA STORY ───────────────────────────────────────────
    if story_text and story_text.strip():
        elems.append(P("Part II — AI Data Story",h2_s)); elems.append(HR(1.0,GOLD,12))
        section_titles=["The Headline Discovery","The Pattern in the Data",
                         "Who Is Winning","The Hidden Risk","The Root Cause","Monday Morning Actions"]
        for i,para in enumerate([p.strip() for p in story_text.split("\n\n") if p.strip()]):
            sec=section_titles[i] if i<len(section_titles) else f"Section {i+1}"
            elems.append(P(sec,h3_s)); elems.append(P(para,story_s))
        elems.append(PageBreak())

    # ── PART III: QUERY ANALYSES ──────────────────────────────────────
    if history:
        elems.append(P("Part III — Query Analysis History",h2_s)); elems.append(HR(1.0,GOLD,12))
        for i,e in enumerate(history,1):
            items=[]
            items.append(P(f"Analysis {i} · {e.get('ts','')}",h3_s))
            items.append(HR(0.4,rc.HexColor("#bfdbfe"),4))
            qd=[[P(f"Q: {e.get('question','')}",S("q",fontSize=11,textColor=BLUE,
                                                    fontName="Helvetica-BoldOblique",leading=15))]]
            qt=Table(qd,colWidths=[14.4*cm])
            qt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),rc.HexColor("#eff6ff")),
                ("LEFTPADDING",(0,0),(-1,-1),12),("TOPPADDING",(0,0),(-1,-1),8),
                ("BOTTOMPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),12),
                ("BOX",(0,0),(-1,-1),1,rc.HexColor("#93c5fd"))]))
            items.append(qt); items.append(Spacer(1,0.2*cm))
            items.append(P("Summary",h4_s)); items.append(P(e.get("summary",""),body_s))
            conf=e.get("confidence","high").lower()
            items.append(P(f"Confidence: {conf.upper()}",conf_map.get(conf,conf_map["high"])))
            if e.get("kpis"):
                items.append(P("Key Metrics",h4_s))
                kd=[["Metric","Value","Change"]]
                for k in e["kpis"]: kd.append([_st(k.get("label","")),_st(k.get("value","")),_st(k.get("delta","—") or "—")])
                kt=Table(kd,colWidths=[7*cm,3.5*cm,3.5*cm],repeatRows=1)
                kt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),VIOLET),("TEXTCOLOR",(0,0),(-1,0),WHITE),
                    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8),
                    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("TEXTCOLOR",(0,1),(-1,-1),GRAY),
                    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                    ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
                    ("GRID",(0,0),(-1,-1),0.3,MDGRAY),("LINEBELOW",(0,0),(-1,0),1,VIOLET),
                    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LTGRAY])]))
                items.extend([Spacer(1,0.1*cm),kt,Spacer(1,0.2*cm)])
            if e.get("fig"):
                items.append(P("Chart",h4_s))
                imgs=img_from_fig(e["fig"],w=14*cm,h=6.5*cm)
                items.extend(imgs if imgs else [P("[kaleido required]",note_s)])
            if e.get("query_story","").strip():
                items.append(P("Plain-English Explanation",h4_s))
                for para in e["query_story"].split("\n\n"):
                    if para.strip(): items.append(P(para,story_s))
            if e.get("insights"):
                items.append(P("Key Insights",h4_s))
                for ins in e["insights"]: items.append(P(f"* {ins}",bul_s))
            if e.get("anomalies"):
                items.append(P("Anomalies",h4_s))
                for an in e["anomalies"]: items.append(P(f"[!] {an}",anom_s))
            if e.get("sql_query","").strip():
                items.append(P("SQL",h4_s))
                for line in e["sql_query"].split("\n"): items.append(P(line or " ",mono_s))
            items.append(Spacer(1,0.3*cm)); items.append(HR(0.6,MDGRAY,8))
            elems.extend(items)

    # ── BACK COVER ────────────────────────────────────────────────────
    elems.append(PageBreak()); elems.append(Spacer(1,4*cm))
    elems.append(P("NLDA Pro · Business Data Intelligence",
                   S("fp",fontSize=16,textColor=GOLD,fontName="Helvetica-Bold",spaceAfter=8,alignment=TA_CENTER)))
    elems.append(P(f"Report generated {datetime.now().strftime('%d %B %Y at %H:%M')}",
                   S("fd",fontSize=10,textColor=DKGRAY,spaceAfter=4,alignment=TA_CENTER)))
    elems.append(HR(0.5,GOLD,10))
    elems.append(P("Powered by AI · Powered by NLDA Pro",
                   S("fdt",fontSize=9,textColor=DKGRAY,spaceAfter=2,alignment=TA_CENTER)))

    doc.build(elems)
    return buf.getvalue()
# ─────────────────────────────────────────────────────────────────────
#  HTTP LAYER
# ─────────────────────────────────────────────────────────────────────
def _http_post(url, headers, payload):
    import http.client, urllib.parse, ssl
    body=json.dumps(payload,ensure_ascii=False).encode("utf-8")
    safe_h={str(k):str(v).encode("ascii",errors="replace").decode("ascii") for k,v in headers.items()}
    safe_h["Content-Type"]="application/json; charset=utf-8"
    safe_h["Content-Length"]=str(len(body))
    p=urllib.parse.urlparse(url); host=p.netloc
    path=p.path+(f"?{p.query}" if p.query else "")
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

def _call_openai(url,key,model,system,question,temperature=0.1,max_tokens=3500,json_mode=True):
    payload={"model":model,"messages":[{"role":"system","content":system},{"role":"user","content":question}],
             "max_tokens":max_tokens,"temperature":temperature}
    if json_mode: payload["response_format"]={"type":"json_object"}
    d=_http_post(url,{"Authorization":f"Bearer {key}"},payload)
    return d["choices"][0]["message"]["content"]

def _call_gemini(url,key,system,question,temperature=0.1,max_tokens=3500):
    prompt=f"{system}\n\nUser question: {question}"
    d=_http_post(f"{url}?key={key}",{},
        {"contents":[{"role":"user","parts":[{"text":prompt}]}],
         "generationConfig":{"temperature":temperature,"maxOutputTokens":max_tokens}})
    try: return d["candidates"][0]["content"]["parts"][0]["text"]
    except(KeyError,IndexError): raise RuntimeError(f"Unexpected Gemini response: {str(d)[:300]}")

def _call_anthropic(url,key,model,system,question,temperature=0.1,max_tokens=3500):
    d=_http_post(url,{"x-api-key":key,"anthropic-version":"2023-06-01"},
        {"model":model,"max_tokens":max_tokens,"system":system,"messages":[{"role":"user","content":question}],"temperature":temperature})
    st.session_state.query_tokens_used+=d.get("usage",{}).get("input_tokens",0)+d.get("usage",{}).get("output_tokens",0)
    return d["content"][0]["text"]

def _parse_raw(raw):
    raw=re.sub(r'^```(?:json)?\s*','',raw.strip()); raw=re.sub(r'\s*```$','',raw)
    try: return json.loads(raw)
    except json.JSONDecodeError:
        m=re.search(r'\{.*\}',raw,re.DOTALL)
        if m:
            try: return json.loads(m.group())
            except: pass
        raise RuntimeError(f"Could not parse AI JSON response:\n{raw[:500]}")

def _route_text(system, question, temperature=0.7, max_tokens=2000):
    """Route for plain text responses (stories)."""
    provider=st.session_state.get("provider","Groq (Free)")
    key=st.session_state.get("provider_key","").strip()
    if not key: raise RuntimeError("No API key. Add it in the sidebar.")
    cfg=PROVIDERS[provider]
    if   cfg["style"]=="openai":    return _call_openai(cfg["url"],key,cfg["model"],system,question,temperature,max_tokens,json_mode=False)
    elif cfg["style"]=="gemini":    return _call_gemini(cfg["url"],key,system,question,temperature,max_tokens)
    elif cfg["style"]=="anthropic": return _call_anthropic(cfg["url"],key,cfg["model"],system,question,temperature,max_tokens)

def _route_json(system, question):
    """Route for JSON responses (analysis)."""
    provider=st.session_state.get("provider","Groq (Free)")
    key=st.session_state.get("provider_key","").strip()
    if not key: raise RuntimeError(f"No API key for {provider}. Add it in the sidebar.")
    cfg=PROVIDERS[provider]
    if   cfg["style"]=="openai":    return _call_openai(cfg["url"],key,cfg["model"],system,question,0.1,3500,True)
    elif cfg["style"]=="gemini":    return _call_gemini(cfg["url"],key,system,f"{question}\n\nRespond with ONLY a valid JSON object.",0.1,3500)
    elif cfg["style"]=="anthropic": return _call_anthropic(cfg["url"],key,cfg["model"],system,question,0.1,3500)

# ─────────────────────────────────────────────────────────────────────
#  AI PROMPTS  — v5.0 enhanced
# ─────────────────────────────────────────────────────────────────────
ANALYSIS_PROMPT = """You are NLDA Pro — a world-class senior data analyst.

Datasets:
{schemas}

Conversation history:
{context}

Respond with ONLY a valid JSON object (no markdown, no extra text):

{{
  "summary": "2-3 crisp sentences with ACTUAL numbers from the data. Be specific.",
  "pandas_code": "Complete pandas code. Use df (single) or dfs['name'] (multi-table). MUST assign result to result_df. pd/np/datetime available. No imports. No file I/O.",
  "sql_query": "Complete, runnable SQL SELECT statement",
  "chart_type": "bar|grouped bar|stacked bar|horizontal bar|line|area|scatter|bubble|pie|donut|sunburst|treemap|histogram|box|violin|heatmap|density heatmap|waterfall|funnel|gauge|radar|parallel coordinates|candlestick|none",
  "chart_config": {{
    "x": "exact column name for X axis, or null",
    "y": "MUST be a numeric column that exists in the data, or null",
    "color": "exact column name for color grouping, or null",
    "size": "exact column name for bubble/scatter size, or null",
    "title": "Descriptive chart title with the key metric"
  }},
  "kpis": [
    {{"label": "short label max 3 words", "value": "formatted e.g. $4.2M or 38%", "delta": "+12.3% vs prior or null"}}
  ],
  "insights": [
    "INSIGHT 1: [Trend/Pattern/Comparison] — specific finding with exact number and context",
    "INSIGHT 2: [Anomaly/Outlier/Spike] — what stands out and why it matters",
    "INSIGHT 3: [Recommendation/Action] — what to do based on this data"
  ],
  "insight_types": ["trend", "anomaly", "recommendation"],
  "anomalies": ["Specific outlier: column X value Y is Z standard deviations from mean"],
  "follow_up_questions": ["Smarter deeper follow-up 1?", "Question 2?", "Question 3?"],
  "query_story": "2-paragraph plain-text narrative: Paragraph 1 — what this specific analysis reveals. Paragraph 2 — why it matters and what action it suggests. Write as an analyst briefing a business leader. Use actual numbers.",
  "confidence": "high|medium|low",
  "reasoning": "2-sentence description of analytical approach used"
}}

STRICT RULES:
1. chart_config.y MUST be a numeric column (not a date/string column)
2. pandas_code MUST assign final result to result_df
3. insights[0] = trend or pattern (with %)
4. insights[1] = biggest anomaly or surprise (with specific value)
5. insights[2] = actionable recommendation (with evidence)
6. query_story MUST be 2 paragraphs separated by blank line, plain text only
7. kpis: 3-5 items max, all values pre-formatted as strings
"""

FULL_STORY_PROMPT = """You are a world-class data journalist and business analyst.

You have been given complete data about the following datasets and their analyses:

=== DATASET OVERVIEW ===
{dataset_summary}

=== ANALYSIS RESULTS ===
{analyses}

Write a COMPREHENSIVE DATA STORY in exactly 6 sections. Each section must be a full paragraph (minimum 4 sentences). Use SPECIFIC NUMBERS throughout.

SECTION 1 — THE HEADLINE DISCOVERY
The single most important finding across all the data. What is the ONE thing a CEO must know? Quote exact numbers. Make it punchy and memorable.

SECTION 2 — THE PATTERN IN THE DATA
What systematic trend or relationship runs through this dataset? How do different variables connect? What does the overall shape of the data tell us?

SECTION 3 — WHO OR WHAT IS WINNING
Which segment, product, region, channel, or person is performing best — and by how much? What makes them different? Quote specific performance numbers.

SECTION 4 — THE HIDDEN RISK OR SURPRISE
What counter-intuitive finding lurks in the data? What would a naive observer have gotten wrong? Is there a warning signal that needs attention? Cite specific values.

SECTION 5 — THE ROOT CAUSE
Why is this happening? What correlations or underlying factors explain the headline finding? Connect the variables with logical reasoning backed by data.

SECTION 6 — MONDAY MORNING ACTIONS
3 specific, concrete, numbered recommendations. Each must: name a specific action, specify who should do it, state the expected impact with a number. Format as 1. ... 2. ... 3. ...

Style: Write like a McKinsey partner presenting to a board. Authoritative, direct, data-driven. No bullet points except in section 6. No generic statements — every sentence must contain a specific insight.

Return ONLY the story — no JSON, no markdown headers, no section labels."""

QUERY_STORY_PROMPT = """You are explaining a data chart to someone who has never studied statistics or business analytics. They are a curious, intelligent person but not a data expert.

Chart/Query: {question}
What the numbers show: {summary}
Key findings: {insights}
Important numbers: {kpis}
About the data: {schema_snippet}

Write 3 short paragraphs that any person can understand:

Paragraph 1 — WHAT'S HAPPENING (The simple truth):
Explain in everyday language what this chart shows. Imagine you're telling a friend over coffee. Avoid jargon. Use analogies if helpful. Lead with the most surprising or important number.

Paragraph 2 — WHY IT MATTERS (So what?):
Explain why a normal person should care about this. What does it mean for the business, the people, or daily decisions? Connect it to real-world outcomes. What could happen if this trend continues?

Paragraph 3 — WHAT TO DO (The action):
Give 1-2 concrete actions that a manager or team could take based on this data. Make it specific and practical — not "improve performance" but "focus sales team on the North America region which generates 3x more revenue per deal."

Rules:
- Write like you're texting a smart friend, not writing a report
- Every number you mention must be from the actual data provided
- No bullet points, no headers, no jargon (no "KPI", "metric", "leverage", "synergy")
- Maximum 3 sentences per paragraph
- If you don't have specific numbers, say "roughly" or "about" — never make up exact figures"""

def call_ai(question, schemas, history, extra=""):
    ctx="\n".join(f"Q:{h['question']}\nA:{h.get('summary','')}" for h in history[-4:]) or "(none)"
    system=ANALYSIS_PROMPT.format(schemas=schemas,context=ctx)
    if extra: system+=f"\n\nContext: {extra}"
    raw=_route_json(system,question)
    return _parse_raw(raw)

def call_query_story(question, summary, insights, kpis, schema_snippet):
    """Generate a per-query narrative story."""
    kpi_str=", ".join(f"{k.get('label')}={k.get('value')}" for k in kpis[:4])
    ins_str="\n".join(f"- {i}" for i in insights[:3])
    system=QUERY_STORY_PROMPT.format(
        question=question, summary=summary,
        insights=ins_str, kpis=kpi_str, schema_snippet=schema_snippet[:500])
    try: return _route_text(system,"Write the narrative now.",temperature=0.6,max_tokens=600)
    except Exception as e: return f"Story generation note: {e}"

def call_full_story(dataset_summary, analyses_text):
    """Generate comprehensive 6-section story of entire dataset."""
    system=FULL_STORY_PROMPT.format(
        dataset_summary=dataset_summary, analyses=analyses_text)
    try: return _route_text(system,"Write the complete data story now.",temperature=0.7,max_tokens=2000)
    except Exception as e: return f"Story generation error: {e}"

def safe_exec(code, dfs):
    env={"pd":pd,"np":np,"datetime":datetime,
         "dfs":dfs,"df":list(dfs.values())[0] if dfs else pd.DataFrame(),"result_df":None}
    try:
        exec(compile(code,"<nlda>","exec"),env)
        res=env.get("result_df")
        if res is not None and not isinstance(res,pd.DataFrame):
            try: res=pd.DataFrame({"result":[res]})
            except: res=None
        return res,None
    except Exception as e: return None,str(e)

def run_query(question, prog=None):
    schemas="\n\n".join(df_schema_str(df,n) for n,df in st.session_state.dataframes.items())
    STEPS=["PARSE","AI CALL","EXECUTE","VISUALIZE","STORY"]
    def show(active):
        if not prog: return
        items="".join(
            f'<div class="step-item {"done" if STEPS.index(s)<STEPS.index(active) else "active" if s==active else ""}"><span class="step-dot">{"✓" if STEPS.index(s)<STEPS.index(active) else "⬡"}</span>{s}</div>'
            for s in STEPS)
        prog.markdown(f'<div class="step-track">{items}</div>',unsafe_allow_html=True)

    show("PARSE"); show("AI CALL")
    result=call_ai(question,schemas,st.session_state.chat_history)
    show("EXECUTE")
    rdf,err=None,None
    if result.get("pandas_code"): rdf,err=safe_exec(result["pandas_code"],st.session_state.dataframes)
    show("VISUALIZE")
    fig=None; ctype=result.get("chart_type","none")
    if ctype and ctype.lower()!="none" and rdf is not None and not rdf.empty:
        fig=make_chart(rdf,ctype,result.get("chart_config",{}))
        if fig: st.session_state.charts_generated+=1
    show("STORY")
    # Per-query story generation
    query_story=result.get("query_story","")
    if not query_story.strip():
        schema_snip=schemas[:600]
        query_story=call_query_story(
            question, result.get("summary",""),
            result.get("insights",[]), result.get("kpis",[]), schema_snip)
    if prog: prog.empty()
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
        "insight_types":result.get("insight_types",[]),
        "anomalies":   result.get("anomalies",[]),
        "follow_up_questions":result.get("follow_up_questions",[]),
        "confidence":  result.get("confidence","high"),
        "reasoning":   result.get("reasoning",""),
        "query_story": query_story,
        "result_df":   rdf,
        "exec_error":  err,
        "fig":         fig,
        "provider":    PROVIDERS[st.session_state.get("provider","Groq (Free)")]["label"],
    }

# ─────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div class="logo-bar">
        <span class="logo-hex">⬡</span>
        <span class="logo-name">NLDA Pro</span>
        <span class="logo-tag">Business Data Intelligence </span>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">AI Provider</div>', unsafe_allow_html=True)
    provider=st.selectbox("Provider",list(PROVIDERS.keys()),
        index=list(PROVIDERS.keys()).index(st.session_state.get("provider","Groq (Free)")),
        key="provider_select")
    st.session_state["provider"]=provider
    pc=PROVIDERS[provider]
    st.markdown(f'<div style="font-family:var(--fm);font-size:9px;color:{pc["badge"]};padding:2px 0 6px">{"● FREE tier" if pc["free"] else "● Paid"} · {pc["model"]}</div>',unsafe_allow_html=True)
    kv=st.text_input(f"{pc['label']} API Key",type="password",
                     value=st.session_state.get("provider_key",""),
                     placeholder=pc["key_hint"],help=f"Get free key: {pc['key_url']}")
    if kv: st.session_state["provider_key"]=kv
    st.markdown(f'<div style="font-size:10px;color:var(--t3);padding:1px 0 4px">🔑 <a href="{pc["key_url"]}" target="_blank" style="color:var(--gold)">{pc["key_url"].replace("https://","")}</a></div>',unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">Session</div>', unsafe_allow_html=True)
    tr=sum(len(d) for d in st.session_state.dataframes.values())
    st.markdown(f"""<div class="stat-strip">
        <div class="sc"><span class="sc-v">{st.session_state.total_queries}</span><span class="sc-l">Queries</span></div>
        <div class="sc"><span class="sc-v">{st.session_state.charts_generated}</span><span class="sc-l">Charts</span></div>
        <div class="sc"><span class="sc-v">{len(st.session_state.dataframes)}</span><span class="sc-l">Tables</span></div>
        <div class="sc"><span class="sc-v">{fmt(tr,0)}</span><span class="sc-l">Rows</span></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">Data Sources</div>', unsafe_allow_html=True)
    uploaded=st.file_uploader("Upload CSV / Excel",type=["csv","xlsx","xls"],
                              accept_multiple_files=True,label_visibility="collapsed")
    if uploaded:
        for uf in uploaded:
            nm=re.sub(r'\s+','_',uf.name.rsplit(".",1)[0].lower())
            if nm not in st.session_state.dataframes:
                try:
                    dfup=pd.read_csv(uf) if uf.name.endswith(".csv") else pd.read_excel(uf)
                    for col in dfup.columns:
                        if any(kw in col.lower() for kw in ["date","time","period","month","year"]):
                            try: dfup[col]=pd.to_datetime(dfup[col])
                            except: pass
                    st.session_state.dataframes[nm]=dfup
                    st.session_state.df_meta[nm]=col_profile(dfup)
                    st.success(f"✓ {nm} ({len(dfup):,} rows)")
                except Exception as e: st.error(f"Error: {e}")

    for dn,dd in list(st.session_state.dataframes.items()):
        nc=len(smart_numeric_cols(dd))
        st.markdown(f"""<div class="ds-card active">
            <div class="ds-name">{dn}</div>
            <div class="ds-meta"><span class="ds-badge">{len(dd):,}r</span><span class="ds-badge">{len(dd.columns)}c</span><span class="ds-badge">{nc}num</span></div>
        </div>""", unsafe_allow_html=True)
        if st.button(f"✕ {dn}",key=f"rm_{dn}"):
            del st.session_state.dataframes[dn]; st.session_state.df_meta.pop(dn,None); st.rerun()

    st.markdown('<div class="sb-sec">Quick Start</div>', unsafe_allow_html=True)
    if st.button("⚡ Load Demo Datasets",use_container_width=True,key="sb_demo"):
        for k,v in generate_demo_datasets().items():
            st.session_state.dataframes[k]=v; st.session_state.df_meta[k]=col_profile(v)
        st.rerun()

    if st.session_state.query_library:
        st.markdown('<div class="sb-sec">📚 Query Library</div>', unsafe_allow_html=True)
        for qi,q in enumerate(st.session_state.query_library[:8]):
            lbl=f"{q[:30]}…" if len(q)>30 else q
            if st.button(lbl,key=f"ql_{qi}"):
                st.session_state["_prefill"]=q; st.rerun()
        if st.button("🗑 Clear Library",key="clr_lib"): st.session_state.query_library=[]; st.rerun()

    if st.session_state.dataframes or st.session_state.chat_history:
        st.markdown('<div class="sb-sec">Export</div>', unsafe_allow_html=True)

        # Full report (dashboard + story + queries)
        if st.button("📊 Full Intelligence Report",use_container_width=True,key="pdf_full_btn"):
            with st.spinner("Building full PDF report…"):
                try:
                    # Pre-compute all dashboard data
                    dash_by_name = {dn: make_powerbi_dashboard(dd, dn)
                                    for dn, dd in st.session_state.dataframes.items()}
                    # Get cached story if available
                    cached_story = ""
                    for v in st.session_state.story_cache.values():
                        if v: cached_story = v; break
                    pdf = make_dashboard_pdf(
                        datasets_dict        = dict(st.session_state.dataframes),
                        dashboard_data_by_name = dash_by_name,
                        story_text           = cached_story,
                        history              = st.session_state.chat_history,
                    )
                    st.download_button(
                        "⬇ Download Full Report", pdf,
                        file_name=f"nlda_full_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf", key="dl_full_pdf")
                except RuntimeError as e: st.error(str(e))
                except Exception as e:    st.error(f"PDF error: {e}")

        # Queries-only report
        if st.session_state.chat_history:
            if st.button("📝 Query Analysis Report",use_container_width=True,key="pdf_btn"):
                with st.spinner("Generating query report…"):
                    try:
                        pdf = make_pdf(st.session_state.chat_history)
                        st.download_button(
                            "⬇ Download Queries PDF", pdf,
                            file_name=f"nlda_queries_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                            mime="application/pdf", key="dl_pdf")
                    except RuntimeError as e: st.error(str(e))
                    except Exception as e:    st.error(f"PDF error: {e}")

        if st.button("🗑 Clear Session",use_container_width=True,key="clr_btn"):
            for k,v in _D.items(): st.session_state[k]=v; st.rerun()

# ─────────────────────────────────────────────────────────────────────
#  MAIN PANEL
# ─────────────────────────────────────────────────────────────────────
st.markdown("""<div class="hero">
    <div class="hero-grid"></div><div class="hero-glow"></div><div class="hero-glow2"></div><div class="hero-glow3"></div>
    <div class="hero-eye">Business Data Intelligence Platform </div>
    <h1 class="hero-title">Your data has<br><span>a story to tell.</span></h1>
    <p class="hero-sub">Ask anything in plain English. Get charts, insights, per-query narratives, AI data stories, and professional PDF reports — all in seconds.</p>
    <div class="hero-badges">
        <div class="hb"><div class="dot" style="background:#34d399"></div>25+ chart types</div>
        <div class="hb"><div class="dot" style="background:#f0c040"></div>AI storytelling</div>
        <div class="hb"><div class="dot" style="background:#a78bfa"></div>Per-query stories</div>
        <div class="hb"><div class="dot" style="background:#22d3ee"></div>Industry presets</div>
        <div class="hb"><div class="dot" style="background:#fb7185"></div>Rich PDF export</div>
        <div class="hb"><div class="dot" style="background:#f472b6"></div>Smart insights</div>
    </div>
</div>""", unsafe_allow_html=True)

# Onboarding
if not st.session_state.dataframes:
    st.markdown("""<div class="ob-grid">
        <div class="ob-card"><div class="ob-num">01</div><div class="ob-title">Upload Data</div><div class="ob-desc">CSV or Excel. Multiple files. Auto date parsing and schema detection.</div></div>
        <div class="ob-card"><div class="ob-num">02</div><div class="ob-title">Ask Anything</div><div class="ob-desc">Plain English. AI understands intent. Gets smarter with context across queries.</div></div>
        <div class="ob-card"><div class="ob-num">03</div><div class="ob-title">25+ Chart Types</div><div class="ob-desc">Bar, violin, radar, waterfall, gauge, sunburst — auto-rendered and interactive.</div></div>
        <div class="ob-card"><div class="ob-num">04</div><div class="ob-title">AI Stories</div><div class="ob-desc">Every query gets a narrative. The full dataset gets a CEO-ready 6-section story.</div></div>
    </div>""", unsafe_allow_html=True)
    c1,c2,c3=st.columns([1,2,1])
    with c2:
        if st.button("⚡ Try it — Load Demo Datasets",use_container_width=True,key="ob_demo"):
            for k,v in generate_demo_datasets().items():
                st.session_state.dataframes[k]=v; st.session_state.df_meta[k]=col_profile(v)
            st.rerun()
    st.stop()

# ─────────────────────────────────────────────────────────────────────
#  FEATURE STRIP
# ─────────────────────────────────────────────────────────────────────
fc=st.columns(6)
FEATS=[("🔬","Data DNA","show_dna"),("🚀","Auto-Dash","show_autodash"),
       ("⚔","Compare","compare_mode"),("📖","Data Story","show_story"),
       ("⏱","Timeline","show_timeline"),("🎨","Composer","show_composer")]
for col,(icon,label,key) in zip(fc,FEATS):
    with col:
        active=st.session_state.get(key,False)
        if st.button(f"{icon} {label}",key=f"f_{key}"):
            st.session_state[key]=not active; st.rerun()

# ─────────────────────────────────────────────────────────────────────
#  DATASET EXPLORER
# ─────────────────────────────────────────────────────────────────────
with st.expander("🗃  Dataset Explorer & Column Profiles",expanded=False):
    dstabs=st.tabs([f"  {n}  " for n in st.session_state.dataframes])
    for tab,(dn,dd) in zip(dstabs,st.session_state.dataframes.items()):
        with tab:
            nc=smart_numeric_cols(dd)
            c1,c2,c3,c4,c5=st.columns(5)
            c1.metric("Rows",f"{len(dd):,}"); c2.metric("Cols",len(dd.columns))
            c3.metric("Numeric",len(nc)); c4.metric("Null%",f"{dd.isna().mean().mean()*100:.1f}%")
            c5.metric("Memory",f"{dd.memory_usage(deep=True).sum()/1024:.0f}KB")
            prof=st.session_state.df_meta.get(dn,col_profile(dd))
            html="".join(
                f'<div class="cp-card"><div class="cp-name">{col}</div>'
                f'<div class="cp-type">{info["dtype"].replace("float64","float").replace("int64","int").replace("object","str")} · {info["unique"]}u</div>'
                f'<div class="cp-bar-w"><div class="cp-bar" style="width:{info.get("completeness",100-info.get("null_pct",0))}%"></div></div></div>'
                for col,info in list(prof.items())[:16])
            st.markdown(f'<div class="cp-grid">{html}</div>',unsafe_allow_html=True)
            st.dataframe(dd.head(30),use_container_width=True,height=240)

# ─────────────────────────────────────────────────────────────────────
#  DATA DNA
# ─────────────────────────────────────────────────────────────────────
if st.session_state.get("show_dna"):
    st.markdown('<div class="div">🔬 Data DNA — Column Fingerprints & Outlier Detection</div>',unsafe_allow_html=True)
    for dn,dd in st.session_state.dataframes.items():
        st.markdown(f"**{dn}**")
        nc=smart_numeric_cols(dd)
        if not nc: st.info("No numeric columns."); continue
        cards=""
        for col in nc[:12]:
            s=dd[col].dropna()
            if len(s)==0: continue
            q1,q3=s.quantile(.25),s.quantile(.75); iqr=q3-q1
            out=int(((s<q1-1.5*iqr)|(s>q3+1.5*iqr)).sum())
            skw=float(s.skew()); kurt=float(s.kurt())
            cards+=(f'<div class="dna-card"><div class="dna-col">{col}</div>'
                f'<div class="dna-row"><span class="dna-k">Mean</span><span class="dna-v">{fmt(float(s.mean()))}</span></div>'
                f'<div class="dna-row"><span class="dna-k">Std</span><span class="dna-v">{fmt(float(s.std()))}</span></div>'
                f'<div class="dna-row"><span class="dna-k">Skew</span><span class="dna-v" style="color:{"#fb7185" if abs(skw)>1 else "#34d399"}">{skw:.2f}</span></div>'
                f'<div class="dna-row"><span class="dna-k">Kurt</span><span class="dna-v">{kurt:.2f}</span></div>'
                f'<div class="dna-row"><span class="dna-k">Outliers</span><span class="dna-v" style="color:{"#fb7185" if out>0 else "#34d399"}">{out}</span></div>'
                f'</div>')
        st.markdown(f'<div class="dna-grid">{cards}</div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
#  AUTO-DASHBOARD  — Power BI style
# ─────────────────────────────────────────────────────────────────────
if st.session_state.get("show_autodash"):
    st.markdown('<div class="div">🚀 Auto-Dashboard — Power BI Style Overview</div>', unsafe_allow_html=True)

    for dn, dd in st.session_state.dataframes.items():
        dash = make_powerbi_dashboard(dd, dn)
        nc   = smart_numeric_cols(dd)
        cc   = smart_cat_cols(dd)

        # ── Header ──────────────────────────────────────────────────
        st.markdown(f"""<div class="pbi-wrap">
          <div class="pbi-header">
            <div>
              <div class="pbi-title">📊 {dn.replace("_"," ").title()}</div>
              <div class="pbi-subtitle">
                {len(dd):,} rows · {len(dd.columns)} columns ·
                {len(nc)} numeric · {len(cc)} categorical
              </div>
            </div>
            <div class="pbi-stamp">
              Generated {datetime.now().strftime("%d %b %Y · %H:%M")}
            </div>
          </div>""", unsafe_allow_html=True)

        # ── KPI Strip ───────────────────────────────────────────────
        if dash["kpis"]:
            kpi_html = '<div style="display:flex;gap:12px;flex-wrap:wrap;padding:16px 20px;background:var(--surface);border-bottom:1px solid var(--bd0)">'
            for kpi in dash["kpis"]:
                clr = kpi["color"]
                delta_html = ""
                if kpi.get("delta"):
                    is_up  = "+" in str(kpi["delta"])
                    arrow  = "▲" if is_up else "▼"
                    dclr   = "#34d399" if is_up else "#fb7185"
                    delta_html = (f'<div style="font-family:var(--fm);font-size:10px;'
                                  f'color:{dclr};margin-top:3px">{arrow} {kpi["delta"]}</div>')
                kpi_html += (
                    f'<div style="flex:1;min-width:130px;max-width:200px;'
                    f'background:var(--raised);border:1px solid var(--bd1);'
                    f'border-top:3px solid {clr};border-radius:var(--r2);padding:14px 16px;">'
                    f'<div style="font-size:17px;margin-bottom:6px">{kpi["icon"]}</div>'
                    f'<div style="font-family:var(--fm);font-size:20px;font-weight:500;color:{clr}">{kpi["value"]}</div>'
                    f'<div style="font-family:var(--fm);font-size:10px;color:var(--t3);text-transform:uppercase;letter-spacing:.07em;margin-top:4px">{kpi["label"]}</div>'
                    f'<div style="font-family:var(--fm);font-size:9px;color:var(--t3);margin-top:2px">avg {kpi["avg"]}</div>'
                    f'{delta_html}'
                    f'</div>'
                )
            kpi_html += '</div>'
            st.markdown(kpi_html, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # close pbi-wrap header portion

        # ── Charts Grid — render ALL charts in responsive 2-col grid ──
        charts = dash["charts"]
        if charts:
            # Render in pairs (2-column grid)
            for row_start in range(0, len(charts), 2):
                pair = charts[row_start:row_start+2]
                cols_list = st.columns(len(pair))
                for ci, (lbl, fig) in enumerate(pair):
                    with cols_list[ci]:
                        st.markdown(
                            f'<div style="font-family:var(--fm);font-size:9px;'
                            f'color:var(--t3);letter-spacing:.12em;text-transform:uppercase;'
                            f'padding:8px 4px 4px">{lbl}</div>',
                            unsafe_allow_html=True)
                        st.plotly_chart(fig, use_container_width=True,
                                        key=f"pbi_{dn}_{row_start}_{ci}")
        else:
            st.warning(f"No charts could be generated for {dn}. Check that the dataset has numeric and categorical columns.")

        # ── Footer ──────────────────────────────────────────────────
        st.markdown(f"""<div style="background:var(--base);border:1px solid var(--bd0);
            border-radius:0 0 var(--r3) var(--r3);padding:10px 20px;
            display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;margin-top:-8px">
          <span style="font-family:var(--fm);font-size:9px;color:var(--t3)">
            NLDA Pro · Auto-Dashboard · {dn}
          </span>
          <span style="font-family:var(--fm);font-size:9px;color:var(--t3)">
            {len(charts)} charts · {len(nc)} metrics analysed
          </span>
        </div>""", unsafe_allow_html=True)

    # ── Dashboard PDF export button ──────────────────────────────────
    st.markdown('<div style="margin:16px 0 4px"></div>', unsafe_allow_html=True)
    exp_c1, exp_c2, _ = st.columns([2, 2, 4])
    with exp_c1:
        if st.button("📥 Export Full Dashboard PDF", key="dash_pdf_btn", type="primary", use_container_width=True):
            with st.spinner("Building dashboard PDF — embedding all charts…"):
                try:
                    story_txt = next(iter(st.session_state.get("story_cache", {}).values()), "")
                    dash_by_name = {dn: make_powerbi_dashboard(dd, dn)
                                    for dn, dd in st.session_state.dataframes.items()}
                    dpdf = make_dashboard_pdf(
                        datasets_dict          = dict(st.session_state.dataframes),
                        dashboard_data_by_name = dash_by_name,
                        story_text             = story_txt,
                        history                = st.session_state.chat_history,
                    )
                    fname = f"nlda_dashboard_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                    st.download_button(
                        "⬇ Download Dashboard PDF", dpdf,
                        file_name=fname,
                        mime="application/pdf",
                        key="dl_dash_pdf")
                    st.success(f"✓ Dashboard PDF ready — {len(dpdf)//1024}KB")
                except RuntimeError as e: st.error(str(e))
                except Exception as e: st.error(f"Dashboard PDF error: {e}")
    with exp_c2:
        st.markdown(
            '<div style="font-family:var(--fm);font-size:9px;color:var(--t3);padding:10px 0;line-height:1.6">'
            'Includes: all charts, KPIs, dataset stats, AI story, query appendix.<br>'
            'For chart images: <code>pip install kaleido</code>'
            '</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
#  COMPARE MODE
# ─────────────────────────────────────────────────────────────────────
if st.session_state.get("compare_mode"):
    st.markdown('<div class="div">⚔ Side-by-Side Comparison</div>',unsafe_allow_html=True)
    cm1,cm2=st.columns(2)
    with cm1:
        st.markdown('<span class="compare-lbl cmp-a">Query A</span>',unsafe_allow_html=True)
        qa=st.text_input("qa",value=st.session_state.compare_a,placeholder="First question…",key="qa_in",label_visibility="collapsed")
        st.session_state.compare_a=qa
    with cm2:
        st.markdown('<span class="compare-lbl cmp-b">Query B</span>',unsafe_allow_html=True)
        qb=st.text_input("qb",value=st.session_state.compare_b,placeholder="Second question…",key="qb_in",label_visibility="collapsed")
        st.session_state.compare_b=qb
    if st.button("⚔ Run Both",key="cmp_run",type="primary"):
        if qa.strip() and qb.strip():
            ra=rb=None
            with st.spinner("Running A…"):
                try: ra=run_query(qa.strip())
                except Exception as e: st.error(str(e))
            with st.spinner("Running B…"):
                try: rb=run_query(qb.strip())
                except Exception as e: st.error(str(e))
            if ra and rb: st.session_state["cmp_results"]=(qa,qb,ra,rb)
    if st.session_state.get("cmp_results"):
        qa2,qb2,ra2,rb2=st.session_state["cmp_results"]
        cr1,cr2=st.columns(2)
        for col,q,r,lab,cls in [(cr1,qa2,ra2,"A","cmp-a"),(cr2,qb2,rb2,"B","cmp-b")]:
            with col:
                st.markdown(f'<div class="compare-panel"><span class="compare-lbl {cls}">Result {lab}</span><br><div style="font-size:11px;color:var(--t1);font-weight:600;margin:6px 0">{q[:55]}</div><div style="font-size:13px;color:var(--t2);margin-bottom:10px">{r.get("summary","")}</div>',unsafe_allow_html=True)
                if r.get("fig"): st.plotly_chart(r["fig"],use_container_width=True,key=f"cmp_{lab}_fig")
                elif r.get("result_df") is not None and not r["result_df"].empty:
                    st.dataframe(r["result_df"].head(8),use_container_width=True)
                st.markdown('</div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
#  DATA STORY  — works with OR without prior queries
# ─────────────────────────────────────────────────────────────────────
if st.session_state.get("show_story"):
    st.markdown('<div class="div">📖 AI Data Story — Full Dataset Narrative</div>', unsafe_allow_html=True)

    # Build rich dataset summary regardless of query history
    ds_summary_parts = []
    for dn, dd in st.session_state.dataframes.items():
        nc = smart_numeric_cols(dd); cc2 = smart_cat_cols(dd)
        lines = [f"Dataset: {dn} ({len(dd):,} rows, {len(dd.columns)} columns)"]
        for col in nc[:8]:
            try:
                lines.append(
                    f"  {col}: mean={dd[col].mean():.2f}, "
                    f"min={dd[col].min():.2f}, max={dd[col].max():.2f}, "
                    f"total={dd[col].sum():.2f}, std={dd[col].std():.2f}"
                )
            except: pass
        for col in cc2[:4]:
            top = dd[col].value_counts().head(4)
            lines.append(f"  {col} distribution: {', '.join(f'{k}({v})' for k,v in top.items())}")
        # Date range if any
        for col in dd.columns:
            if pd.api.types.is_datetime64_any_dtype(dd[col]):
                lines.append(f"  {col} range: {dd[col].min().date()} to {dd[col].max().date()}")
                break
        ds_summary_parts.append("\n".join(lines))
    dataset_summary = "\n\n".join(ds_summary_parts)

    # Past queries (optional — empty string if none)
    def _fmt_e(i, e):
        kpi_str = "; ".join(f"{k.get('label')}={k.get('value')}" for k in e.get("kpis", []))
        return (f"Query {i+1}: {e['question']}\n"
                f"Finding: {e.get('summary','')}\n"
                f"Insights: {'; '.join(e.get('insights',[]))}\n"
                f"KPIs: {kpi_str}")
    analyses = "\n\n".join(_fmt_e(i, e) for i, e in enumerate(st.session_state.chat_history[-10:])) \
               if st.session_state.chat_history else "(No queries run yet — story is based entirely on raw dataset statistics above.)"

    story_key = hashlib.md5((dataset_summary + analyses).encode()).hexdigest()[:8]
    cached = st.session_state.story_cache.get(story_key)

    if cached is None:
        with st.spinner("✍ Writing your comprehensive data story…"):
            cached = call_full_story(dataset_summary, analyses)
            st.session_state.story_cache[story_key] = cached

    # Render story
    paras = [p.strip() for p in cached.split("\n\n") if p.strip()]
    section_titles = ["The Headline Discovery", "The Pattern in the Data",
                      "Who Is Winning", "The Hidden Risk",
                      "The Root Cause", "Monday Morning Actions"]
    section_colors = ["#f0c040", "#22d3ee", "#34d399", "#fb7185", "#a78bfa", "#fbbf24"]

    st.markdown(f"""<div class="story-wrap">
        <div class="story-eyebrow">
            AI Data Story · {len(st.session_state.dataframes)} dataset(s) ·
            {len(st.session_state.chat_history)} {'analyses' if st.session_state.chat_history else 'queries (raw stats mode)'}
        </div>
        <div class="story-headline">Comprehensive Business Intelligence Narrative</div>
    """, unsafe_allow_html=True)

    for i, para in enumerate(paras):
        sec = section_titles[i] if i < len(section_titles) else f"Section {i+1}"
        col = section_colors[i] if i < len(section_colors) else "#94a3b8"
        st.markdown(
            f'<div class="story-chapter" style="color:{col}">{sec}</div>'
            f'<p style="font-size:15px;color:var(--t1);line-height:1.9;margin:0 0 10px">{para}</p>',
            unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, _ = st.columns([1, 1, 5])
    with c1:
        if st.button("🔄 Regenerate", key="regen_story"):
            st.session_state.story_cache.pop(story_key, None); st.rerun()
    with c2:
        show_raw = st.session_state.get("story_show_raw", False)
        if st.button("📋 Hide raw text" if show_raw else "📋 Show raw text", key="copy_story"):
            st.session_state["story_show_raw"] = not show_raw; st.rerun()
    if st.session_state.get("story_show_raw", False):
        st.code(cached, language=None)

# ─────────────────────────────────────────────────────────────────────
#  TIMELINE  — works always, shows placeholder when no queries yet
# ─────────────────────────────────────────────────────────────────────
if st.session_state.get("show_timeline"):
    st.markdown('<div class="div">⏱ Insight Timeline — Every Query at a Glance</div>', unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="background:var(--raised);border:1px dashed var(--bd2);border-radius:var(--r3);
            padding:36px;text-align:center;color:var(--t3);">
            <div style="font-size:32px;margin-bottom:10px">⏱</div>
            <div style="font-family:var(--fd);font-size:15px;font-weight:700;color:var(--t2);margin-bottom:6px">
                No queries yet
            </div>
            <div style="font-size:13px;line-height:1.6">
                Run your first analysis below and the timeline will<br>
                automatically track every query, insight, and finding.
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        dot_colors = ["#f0c040","#a78bfa","#22d3ee","#34d399","#fb7185","#fbbf24","#f472b6","#38bdf8"]
        conf_icons = {"high":"✦","medium":"◆","low":"▲"}

        tl = '<div class="timeline">'
        for i, e in enumerate(st.session_state.chat_history):
            dc   = dot_colors[i % len(dot_colors)]
            ins  = e.get("insights", [""])[0][:100] if e.get("insights") else ""
            conf = e.get("confidence","high")
            ci   = conf_icons.get(conf,"✦")
            kpi_badges = "".join(
                f'<span style="display:inline-block;background:{dc}18;border:1px solid {dc}40;'
                f'border-radius:4px;font-family:var(--fm);font-size:9px;color:{dc};'
                f'padding:1px 7px;margin-right:5px;margin-top:4px">'
                f'{k.get("label","")}: {k.get("value","")}</span>'
                for k in e.get("kpis",[])[:3]
            )
            tl += (
                f'<div class="tl-item">'
                f'<div class="tl-dot" style="background:{dc}"></div>'
                f'<div class="tl-time">Query {i+1} · {e.get("ts","")} · {ci} {conf} confidence · {e.get("provider","AI")}</div>'
                f'<div class="tl-q">{e["question"]}</div>'
                f'<div class="tl-a">{e.get("summary","")[:130]}</div>'
                f'{f"""<div style="font-size:12px;color:{dc};margin-top:4px;font-style:italic">↳ {ins}</div>""" if ins else ""}'
                f'{f"""<div style="margin-top:6px">{kpi_badges}</div>""" if kpi_badges else ""}'
                f'</div>'
            )
        tl += '</div>'
        st.markdown(tl, unsafe_allow_html=True)

        # Mini summary bar
        total_insights = sum(len(e.get("insights",[])) for e in st.session_state.chat_history)
        total_charts   = sum(1 for e in st.session_state.chat_history if e.get("fig"))
        st.markdown(
            f'<div style="display:flex;gap:20px;padding:12px 16px;background:var(--raised);'
            f'border:1px solid var(--bd1);border-radius:var(--r2);margin-top:8px;flex-wrap:wrap">'
            f'<span style="font-family:var(--fm);font-size:10px;color:var(--t3)">Total queries: '
            f'<b style="color:var(--gold)">{len(st.session_state.chat_history)}</b></span>'
            f'<span style="font-family:var(--fm);font-size:10px;color:var(--t3)">Insights generated: '
            f'<b style="color:var(--cyan)">{total_insights}</b></span>'
            f'<span style="font-family:var(--fm);font-size:10px;color:var(--t3)">Charts rendered: '
            f'<b style="color:var(--violet)">{total_charts}</b></span>'
            f'</div>',
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────────────────────────────────
#  CHART COMPOSER  — v5.0: industry presets + smart column mapping
# ─────────────────────────────────────────────────────────────────────
if st.session_state.get("show_composer"):
    st.markdown('<div class="div">🎨 Chart Composer — Industry Presets & Manual Builder</div>',unsafe_allow_html=True)
    dnames=list(st.session_state.dataframes.keys())
    if dnames:
        # Dataset selector
        cds=st.selectbox("Select Dataset",dnames,key="comp_ds")
        cdf=st.session_state.dataframes[cds]
        # ── Industry Preset Pills ─────────────────────────────────────
        st.markdown("""<div style="font-family:var(--fm);font-size:9px;color:var(--t3);
            letter-spacing:.22em;text-transform:uppercase;margin:16px 0 10px;
            display:flex;align-items:center;gap:8px">
            <span style="width:16px;height:1px;background:var(--t3);display:inline-block"></span>
            Industry Presets — Click to instantly generate chart &amp; insights
            <span style="flex:1;height:1px;background:var(--bd0);display:inline-block"></span>
        </div>""", unsafe_allow_html=True)

        active_preset = st.session_state.get("selected_preset", "")

        # Build pill HTML
        pills_html = '<div class="preset-pill-row">'
        for pname, pdata in INDUSTRY_PRESETS.items():
            ac = "active" if pname == active_preset else ""
            pills_html += (
                f'<div class="preset-pill {ac}">'
                f'<span class="pill-icon">{pdata["icon"]}</span>'
                f'<span class="pill-label">{pname}</span>'
                f'</div>'
            )
        pills_html += '</div>'
        st.markdown(pills_html, unsafe_allow_html=True)

        # Real Streamlit selectbox hidden below — selecting triggers rerun
        # We map the pill click via a selectbox (visible but compact)
        preset_choice = st.selectbox(
            "Select preset",
            ["— choose a preset —"] + list(INDUSTRY_PRESETS.keys()),
            index=(["— choose a preset —"] + list(INDUSTRY_PRESETS.keys())).index(active_preset)
                  if active_preset in INDUSTRY_PRESETS else 0,
            key="preset_select_box",
            label_visibility="collapsed",
        )
        if preset_choice != "— choose a preset —" and preset_choice != active_preset:
            pdata = INDUSTRY_PRESETS[preset_choice]
            ax  = _pick_col(cdf, pdata.get("x_pref") or [])
            ay  = _pick_col(cdf, pdata.get("y_pref") or [])
            ac2 = _pick_col(cdf, pdata.get("color_pref") or [])
            st.session_state["selected_preset"]   = preset_choice
            st.session_state["comp_x_val"]         = ax  or "(auto)"
            st.session_state["comp_y_val"]         = ay  or "(auto)"
            st.session_state["comp_col_val"]       = ac2 or "(none)"
            st.session_state["comp_ct_val"]        = pdata["chart"]
            st.session_state["comp_title_val"]     = f"{preset_choice} Analysis"
            fc_p = {"x": ax, "y": ay, "color": ac2, "title": f"{preset_choice} Analysis"}
            st.session_state["comp_preset_fig"]    = make_chart(cdf, pdata["chart"], fc_p)
            st.session_state["comp_preset_name"]   = preset_choice
            st.session_state["comp_preset_desc"]   = pdata["desc"]
            st.session_state["comp_preset_query"]  = {
                "Sales Performance":  f"Show top performers by revenue with breakdown by {ax or 'category'}",
                "Trend Analysis":     f"Show the trend of {ay or 'revenue'} over time",
                "Distribution":       f"Show the distribution and outliers of {ay or 'revenue'} by {ax or 'category'}",
                "Part-of-Whole":      f"Show the share of {ay or 'revenue'} by {ax or 'category'} as a percentage",
                "Correlation":        f"Show the correlation between {ax or 'spend'} and {ay or 'revenue'}",
                "Marketing ROI":      f"Show ROAS and ROI by {ax or 'channel'} with revenue attribution",
                "HR Analytics":       f"Show {ay or 'salary'} distribution by {ax or 'department'}",
                "Operations":         f"Show the correlation matrix of all operational metrics",
                "Funnel / Pipeline":  f"Show the conversion funnel from {ax or 'stage'} by {ay or 'count'}",
                "Geographic":         f"Show {ay or 'revenue'} by {ax or 'region'} ranked highest to lowest",
            }.get(preset_choice, f"Analyze {preset_choice.lower()} metrics")
            st.rerun()

        # Show active preset result
        if st.session_state.get("comp_preset_fig") is not None:
            pname_a = st.session_state.get("comp_preset_name", "")
            pdesc_a = st.session_state.get("comp_preset_desc", "")
            st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;margin:16px 0 8px">
                <span style="font-family:var(--fd);font-size:14px;font-weight:700;color:var(--gold)">{pname_a}</span>
                <span style="font-family:var(--fm);font-size:10px;color:var(--t3)">{pdesc_a}</span>
            </div>""", unsafe_allow_html=True)
            st.plotly_chart(st.session_state["comp_preset_fig"],
                            use_container_width=True, key="comp_preset_chart")
            pq = st.session_state.get("comp_preset_query","")
            pq1, pq2 = st.columns([2,5])
            with pq1:
                if st.button(f"💡 Get {pname_a} Insights", key="preset_ins_btn", type="primary"):
                    prog_ph = st.empty()
                    try:
                        pe = run_query(pq, prog_ph)
                        st.session_state.chat_history.append(pe)
                        st.session_state.total_queries += 1
                        st.session_state["query_counter"] = st.session_state.get("query_counter",0)+1
                        st.rerun()
                    except Exception as ex:
                        prog_ph.empty(); st.error(str(ex))
            with pq2:
                if st.button("📌 Pin chart", key="pin_preset_ch"):
                    st.session_state.pinned_charts.append(st.session_state["comp_preset_fig"])
                    st.success("Pinned!")
            st.markdown('<div style="margin:16px 0;border-top:1px solid var(--bd0)"></div>', unsafe_allow_html=True)

        # ── Manual Builder ──────────────────────────────────────────
        st.markdown('<div style="font-family:var(--fm);font-size:9px;color:var(--t3);letter-spacing:.2em;text-transform:uppercase;margin:14px 0 8px">Manual Chart Builder</div>',unsafe_allow_html=True)

        all_cols=["(auto)"]+list(cdf.columns)
        chart_types_list=["bar","grouped bar","stacked bar","horizontal bar","line","area","scatter",
                          "bubble","pie","donut","sunburst","treemap","histogram","box","violin",
                          "heatmap","density heatmap","waterfall","funnel","gauge","radar",
                          "parallel coordinates","candlestick"]

        mn1,mn2,mn3,mn4,mn5=st.columns(5)
        with mn1:
            ct_idx=chart_types_list.index(st.session_state.get("comp_ct_val","bar")) if st.session_state.get("comp_ct_val","bar") in chart_types_list else 0
            cct=st.selectbox("Chart Type",chart_types_list,index=ct_idx,key="comp_ct")
        with mn2:
            x_idx=all_cols.index(st.session_state.get("comp_x_val","(auto)")) if st.session_state.get("comp_x_val","(auto)") in all_cols else 0
            cx=st.selectbox("X Axis",all_cols,index=x_idx,key="comp_x")
        with mn3:
            y_idx=all_cols.index(st.session_state.get("comp_y_val","(auto)")) if st.session_state.get("comp_y_val","(auto)") in all_cols else 0
            cy=st.selectbox("Y Axis (numeric)",all_cols,index=y_idx,key="comp_y")
        with mn4:
            none_cols=["(none)"]+list(cdf.columns)
            col_idx=none_cols.index(st.session_state.get("comp_col_val","(none)")) if st.session_state.get("comp_col_val","(none)") in none_cols else 0
            ccol=st.selectbox("Color By",none_cols,index=col_idx,key="comp_col")
        with mn5:
            ctitle=st.text_input("Chart Title",value=st.session_state.get("comp_title_val","My Chart"),key="comp_title")

        if st.button("🎨 Render Chart",key="comp_go",type="primary"):
            fc2={"x":None if cx in ("(auto)","(none)") else cx,
                 "y":None if cy in ("(auto)","(none)") else cy,
                 "color":None if ccol=="(none)" else ccol,
                 "title":ctitle}
            fg=make_chart(cdf,cct,fc2)
            if fg:
                st.plotly_chart(fg,use_container_width=True,key="comp_fig")
                if st.button("📌 Pin this chart",key="pin_comp"):
                    st.session_state.pinned_charts.append(fg); st.success("Pinned!")
            else:
                st.warning(f"Could not render '{cct}'.")
                nc_=smart_numeric_cols(cdf); cc_=smart_cat_cols(cdf)
                st.info(f"Numeric columns: {nc_[:5]}  |  Categorical: {cc_[:5]}")

# ─────────────────────────────────────────────────────────────────────
#  CHAT HISTORY
# ─────────────────────────────────────────────────────────────────────
if st.session_state.chat_history:
    st.markdown('<div class="div">Analysis History</div>',unsafe_allow_html=True)

    for idx,entry in enumerate(st.session_state.chat_history):
        is_editing=(st.session_state.editing_idx==idx)

        # User bubble
        st.markdown(f"""<div class="msg-row">
            <div class="msg-user-wrap"><div class="msg-user">{entry['question']}</div></div>
            <div class="msg-meta" style="text-align:right">You · {entry.get('ts','')} · {entry.get('provider','AI')}</div>
        </div>""",unsafe_allow_html=True)

        # Controls
        ec1,ec2,ec3,ec4=st.columns([1,1,1,7])
        with ec1:
            if st.button("✎ Edit",key=f"edit_{idx}"):
                st.session_state.editing_idx=idx; st.session_state["_prefill"]=entry["question"]; st.rerun()
        with ec2:
            if st.button("🗑 Del",key=f"del_{idx}"):
                st.session_state.chat_history.pop(idx); st.rerun()
        with ec3:
            if st.button("📚 Save",key=f"save_{idx}"):
                if entry["question"] not in st.session_state.query_library:
                    st.session_state.query_library.append(entry["question"]); st.success("Saved!")

        # Edit box
        if is_editing:
            st.markdown('<div class="edit-wrap"><div class="edit-lbl">Edit query and re-run</div>',unsafe_allow_html=True)
            eq=st.text_input("eq",value=entry["question"],key=f"eq_{idx}",label_visibility="collapsed")
            er1,er2,_=st.columns([1,1,5])
            with er1:
                if st.button("▶ Re-run",key=f"rerun_{idx}",type="primary"):
                    ph=st.empty()
                    try:
                        ne=run_query(eq.strip(),ph)
                        st.session_state.chat_history[idx]=ne
                        st.session_state.editing_idx=None
                        st.session_state.total_queries+=1; st.rerun()
                    except Exception as ex: ph.empty(); st.error(str(ex))
            with er2:
                if st.button("✕ Cancel",key=f"cancel_{idx}"):
                    st.session_state.editing_idx=None; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

        # AI response
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

        # KPI tiles
        _rdf=entry.get("result_df"); _kpis=entry.get("kpis") or []
        if not _kpis and _rdf is not None and not _rdf.empty: _kpis=generate_auto_kpis(_rdf)
        if _kpis:
            cc2=["c-gold","c-cyan","c-violet","c-emerald","c-rose","c-sky"]
            tiles=""
            for i,kpi in enumerate(_kpis[:6]):
                c=kpi.get("color",cc2[i%6]); dh=""
                if kpi.get("delta"):
                    cls2="pos" if "+" in str(kpi["delta"]) else "neg"
                    dh=f'<div class="kpi-delta {cls2}">{kpi["delta"]}</div>'
                tiles+=f'<div class="kpi-tile {c}"><span class="kpi-val">{kpi["value"]}</span><span class="kpi-lbl">{kpi["label"]}</span>{dh}</div>'
            st.markdown(f'<div class="kpi-grid">{tiles}</div>',unsafe_allow_html=True)

        # Result tabs — 8 tabs in v5.0
        rt=st.tabs(["📊 Chart","📋 Table","💡 Insights","📖 Story","🔎 SQL","🐍 Code","🧠 Reasoning","➕ Alt Charts"])

        with rt[0]:  # CHART
            if entry.get("fig"):
                pc_col,_=st.columns([1,9])
                with pc_col:
                    if st.button("📌 Pin",key=f"pin_{entry['id']}"):
                        st.session_state.pinned_charts.append(entry["fig"]); st.success("Pinned!")
                st.plotly_chart(entry["fig"],use_container_width=True,key=f"fig_{entry['id']}")
            else:
                st.markdown('<div class="no-chart"><span style="font-size:32px;display:block;margin-bottom:8px">📊</span>No chart rendered. Try asking "show as a bar chart" or use the Alt Charts tab.</div>',unsafe_allow_html=True)

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
            else: st.info("No tabular data for this query.")

        with rt[2]:  # INSIGHTS v5.0 — rich insight cards with types and mini-charts
            insight_types=entry.get("insight_types",[])
            type_colors={"trend":"#22d3ee","anomaly":"#fb7185","recommendation":"#34d399","pattern":"#a78bfa"}
            type_icons={"trend":"📈","anomaly":"⚠","recommendation":"💡","pattern":"🔗"}
            insights=entry.get("insights",[])
            anomalies=entry.get("anomalies",[])

            if insights:
                for i,ins in enumerate(insights):
                    itype=insight_types[i] if i<len(insight_types) else "insight"
                    icolor=type_colors.get(itype,"#f0c040")
                    iicon=type_icons.get(itype,"★")
                    badge_label=itype.upper() if itype else "INSIGHT"

                    st.markdown(f"""<div class="insight-card" style="border-left:3px solid {icolor}">
                        <div class="ins-header">
                            <span class="ins-title">{iicon} Insight {i+1}</span>
                            <span class="ins-badge" style="background:{icolor}20;color:{icolor};border:1px solid {icolor}40">{badge_label}</span>
                        </div>
                        <div class="ins-text">{ins}</div>
                    </div>""",unsafe_allow_html=True)

                    # Mini supporting chart for first insight
                    if i==0 and entry.get("result_df") is not None:
                        mini=make_insight_chart(entry["result_df"],ins,idx)
                        if mini:
                            with st.expander("📊 Supporting chart",expanded=False):
                                st.plotly_chart(mini,use_container_width=True,key=f"mini_{entry['id']}_{i}")

            for an in anomalies:
                st.markdown(f'<div class="anomaly-card"><div class="anomaly-icon">⚠</div><div class="anomaly-text"><strong>Anomaly Detected:</strong> {an}</div></div>',unsafe_allow_html=True)

            if not insights and not anomalies:
                st.info("No insights generated for this query.")

            fqs=entry.get("follow_up_questions",[])
            if fqs:
                st.markdown('<div style="font-family:var(--fm);font-size:9px;color:var(--t3);letter-spacing:.2em;text-transform:uppercase;margin:16px 0 8px">Suggested follow-up questions</div>',unsafe_allow_html=True)
                fq_c=st.columns(len(fqs))
                for col,q in zip(fq_c,fqs):
                    with col:
                        if st.button(f"↗ {q}",key=f"fq_{entry['id']}_{q[:14]}"):
                            st.session_state["_prefill"]=q; st.rerun()

        with rt[3]:  # PER-QUERY STORY — plain English for anyone
            qs = entry.get("query_story", "").strip()
            plain_labels = [
                ("💬", "What's Happening", "#f0c040"),
                ("🎯", "Why It Matters",   "#22d3ee"),
                ("✅", "What To Do",       "#34d399"),
            ]
            if qs:
                paras_qs = [p.strip() for p in qs.split("\n\n") if p.strip()]
                st.markdown('<div class="qstory-wrap">', unsafe_allow_html=True)
                st.markdown(
                    '<div class="qstory-lbl">📖 Chart Story — Written for everyone</div>',
                    unsafe_allow_html=True)
                for i, para in enumerate(paras_qs):
                    icon, lbl, clr = plain_labels[i] if i < len(plain_labels) else ("•", f"Part {i+1}", "#94a3b8")
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:7px;'
                        f'font-family:var(--fm);font-size:9px;color:{clr};'
                        f'letter-spacing:.18em;text-transform:uppercase;margin:14px 0 5px">'
                        f'{icon} {lbl}</div>'
                        f'<div class="qstory-text">{para}</div>',
                        unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                if st.button("🔄 Rewrite Story", key=f"regen_qs_{entry['id']}"):
                    schema_snip = "\n\n".join(
                        df_schema_str(df, n)[:300]
                        for n, df in st.session_state.dataframes.items())
                    with st.spinner("Rewriting in plain English…"):
                        ns = call_query_story(
                            entry["question"], entry.get("summary",""),
                            entry.get("insights",[]), entry.get("kpis",[]), schema_snip)
                    st.session_state.chat_history[idx]["query_story"] = ns; st.rerun()
            else:
                st.markdown(
                    '<div style="padding:24px;text-align:center;color:var(--t3);'
                    'font-family:var(--fm);font-size:11px">'
                    'No story yet for this chart.</div>',
                    unsafe_allow_html=True)
                if st.button("✍ Generate Plain-English Story", key=f"gen_qs_{entry['id']}", type="primary"):
                    schema_snip = "\n\n".join(
                        df_schema_str(df, n)[:300]
                        for n, df in st.session_state.dataframes.items())
                    with st.spinner("Writing plain-English story…"):
                        ns = call_query_story(
                            entry["question"], entry.get("summary",""),
                            entry.get("insights",[]), entry.get("kpis",[]), schema_snip)
                    st.session_state.chat_history[idx]["query_story"] = ns; st.rerun()

        with rt[4]:  # SQL
            sql=entry.get("sql_query","").strip()
            if sql: st.markdown(code_html(sql,"sql"),unsafe_allow_html=True)
            else:   st.info("No SQL generated.")

        with rt[5]:  # CODE
            pyc=entry.get("pandas_code","").strip(); err=entry.get("exec_error","")
            if pyc: st.markdown(code_html(pyc,"python"),unsafe_allow_html=True)
            if err: st.error(f"Execution note: {err}")
            if not pyc: st.info("No code generated.")

        with rt[6]:  # REASONING
            r=entry.get("reasoning","").strip()
            if r: st.markdown(f'<div style="background:var(--raised);border:1px solid var(--bd1);border-radius:9px;padding:16px 20px;font-size:13px;color:#94a3b8;line-height:1.75"><span style="font-family:var(--fm);font-size:8px;color:#475569;letter-spacing:.15em;text-transform:uppercase;display:block;margin-bottom:8px">AI Reasoning Chain</span>{r}</div>',unsafe_allow_html=True)
            else: st.info("No reasoning available.")

        with rt[7]:  # ALT CHARTS
            rdf2=entry.get("result_df")
            if rdf2 is not None and not rdf2.empty:
                nc2=smart_numeric_cols(rdf2); cc3=smart_cat_cols(rdf2)
                alt_opts=[]
                if cc3 and nc2:
                    for ct2 in ["bar","horizontal bar","pie","donut","radar","treemap","sunburst","funnel","stacked bar"]:
                        alt_opts.append((ct2,{"x":cc3[0],"y":nc2[0],"title":f"{ct2.title()} — {nc2[0]} by {cc3[0]}"}))
                if len(nc2)>=2:
                    for ct2 in ["scatter","bubble","box","violin","heatmap","parallel coordinates","density heatmap"]:
                        alt_opts.append((ct2,{"x":nc2[0],"y":nc2[1],"title":ct2.title()}))
                if nc2:
                    for ct2 in ["histogram","gauge","waterfall"]:
                        alt_opts.append((ct2,{"x":cc3[0] if cc3 else None,"y":nc2[0],"title":ct2.title()}))
                if alt_opts:
                    sel=st.selectbox("Chart type",[ct for ct,_ in alt_opts],key=f"altsel_{entry['id']}")
                    sel_cfg=next(c for ct,c in alt_opts if ct==sel)
                    afig=make_chart(rdf2,sel,sel_cfg)
                    if afig:
                        st.plotly_chart(afig,use_container_width=True,key=f"alt_{entry['id']}_{sel}")
                        if st.button("📌 Pin",key=f"pin_alt_{entry['id']}"):
                            st.session_state.pinned_charts.append(afig); st.success("Pinned!")
                    else: st.warning("Cannot render this chart type with the current data.")
                else: st.info("Not enough column types for alternative charts.")
            else: st.info("No data to visualize.")

        st.markdown('<div style="margin:8px 0;border-top:1px solid #1a2035"></div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
#  PINNED DASHBOARD
# ─────────────────────────────────────────────────────────────────────
if st.session_state.pinned_charts:
    st.markdown('<div class="div">📌 Pinned Charts Dashboard</div>',unsafe_allow_html=True)
    pcols=st.columns(min(2,len(st.session_state.pinned_charts)))
    for i,fg in enumerate(st.session_state.pinned_charts):
        with pcols[i%2]: st.plotly_chart(fg,use_container_width=True,key=f"pin_{i}")
    if st.button("Clear All Pins",key="clr_pins"):
        st.session_state.pinned_charts=[]; st.rerun()

# ─────────────────────────────────────────────────────────────────────
#  QUERY INPUT  — clears after submit
# ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="div">New Analysis</div>',unsafe_allow_html=True)

CHIPS=["Top 10 by revenue","Monthly revenue trend","Correlation heatmap",
       "Profit by region","ROAS by channel","Revenue vs spend",
       "Violin distribution","Waterfall chart"]

prefill=st.session_state.pop("_prefill","")
chip_cols=st.columns(len(CHIPS))
for i,(col,sug) in enumerate(zip(chip_cols,CHIPS)):
    with col:
        if st.button(sug,key=f"chip_{i}"): prefill=sug

st.markdown('<div class="q-wrap">',unsafe_allow_html=True)
st.markdown('<div class="q-lbl">Natural Language Query</div>',unsafe_allow_html=True)
qkey=f"main_q_{st.session_state.get('query_counter',0)}"
query=st.text_input("q",value=prefill,
    placeholder='e.g. "Show profit margin by region as a violin chart and highlight outliers"',
    label_visibility="collapsed",key=qkey)
qc1,qc2,qc3,qc4=st.columns([2,1,1,5])
with qc1: run=st.button("⬡  Analyze",use_container_width=True,key="run_btn",type="primary")
with qc2: deep=st.checkbox("Deep",value=False,help="More thorough analysis")
with qc3:
    if st.button("✕ Clear",key="clear_q"):
        st.session_state["query_counter"]=st.session_state.get("query_counter",0)+1; st.rerun()
st.markdown('</div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
#  ANALYSIS ENGINE
# ─────────────────────────────────────────────────────────────────────
if run and query.strip():
    if not st.session_state.get("provider_key","").strip():
        pn=st.session_state.get("provider","Groq (Free)")
        st.error(f"⚠ No API key for **{pn}**. Get a free key at {PROVIDERS[pn]['key_url']} and paste in sidebar.")
        st.stop()

    prog=st.empty()
    try:
        extra="Be especially thorough and detailed in all fields." if deep else ""
        entry=run_query(query.strip(),prog)
    except RuntimeError as e: prog.empty(); st.error(str(e)); st.stop()
    except json.JSONDecodeError as e: prog.empty(); st.error(f"JSON parse error — rephrase your question. ({e})"); st.stop()
    except Exception as e: prog.empty(); st.error(f"Unexpected error: {e}"); st.stop()

    st.session_state.chat_history.append(entry)
    st.session_state.total_queries+=1
    # Clear input
    st.session_state["query_counter"]=st.session_state.get("query_counter",0)+1
    st.rerun()


