# ⬡ NLDA Pro — Natural Language Data Analyst
### Ultimate Elite Edition · v3.0

> **Upload data → ask anything in plain English → get SQL, code, interactive charts, KPIs, and expert insights in seconds.**

Built with Python · Streamlit · Anthropic Claude Sonnet 4 · Plotly

---

## ✨ What It Does

NLDA Pro is a full-stack AI analytics platform that lets anyone — regardless of SQL or Python skill — have a real conversation with their data. Type a question, get a complete analysis: auto-generated pandas code that actually runs, equivalent SQL, an interactive Plotly chart, colour-coded KPI tiles, anomaly flags, expert insights, and follow-up question suggestions — all in one click.

```
You:     "Which region had the highest profit margin last quarter?"
NLDA:    ─ Summary answer with exact numbers
         ─ KPI tiles  (Total Revenue · Avg Margin · Top Region · ...)
         ─ Plotly bar chart (interactive, pinnable)
         ─ Pandas code  (syntax-highlighted, downloadable)
         ─ SQL query    (syntax-highlighted)
         ─ 3 key insights with real figures
         ─ Anomaly flags  (if any outliers found)
         ─ 3 follow-up question chips
         ─ AI reasoning chain
```

---

## 🚀 Quick Start

### 1 · Clone & install

```bash
git clone https://github.com/your-username/nlda-pro.git
cd nlda-pro
pip install -r requirements.txt
```

### 2 · Add your Anthropic API key

Get a key at [console.anthropic.com](https://console.anthropic.com) (free tier available).

**Option A — paste in UI** (easiest): open the app, expand **Configuration** in the sidebar, paste your key.

**Option B — environment variable** (for deployment):

```bash
export ANTHROPIC_API_KEY=sk-ant-api03-...
```

Or create a `.env` file:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 3 · Launch

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) — you'll see the landing screen. Either upload your own CSV/Excel or click **"⚡ Try it now — Load Demo Datasets"** to start immediately with synthetic sales + marketing data.

---

## 📁 Project Structure

```
nlda-pro/
├── app.py                  ← entire application (single file)
├── requirements.txt        ← Python dependencies
├── .streamlit/
│   └── config.toml         ← theme & server settings
└── README.md
```

---

## 🎯 Features

### Core Analysis Engine
| Feature | Detail |
|---|---|
| Natural language queries | Plain English → full analysis pipeline |
| Multi-turn conversation | Last 4 queries kept as context — ask follow-ups naturally |
| Confidence scoring | Claude rates each answer `high / medium / low` |
| AI reasoning chain | See exactly how the AI approached your question |
| Anomaly detection | Automatic flagging of statistical outliers |
| Follow-up suggestions | 3 smart next questions generated per query |

### Data Handling
| Feature | Detail |
|---|---|
| Multi-file upload | CSV and Excel (`.csv`, `.xlsx`, `.xls`) |
| Multi-table queries | Reference multiple datasets in one question |
| Auto date parsing | Columns named `date/time/month/year` cast automatically |
| Column profiler | dtype, unique count, null %, completeness bar per column |
| Dataset memory | Full stats (rows, cols, numeric count, null %, memory KB) |

### Output Formats (per query)
| Tab | What you get |
|---|---|
| 📊 Chart | Interactive Plotly chart — pinnable to dashboard |
| 📋 Table | Pageable result table — download as CSV or Excel |
| 💡 Insights | 3 data-backed insight cards + anomaly flags |
| 🔎 SQL | Syntax-highlighted SQL SELECT query |
| 🐍 Code | Syntax-highlighted Python/pandas code |
| 🧠 Reasoning | Claude's analytical chain-of-thought |

### Chart Types (10 total)
`bar` · `line` · `area` · `scatter` (with OLS trendline) · `pie` (donut) · `histogram` · `heatmap` (correlation) · `box` · `treemap` · `funnel`

### Export
- **CSV** — every result table, one click
- **Excel** — `.xlsx` download per result
- **PDF** — full session intelligence report (requires `reportlab`)
- **Pin charts** — save any chart to a live 2-column dashboard at the bottom of the page

---

## 💬 Example Queries

Paste any of these into the query box after loading the demo datasets:

