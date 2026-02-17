import streamlit as st
import google.generativeai as genai

st.title("🤖 Alex - Tutor Inglês")
st.caption("Fale inglês! Corrijo erros (daily, fitness, filmes).")

# Config
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')  # Sempre funciona free

prompt_system = """
Você é Alex, tutor inglês gentil brasileiros.
Corrige 1 erro: "Good! Use 'went' past."
Inglês A1-B2, 1-2 frases.
Incentive: "Practice?"
Temas: daily, fitness, filmes.
SEM emojis/português.
Ex: User: "I eated". Alex: "Good! 'I ate'. Flavor?"
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if user_input := st.chat_input("Ex: 'I go gym yesterday'..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)
    
    # Prompt completo com histórico
    full_prompt = prompt_system + "\nHistórico:\n"
    for m in st.session_state.messages:
        full_prompt += f"{m['role']}: {m['content']}\n"
    full_prompt += f"User: {user_input}\nAlex: "
    
    resp = model.generate_content(full_prompt).text
    st.chat_message("assistant").markdown(resp)
    st.session_state.messages.append({"role": "assistant", "content": resp})
