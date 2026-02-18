import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Alex Tutor", page_icon="🎓", layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para tema ESCURO com bolhas de chat perfeitas
st.markdown("""
<style>
/* Tema escuro geral */
section[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
}
.stApp { background: transparent !important; }

/* Container principal escuro */
main { background-color: #0f1419; }

/* Bolhas de chat - USER (direita, azul) */
div[data-testid="stHorizontalBlock"] > div:nth-child(2) > div > div.block-container {
    padding: 1rem; margin: 0.5rem 0; border-radius: 20px;
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%) !important;
    color: white !important; font-weight: 500;
}

/* Bolhas de chat - ASSISTANT (esquerda, verde) */
div[data-testid="stHorizontalBlock"] > div:nth-child(1) > div > div.block-container {
    padding: 1rem; margin: 0.5rem 0; border-radius: 20px;
    background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%) !important;
    color: black !important; font-weight: 500;
}

/* Header */
h1 {font-family: 'Georgia'; font-size: 3rem; color: #ffffff; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);}

/* Chat input escuro */
div[data-testid="stChatInput"] { background-color: #1a1a2e !important; }

/* Sidebar escura */
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%); }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Alex - Tutor Inglês")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model_name = "models/gemini-2.5-flash"
model = genai.GenerativeModel(model_name)

# Sidebar com botão New Chat FUNCIONAL
with st.sidebar:
    st.caption(f"🤖 {model_name}")
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = []  # Limpa o chat

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

# Mostra mensagens
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input do usuário
if user_input := st.chat_input("Teste aqui!"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)
    
    full_prompt = prompt_system + f"\nUser: {user_input}\nAlex: "
    
    with st.chat_message("assistant"):
        resp = model.generate_content(full_prompt).text
        st.markdown(resp)
    st.session_state.messages.append({"role": "assistant", "content": resp})
