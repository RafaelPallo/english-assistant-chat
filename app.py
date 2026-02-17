import streamlit as st
import google.generativeai as genai

system_prompt = """
Você é Alex, tutor de inglês gentil para brasileiros iniciantes.
- Corrige APENAS 1 erro por frase: "Bom! Use 'went' no passado."
- Fale inglês simples A1-B2, 1-2 frases curtas.
- Incentive: "Pratique mais?" ou "What next?"
- Temas: daily life, fitness, nutrition, filmes com plot twists, classics.
- SEM emojis. SEM português nas respostas.
Exemplo:
User: "I eated apple yesterday."
Alex: "Good try! Say 'I ate an apple yesterday'. What flavor?"
"""

# Testa conexão e lista modelos
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    st.success(f"✅ Conectado! Modelos disponíveis: {len(models)}")
    model = genai.GenerativeModel('gemini-1.5-flash')  # Seguro, funciona sempre
except Exception as e:
    st.error(f"❌ Erro: {str(e)}")
    st.stop()

st.title("🤖 Alex - Seu Tutor de Inglês")
st.caption("Fale inglês! Corrijo gentil (daily, fitness, filmes).")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ex: 'I go gym yesterday'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = model.generate_content(prompt, stream=False)
        resp = response.text
        st.markdown(resp)
        st.session_state.messages.append({"role": "assistant", "content": resp})
