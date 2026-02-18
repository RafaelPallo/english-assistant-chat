import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Alex Tutor", page_icon="🎓", layout="wide",
    initial_sidebar_state="expanded"
)

# CSS ESCURO PERFEITO - Bolhas coloridas e visíveis
st.markdown("""
<style>
/* Fundo escuro TOTAL */
section[data-testid="stAppViewContainer"] {background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%) !important;}
.stApp {background: transparent !important;}
main {background-color: #0f1419 !important; color: white !important;}
/* Sidebar escura */
section[data-testid="stSidebar"] {background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%) !important;}
/* Chat input escuro */
div[style*="height: auto"] > div {background-color: #1a1a2e !important;}
/* Bolhas USER (direita - AZUL) */
[data-testid="column"]:nth-of-type(2) div.block-container { 
    background: linear-gradient(135deg, #4facfe, #00f2fe) !important; 
    color: white !important; border-radius: 25px !important; padding: 1.2rem !important; 
    margin: 0.5rem 0 !important; box-shadow: 0 4px 12px rgba(79, 172, 254, 0.4) !important;
}
/* Bolhas ASSISTANT (esquerda - VERDE) */
[data-testid="column"]:nth-of-type(1) div.block-container { 
    background: linear-gradient(135deg, #43e97b, #38f9d7) !important; 
    color: #1a1a2e !important; border-radius: 25px !important; padding: 1.2rem !important; 
    margin: 0.5rem 0 !important; box-shadow: 0 4px 12px rgba(67, 233, 123, 0.4) !important;
}
/* Header */
h1 {font-family: 'Georgia'; font-size: 3rem; color: #e0e7ff !important; text-align: center; text-shadow: 2px 2px 8px rgba(0,0,0,0.9);}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Alex - Tutor Inglês")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model_name = "models/gemini-2.5-flash"
model = genai.GenerativeModel(model_name)

# Sidebar com New Chat
with st.sidebar:
    st.caption(f"🤖 {model_name}")
    if st.button("🆕 New Chat", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun()  # Força reload pra limpar visual

prompt_system = """
Você é Alex, tutor inglês gentil para brasileiros.
- Corrige APENAS 1 erro gramatical/vocab: "Good try! Use 'went' for past."
- Inglês A1-B2, 1-2 frases curtas.
- Responde ao tema (daily life, fitness, movies, amor/relationships).
- Incentive VARIADO no final: "Try again?", "What else?", "Tell me more?", "Good job! Next?", "Practice that?" (use 1x/3 respostas).
- SEM emojis, português ou repetição.
Ex: 
User: "I eated". Alex: "Good try! Say 'I ate'. What flavor?"
User: "I love movies". Alex: "Nice! What movies do you love? Tell me more."
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if user_input := st.chat_input("Digite sua frase em inglês aqui!"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)
    
    full_prompt = prompt_system + f"\nUser: {user_input}\nAlex: "
    
    with st.chat_message("assistant"):
        with st.spinner("Alex está pensando..."):
            resp = model.generate_content(full_prompt).text
            st.markdown(resp)
    st.session_state.messages.append({"role": "assistant", "content": resp})
