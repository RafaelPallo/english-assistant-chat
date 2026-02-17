import streamlit as st
import openai
from streamlit_chat import message  # Não precisa, mas opcional; use st.chat_message

# Configura API (key vai em secrets.toml no deploy)
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# System prompt do tutor
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

# Inicializa chat history na session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Título da app
st.title("🤖 Alex - Seu Tutor de Inglês")
st.caption("Fale em inglês! Eu corrijo gentil e converso sobre daily, fitness, filmes.")

# Exibe histórico do chat
for message in st.session_state.messages[1:]:  # Pula system
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    else:
        st.chat_message("assistant").markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua frase em inglês aqui..."):
    # Adiciona user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Gera resposta
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
        )
        resp = response.choices[0].message.content
        st.markdown(resp)
        st.session_state.messages.append({"role": "assistant", "content": resp})
