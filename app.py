import streamlit as st
import google.generativeai as genai

# Config PRO
st.set_page_config(
    page_title="Alex - Tutor Inglês AI", page_icon="🎓", 
    layout="wide", initial_sidebar_state="expanded"
)

# CSS Layout BONITO
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); min-height: 100vh;}
.stApp {background: transparent !important;}
.header {font-family: 'Segoe UI', sans-serif; font-size: 3.5rem; color: white; text-align: center; text-shadow
