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
GSHEET_WEBAPP_URL = st.secrets.get("GSHEET_WEBAPP_URL", os.environ.get("GSHEET_WEBAPP_URL", ""))

if "form_reset_key" not in st.session_state:
    st.session_state.form_reset_key = 0

def clear_form():
    st.session_state.form_reset_key += 1

# --- STYLING UI ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #0f172a; }
    h1 { color: #7A1C1C !important; text-align: center; font-weight: 800; }
    .academic-subtitle { text-align: center; color: #475569; font-size: 14px; margin-bottom: 25px; }
    .nowrap-text { white-space: nowrap; }
    div[data-testid="stForm"] { background-color: #ffffff !important; border: 3px solid #D4AF37 !important; border-radius: 20px !important; padding: 24px !important; }
    label, div[data-testid="stWidgetLabel"] p { color: #334155 !important; font-weight: 700 !important; }
    span[data-baseweb="tag"] { background: linear-gradient(135deg, #7A1C1C 0%, #A32A2A 100%) !important; border: 1px solid #D4AF37 !important; }
    span[data-baseweb="tag"] span { color: #ffffff !important; font-weight: 600; }
    h3 { color: #7A1C1C !important; font-size: 1.2rem !important; font-weight: 700 !important; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #7A1C1C 0%, #A32A2A 100%); color: #ffffff; font-weight: bold; border-radius: 12px; padding: 14px; border: 2px solid #D4AF37; }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("giphy.gif"):
        st.image("giphy.gif", use_container_width=True)

st.title("AI BUSINESS POTENTIAL NAVIGATOR")
st.markdown("""
    <div class="academic-subtitle">
        Asisten Berbasis Artificial Intelligence (AI) yang Dikembangkan oleh Program Studi Manajemen Universitas Nasional Karangturi Semarang untuk Menganalisis Potensi Bisnis Generasi Muda Berdasarkan Teori Effectuation (<span class="nowrap-text">Prof. Saras D. Sarasvathy, Ph.D. - University of Virginia</span>).
    </div>
""", unsafe_allow_html=True)

WHO_OPTIONS = [
    "📱 Suka bikin konten media sosial / video kreatif",
    "👗 Tertarik dengan tren fashion & apparel",
    "🗣️ Komunikatif, percaya diri & ramah",
    "🎮 Hobi gaming & paham tren teknologi/E-sports",
    "🎨 Kreatif, suka menggambar / seni visual & desain",
    "🍰 Suka memasak / eksplorasi kuliner",
    "🛍️ Gemar bernegosiasi & menawarkan barang ke teman",
    "✈️ Suka fotografi & eksplorasi tempat baru",
    "🌱 Peduli gaya hidup sehat & produk ramah lingkungan",
    "🎧 Mengikuti tren pop culture, musik & gaya hidup generasi muda"
]

WHAT_OPTIONS = [
    "📚 Pemahaman ilmu sosial, ekonomi & bisnis dasar",
    "🔬 Pemahaman sains, logika & analitikal",
    "💻 Keterampilan teknologi, desain grafis & digital",
    "🎤 Kemampuan public speaking & presentasi",
    "📈 Pemahaman tren digital & media sosial",
    "🎬 Kemampuan editing foto & video",
    "✍️ Kemampuan menulis kreatif & copywriting",
    "🧮 Keterampilan perhitungan & manajemen keuangan dasar",
    "🌐 Menguasai bahasa asing (Inggris/Lainnya)",
    "💡 Kemampuan pemecahan masalah & ide inovatif"
]

WHOM_OPTIONS = [
    "📸 Punya rekan/saudara yang jago fotografi & videografi",
    "🧵 Kerabat/keluarga memiliki bisnis/UMKM",
    "🛍️ Teman sebaya yang konsumtif & menyukai barang tren",
    "🌟 Memiliki akses/kontak dengan pembuat konten (content creator)",
    "👥 Aktif di organisasi sekolah / komunitas pemuda",
    "🚚 Akses mudah ke distributor grosir / pasar utama",
    "💻 Punya rekan yang mahir di bidang IT / pembuatan website",
    "📊 Memiliki relasi yang berpengalaman di bidang manajemen/hukum",
    "🤝 Komunitas / teman sekelas yang kompak & suportif",
    "🏫 Akses untuk berpartisipasi di bazar / pameran"
]

TARGET_OPTIONS = [
    "Membangun bisnis mandiri saat berkuliah",
    "Mendapatkan penghasilan tambahan saat sekolah/kuliah",
    "Membangun brand produk (fashion/skincare/lifestyle) sendiri",
    "Mendirikan agensi kreatif / penyedia jasa digital",
    "Mengembangkan bisnis keluarga / UMKM lokal",
    "Mendirikan usaha kuliner modern",
    "Mengembangkan bisnis berbasis teknologi / aplikasi"
]

reset_key = st.session_state.form_reset_key

with st.form("fortune_form"):
    nama = st.text_input("Nama Kamu & Asal Sekolah (Opsional)", placeholder="Contoh: Budi - SMAN 1", key=f"nama_{reset_key}")
    target = st.selectbox("🎯 Target Impian Kamu", TARGET_OPTIONS, key=f"target_{reset_key}")
    
    st.subheader("🃏 Pilih Kartu Modal Kamu (Bisa Pilih Banyak)")
    selected_who = st.multiselect("Kartu 1: Who I Am (Karakter / Minat / Hobi)", WHO_OPTIONS, key=f"who_{reset_key}")
    selected_what = st.multiselect("Kartu 2: What I Know (Pengetahuan & Keahlian)", WHAT_OPTIONS, key=f"what_{reset_key}")
    selected_whom = st.multiselect("Kartu 3: Whom I Know (Jaringan & Akses Relasi)", WHOM_OPTIONS, key=f"whom_{reset_key}")
    
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

            Format output HANYA gunakan Markdown seperti ini:

            ### 🎓 Hasil Analisis Rekomendasi Bisnis

            1. **[Kategori Bisnis Opsi 1]**
               - **Gambaran Bisnis:** [Penjelasan singkat 1-2 kalimat]
               - **Alasan Cocok:** [Penjelasan singkat mengapa cocok]

            2. **[Kategori Bisnis Opsi 2]**
               - **Gambaran Bisnis:** [Penjelasan singkat 1-2 kalimat]
               - **Alasan Cocok:** [Penjelasan singkat mengapa cocok]

            3. **[Kategori Bisnis Opsi 3]**
               - **Gambaran Bisnis:** [Penjelasan singkat 1-2 kalimat]
               - **Alasan Cocok:** [Penjelasan singkat mengapa cocok]
            """

            try:
                # 1. Kirim Prompt ke Groq API
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

                # 2. Simpan Otomatis ke Google Sheets (jika URL diset)
                if GSHEET_WEBAPP_URL:
                    payload = json.dumps({
                        "nama": nama if nama else "Siswa",
                        "target": target,
                        "who": who_str,
                        "what": what_str,
                        "whom": whom_str,
                        "hasil": ai_result
                    }).encode('utf-8')

                    gsheet_req = urllib.request.Request(
                        GSHEET_WEBAPP_URL,
                        headers={"Content-Type": "application/json"},
                        data=payload
                    )
                    urllib.request.urlopen(gsheet_req)

            except Exception as e:
                st.error(f"Gagal memproses data: {str(e)}")
