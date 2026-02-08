import streamlit as st
import google.generativeai as genai
from io import StringIO

# 1. API Configuration
# Replace with your actual API key from Google AI Studio
# Change "GOOGLE_API_KEY" to "GEMINI_API_KEY" to match your dashboard
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# 2. Supported Languages (Expanded to 15+)
languages = [
    "English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam", 
    "Bengali", "Marathi", "Gujarati", "Spanish", "French", "German", 
    "Chinese", "Japanese", "Korean", "Russian", "Arabic"
]

# 3. Enhanced Translation Function
def translate_text(text, source_lang, target_lang):
    try:
        # UPDATED: Using gemini-2.5-flash for 2026 compatibility
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"Translate the following text from {source_lang} to {target_lang}. Return only the translated text: {text}"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Fallback for different API versions
        return f"Technical Error: {str(e)}"

# 4. Streamlit UI Design
def main():
    st.set_page_config(page_title="TransLingua Pro", page_icon="🌐", layout="wide")
    
    # Custom Header
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🌐 TransLingua AI Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Professional AI-Powered Multi-Language Translator</p>", unsafe_allow_html=True)
    st.divider()

    # Layout: Sidebar for File Upload
    with st.sidebar:
        st.header("📁 File Upload")
        uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
        st.info("You can upload a text file to translate large content.")

    # Main Translation Interface
    col1, col2 = st.columns(2)
    
    with col1:
        src = st.selectbox("Select Source Language", languages, index=0)
    with col2:
        tar = st.selectbox("Select Target Language", languages, index=1)

    # File reading logic
    file_content = ""
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        file_content = stringio.read()

    # Input Area
    input_text = st.text_area("Enter Text:", value=file_content, height=200, placeholder="Type here or upload a file...")

  # 5. Action Buttons & Display Logic
    if st.button("🚀 Translate"):
        if input_text.strip():
            with st.spinner(f"Translating to {tar}..."):
                # Run the translation
                result = translate_text(input_text, src, tar)
                
                # Save to session state so it stays on screen
                st.session_state.translated_result = result
        else:
            st.warning("Please provide text or a file.")

    if st.button("🧹 Clear"):
        st.session_state.translated_result = ""
        st.rerun()

    st.divider()

    # 6. Horizontal Result Box (Full Width)
    if "translated_result" in st.session_state and st.session_state.translated_result:
        st.subheader("🎯 Translation Result:")
        
        # This text_area gives you the clean horizontal look you want
        st.text_area(
            label="Translated Text", 
            value=st.session_state.translated_result, 
            height=300, 
            key="output_box"
        )
        
        # Download button placed clearly below the result
        st.download_button(
            label="📥 Download Translation",
            data=st.session_state.translated_result,
            file_name=f"translated_{tar}.txt",
            mime="text/plain"
        )