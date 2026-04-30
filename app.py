import re
from dataclasses import dataclass
from typing import List, Tuple

import mammoth
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from PyPDF2 import PdfReader

load_dotenv()


@dataclass
class ParsedDocument:
    name: str
    extension: str
    text: str
    page_count: int | None = None


MODEL_CONTEXT_WINDOWS = {
    "mixtral-8x7b-32768": 32768,
    "llama3-70b-8192": 8192,
    "gemma2-9b-it": 8192,
    "llama3-8b-8192": 8192,
}


def extract_pdf_text(file) -> Tuple[str, int]:
    reader = PdfReader(file)
    page_texts = []
    for page in reader.pages:
        page_texts.append(page.extract_text() or "")
    return "\n".join(page_texts).strip(), len(reader.pages)


def extract_docx_text(file) -> str:
    result = mammoth.extract_raw_text(file)
    return result.value.strip()


def extract_txt_text(file) -> str:
    return file.getvalue().decode("utf-8", errors="ignore").strip()


def parse_uploaded_files(uploaded_files) -> Tuple[List[ParsedDocument], List[str]]:
    parsed_docs: List[ParsedDocument] = []
    warnings: List[str] = []

    for file in uploaded_files:
        name = file.name
        ext = name.lower().split(".")[-1] if "." in name else ""

        try:
            if ext == "pdf":
                text, pages = extract_pdf_text(file)
                parsed_docs.append(ParsedDocument(name=name, extension=ext, text=text, page_count=pages))
            elif ext == "docx":
                text = extract_docx_text(file)
                parsed_docs.append(ParsedDocument(name=name, extension=ext, text=text))
            elif ext == "txt":
                text = extract_txt_text(file)
                parsed_docs.append(ParsedDocument(name=name, extension=ext, text=text))
            else:
                warnings.append(f"Skipped unsupported file type: {name}")
        except Exception as err:
            warnings.append(f"Could not process {name}: {err}")

    return parsed_docs, warnings


def build_combined_text(parsed_docs: List[ParsedDocument]) -> str:
    chunks = []
    for i, doc in enumerate(parsed_docs, start=1):
        chunks.append(f"========== DOCUMENT {i}: {doc.name} ==========\n{doc.text}\n")
    return "\n".join(chunks).strip()


def detect_has_finance(text: str) -> bool:
    finance_keywords = [
        "revenue", "cost", "margin", "ebitda", "profit", "valuation", "funding", "capex", "opex", "cash flow"
    ]
    has_keyword = any(k in text.lower() for k in finance_keywords)
    has_numbers = bool(re.search(r"\$\s?\d+[\d,]*(\.\d+)?|\d+(\.\d+)?%|\b\d{4}\b", text))
    return has_keyword and has_numbers


def detect_has_technical(text: str) -> bool:
    technical_terms = [
        "hereby", "whereas", "patent", "algorithm", "architecture", "api", "compliance", "liability", "protocol"
    ]
    lowered = text.lower()
    return any(term in lowered for term in technical_terms)


def detect_non_english(text: str) -> bool:
    sample = text[:4000]
    ascii_ratio = sum(1 for c in sample if ord(c) < 128) / max(len(sample), 1)
    common_english_words = [" the ", " and ", " is ", " of ", " to ", " in "]
    english_score = sum(word in sample.lower() for word in common_english_words)
    return ascii_ratio < 0.92 or english_score <= 1


def auto_select_model(total_chars: int, has_finance: bool, has_technical: bool, non_english: bool) -> Tuple[str, str]:
    if total_chars > 25000:
        return "mixtral-8x7b-32768", "Selected for large combined input (>25,000 chars)."
    if has_finance or has_technical:
        return "llama3-70b-8192", "Selected for complex financial/technical reasoning."
    if non_english:
        return "gemma2-9b-it", "Selected for better multilingual handling."
    if total_chars <= 5000:
        return "llama3-8b-8192", "Selected for fast and efficient short-document analysis."
    return "llama3-70b-8192", "Default safe fallback model."


def apply_context_safety(text: str, model: str) -> Tuple[str, bool, int]:
    context_window = MODEL_CONTEXT_WINDOWS.get(model, 8192)

    # Conservative estimate: 1 token ≈ 4 chars
    approx_char_limit = context_window * 4

    if len(text) <= approx_char_limit:
        return text, False, approx_char_limit

    keep_chars = int(approx_char_limit * 0.8)
    return text[:keep_chars], True, approx_char_limit


