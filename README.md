# Client-Ready Multi-Document Analyzer (Streamlit + Groq)

This project is a local Streamlit app that lets you upload multiple documents (PDF, DOCX, TXT), extract clean text, automatically choose the best Groq model, and generate a very detailed, decision-ready report using a strict 9-section framework.

## Folder Structure

```text
doc_analyzer/
├── app.py
├── requirements.txt
├── .env                   # optional
└── README.md
```

## What the app does

- Upload multiple files in any mix: PDF, DOCX, TXT.
- Extract clean text from all files.
- Combine extracted text with clear separators by document.
- Auto-select a Groq model based on text size and content characteristics.
- Generate a detailed, structured, client-friendly report with strict anti-hallucination instructions.

## 9-Section Analysis Framework

The generated report uses exactly these sections:

1. 🧾 DOCUMENT OVERVIEW  
2. 🔑 KEY INSIGHTS  
3. 💰 FINANCIALS (if present)  
4. ⚙️ BUSINESS / OPERATIONAL MODEL  
5. 🚀 STRENGTHS  
6. ⚠️ RISKS / GAPS  
7. 📈 OPPORTUNITIES  
8. 🧠 DECISION INSIGHT  
9. 📌 FINAL SUMMARY

If data is missing, the model is instructed to write: **Not specified**.

## Auto-Model Selection Logic

The app inspects combined text and chooses:

1. If total chars > 25,000 → `mixtral-8x7b-32768`
2. Else if finance or technical/legal content is detected → `llama3-70b-8192`
3. Else if non-English is detected → `gemma2-9b-it`
4. Else if chars <= 5,000 → `llama3-8b-8192`
5. Else fallback → `llama3-70b-8192`

### Truncation Safety

If input exceeds the selected model context, the app keeps the **first 80%** of text within a conservative context estimate and shows a warning.

---

## Beginner Setup (Step-by-Step)

### 1) Install Python
Install Python 3.9+ and verify:

```bash
python --version
```

### 2) Create project folder
Create a folder named `doc_analyzer` and place these files inside it:
- `app.py`
- `requirements.txt`
- `README.md`

### 3) Install dependencies
Open terminal in that folder and run:

```bash
pip install -r requirements.txt
```

### 4) Get a Groq API key
1. Go to `https://console.groq.com`
2. Sign up / log in
3. Create an API key
4. Copy it

### 5) (Optional) Use `.env`
Create a `.env` file if you want local key management:

```env
GROQ_API_KEY=your_key_here
```

### 6) Run the app

```bash
streamlit run app.py
```

### 7) Use the app
1. Paste Groq API key in sidebar
2. Upload one or more files (PDF, DOCX, TXT)
3. Click **Analyze Documents**
4. Read and copy the generated consultant-style report

## Error Handling Included

- No files uploaded: analysis button disabled + warning.
- Unsupported files: skipped with warning.
- Empty extraction: clear error.
- Missing API key: clear error.
- Groq API failures: user-friendly message.

## Notes

- Runs fully local (no database, no cloud storage).
- API key is kept in session state unless you choose to use `.env`.
- Output is markdown formatted and easy to copy into email or Word docs.
