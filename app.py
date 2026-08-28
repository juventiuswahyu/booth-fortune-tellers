import streamlit as st
import json
import urllib.request
import os

st.set_page_config(
    page_title="AI Business Fortune Teller",
    page_icon="🔮",
    layout="centered"
)

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))

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
        padding: 14px;
        border: none;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 AI BUSINESS FORTUNE TELLER")
st.caption("Ramal Potensi Bisnis Masa Depanmu Berdasarkan 3 Kartu Modalku! (Teori Effectuation)")

# --- DAFTAR PILIHAN DROPDOWN (10 VARIASI PER KARTU) ---

WHO_OPTIONS = [
    "📱 Suka bikin konten TikTok / Reels & hits",
    "👗 Ngerti & update tren fashion / hijab",
    "🗣️ Komunikatif, percaya diri & ramah",
    "🎮 Hobi gaming & paham dunia E-sports",
    "🎨 Kreatif, suka menggambar / seni visual",
    "🍰 Suka masak / bikin kue & kulineran",
    "🛍️ Gemar jualan / nawarin barang ke teman",
    "✈️ Suka jalan-jalan & foto-foto estetis",
    "🌱 Peduli isu lingkungan & produk ramah lingkungan",
    "🎧 Suka dengerin musik & paham tren Gen-Z"
]

WHAT_OPTIONS = [
    "📚 Anak IPS (Paham ekonomi, bisnis & sosial)",
    "🔬 Anak IPA (Paham sains, logika & analitikal)",
    "💻 Anak SMK / TKJ / DKV (Teknologi, Desain, Coding)",
    "🎤 Jago Public Speaking & Presentasi",
    "📈 Mengerti algoritma medsos & tren viral",
    "🎬 Bisa edit foto & video pro di HP (CapCut/Canva)",
    "✍️ Jago copywriting, nulis & bercerita (Storytelling)",
    "🧮 Jago hitung-hitungan & manajemen keuangan",
    "🌐 Menguasai bahasa asing (Inggris/Korea/Jepang)",
    "💡 Selalu punya ide unik & solusi kreatif"
]

WHOM_OPTIONS = [
    "📸 Punya teman/saudara jago fotografi & videografi",
    "🧵 Orang tua/kerabat punya usaha konveksi / toko / UMKM",
    "🛍️ Teman-teman sekolah konsumtif & suka barang viral",
    "🌟 Punya kenalan selebgram / influencer lokal",
    "👥 Punya jaringan komunitas hobi / OSIS / Remaja Masjid",
    "🚚 Akses mudah ke supplier grosir / pasar pusat",
    "💻 Punya teman jago bikin website / koding",
    "📊 Orang tua / kenalan paham akuntansi & legalitas",
    "🤝 Teman-teman sekelas sangat kompak & suportif",
    "🏫 Punya akses ke acara pameran / bazar sekolah"
]

TARGET_OPTIONS = [
    "Mau punya bisnis sendiri saat kuliah",
    "Ingin dapat penghasilan tambahan pas sekolah",
    "Membangun brand fashion / skincare sendiri",
    "Bikin agency digital / content creator team",
    "Mengembangkan usaha orang tua / keluarga",
    "Bikin usaha kuliner kekinian",
    "Bikin startup teknologi / aplikasi"
]

# --- FORM INPUT ---
with st.form("fortune_form"):
    nama = st.text_input("Nama Kamu & Asal Sekolah (Opsional)", placeholder="Contoh: Budi - SMAN 1")
    target = st.selectbox("🎯 Target Impian Kamu", TARGET_OPTIONS)
    
    st.subheader("🃏 Pilih Kartu Modal Kamu (Bisa Pilih Banyak)")
    
    selected_who = st.multiselect("Kartu 1: Who I Am (Siapa Kamu / Hobi)", WHO_OPTIONS)
    selected_what = st.multiselect("Kartu 2: What I Know (Keahlian / Jurusan)", WHAT_OPTIONS)
    selected_whom = st.multiselect("Kartu 3: Whom I Know (Relasi / Akses)", WHOM_OPTIONS)
    
    submitted = st.form_submit_button("✨ RAMAL BISNIS MASA DEPANKU SEKARANG!")

if submitted:
    if not selected_who and not selected_what and not selected_whom:
        st.warning("Pilih minimal satu opsi dari kartu modal kamu!")
    elif not GROQ_API_KEY:
        st.error("API Key Groq belum diatur di Streamlit Secrets!")
    else:
        with st.spinner("🔮 AI sedang meramal masa depan bisnismu..."):
            who_str = ", ".join(selected_who) if selected_who else "Tidak diisi"
            what_str = ", ".join(selected_what) if selected_what else "Tidak diisi"
            whom_str = ", ".join(selected_whom) if selected_whom else "Tidak diisi"

            prompt = f"""
            Kamu adalah AI "Business Fortune Teller" inspiratif untuk prodi Kewirausahaan.
            Gunakan Teori Effectuation dari Saras Sarasvathy (Prinsip "Bird-in-Hand").

            Data Siswa:
            - Nama: {nama if nama else 'Siswa Kreatif'}
            - Cita-Cita: {target}
            - Modal Kartu 1 (Who I Am): {who_str}
            - Modal Kartu 2 (What I Know): {what_str}
            - Modal Kartu 3 (Whom I Know): {whom_str}

            Buatkan hasil ramalan bisnis format Markdown:
            ### 🏆 Julukan Bisnis Masa Depan
            ### 💡 Konsep Bisnis 'Bird-in-Hand' (Tabel/Poin menggabungkan modal yang mereka pilih di atas)
            ### 📊 Skor Potensi Ide (Keunikan % & Kemudahan Eksekusi %)
            ### 🚀 Langkah Pertama Hari Ini (Aksi konkret tanpa modal uang besar)

            Gunakan bahasa kasual, ramah anak muda, dan memotivasi.
            """

            try:
                req_data = json.dumps({
                    "model": "openai/gpt-oss-20b",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                }).encode('utf-8')

                groq_req = urllib.request.Request(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0"
                    },
                    data=req_data
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
