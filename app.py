import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

st.set_page_config(page_title="Agent Instalatii", layout="wide")
st.title("Asistent Normative Proiectare Instalatii")

api_key = st.secrets.get("GOOGLE_API_KEY", "")

if not api_key:
    st.warning("Adauga cheia Google API in setarile Streamlit pentru a continua.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Meniu lateral pentru incarcarea fișierelor PDF
st.sidebar.header("Documente si Normative")
uploaded_files = st.sidebar.file_uploader(
    "Incarca normativele PDF (ex: I5, I7, P118)", 
    type=["pdf"], 
    accept_multiple_files=True
)

# Extragerea textului din PDF-urile incarcate
context_text = ""
if uploaded_files:
    for file in uploaded_files:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                context_text += extracted + "\n"
    st.sidebar.success(f"Incarcat cu succes! Procesate {len(uploaded_files)} fisiere.")

# Initializarea istoricului conversatiei
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afisarea mesajelor din istoric
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Intrebarea utilizatorului
if prompt := st.chat_input("Adreseaza o intrebare despre normative..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if context_text:
                full_prompt = (
                    "Esti un inginer expert in proiectarea instalatiilor pentru constructii. "
                    "Raspunde la intrebare bazandu-te strict pe informatiile din normativele furnizate mai jos. "
                    "Citeaza articolele si capitolele relevante daca le gasesti in text.\n\n"
                    f"TEXT NORMATIVE INCARCATE:\n{context_text}\n\n"
                    f"INTREBARE: {prompt}"
                )
            else:
                full_prompt = prompt

            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Eroare la procesare: {e}")
