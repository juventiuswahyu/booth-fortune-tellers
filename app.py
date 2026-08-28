import http.server
import socketserver
import json
import urllib.request
import os
import webbrowser

# 1. Baca API Key dari file .env (tanpa perlu install library tambahan)
GROQ_API_KEY = ""
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("GROQ_API_KEY="):
                GROQ_API_KEY = line.strip().split("=", 1)[1].strip('"\'')

# HTML Page (Tampilan UI Neon Cyberpunk + Effectuation Theory)
HTML_CONTENT = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>AI Business Fortune Teller - Stand Booth</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Outfit', sans-serif;
            background-color: #0b0719;
            color: #f3f4f6;
            background-image: 
                radial-gradient(circle at 15% 20%, rgba(147, 51, 234, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 85% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 40%);
        }
        .heading-font { font-family: 'Space Grotesk', sans-serif; }
        .neon-card {
            background: rgba(23, 15, 48, 0.75);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(168, 85, 247, 0.3);
            box-shadow: 0 8px 32px 0 rgba(112, 26, 117, 0.2);
        }
        .neon-button {
            background: linear-gradient(135deg, #a855f7 0%, #06b6d4 100%);
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.6);
            transition: all 0.3s ease;
        }
        .neon-button:hover {
            box-shadow: 0 0 30px rgba(6, 182, 212, 0.9);
            transform: translateY(-2px);
        }
        .pulse-glow { animation: pulseGlow 2s infinite alternate; }
        @keyframes pulseGlow {
            0% { filter: drop-shadow(0 0 5px rgba(168, 85, 247, 0.6)); }
            100% { filter: drop-shadow(0 0 20px rgba(6, 182, 212, 0.9)); }
        }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between p-4 md:p-8">

    <header class="max-w-4xl mx-auto w-full text-center my-4">
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-purple-900/40 border border-purple-500/30 text-purple-300 text-sm mb-3">
            <i class="fa-solid fa-wand-magic-sparkles text-amber-400"></i>
            <span>Effectuation AI Engine • Saras Sarasvathy Theory</span>
        </div>
        <h1 class="heading-font text-4xl md:text-6xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400">
            AI BUSINESS FORTUNE TELLER
        </h1>
        <p class="text-gray-400 text-lg mt-2">Ramal Potensi Bisnis Masa Depanmu Berdasarkan 3 Kartu Modalku!</p>
    </header>

    <main class="max-w-4xl mx-auto w-full flex-grow my-4">
        
        <!-- Form Input 3 Kartu (Bird in Hand) -->
        <div id="inputSection" class="space-y-6">
            <div class="grid md:grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-semibold text-purple-300 mb-1">Nama Kamu & Asal Sekolah</label>
                    <input type="text" id="namaInput" placeholder="Contoh: Budi - SMAN 1" 
                           class="w-full bg-slate-900/80 border border-purple-500/30 rounded-xl p-3.5 text-white focus:outline-none focus:border-cyan-400">
                </div>
                <div>
                    <label class="block text-sm font-semibold text-cyan-300 mb-1">Cita-Cita / Target Impian</label>
                    <input type="text" id="targetInput" placeholder="Contoh: Mau punya usaha sendiri pas kuliah" 
                           class="w-full bg-slate-900/80 border border-purple-500/30 rounded-xl p-3.5 text-white focus:outline-none focus:border-cyan-400">
                </div>
            </div>

            <div class="grid md:grid-cols-3 gap-4">
                <!-- Card 1 -->
                <div class="neon-card rounded-2xl p-5">
                    <div class="flex items-center gap-3 mb-3">
                        <div class="w-10 h-10 rounded-xl bg-purple-600/30 flex items-center justify-center text-purple-400 text-lg">
                            <i class="fa-solid fa-user-astronaut"></i>
                        </div>
                        <div>
                            <span class="text-xs uppercase tracking-wider text-purple-400 font-bold block">Kartu 1</span>
                            <h3 class="heading-font text-base font-bold text-white">Who I Am</h3>
                        </div>
                    </div>
                    <p class="text-xs text-gray-400 mb-2">Hobi, kepribadian, atau hal favorit:</p>
                    <textarea id="whoInput" rows="3" placeholder="Contoh: Suka dandan, main TikTok, estetik"
                              class="w-full bg-slate-950/60 border border-purple-500/20 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-purple-400 resize-none"></textarea>
                </div>

                <!-- Card 2 -->
                <div class="neon-card rounded-2xl p-5">
                    <div class="flex items-center gap-3 mb-3">
                        <div class="w-10 h-10 rounded-xl bg-cyan-600/30 flex items-center justify-center text-cyan-400 text-lg">
                            <i class="fa-solid fa-brain"></i>
                        </div>
                        <div>
                            <span class="text-xs uppercase tracking-wider text-cyan-400 font-bold block">Kartu 2</span>
                            <h3 class="heading-font text-base font-bold text-white">What I Know</h3>
                        </div>
                    </div>
                    <p class="text-xs text-gray-400 mb-2">Jurusan SMA/SMK atau keahlian:</p>
                    <textarea id="whatInput" rows="3" placeholder="Contoh: Anak IPS, jago komunikasi & desain"
                              class="w-full bg-slate-950/60 border border-cyan-500/20 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-cyan-400 resize-none"></textarea>
                </div>

                <!-- Card 3 -->
                <div class="neon-card rounded-2xl p-5">
                    <div class="flex items-center gap-3 mb-3">
                        <div class="w-10 h-10 rounded-xl bg-pink-600/30 flex items-center justify-center text-pink-400 text-lg">
                            <i class="fa-solid fa-people-group"></i>
                        </div>
                        <div>
                            <span class="text-xs uppercase tracking-wider text-pink-400 font-bold block">Kartu 3</span>
                            <h3 class="heading-font text-base font-bold text-white">Whom I Know</h3>
                        </div>
                    </div>
                    <p class="text-xs text-gray-400 mb-2">Relasi, teman, atau akses orang tua:</p>
                    <textarea id="whomInput" rows="3" placeholder="Contoh: Punya temen jago foto, ortu usaha baju"
                              class="w-full bg-slate-950/60 border border-pink-500/20 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-pink-400 resize-none"></textarea>
                </div>
            </div>

            <button onclick="ramalBisnis()" id="btnRamal" 
                    class="neon-button w-full py-4 rounded-2xl text-white font-extrabold text-lg heading-font tracking-wide flex items-center justify-center gap-3">
                <i class="fa-solid fa-crystal-ball text-xl pulse-glow"></i>
                <span>RAMAL BISNIS MASA DEPANKU SEKARANG!</span>
            </button>
        </div>

        <!-- Loading -->
        <div id="loadingState" class="hidden text-center py-16 space-y-4">
            <div class="relative w-24 h-24 mx-auto">
                <div class="absolute inset-0 rounded-full border-4 border-purple-500/20 animate-ping"></div>
                <div class="w-24 h-24 rounded-full bg-gradient-to-tr from-purple-600 to-cyan-400 flex items-center justify-center text-3xl pulse-glow">
                    🔮
                </div>
            </div>
            <h3 class="heading-font text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-300 to-cyan-300">
                Memproses Teori Bird-in-Hand...
            </h3>
            <p class="text-gray-400 text-sm">AI sedang mengombinasikan modal dasar milikmu menjadi mahakarya bisnis!</p>
        </div>

        <!-- Result -->
        <div id="resultSection" class="hidden space-y-6">
            <div class="neon-card rounded-3xl p-6 md:p-8 border-2 border-purple-500/50">
                <div class="flex justify-between items-start border-b border-purple-500/20 pb-4 mb-6">
                    <div>
                        <span class="text-xs uppercase tracking-widest text-cyan-400 font-bold">Hasil Ramalan Masa Depan</span>
                        <h2 id="resultTitle" class="heading-font text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-pink-400 to-purple-400"></h2>
                    </div>
                    <button onclick="resetForm()" class="text-xs bg-slate-800 hover:bg-slate-700 px-3 py-1.5 rounded-lg text-gray-300">
                        <i class="fa-solid fa-rotate-right mr-1"></i> Ulangi
                    </button>
                </div>

                <div id="resultContent" class="space-y-4 text-gray-200 text-sm md:text-base leading-relaxed"></div>

                <div class="mt-8 pt-6 border-t border-purple-500/30 bg-purple-950/40 -mx-6 -mb-6 p-6 rounded-b-3xl flex flex-col md:flex-row items-center justify-between gap-4">
                    <div class="text-left">
                        <h4 class="heading-font font-bold text-white text-lg">Mau Bikin Ramalan Ini Jadi Nyata? 🚀</h4>
                        <p class="text-xs text-purple-300">Pelajari Effectuation & Kembangkan bisnismu di Program Studi Kewirausahaan Kampus Kami!</p>
                    </div>
                    <button class="px-6 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-sm transition-all shadow-lg shadow-cyan-500/30">
                        Daftar / Konsultasi Beasiswa <i class="fa-solid fa-arrow-right ml-1"></i>
                    </button>
                </div>
            </div>
        </div>

    </main>

    <footer class="text-center text-xs text-gray-500 my-4">
        &copy; 2026 Program Studi Kewirausahaan • Interactive Booth AI Experience
    </footer>

    <script>
        async function ramalBisnis() {
            const nama = document.getElementById("namaInput").value || "Siswa Kreatif";
            const target = document.getElementById("targetInput").value || "Punya bisnis sendiri";
            const who = document.getElementById("whoInput").value;
            const what = document.getElementById("whatInput").value;
            const whom = document.getElementById("whomInput").value;

            if (!who && !what && !whom) {
                alert("Isi minimal salah satu kartu modal kamu!");
                return;
            }

            document.getElementById("inputSection").classList.add("hidden");
            document.getElementById("loadingState").classList.remove("hidden");

            try {
                const response = await fetch("/api/ramal", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ nama, target, who, what, whom })
                });

                const data = await response.json();
                
                if (data.error) {
                    alert("Error: " + data.error);
                    resetForm();
                    return;
                }

                document.getElementById("loadingState").classList.add("hidden");
                document.getElementById("resultSection").classList.remove("hidden");
                document.getElementById("resultTitle").innerHTML = `🔮 Ramalan Bisnis untuk ${nama}`;
                document.getElementById("resultContent").innerHTML = data.result;

            } catch (error) {
                alert("Gagal terhubung ke server local Python.");
                resetForm();
            }
        }

        function resetForm() {
            document.getElementById("resultSection").classList.add("hidden");
            document.getElementById("loadingState").classList.remove("hidden");
            document.getElementById("loadingState").classList.add("hidden");
            document.getElementById("inputSection").classList.remove("hidden");
        }
    </script>