```
"Top 5 products by total revenue"
"Monthly revenue trend as a line chart"
"Correlation heatmap of all numeric columns"
"Which sales rep has the highest average deal size?"
"Revenue vs marketing spend — show as scatter with trendline"
"Profit margin by region (horizontal bar chart)"
"Marketing ROAS by channel — bar chart"
"Show me quarterly revenue broken down by product"
"What are the anomalies in churn rate?"
"Which month had the lowest NPS score and why?"
"Revenue distribution — histogram"
"Compare conversion rates across marketing channels"
```

---

## 🗂 Demo Datasets

Loaded via the "⚡ Try it now" button or **Quick Start** in the sidebar. Two tables, reproducible seed (`np.random.seed(42)`):

### `sales_data` — 300 rows × 15 columns
| Column | Type | Description |
|---|---|---|
| `date` | datetime | Daily dates Jan 2022 – Oct 2022 |
| `region` | str | North America, Europe, Asia-Pacific, Latin America, Middle East |
| `product` | str | Enterprise Suite, Pro Plan, Starter, Add-ons, Services |
| `sales_rep` | str | Rep A through Rep H |
| `revenue` | float | Log-normal, ~$3K–$50K range |
| `units_sold` | int | 1–120 |
| `marketing_spend` | float | Per-deal marketing cost |
| `cac` | float | Customer acquisition cost |
| `churn_rate` | float | 1%–18% |
| `nps` | int | Net Promoter Score 1–10 |
| `cost` | float | Cost of goods |
| `profit` | float | revenue − cost |
| `profit_margin` | float | profit / revenue × 100 |
| `month` | str | e.g. `2022-01` |
| `quarter` | str | e.g. `2022Q1` |

### `marketing_data` — 60 rows × 10 columns
| Column | Type | Description |
|---|---|---|
| `month` | str | Monthly periods |
| `channel` | str | Paid Search, Social, Email, Content, Events, Referral |
| `spend` | float | Monthly channel spend |
| `impressions` | int | Ad impressions |
| `clicks` | int | Click-throughs |
| `conversions` | int | Converted leads |
| `revenue_attr` | float | Revenue attributed to channel |
| `cpc` | float | Cost per click |
| `roas` | float | Return on ad spend |
| `ctr_pct` | float | Click-through rate % |

---

## ☁️ Deployment

### Streamlit Cloud (free, recommended)

