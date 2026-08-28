import streamlit as st
import json
import urllib.request
import os

st.set_page_config(
    page_title="AI Business Potential Navigator",
    page_icon="🎓",
    layout="centered"
)

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))

# --- INITALIZE SESSION STATE UNTUK RESET ---
if "form_reset_key" not in st.session_state:
    st.session_state.form_reset_key = 0

def clear_form():
    st.session_state.form_reset_key += 1

# --- STYLING UI ACADEMIC THEME (MAROON & GOLD) ---
st.markdown("""
    <style>
    /* Latar Belakang Utama Halaman */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }
    
    /* Title Utama (Merah Maroon) */
    h1 {
        color: #7A1C1C !important;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        margin-top: 5px;
        letter-spacing: 0.5px;
    }
    
    /* Subtitle Akademik Rata Tengah */
    .academic-subtitle {
        text-align: center;
        color: #475569;
        font-size: 14px;
        font-weight: 500;
        line-height: 1.6;
        margin-bottom: 25px;
        padding: 0 10px;
    }

    /* Kunci nama agar 1 baris utuh */
    .nowrap-text {
        white-space: nowrap;
    }

    /* Container Form Input dengan Frame GOLD */
    div[data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 3px solid #D4AF37 !important; /* Warna Gold */
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 0 10px 25px -5px rgba(212, 175, 55, 0.2);
    }

    /* Label Input */
    label, div[data-testid="stWidgetLabel"] p {
        color: #334155 !important;
        font-weight: 700 !important;
    }

    /* Input Text & Selectbox Background */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #f8fafc !important;
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
        border-radius: 10px !important;
    }

    /* Tag Pilihan Multiselect (Chips) - Warna Maroon & Gold Accent */
    span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #7A1C1C 0%, #A32A2A 100%) !important;
        border-radius: 8px !important;
        border: 1px solid #D4AF37 !important;
    }
    span[data-baseweb="tag"] span {
        color: #ffffff !important;
        font-weight: 600;
    }

    /* Subheader di Dalam Form (Merah Maroon) */
    h3 {
        color: #7A1C1C !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }

    /* Tombol Utama (Button Maroon - Gold) */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #7A1C1C 0%, #A32A2A 100%);
        color: #ffffff;
        font-weight: bold;
        border-radius: 12px;
        padding: 14px;
        border: 2px solid #D4AF37;
        font-size: 16px;
        box-shadow: 0 4px 14px rgba(122, 28, 28, 0.35);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #8C2222 0%, #B83232 100%);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
    }

    /* Box Hasil Markdown */
    div[data-testid="stMarkdownContainer"] p {
        color: #1e293b;
    }
    </style>
""", unsafe_allow_html=True)

# --- MENAMPILKAN LOGO DI TENGAH ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("giphy.gif"):
        st.image("giphy.gif", use_container_width=True)

st.title("AI BUSINESS POTENTIAL NAVIGATOR")

# Subtitle Rata Tengah (Nama Profesor Dibuat 1 Baris Utuh)
st.markdown("""
    <div class="academic-subtitle">
        Asisten Berbasis Artificial Intelligence (AI) yang Dikembangkan oleh Program Studi Manajemen Universitas Nasional Karangturi Semarang untuk Menganalisis Potensi Bisnis Generasi Muda Berdasarkan Teori Effectuation (<span class="nowrap-text">Prof. Saras D. Sarasvathy, Ph.D. - University of Virginia</span>).
    </div>
""", unsafe_allow_html=True)

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
reset_key = st.session_state.form_reset_key

with st.form("fortune_form"):
    nama = st.text_input(
        "Nama Kamu & Asal Sekolah (Opsional)", 
        placeholder="Contoh: Budi - SMAN 1",
        key=f"nama_{reset_key}"
    )
    target = st.selectbox(
        "🎯 Target Impian Kamu", 
        TARGET_OPTIONS,
        key=f"target_{reset_key}"
    )
    
    st.subheader("🃏 Pilih Kartu Modal Kamu (Bisa Pilih Banyak)")
    
    selected_who = st.multiselect(
        "Kartu 1: Who I Am (Siapa Kamu / Hobi)", 
        WHO_OPTIONS,
        key=f"who_{reset_key}"
    )
    selected_what = st.multiselect(
        "Kartu 2: What I Know (Keahlian / Jurusan)", 
        WHAT_OPTIONS,
        key=f"what_{reset_key}"
    )
    selected_whom = st.multiselect(
        "Kartu 3: Whom I Know (Relasi / Akses)", 
        WHOM_OPTIONS,
        key=f"whom_{reset_key}"
    )
    
    # Grid 2 Kolom untuk Tombol
    btn_col1, btn_col2 = st.columns([3, 1])
    
    with btn_col1:
        submitted = st.form_submit_button("✨ ANALISIS POTENSI BISNIS SEKARANG!")
    with btn_col2:
        cleared = st.form_submit_button("🗑️ CLEAR", on_click=clear_form)

if submitted and not cleared:
    if not selected_who and not selected_what and not selected_whom:
        st.warning("Pilih minimal satu opsi dari kartu modal kamu!")
    elif not GROQ_API_KEY:
        st.error("API Key Groq belum diatur di Streamlit Secrets!")
    else:
        with st.spinner("🤖 AI sedang menganalisis potensi bisnismu..."):
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

            ### 🎓 Hasil Analisis Rekomendasi Bisnis

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
                    
                    st.success("Analisis Selesai!")
                    st.markdown(ai_result)
            except Exception as e:
                st.error(f"Gagal memproses analisis: {str(e)}")
