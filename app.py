import streamlit as st
from groq import Groq

# 1. Konfiqurasiya
st.set_page_config(page_title="AvtoFix Pro AI", layout="wide")
client = Groq(api_key="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")

# 2. Dizayn
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🛠️ AvtoFix Pro AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Maşın modelini və problemi yaz, AI dərhal təmir yolunu göstərsin.</p>", unsafe_allow_html=True)

# 3. Söhbət Tarixçəsi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. İstifadəçi girişi
if prompt := st.chat_input("Məsələn: Lada 2107 mühərrik səs edir..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI Diaqnostika
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Sən peşəkar avtomobil mühəndisisən. Azərbaycan dilində cavab verirsən. Problemi analiz et, səbəbi yaz və 3 addımda həll yolunu göstər."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
            )
            cavab = response.choices[0].message.content
            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
        except Exception as e:
            st.error("Sistemdə müvəqqəti xəta yarandı. Yenidən cəhd et.")
          
