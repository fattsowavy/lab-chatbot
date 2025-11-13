# NOTE: Masih dalam tahap awal

# Chatbot Q&A Labkom FIKOM UMI

Chatbot berbasis web untuk membantu **mahasiswa FIKOM UMI** mendapatkan informasi **Laboratorium Komputer** secara cepat:  
- Jadwal buka/tutup  
- Aturan penggunaan  
- Spesifikasi PC & software  

## Fitur Utama

| Fitur | Deskripsi |
|------|-----------|
| **Tanya Jawab Instan** | Ketik pertanyaan → jawaban otomatis |
| **NLP Sederhana** | Deteksi kata kunci + fuzzy matching |
| **Knowlede Base** | Data disimpan di `knowledge_base.json` |
| **UI** | Tailwind CSS |

---

## Tech Stack

```text
Python 3.11
├── Flask
├── FuzzyWuzzy (NLP)
├── Jinja2 + Tailwind CSS
└── JSON (knowledge base)
