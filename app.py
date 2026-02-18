import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Alex Tutor", page_icon="🎓", layout="wide",
    initial_sidebar_state="expanded"
)

# CSS ESCURO (mantido do anterior)
st.markdown("""
<style>
section[data-testid="stAppViewContainer"] {background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%) !important;}
.stApp {background: transparent !important;}
main {background-color: #0f1419 !important; color: white !important;}
section[data-testid="stSidebar"] {background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%) !important;}
[data-testid="column"]:nth-of-type(2) div.block-container { background: linear-gradient(135deg, #4facfe, #00f2fe) !important; color: white !important; border-radius: 25px !important; padding: 1.2rem !important; margin: 0.5rem 0 !important; box-shadow: 0 4px 12px rgba(79, 172, 254, 0.4) !important; }
[data-testid="column"]:nth-of-type(1) div.block-container { background: linear-gradient(135deg, #43e97b, #38f9d7) !important; color: #1a1a2e !important; border-radius: 25px !important; padding: 1.2rem !important; margin: 0.5rem 0 !important; box-shadow: 0 4px 12px rgba(67, 233, 123, 0.4) !important; }
h1 {font-family: 'Georgia'; font-size: 3rem; color: #e0e7ff !important; text-align: center; text-shadow: 2px 2px 8px rgba(0,0,0,0.9);}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Alex - Tutor Inglês")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model_name = "models/gemini-2.5-flash"
model = genai.GenerativeModel(model_name)

# Sidebar
with st.sidebar:
    st.caption(f"🤖 {model_name}")
    if st.button("🆕 New Chat", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.level = None
        st.rerun()

# Inicializa session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "level" not in st.session_state:
    st.session_state.level = None

# SELEÇÃO DE NÍVEL - BLOQUEIA CHAT ATÉ ESCOLHER
if st.session_state.level is None:
    st.markdown("### 👋 Escolha seu nível de Inglês para começar!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🥚 **Pré-iniciante (A1)**", use_container_width=True, type="secondary"):
            st.session_state.level = "A1"
            st.rerun()
        if st.button("🚀 **Iniciante (A2)**", use_container_width=True, type="secondary"):
            st.session_state.level = "A2"
            st.rerun()
    with col2:
        if st.button("⭐ **Intermediário (B1-B2)**", use_container_width=True, type="primary"):
            st.session_state.level = "B1-B2"
            st.rerun()
        if st.button("🔥 **Avançado (C1-C2)**", use_container_width=True, type="primary"):
            st.session_state.level = "C1-C2"
            st.rerun()
    
    st.info("💡 Clique no seu nível! Alex vai adaptar frases, vocabulário e correções.")
    st.stop()  # Para aqui até escolher

# Prompt adaptado por nível
level_prompts = {
    "A1": "Use ONLY basic words (hello, eat, go). 1-word answers. Correct gently: 'Good! Say \"hello\".'",
    "A2": "Simple sentences (I like...). 1-2 short sentences. Correct 1 error: 'Nice! Use \"go\" not \"goes\".'",
    "B1-B2": "Medium vocab (movies, gym, love). 2 sentences. Vary incentives: 'Tell more?', 'Good job!'",
    "C1-C2": "Advanced topics (relationships, plot twists). Complex grammar. Challenge: 'Why that tense? Explain.'"
}

prompt_system = f"""
Você é Alex, tutor inglês gentil para brasileiros no nível {st.session_state.level}.
{level_prompts[st.session_state.level]}
- Corrige APENAS 1 erro gramatical/vocab.
- Inglês adaptado ao nível, 1-2 frases curtas.
- Incentive VARIADO: "Try again?", "What else?", "Tell me more?", "Good job! Next?", "Practice that?".
- SEM emojis, português ou repetição.
"""

st.sidebar.success(f"✅ Nível: **{st.session_state.level}**")

# Chat normal (após nível escolhido)
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if user_input := st.chat_input("Digite sua frase em inglês!"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)
    
    full_prompt = prompt_system + f"\nUser: {user_input}\nAlex: "
    
    with st.chat_message("assistant"):
        with st.spinner("Alex respondendo..."):
            resp = model.generate_content(full_prompt).text
            st.markdown(resp)
    st.session_state.messages.append({"role": "assistant", "content": resp})
