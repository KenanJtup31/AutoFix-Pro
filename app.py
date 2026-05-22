import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# 1. Səhifə Ayarları
st.set_page_config(page_title="AutoFix Pro AI", page_icon="🚗", layout="centered")

# CSS Dizaynı
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #f8f9fa; border: 1px solid #ddd; }
    .developed-by { text-align: center; color: #888; font-size: 14px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. API
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Üst Başlıq
st.markdown("<div class='developed-by'>Developed by Kenan Elizade</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>🛠️ AvtoFix Pro AI</h1>", unsafe_allow_html=True)

models = {
    "Mercedes-Benz": "https://www.carlogos.org/car-logos/mercedes-benz-logo.png",
    "BMW": "https://www.carlogos.org/car-logos/bmw-logo.png",
    "Lada 2107": "https://seeklogo.com/images/L/lada-logo-A27757917C-seeklogo.com.png",
    "Lada 2106": "https://seeklogo.com/images/L/lada-logo-A27757917C-seeklogo.com.png",
    "Toyota": "https://www.carlogos.org/car-logos/toyota-logo.png",
    "Hyundai": "https://www.carlogos.org/car-logos/hyundai-logo.png",
    "Audi": "https://www.carlogos.org/car-logos/audi-logo.png",
    "Kia": "https://www.carlogos.org/car-logos/kia-logo.png"
}

if "selected_model" not in st.session_state: st.session_state.selected_model = None
if "messages" not in st.session_state: st.session_state.messages = []

# Məntiq
if st.session_state.selected_model is None:
    st.markdown("<h4 style='text-align: center;'>Maşın modelini seçin:</h4>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (name, img_url) in enumerate(models.items()):
        with cols[i % 3]:
            st.image(img_url, width=80)
            if st.button(name):
                st.session_state.selected_model = name
                st.rerun()
else:
    st.markdown(f"### 🚗 {st.session_state.selected_model} Diaqnostika")
    if st.button("⬅️ Geri qayıt"):
        st.session_state.selected_model = None
        st.session_state.messages = []
        st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"{st.session_state.selected_model} üçün probleminiz nədir?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # 1. AI Cavabı
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"Sən peşəkar avtomobil mühəndisisən. {st.session_state.selected_model} üçün verilən problemin səbəbini və addım-addım həll yolunu izah et."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                
                # 2. Şəkil Axtarışı
                st.info("🔍 Problemlə bağlı şəkillər axtarılır...")
                with DDGS() as ddgs:
                    query = f"{st.session_state.selected_model} {prompt} repair"
                    results = list(ddgs.images(query, max_results=2))
                    for res in results:
                        st.image(res['image'], caption="İnternetdən tapılan köməkçi şəkil")
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Xəta baş verdi: {e}")
                
