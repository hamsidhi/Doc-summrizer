# 📜 Document Intelligence Analyzer

> Investor-grade document analysis powered by Groq LLMs — built for fundraising consultants who deal with unstructured, complex, multi-domain documents.

---

## 🧠 What It Does

Upload any document — financial pitch deck, agricultural report, solar DPR, NGO proposal, educational prospectus — and get a structured 13-section investment-grade analysis in seconds. No manual reading. No guesswork.

---

## ✨ Features

- **Multi-document support** — Upload and analyze multiple PDFs, DOCX, or TXT files simultaneously
- **Domain-adaptive analysis** — Auto-detects document type (Finance, Agri, Energy, Healthcare, Real Estate, NGO, Education) and adapts all metrics accordingly
- **13-section investor report** — Overview, Key Metrics, Insights, Financial Analysis, Business Model, Strengths, Weaknesses, Risks, Opportunities, Competitive Position, Multi-doc Synthesis, Final Decision, Summary
- **Smart model fallback** — Tries 4 Groq models in sequence; never fails silently
- **Token-safe truncation** — Smart head+tail truncation respects free-tier 6K TPM limits
- **Downloadable report** — Export full analysis as `.txt` after every run
- **Beige & brown themed UI** — Clean, professional Streamlit interface

---

## 🗂️ Project Structure

```
doc_analyzer/
│
├── app.py                  # Main Streamlit application
├── key_manager.py          # API key save/load logic
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourname/doc-analyzer.git
cd doc-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Streamlit theme

Create `.streamlit/config.toml` in the project root:

```toml
[theme]
base = "light"
primaryColor = "#8b5e3c"
backgroundColor = "#f5f0e8"
secondaryBackgroundColor = "#e8dcc8"
textColor = "#3b2f1e"
font = "serif"
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📦 Requirements

```
streamlit
groq
PyPDF2
mammoth
markdown
```

Install all at once:

```bash
pip install streamlit groq PyPDF2 mammoth markdown
```

---

## 🔑 API Key Setup

1. Go to [console.groq.com](https://console.groq.com) and create a free account
2. Generate an API key from the dashboard
3. Paste it in the sidebar of the app and click **Save**
4. Key is stored locally via `key_manager.py` — never sent anywhere except Groq's API

---

## 🤖 Model Fallback Chain

The app tries models in this order until one succeeds:

| Priority | Model | Why |
|----------|-------|-----|
| 1st | `llama-3.3-70b-versatile` | Best quality, complex reasoning |
| 2nd | `meta-llama/llama-4-maverick-17b-128e-instruct` | Multilingual, multimodal |
| 3rd | `moonshotai/kimi-k2-instruct-0905` | 256K context for long docs |
| 4th | `llama-3.1-8b-instant` | Fastest, lightweight fallback |

---

## 📄 Supported Document Types

| Domain | Examples |
|--------|---------|
| Financial / Startup | Pitch decks, P&L statements, investor memos |
| Agricultural | Crop reports, co-op proposals, farm budgets |
| Energy / Infrastructure | Solar DPRs, grid reports, capex plans |
| Educational | Prospectuses, placement reports, fee structures |
| Healthcare | Hospital budgets, patient reports, insurance docs |
| Real Estate | Project brochures, valuation reports |
| NGO / Social | Grant proposals, impact reports, utilization statements |
| Mixed / Other | Any combination of the above |

---

## ⚠️ Free Tier Limitations

Groq's free tier has a **6,000 tokens-per-minute (TPM)** limit.

- Documents larger than ~9,600 characters are automatically truncated
- Truncation is smart: first 60% + last 20% of content is preserved
- A warning is shown with exact character counts when truncation occurs
- Upgrade to Groq Dev Tier at [console.groq.com/settings/billing](https://console.groq.com/settings/billing) to remove limits

---

## 📊 Sample Output Sections

1. **Document Overview** — Type, subject, purpose
2. **Key Metrics Table** — Every quantifiable figure extracted
3. **Key Insights** — 5–7 number-backed bullets
4. **Domain-Specific Analysis** — Cost structure, income drivers, subsidies
5. **Business / Operating Model** — How value is created
6. **Strengths** — With numeric proof
7. **Weaknesses** — Internal gaps quantified
8. **Risks** — Impact + likelihood + mitigation
9. **Opportunities** — Upside potential quantified
10. **Competitive Position** — vs sector benchmarks
11. **Multi-Document Synthesis** — Cross-doc comparison (if multiple uploaded)
12. **Final Decision** — PROCEED / CAUTION / PASS with justification
13. **Final Summary** — 150–200 word VC-brief style note

---

## 👨‍💻 Built By

Built for a fundraising consulting firm to automate the analysis of complex, unstructured investment documents across multiple domains.

---

## 📃 License

MIT License — free to use, modify, and distribute.
