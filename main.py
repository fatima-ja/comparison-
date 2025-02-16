import streamlit as st
import fitz  # PyMuPDF for extracting text from PDFs
from groq import Groq

api_key = "GROQ_API_KEY"  # Replace with your Groq API key
client = Groq(api_key=api_key)



def extract_text_from_pdf(pdf_file):
    """Extracts text from an uploaded PDF file."""
    pdf_reader = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join(page.get_text("text") for page in pdf_reader)
    return text

def query_groq(query, context):
    """Sends a legal query to Groq API with extracted document context."""
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a legal expert. Provide precise legal analysis."},
            {"role": "user", "content": f"Context: {context[:4000]}\n\nQuery: {query}"}  # Limit text to 4000 chars
        ],
        model="deepseek-r1-distill-llama-70b",
        temperature=0.7,
        max_tokens=256,
    )
    return chat_completion.choices[0].message.content
# Streamlit UI
st.title("📜 Legal Document Analyzer")

uploaded_file = st.file_uploader("Upload a Legal PDF", type="pdf")

if uploaded_file:
    st.success("✅ PDF uploaded successfully!")
    extracted_text = extract_text_from_pdf(uploaded_file)

    query = st.text_input("🔍 Ask a legal question about the document:")

    if query:
        st.write("### 🏛️ Answer:")
        answer = query_groq(query, extracted_text)
        st.write(answer)