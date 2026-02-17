import streamlit as st
import google.generativeai as genai

# Seu system prompt PRIMEIRO
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

# Configura Gemini DEPOIS do prompt
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-exp', system_instruction=system_prompt)
    st.success("✅ Gemini conectado! Alex pronto.")
except Exception as e:
    st.error(f"❌ Erro conexão: {str(e)}")
    st.stop()

st.title("🤖 Alex - Seu Tutor de Inglês")
st.caption("Fale em inglês! Corrijo erros e converso daily, fitness, filmes.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Digite aqui (ex: 'I go gym yesterday')..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            resp = response.text
            st.markdown(resp)
            st.session_state.messages.append({"role": "assistant", "content": resp})
        except Exception as e:
            st.error(f"Erro resposta: {str(e)}")
