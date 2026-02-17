import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Alex Tutor", page_icon="🎓", layout="wide",
    initial_sidebar_state="expanded"
)

# CSS PRO
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem;}
.chat-user {background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); color: white; border-radius: 20px; padding: 1rem; margin: 0.5rem 0;}
.chat-assist {background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%); color: black; border-radius: 20px; padding: 1rem; margin: 0.5rem 0;}
.header {font-family: 'Georgia'; font-size

st.title("🤖 Alex - Tutor Inglês")
st.caption("Testando modelos...")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Lista TODOS modelos disponíveis na SUA key
models = genai.list_models()
available = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
st.write("**Modelos OK na sua key:**", available)

if not available:
    st.error("Nenhum modelo text disponível. Use OpenAI.")
    st.stop()

# Usa PRIMEIRO modelo (funciona sempre)
model_name = available[0]
model = genai.GenerativeModel(model_name)
st.success(f"✅ Usando: {model_name}")

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

if user_input := st.chat_input("Teste aqui!"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)
    
    full_prompt = prompt_system + f"\nUser: {user_input}\nAlex: "
    
    resp = model.generate_content(full_prompt).text
    st.chat_message("assistant").markdown(resp)
    st.session_state.messages.append({"role": "assistant", "content": resp})
