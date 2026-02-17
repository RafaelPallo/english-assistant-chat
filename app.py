import streamlit as st
import openai

# Configura API do secrets.toml
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# System prompt do Alex (seu tutor)
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

st.title("🤖 Alex - Seu Tutor de Inglês")
st.caption("Fale em inglês! Eu corrijo gentil e converso sobre daily, fitness, filmes.")

# Inicializa histórico (inclui system prompt)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Mostra chat history
for msg in st.session_state.messages[1:]:
    role = msg["role"]
    content = msg["content"]
    with st.chat_message(role):
        st.markdown(content)

# Chat input
if prompt := st.chat_input("Digite sua frase em inglês aqui..."):
    # Adiciona mensagem user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera e mostra resposta
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
        )
        resp = response.choices[0].message.content
        st.markdown(resp)
        # Salva no histórico
        st.session_state.messages.append({"role": "assistant", "content": resp})