1. Push this repo to GitHub (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo → `app.py` → Python 3.11
4. Open **Advanced settings → Secrets** and add:

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

5. Click **Deploy** — live in ~2 minutes with a shareable URL.

Then update `app.py` to read the key from secrets as a fallback:

```python
# Add this near the top of the sidebar API key section:
if not st.session_state.api_key:
    st.session_state.api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
```

### Hugging Face Spaces (free)

1. Create a new Space → SDK: **Streamlit**
2. Upload `app.py`, `requirements.txt`, `.streamlit/config.toml`
3. Go to **Settings → Repository secrets** → add `ANTHROPIC_API_KEY`
4. The Space builds automatically on push.

Add the same secrets fallback shown above.

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t nlda-pro .
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=sk-ant-... nlda-pro
```

---

## 🏗 Architecture

```
app.py
│
├── DESIGN SYSTEM (CSS)
│   ├── CSS variables / tokens (void, gold, cyan, violet …)
│   ├── Sidebar, hero, onboarding, query panel
│   ├── Chat bubbles, KPI tiles, insight cards, code blocks
│   └── Step-progress tracker, column profile grid
│
├── SESSION STATE
│   └── dataframes, df_meta, chat_history, api_key,
│       total_queries, charts_generated, pinned_charts
│
├── UTILITIES
│   ├── fmt()                  — smart number formatting (K/M/B)
│   ├── col_profile()          — per-column stats (dtype, nulls, unique, min/max/mean)
│   ├── df_schema_str()        — compact schema string sent to Claude
│   ├── code_html()            — syntax-highlighted code blocks (Python + SQL)
│   ├── generate_auto_kpis()   — auto KPI tiles from numeric result columns
│   ├── make_pdf()             — ReportLab PDF export
│   └── generate_demo_datasets() — reproducible synthetic sales + marketing data
│
├── CLAUDE API
│   ├── SYSTEM_PROMPT_TEMPLATE — schema + last-4-turn context + JSON spec
│   ├── call_claude()          — REST call → parse structured JSON response
│   ├── safe_exec()            — sandboxed exec() for AI-generated pandas code
│   └── make_chart()           — Plotly figure factory (10 chart types)
│
├── SIDEBAR
│   ├── Logo + branding
│   ├── API key input
│   ├── Session metrics strip
│   ├── Multi-file uploader (CSV / Excel, auto date parsing)
│   ├── Dataset cards (rows · cols · numeric count)
│   ├── Demo dataset loader
│   └── PDF export + Clear session
│
└── MAIN PANEL
    ├── Hero card (grid texture + radial glow)
    ├── Onboarding (4-step cards + inline demo button)   [no data]
    ├── Dataset Explorer expander                        [data loaded]
    │   └── Per-dataset tab: KPI row + column profile cards + dataframe preview
    ├── Analysis History
    │   └── Per query:
    │       ├── User bubble + AI summary bubble (confidence badge)
    │       ├── KPI tile row
    │       └── Tabbed results: Chart · Table · Insights · SQL · Code · Reasoning
    ├── Pinned Charts Dashboard
    └── Query Input
        ├── 8 suggestion chips
        ├── Text input
        ├── Analyze button (type="primary") + Deep mode checkbox
        └── 4-step animated progress tracker (Parse → Claude → Execute → Visualize)
```

---

## 🔧 Configuration

### `.streamlit/config.toml`

```toml
[theme]
primaryColor          = "#f0c040"        # gold — primary interactive colour
backgroundColor       = "#05060a"        # void black
secondaryBackgroundColor = "#0e1117"     # surface
textColor             = "#f1f5f9"

[server]
maxUploadSize  = 400                     # MB
headless       = true

[browser]
gatherUsageStats = false
```

### Environment variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (can also be pasted in UI) |

---

## 🔒 Security

- API keys are stored only in Streamlit `session_state` — never logged, never sent anywhere except the Anthropic API.
- AI-generated pandas code runs in a sandboxed `exec()` environment with no file I/O, no subprocess, no `__import__` — only `pd`, `np`, `datetime`, and your loaded dataframes are available.
- Uploaded files are parsed in-memory and never written to disk.
- No telemetry: `gatherUsageStats = false` in `config.toml`.

---

## 📦 Dependencies

```
streamlit>=1.35.0       # UI framework
pandas>=2.1.0           # data manipulation
numpy>=1.26.0           # numerics
plotly>=5.21.0          # interactive charts
openpyxl>=3.1.2         # Excel read/write
xlrd>=2.0.1             # legacy .xls
anthropic>=0.28.0       # Claude API client (optional — app uses urllib directly)
scipy>=1.13.0           # stats helpers
reportlab>=4.2.0        # PDF export (optional — gracefully skipped if missing)
```

> **Note:** `reportlab` is optional. If not installed, the PDF export button will display an install prompt instead of crashing.

---

## 🛣 Roadmap

- [ ] Voice input via Whisper API
- [ ] Google Sheets connector
- [ ] PostgreSQL / BigQuery / Snowflake connectors
- [ ] Scheduled email reports
- [ ] Shareable analysis permalinks
- [ ] Chart annotation and export as PNG/SVG
- [ ] Custom system prompt editor (advanced mode)
- [ ] Multi-user session support

---

## 🐛 Known Bugs Fixed (v3.0 → v3.0.1)

| Bug | Symptom | Fix |
|---|---|---|
| `fmt()` string arg crash | Sidebar stats caused `ValueError` on every page load | `int()` coercion on `decimals` param |
| `st.stop()` blocking demo button | Clicking demo button appeared to do nothing | Moved `st.stop()` after `st.rerun()` in the onboarding block; added inline demo button |
| `pandas freq="ME"` error | Demo datasets failed on pandas < 2.2 | try/except fallback to `"M"` |
| Button CSS killing interactivity | Analyze button clicked but did nothing | Switched to `type="primary"` (native Streamlit), removed conflicting CSS specificity |
| KPI operator precedence crash | `None` passed to `generate_auto_kpis()` | Replaced ternary expression with explicit if/elif/else |
| `st.success()` before `st.rerun()` | Toast never appeared | Removed orphaned toast call |

---

## 📄 License

MIT — free to use, modify, and deploy commercially.

---

## 🙏 Credits

Built with [Streamlit](https://streamlit.io) · [Anthropic Claude](https://www.anthropic.com) · [Plotly](https://plotly.com) · [Pandas](https://pandas.pydata.org)

Typography: [Syne](https://fonts.google.com/specimen/Syne) · [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) · [Inter](https://fonts.google.com/specimen/Inter) via Google Fonts
