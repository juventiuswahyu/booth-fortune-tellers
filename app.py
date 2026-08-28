import streamlit as st
import json
import urllib.request
import os

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="AI Business Fortune Teller",
    page_icon="🔮",
    layout="centered"
)

# Membaca API Key dari Streamlit Secrets atau Environment Variable
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))

# Styling Tampilan Neon / Futuristic
st.markdown("""
    <style>
    .main { background-color: #0b0719; }
    h1 { color: #a855f7 !important; text-align: center; font-family: sans-serif; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #a855f7 0%, #06b6d4 100%);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 AI BUSINESS FORTUNE TELLER")
st.caption("Ramal Potensi Bisnis Masa Depanmu Berdasarkan 3 Kartu Modalku! (Teori Effectuation)")

with st.form("fortune_form"):
    nama = st.text_input("Nama Kamu & Asal Sekolah", placeholder="Contoh: Budi - SMAN 1")
    target = st.text_input("Cita-Cita / Target Impian", placeholder="Contoh: Mau punya usaha sendiri pas kuliah")
    
    st.subheader("🃏 3 Kartu Modal Kamu")
    who = st.text_area("Kartu 1: Who I Am", placeholder="Hobi, kepribadian, atau hal favorit (Contoh: Suka dandan, main TikTok)")
    what = st.text_area("Kartu 2: What I Know", placeholder="Jurusan SMA/SMK atau keahlian (Contoh: Anak IPS, jago komunikasi)")
    whom = st.text_area("Kartu 3: Whom I Know", placeholder="Relasi/akses teman atau ortu (Contoh: Temen jago foto, ortu usaha baju)")
    
    submitted = st.form_submit_button("✨ RAMAL BISNIS MASA DEPANKU SEKARANG!")

if submitted:
    if not who and not what and not whom:
        st.warning("Isi minimal salah satu dari 3 kartu modal kamu!")
    elif not GROQ_API_KEY:
        st.error("API Key Groq belum diatur di Streamlit Secrets!")
    else:
        with st.spinner("🔮 AI sedang meramal masa depan bisnismu..."):
            prompt = f"""
            Kamu adalah AI "Business Fortune Teller" inspiratif untuk prodi Kewirausahaan.
            Gunakan Teori Effectuation dari Saras Sarasvathy (Prinsip "Bird-in-Hand").

            Data Siswa:
            - Nama: {nama if nama else 'Siswa Kreatif'}
            - Cita-Cita: {target if target else 'Punya bisnis sendiri'}
            - Modal Kartu 1 (Who I Am): {who}
            - Modal Kartu 2 (What I Know): {what}
            - Modal Kartu 3 (Whom I Know): {whom}

            Buatkan hasil ramalan bisnis format Markdown:
            ### 🏆 Julukan Bisnis Masa Depan
            ### 💡 Konsep Bisnis 'Bird-in-Hand' (Gabungkan modal mereka)
            ### 📊 Skor Potensi Ide (Keunikan % & Kemudahan Eksekusi %)
            ### 🚀 Langkah Pertama Hari Ini (Aksi konkret tanpa modal uang besar)

            Gunakan bahasa kasual, ramah anak muda, dan memotivasi.
            """

            try:
                groq_req = urllib.request.Request(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0"
                    },
                    data=json.dumps({
                        "model": "llama-3.3-70b-versatile",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.8
                    }).encode('utf-8')
                )
                with urllib.request.urlopen(groq_req) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    ai_result = res_data['choices'][0]['message']['content']
                    
                    st.success("Ramalan Selesai!")
                    st.markdown(ai_result)
                    st.divider()
                    st.info("💡 **Mau bikin ramalan ini jadi nyata?** Pelajari Effectuation & Kembangkan bisnismu di Program Studi Kewirausahaan!")
            except Exception as e:
                st.error(f"Gagal memproses ramalan: {str(e)}")
