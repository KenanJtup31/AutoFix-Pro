import streamlit as st
from groq import Groq
import streamlit as st
from groq import Groq

# API açarını birbaşa buraya yazırıq (Secrets bölməsi ilə işimiz qalmır)
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 1. Səhifə Ayarları və Ağ Ekran Dizaynı
st.set_page_config(page_title="AutoFix Pro", page_icon="🚗", layout="centered")

# CSS ilə ağ ekran və səliqəli dizayn
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #f8f9fa; border: 1px solid #ddd; }
    .stButton>button:hover { border-color: #FF4B4B; color: #FF4B4B; }
    h1, h2, h3 { color: #1E1E1E; }
    .developed-by { text-align: center; color: #888; font-size: 14px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Üst Başlıq
st.markdown("<div class='developed-by'>Developed by Kenan Elizade</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>🛠️ AvtoFix Pro</h1>", unsafe_allow_html=True)

# API Girişi (Xətanı önləmək üçün)
# API açarını birbaşa bura qoyuram ki xəta verməsin (amma gələcəkdə Secrets-ə qoymalısan)
api_key = st.secrets.get("GROQ_API_KEY", "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")
client = Groq(api_key=api_key)

# 2. Maşın Modelləri Bazası (Şəkillərlə)
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

# Session State - Seçilmiş maşını yadda saxla
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. ANA SƏHİFƏ (Maşın seçimi)
if st.session_state.selected_model is None:
    st.markdown("<h4 style='text-align: center;'>Aşağıdakı maşın modellərindən birini seçin:</h4>", unsafe_allow_html=True)
    
    # 3 sütunlu grid sistemi
    cols = st.columns(3)
    for i, (name, img_url) in enumerate(models.items()):
        with cols[i % 3]:
            st.image(img_url, width=80)
            if st.button(name):
                st.session_state.selected_model = name
                st.rerun()

# 4. ÇAT EKRANI (Maşın seçildikdən sonra)
else:
    st.markdown(f"### 🚗 {st.session_state.selected_model} Diaqnostika")
    if st.button("⬅️ Geri qayıt"):
        st.session_state.selected_model = None
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    # Çat tarixçəsi
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Sual vermə yeri
    if prompt := st.chat_input(f"{st.session_state.selected_model} üçün probleminiz nədir?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # AI Cavabı
        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"Sən səmimi, peşəkar və usta bir avtomobil mühəndisisən. İstifadəçi {st.session_state.selected_model} modelində bir problem yaşayır. Ona səmimi dost kimi yanaş, problemin səbəbini və həllini professional izah et."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama3-8b-8192",
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error("Xəta baş verdi! Lütfən API açarını yoxlayın.")
                
