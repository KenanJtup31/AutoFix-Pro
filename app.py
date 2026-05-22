import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# Səhifə Ayarları
st.set_page_config(page_title="AutoFix Pro AI", page_icon="🚗", layout="centered")

# CSS Dizayn
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #f8f9fa; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# API Girişi
API_KEY = "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"
client = Groq(api_key=API_KEY)

st.markdown("<h1 style='text-align: center;'>🛠️ AvtoFix Pro AI</h1>", unsafe_allow_html=True)

# Modellər
models = {
    "Mercedes-Benz": "https://www.carlogos.org/car-logos/mercedes-benz-logo.png",
    "BMW": "https://www.carlogos.org/car-logos/bmw-logo.png",
    "Lada 2107": "https://seeklogo.com/images/L/lada-logo-A27757917C-seeklogo.com.png",
    "Lada 2106": "https://seeklogo.com/images/L/lada-logo-A27757917C-seeklogo.com.png",
    "Toyota": "https://www.carlogos.org/car-logos/toyota-logo.png",
    "Audi": "https://www.carlogos.org/car-logos/audi-logo.png"
}

if "selected_model" not in st.session_state: st.session_state.selected_model = None
if "messages" not in st.session_state: st.session_state.messages = []

# Məntiq
if st.session_state.selected_model is None:
    cols = st.columns(3)
    for i, (name, img_url) in enumerate(models.items()):
        with cols[i % 3]:
            st.image(img_url, width=80)
            if st.button(name):
                st.session_state.selected_model = name
                st.rerun()
else:
    if st.button("⬅️ Geri qayıt"):
        st.session_state.selected_model = None
        st.session_state.messages = []
        st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"{st.session_state.selected_model} problemi nədir?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # DAHA DƏQİQ MƏNTİQ
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Sən peşəkar avtomexaniksən. Cavab verərkən yalnız dəqiq avtomobil terminlərindən istifadə et (məsələn: şam, karbürator, porşen, distribyutor). 'Quyu', 'lövhə', 'göbələk' kimi yalnış sözlər işlətmə. Hər problemi mərhələli (addım-addım) izah et."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                
                # Şəkil axtarışı (Yalnız texniki terminlər olduqda)
                if len(prompt) > 5:
                    with st.spinner("🔍 Texniki diaqramlar axtarılır..."):
                        with DDGS() as ddgs:
                            query = f"{st.session_state.selected_model} {prompt} parts diagram technical"
                            results = list(ddgs.images(query, max_results=1))
                            for res in results:
                                st.image(res['image'], caption="Texniki diaqram")
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception:
                st.error("Bağlantı xətası: AI cavab vermədi. Yenidən cəhd et.")
            
