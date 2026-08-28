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

# --- STYLING UI KEREN (LIGHT THEME & ELEGANT PURPLE) ---
st.markdown("""
    <style>
    /* Latar Belakang Utama Halaman (Putih Bersih) */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }
    
    /* Title & Caption */
    h1 {
        color: #6d28d9 !important;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        margin-top: 10px;
    }
    .stCaption {
        text-align: center;
        color: #64748b !important;
        font-size: 15px;
        font-weight: 500;
    }

    /* Container Form Input */
    div[data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
    }

    /* Label Input */
    label, div[data-testid="stWidgetLabel"] p {
        color: #334155 !important;
        font-weight: 700 !important;
    }

    /* Input Text & Selectbox Background */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #f1f5f9 !important;
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
        border-radius: 10px !important;
    }

    /* Tag Pilihan Multiselect (Chips) */
    span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%) !important;
        border-radius: 8px !important;
    }
    span[data-baseweb="tag"] span {
        color: #ffffff !important;
        font-weight: 600;
    }

    /* Subheader di Dalam Form */
    h3 {
        color: #4c1d95 !important;
        font-size: 1.2rem !important;
    }

    /* Tombol Utama (Button) */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%);
        color: #ffffff;
        font-weight: bold;
        border-radius: 12px;
        padding: 14px;
        border: none;
        font-size: 18px;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.45);
    }

    /* Box Hasil Markdown */
    div[data-testid="stMarkdownContainer"] p {
        color: #1e293b;
    }
    </style>
""", unsafe_allow_html=True)

# --- ANIMASI BOLA KRISTAL BERGERAK ---
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image(
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWc1b3N6bXZyeGF3MnV4OGd5ZnQ4Z2NzaWc4aDlhMnEzZ3ZtdnA3ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/3o7TKsjLu182aQvNbc/giphy.gif",
        use_container_width=True
    )

st.title("AI BUSINESS FORTUNE TELLER")
st.caption("Ramal Potensi Bisnis Masa Depanmu Berdasarkan 3 Kartu Modalku! (Teori Effectuation)")

# --- DAFTAR PILIHAN DROPDOWN ---

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
            Tugasmu adalah merekomendasikan 3 pilihan jenis bisnis yang cocok berdasarkan modal Effectuation ("Bird-in-Hand") siswa.

            Data Input Siswa:
            - Nama: {nama if nama else 'Siswa'}
            - Cita-Cita: {target}
            - Kartu 1 (Who I Am): {who_str}
            - Kartu 2 (What I Know): {what_str}
            - Kartu 3 (Whom I Know): {whom_str}

            INSTRUKSI OUTPUT:
            - JANGAN membuat nama merek buatan (misal: Nomad Glow, TechWear, dll). Sebutkan jenis/kategori bisnisnya saja.
            - Berikan 3 opsi rekomendasi bisnis yang realistis & relevan dari modal siswa.
            - Gunakan bahasa kasual, ramah anak muda, dan suportif.

            Format output HANYA gunakan Markdown seperti ini:

            ### 🔮 Rekomendasi Bisnis yang Cocok Untukmu

            1. **[Kategori Bisnis Opsi 1]**
               - **Gambaran Bisnis:** [Penjelasan singkat 1-2 kalimat]
               - **Alasan Cocok:** [Penjelasan singkat mengapa cocok dengan kombinasi modalnya]

            2. **[Kategori Bisnis Opsi 2]**
               - **Gambaran Bisnis:** [Penjelasan singkat 1-2 kalimat]
               - **Alasan Cocok:** [Penjelasan singkat mengapa cocok dengan kombinasi modalnya]

            3. **[Kategori Bisnis Opsi 3]**
               - **Gambaran Bisnis:** [Penjelasan singkat 1-2 kalimat]
               - **Alasan Cocok:** [Penjelasan singkat mengapa cocok dengan kombinasi modalnya]

            ---
            💡 *Pilih salah satu ide di atas yang paling bikin kamu bersemangat untuk memulainya!*
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
            except Exception as e:
                st.error(f"Gagal memproses ramalan: {str(e)}")
