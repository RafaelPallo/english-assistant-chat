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
