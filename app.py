import streamlit as st
import google.generativeai as genai
import os

# Setam titlul si configuratia paginii
st.set_page_config(page_title="Agent Instalatii", layout="wide")
st.title("Asistent Normative Proiectare Instalatii")

# Preluam cheia API (o vom introduce ulterior dintr-un meniu securizat in Streamlit)
api_key = st.secrets.get("GOOGLE_API_KEY", "")

if not api_key:
    st.warning("Adauga cheia Google API in setarile Streamlit pentru a continua.")
    st.stop()

# Configuram modelul
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Initializam istoricul conversatiei
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afisam mesajele anterioare
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gestionam input-ul utilizatorului
if prompt := st.chat_input("Adreseaza o intrebare despre normative..."):
    # Adaugam si afisam mesajul utilizatorului
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generam raspunsul cu Gemini
    with st.chat_message("assistant"):
        try:
            # Apelam modelul cu mesajul utilizatorului
            response = model.generate_content(prompt)
            st.markdown(response.text)
            # Salvam raspunsul in istoric
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Eroare de conexiune cu API-ul: {e}")
