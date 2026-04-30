import os
from io import StringIO

import streamlit as st
import mammoth
from PyPDF2 import PdfReader


# -----------------------------
# Text extraction helpers
# -----------------------------

def extract_text_from_docx(file) -> str:
    """Extract plain text from a DOCX file using mammoth."""
    result = mammoth.extract_raw_text(file)
    return result.value.strip()


def extract_text_from_pdf(file) -> str:
    """Extract text from a PDF file using PyPDF2."""
    reader = PdfReader(file)
    pages_text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        pages_text.append(page_text)
    return "\n".join(pages_text).strip()


def extract_text_from_txt(file) -> str:
    """Extract text from a TXT file."""
    content = file.getvalue().decode("utf-8", errors="ignore")
    return StringIO(content).read().strip()


def extract_text(uploaded_file) -> str:
    """Route file to the correct extraction function based on extension."""
    filename = uploaded_file.name.lower()

    if filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    if filename.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)

    raise ValueError("Unsupported file type. Please upload DOCX, PDF, or TXT.")


# -----------------------------
# LLM analysis helper
# -----------------------------

def build_prompt(document_text: str) -> str:
    return f"""
You are a strict business document analyst.
Analyze ONLY the provided text. Do not hallucinate.
If any section data is unavailable, write exactly: Not specified.
Keep output concise, structured, professional, and decision-ready.

Use this EXACT structure and numbering:

1. 🧾 DOCUMENT OVERVIEW
2. 🔑 KEY INSIGHTS
3. 💰 FINANCIALS (if present)
4. ⚙️ BUSINESS / OPERATIONAL MODEL
5. 🚀 STRENGTHS
6. ⚠️ RISKS / GAPS
7. 📈 OPPORTUNITIES
8. 🧠 DECISION INSIGHT
9. 📌 FINAL SUMMARY

Document text:
"""
{document_text}
"""
"""


def analyze_with_openai(document_text: str, api_key: str, model: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You are a precise, factual document analysis assistant.",
            },
            {
                "role": "user",
                "content": build_prompt(document_text),
            },
        ],
    )
    return response.choices[0].message.content.strip()


def analyze_with_groq(document_text: str, api_key: str, model: str) -> str:
    from groq import Groq

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You are a precise, factual document analysis assistant.",
            },
            {
                "role": "user",
                "content": build_prompt(document_text),
            },
        ],
    )
    return response.choices[0].message.content.strip()


# -----------------------------
# Streamlit UI
# -----------------------------

def main() -> None:
    st.set_page_config(page_title="Document Analyzer", page_icon="📄", layout="centered")

    st.title("📄 Document Analysis App")
    st.write("Upload a document, extract text, and generate a structured AI summary.")

    with st.sidebar:
        st.header("⚙️ Settings")
        provider = st.selectbox("LLM Provider", ["OpenAI", "Groq"], index=0)

        if provider == "OpenAI":
            api_key = st.text_input("OpenAI API Key", type="password")
            default_model = "gpt-4o-mini"
            model = st.text_input("OpenAI Model", value=default_model)
        else:
            api_key = st.text_input("Groq API Key", type="password")
            default_model = "llama-3.1-8b-instant"
            model = st.text_input("Groq Model", value=default_model)

    uploaded_file = st.file_uploader(
        "Upload file", type=["docx", "pdf", "txt"], help="Supported formats: DOCX, PDF, TXT"
    )

    analyze_clicked = st.button("Analyze Document", type="primary")

    if analyze_clicked:
        if not uploaded_file:
            st.error("Please upload a file before clicking Analyze Document.")
            return

        if not api_key.strip():
            st.error("Please enter a valid API key in the sidebar.")
            return

        try:
            raw_text = extract_text(uploaded_file)
        except ValueError as file_error:
            st.error(str(file_error))
            return
        except Exception as extraction_error:
            st.error(f"Failed to extract text: {extraction_error}")
            return

        if not raw_text.strip():
            st.error("The file appears empty or no readable text was found.")
            return

        # Limit payload sent to model (2000-3000 chars requirement)
        max_chars = 2500
        truncated_text = raw_text[:max_chars]

        if len(raw_text) > max_chars:
            st.info(f"Document text was truncated to {max_chars} characters before AI analysis.")

        with st.spinner("Analyzing document..."):
            try:
                if provider == "OpenAI":
                    analysis = analyze_with_openai(truncated_text, api_key, model)
                else:
                    analysis = analyze_with_groq(truncated_text, api_key, model)
            except Exception as ai_error:
                st.error(f"AI analysis failed: {ai_error}")
                return

        st.success("Analysis complete!")
        st.subheader("📌 Structured Analysis")
        st.markdown(analysis)

        with st.expander("Preview extracted text"):
            st.text_area("Extracted text", raw_text, height=250)


if __name__ == "__main__":
    main()
