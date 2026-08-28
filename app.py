prompt = f"""
            Tugasmu adalah merekomendasikan 3 pilihan jenis bisnis yang cocok berdasarkan modal Effectuation ("Bird-in-Hand") siswa.

            Data Input Siswa:
            - Nama: {nama if nama else 'Siswa'}
            - Cita-Cita: {target}
            - Kartu 1 (Who I Am): {who_str}
            - Kartu 2 (What I Know): {what_str}
            - Kartu 3 (Whom I Know): {whom_str}

            INSTRUKSI OUTPUT:
            - JANGAN membuat nama merek buatan (misal: "Nomad Glow", "TechWear", dll). Sebutkan jenis/kategori bisnisnya saja.
            - Berikan 3 opsi rekomendasi bisnis yang realistis & relevan dari modal siswa.
            - Gunakan bahasa kasual, ramah anak muda, dan suportif.

            Format output HANYA gunakan Markdown seperti ini:

            ### 🔮 Rekomendasi Bisnis yang Cocok Untukmu

            1. **[Kategori Bisnis Opsi 1]**
               - **Gambaran Bisnis:** [Penjelasan singkat 1-2 kalimat]
               - **Alasan Cocok:** [Penjelasan singkat mengapa cocok dengan kombinasi modal modalnya]

            2. **[Kategori Bisnis Opsi 2]**
               - **Gambaran Bisnis:** [Penjelasan singkat 1-2 kalimat]
               - **Alasan Cocok:** [Penjelasan singkat mengapa cocok dengan kombinasi modalnya]

            3. **[Kategori Bisnis Opsi 3]**
               - **Gambaran Bisnis:** [Penjelasan singkat 1-2 kalimat]
               - **Alasan Cocok:** [Penjelasan singkat mengapa cocok dengan kombinasi modalnya]

            ---
            💡 *Pilih salah satu ide di atas yang paling bikin kamu bersemangat untuk memulainya!*
            """
