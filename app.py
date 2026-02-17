import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Alex Tutor", page_icon="🎓", layout="wide",
    initial_sidebar_state="expanded"
)

# CSS PRO
st.markdown("""
<style>
/* Fundo principal */
section[data-testid="stAppViewContainer"] {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
.stApp {background: transparent !important;}
/* Bubbles chat */
div[data-testid="stHorizontalBlock"] > div > div {border-radius: 20px; padding: 1rem; margin: 0.5rem 0;}
/* User */
.st-md a[href]:nth-of-type(1) {background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%) !important; color: white;}
/* Assist */
.st-md a[href]:nth-of-type(2) {background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%) !important; color: black;}
/* Header */
h1 {font-family: 'Georgia'; font-size: 3rem; color: white; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);}
</style>
""", unsafe_allow_html=True)



st.title("🤖 Alex - Tutor Inglês")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Direto pro melhor modelo (sem lista debug)
model_name = "models/gemini-2.5-flash"  # Seu top da key
model = genai.GenerativeModel(model_name)

# Sidebar info discreta (opcional, pro seu debug)
with st.sidebar:
    st.caption(f"🤖 {model_name}")


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

