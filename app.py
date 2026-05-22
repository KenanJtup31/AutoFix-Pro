import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

st.set_page_config(page_title="AutoFix Pro AI", page_icon="🚗", layout="centered")

API_KEY = "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"
client = Groq(api_key=API_KEY)

st.markdown("<h1 style='text-align: center;'>🛠️ AvtoFix Pro AI</h1>", unsafe_allow_html=True)

# Modellər bazası
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
                # 1. AI Cavabı
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Sən avto-mühəndisəsən. Əgər istifadəçi təmir addımı və ya hissə soruşursa, ətraflı cavab ver. Əgər sadəcə salamlaşırsa, qısa cavab ver."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                
                # 2. Şəkil Axtarışı Məntiqi (Yalnız təmir sorğusu olduqda)
                # Əgər cavabda "həll", "təmir", "dəyiş", "yoxla" kimi sözlər varsa axtar
                if any(word in prompt.lower() for word in ["təmir", "dəyiş", "yoxla", "səs", "problem", "hissə"]):
                    with st.spinner("🔍 Texniki şəkillər axtarılır..."):
                        with DDGS() as ddgs:
                            query = f"{st.session_state.selected_model} {prompt} repair diagram"
                            results = list(ddgs.images(query, max_results=2))
                            for res in results:
                                st.image(res['image'], use_column_width=True)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error("Bağlantı xətası oldu, lütfən bir daha cəhd edin.")
                
