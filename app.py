import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Alex Tutor", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# CSS (mantido igual)
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

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("models/gemini-2.5-flash-exp")  # Modelo LEVE, quota maior
except:
    st.error("❌ **GEMINI_API_KEY** não encontrada em secrets.toml. Adicione no Streamlit Cloud > Settings > Secrets.")
    st.stop()

# Sidebar
with st.sidebar:
    st.caption("🤖 gemini-2.5-flash-exp")
    if st.button("🆕 New Chat", use_container_width=True, type="primary"):
        for key in ["messages", "level", "motivo"]:
            st.session_state[key] = None if key != "messages" else []
        st.rerun()

# Session state
for key in ["messages", "level", "motivo"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "messages" else None

# PASSO 1: NÍVEL
if st.session_state.level is None:
    st.markdown("### 👋 **Passo 1:** Escolha seu nível!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🥚 Pré-iniciante (A1)"): st.session_state.level = "A1"; st.rerun()
        if st.button("🚀 Iniciante (A2)"): st.session_state.level = "A2"; st.rerun()
    with col2:
        if st.button("⭐ Intermediário (B1-B2)"): st.session_state.level = "B1-B2"; st.rerun()
        if st.button("🔥 Avançado (C1-C2)"): st.session_state.level = "C1-C2"; st.rerun()
    st.stop()

# PASSO 2: MOTIVO
if st.session_state.motivo is None:
    st.markdown(f"### 🎯 **Passo 2:** Seu motivo?")
    motivos = ["Fins acadêmicos", "Viagens e turismo", "Emprego e carreira", "Imigração", "Amigos", "Testes/certificados", "Outro"]
    col1, col2, col3 = st.columns(3)
    for i, m in enumerate(motivos):
        col = [col1, col2, col3][i%3]
        if col.button(f"📌 {m}"): st.session_state.motivo = m; st.rerun()
    st.stop()

st.sidebar.success(f"✅ Nível: **{st.session_state.level}**")
st.sidebar.success(f"🎯 Motivo: **{st.session_state.motivo}**")

# FUNÇÃO GENERATE COM RETRY e LIMITE (fixa ResourceExhausted)
@st.cache_data
def generate_response(_prompt):
    for tentativa in range(3):  # 3 tentativas
        try:
            # Encurta prompt pra <1000 tokens
            short_prompt = _prompt[:2000]  # Limite seguro
            resp = model.generate_content(
                short_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=150,  # Resposta curta, menos quota
                    temperature=0.7
                )
            )
            return resp.text
        except Exception as e:
            if "ResourceExhausted" in str(e) or tentativa == 2:
                return f"😅 Quota Gemini esgotada (tente em 1h). Exemplo {st.session_state.level}: 'Good! Say ...' about {st.session_state.motivo}."
            time.sleep(2 ** tentativa)  # Backoff 1s, 2s, 4s
    return "Erro de API. Tente New Chat."

# Prompt otimizado (curto)
level_prompts = {"A1": "Basic words on {motivo}", "A2": "Simple sentences {motivo}", "B1-B2": "Medium {motivo}", "C1-C2": "Advanced {motivo}"}
prompt_system = f"""Alex tutor nível {st.session_state.level}: {level_prompts[st.session_state.level].format(motivo=st.session_state.motivo)}.
Fale SÓ sobre {st.session_state.motivo}. Corrija 1 erro. Incentive: 'Tell more?'."""

# Chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if user_input := st.chat_input("Fale sobre seu motivo!"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)
    
    full_prompt = prompt_system + f"\nUser: {user_input}\nAlex:"
    
    with st.chat_message("assistant"):
        with st.spinner("Alex pensando..."):
            resp = generate_response(full_prompt)
            st.markdown(resp)
    st.session_state.messages.append({"role": "assistant", "content": resp})
