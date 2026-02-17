import streamlit as st
import google.generativeai as genai
from openai import OpenAI

st.title("🤖 Alex - Tutor Inglês")
st.caption("Fale inglês! Corrijo erros (daily, fitness, filmes).")

# Tenta Gemini primeiro
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model_gem = genai.GenerativeModel('gemini-1.0-pro')  # Básico sempre OK
    st.success("✅ Gemini OK")
    use_gemini = True
except:
    st.warning("⚠️ Gemini off - OpenAI fallback")
    client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))
    use_gemini = False

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
    
    full_prompt = prompt_system + "\nHistórico:\n"
    for m in st.session_state.messages[-3:]:
        full_prompt += f"{m['role']}: {m['content']}\n"
    full_prompt += "Alex: "
    
    try:
        if use_gemini:
            model = genai.GenerativeModel('gemini-1.0-pro')
            resp = model.generate_content(full_prompt).text
        else:
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt_system}, {"role": "user", "content": user_input}]
            ).choices[0].message.content
        st.chat_message("assistant").markdown(resp)
        st.session_state.messages.append({"role": "assistant", "content": resp})
    except Exception as e:
        st.error(f"Erro: {e}")