</body>
</html>
"""

# 2. Server Backend (Penangan API tanpa dependensi eksternal)
class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode('utf-8'))

    def do_POST(self):
        if self.path == '/api/ramal':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode('utf-8'))

            if not GROQ_API_KEY:
                self.send_json_response({"error": "API Key tidak ditemukan di file .env!"}, 500)
                return

            # Prompt Teori Bird-in-Hand
            prompt = f"""
            Kamu adalah AI "Business Fortune Teller" inspiratif untuk prodi Kewirausahaan.
            Gunakan Teori Effectuation dari Saras Sarasvathy (Prinsip "Bird-in-Hand").

            Data Siswa:
            - Nama: {body.get('nama')}
            - Cita-Cita: {body.get('target')}
            - Modal Kartu 1 (Who I Am): {body.get('who')}
            - Modal Kartu 2 (What I Know): {body.get('what')}
            - Modal Kartu 3 (Whom I Know): {body.get('whom')}

            Buatkan hasil ramalan bisnis format HTML (tanpa tag ```html, buat lansung elemen div/h3/p):
            1. **Julukan Bisnis Masa Depan** (Keren & Futuristik)
            2. **Konsep Bisnis 'Bird-in-Hand'** (Gunakan gabungan modal mereka).
            3. **Skor Potensi Ide** (Tampilkan Keunikan % & Kemudahan Eksekusi % dengan desain angka tebal).
            4. **Langkah Pertama Hari Ini** (1 aksi konkret tanpa modal uang besar).

            Gunakan bahasa kasual, penuh semangat anak muda, dan memotivasi.
            """

            # Kirim request ke API Groq menggunakan urllib standar
            groq_req = urllib.request.Request(
                "[https://api.groq.com/openai/v1/chat/completions](https://api.groq.com/openai/v1/chat/completions)",
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

            try:
                with urllib.request.urlopen(groq_req) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    ai_result = res_data['choices'][0]['message']['content']
                    self.send_json_response({"result": ai_result})
            except Exception as e:
                self.send_json_response({"error": str(e)}, 500)

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

if __name__ == "__main__":
    PORT = 8000
    print(f"🚀 Application starting at http://localhost:{PORT}")
    webbrowser.open(f"http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        httpd.serve_forever()
