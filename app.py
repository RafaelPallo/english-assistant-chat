import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Alex Tutor", page_icon="🎓", layout="wide",
    initial_sidebar_state="expanded"
)

# CSS ESCURO (mantido)
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
        st.session_state.motivo = None
        st.rerun()

# Inicializa session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "level" not in st.session_state:
    st.session_state.level = None
if "motivo" not in st.session_state:
    st.session_state.motivo = None

# PASSO 1: ESCOLHER NÍVEL
if st.session_state.level is None:
    st.markdown("### 👋 **Passo 1:** Escolha seu nível de Inglês!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🥚 **Pré-iniciante (A1)**", use_container_width=True):
            st.session_state.level = "A1"
            st.rerun()
        if st.button("🚀 **Iniciante (A2)**", use_container_width=True):
            st.session_state.level = "A2"
            st.rerun()
    with col2:
        if st.button("⭐ **Intermediário (B1-B2)**", use_container_width=True):
            st.session_state.level = "B1-B2"
            st.rerun()
        if st.button("🔥 **Avançado (C1-C2)**", use_container_width=True):
            st.session_state.level = "C1-C2"
            st.rerun()
    st.stop()

# PASSO 2: ESCOLHER MOTIVO
if st.session_state.motivo is None:
    st.markdown(f"### 🎯 **Passo 2:** Qual seu principal motivo para aprender inglês?")
    motivos = [
        "Fins acadêmicos, universidade e educação",
        "Viagens e turismo",
        "Emprego e carreira",
        "Imigração e vida no exterior",
        "Melhorar comunicação com amigos",
        "Testes e certificados de idiomas",
        "Outro"
    ]
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for i, motivo in enumerate(motivos):
        with cols[i % 3]:
            if st.button(f"📌 **{motivo[:30]}...**", use_container_width=True):
                st.session_state.motivo = motivo
                st.rerun()
    st.stop()

# MOSTRA CONFIGURAÇÕES
st.sidebar.success(f"✅ **Nível:** {st.session_state.level}")
st.sidebar.success(f"🎯 **Motivo:** {st.session_state.motivo}")

# Prompt adaptado: NÍVEL + MOTIVO
level_prompts = {
    "A1": "Use ONLY basic words related to {motivo}. 1-word answers.",
    "A2": "Simple sentences about {motivo}. Correct 1 basic error.",
    "B1-B2": "Medium sentences focused on {motivo}. Vary topics inside it.",
    "C1-C2": "Advanced discussion ONLY on {motivo}. Challenge vocabulary/grammar."
}

motivo_key = st.session_state.motivo.lower().replace(" ", "_").replace(",", "").replace("é", "e")
prompt_system = f"""
Você é Alex, tutor inglês gentil para brasileiros.
Nível: {st.session_state.level} - {level_prompts[st.session_state.level].format(motivo=st.session_state.motivo)}
FALE APENAS SOBRE '{st.session_state.motivo}' - conecte TODAS respostas a este tema.
- Corrige APENAS 1 erro gramatical/vocab por resposta.
- Inglês adaptado ao nível, 1-2 frases curtas.
- Incentive: "Try again?", "What else about {motivo_key}?", "Tell me more!", "Good job! Next?", "Practice that?".
- SEM emojis, português, repetição ou sair do tema.
Ex: User (Viagens A1): "hotel". Alex: "Good! Hotel is place to sleep. What color?"
"""

# Chat liberado
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if user_input := st.chat_input("Fale sobre seu motivo em inglês!"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)
    
    full_prompt = prompt_system + f"\nUser: {user_input}\nAlex: "
    
    with st.chat_message("assistant"):
        with st.spinner("Alex focando no seu motivo..."):
            resp = model.generate_content(full_prompt).text
            st.markdown(resp)
    st.session_state.messages.append({"role": "assistant", "content": resp})