def build_prompt(combined_text: str) -> str:
    return f"""
You are a world-class business analyst.
Given the document(s) below, produce a report with EXACTLY these 9 headings.
For each section:
- Write in full sentences, with bullet points, sub-headings, and tables where helpful.
- Quote relevant numbers, dates, and phrases from the text.
- If a piece of information is missing, write exactly: Not specified.
- Never add invented facts.
- Ensure every insight is explained thoroughly and is decision-ready.

Use this exact structure:

## 1. 🧾 DOCUMENT OVERVIEW
## 2. 🔑 KEY INSIGHTS
## 3. 💰 FINANCIALS (if present)
## 4. ⚙️ BUSINESS / OPERATIONAL MODEL
## 5. 🚀 STRENGTHS
## 6. ⚠️ RISKS / GAPS
## 7. 📈 OPPORTUNITIES
## 8. 🧠 DECISION INSIGHT
## 9. 📌 FINAL SUMMARY

Additional strict requirements:
- Section 2: provide 5-10 critical takeaways.
- Section 3: include markdown table(s) if financial data exists; otherwise write Not specified.
- Section 6: include likelihood and impact (High/Medium/Low) for each risk and a mitigation where possible.
- Section 8: provide one clear recommendation in 2-3 paragraphs.
- Section 9: 200-300 words condensed summary with a verdict: Proceed / Proceed with caution / Reject.

Now analyse the following text (multiple documents separated by "==========" lines):

{combined_text}
"""


def analyze_with_groq(api_key: str, model: str, combined_text: str) -> str:
    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        max_tokens=4000,
        messages=[
            {
                "role": "system",
                "content": "You are a precise and evidence-based document analyst. Never hallucinate.",
            },
            {
                "role": "user",
                "content": build_prompt(combined_text),
            },
        ],
    )

    return (response.choices[0].message.content or "").strip()


def main() -> None:
    st.set_page_config(page_title="Client Document Analyzer", page_icon="📊", layout="wide")
    st.title("📊 Client-Ready Multi-Document Analyzer")
    st.caption("Upload multiple files (PDF, DOCX, TXT), auto-select the best Groq model, and get a detailed decision-ready report.")

    if "groq_api_key" not in st.session_state:
        st.session_state.groq_api_key = ""

    with st.sidebar:
        st.header("🔐 API Configuration")
        st.session_state.groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            value=st.session_state.groq_api_key,
            help="Stored only in your current session unless you use a local .env file.",
        )

        st.header("🤖 Model Selection")
        manual_override = st.checkbox("Manually override model", value=False)
        manual_model = st.selectbox(
            "Override model",
            list(MODEL_CONTEXT_WINDOWS.keys()),
            index=1,
            disabled=not manual_override,
        )

    uploaded_files = st.file_uploader(
        "Upload one or more documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="You can upload any mix of PDF, DOCX, and TXT files.",
    )

    if not uploaded_files:
        st.warning("Please upload at least one document to begin analysis.")

    analyze_disabled = not uploaded_files
    if st.button("Analyze Documents", type="primary", disabled=analyze_disabled):
        if not st.session_state.groq_api_key.strip():
            st.error("Please enter your Groq API key in the sidebar.")
            return

        with st.spinner("Extracting text from uploaded documents..."):
            parsed_docs, warnings = parse_uploaded_files(uploaded_files)

        for warning in warnings:
            st.warning(warning)

        valid_docs = [d for d in parsed_docs if d.text.strip()]
        if not valid_docs:
            st.error("No readable text was extracted from the uploaded files.")
            return

        combined_text = build_combined_text(valid_docs)
        total_chars = len(combined_text)

        with st.spinner("Selecting best Groq model based on content characteristics..."):
            has_finance = detect_has_finance(combined_text)
            has_technical = detect_has_technical(combined_text)
            non_english = detect_non_english(combined_text)
            auto_model, reason = auto_select_model(total_chars, has_finance, has_technical, non_english)

        selected_model = manual_model if manual_override else auto_model

        st.info(
            f"Auto-selected model: **{auto_model}**  \n"
            f"Reason: {reason}  \n"
            f"Flags → finance: `{has_finance}`, technical/legal: `{has_technical}`, non-English: `{non_english}`  \n"
            f"Final model in use: **{selected_model}**"
        )

        safe_text, was_truncated, approx_char_limit = apply_context_safety(combined_text, selected_model)
        if was_truncated:
            st.warning(
                "Input exceeded the selected model context window. "
                f"Used truncation safety: kept first 80% within approx {approx_char_limit} chars."
            )

        with st.spinner("Asking Groq for detailed analysis..."):
            try:
                report = analyze_with_groq(st.session_state.groq_api_key.strip(), selected_model, safe_text)
            except Exception as err:
                st.error(
                    "Groq API request failed. Please verify your API key, model availability, and rate limits. "
                    f"Details: {err}"
                )
                return

        st.success("Analysis generated successfully.")
        st.markdown("# 📊 Document Analysis Report")
        st.markdown(report)

        with st.expander("📄 Extracted document details"):
            for i, doc in enumerate(valid_docs, start=1):
                page_info = f" | Pages: {doc.page_count}" if doc.page_count is not None else ""
                st.markdown(f"**{i}. {doc.name}** ({doc.extension.upper()}){page_info} | Characters: {len(doc.text)}")
            st.markdown(f"**Combined characters:** {total_chars}")

        with st.expander("🧪 Combined extracted text preview"):
            st.text_area("Combined Text", combined_text[:12000], height=350)


if __name__ == "__main__":
    main()
