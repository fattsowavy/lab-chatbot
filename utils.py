import json
import re
import logging
from fuzzywuzzy import fuzz
from logger_config import logger
from config import MIN_CONFIDENCE_SCORE, MAX_INPUT_LENGTH, KB_FILE
import os

# Load knowledge base dengan error handling yang lebih baik
KB = {}

def load_knowledge_base():
    """Load knowledge base dari file JSON dengan validasi"""
    global KB
    try:
        if not os.path.exists(KB_FILE):
            logger.error(f"Knowledge base file tidak ditemukan: {KB_FILE}")
            KB = {}
            return False
        
        with open(KB_FILE, 'r', encoding='utf-8') as f:
            KB = json.load(f)
        
        # Validasi struktur KB
        if not isinstance(KB, dict):
            logger.error("Knowledge base harus berupa dictionary")
            KB = {}
            return False
        
        logger.info(f"Knowledge base berhasil dimuat dengan {len(KB)} kategori")
        return True
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error saat membaca KB: {str(e)}")
        KB = {}
        return False
    except Exception as e:
        logger.error(f"Error membaca knowledge base: {str(e)}")
        KB = {}
        return False

# Load KB saat startup
load_knowledge_base()
    
KEYWORDS = {
    "jadwal": ["jadwal", "buka", "tutup", "istirahat", "hari kerja", "jam", "berapa"],
    "aturan": ["aturan", "sanksi", "syarat", "peraturan", "dilarang", "boleh"],
    "spesifikasi": ["spesifikasi", "pc", "komputer", "software", "hardware", "mysql", "sistem"],
    "greeting": ["halo", "hai", "hallo", "selamat", "pagi", "siang", "sore", "assalamualaikum", "terima kasih", "makasih", "oke", "ok"]
}

def extract_keywords(text):
    """Extract kata-kata dari teks dengan validasi"""
    if not text or not isinstance(text, str):
        return []
    return re.findall(r'\b\w+\b', text.lower())

def validate_input(user_input):
    """Validasi input user"""
    if not user_input:
        return False, "Input kosong"
    
    if len(user_input) > MAX_INPUT_LENGTH:
        return False, f"Input terlalu panjang (maks {MAX_INPUT_LENGTH} karakter)"
    
    # Check jika input hanya whitespace
    if not user_input.strip():
        return False, "Input hanya whitespace"
    
    return True, None

def match_category(user_input):
    """
    Mencocokkan input user dengan kategori menggunakan pendekatan token-based.
    - Gunakan token_set_ratio per keyword, ambil skor terbaik per kategori.
    - Tangani sapaan/short-input sebagai kategori khusus atau ambiguous.
    """
    try:
        is_valid, error_msg = validate_input(user_input)
        if not is_valid:
            logger.warning(f"Invalid input: {error_msg}")
            return None

        user_input_lower = user_input.lower().strip()

        # Jika sapaan eksplisit, langsung kembalikan 'greeting'
        if re.search(r"\b(halo|hai|hallo|selamat|pagi|siang|sore|assalamualaikum|makasih|terima kasih)\b", user_input_lower):
            return "greeting"

        best_score = 0
        best_cat = None

        for cat, words in KEYWORDS.items():
            if not words or not isinstance(words, list):
                continue

            # Hitung skor terbaik terhadap semua kata kunci kategori
            scores = [fuzz.token_set_ratio(user_input_lower, kw) for kw in words]
            if not scores:
                continue
            cat_best = max(scores)

            if cat_best > best_score:
                best_score = cat_best
                best_cat = cat

        logger.debug(f"Match result - Input: '{user_input}', Category: {best_cat}, Score: {best_score}")

        # Penanganan input pendek / ambiguous: untuk input sangat pendek, butuh threshold lebih tinggi
        if len(user_input_lower) <= 4 and best_score < max(80, MIN_CONFIDENCE_SCORE):
            logger.debug("Short input with low confidence -> treat as ambiguous")
            return None

        # Single-token safeguard: jika user hanya satu kata, pastikan kecocokan sangat kuat
        tokens = extract_keywords(user_input_lower)
        if tokens and len(tokens) == 1 and best_cat is not None:
            kw_list = KEYWORDS.get(best_cat, [])
            token = tokens[0]
            strong = False
            for kw in kw_list:
                # Accept if exact match or high similarity
                if token == kw or token in kw or kw in token:
                    strong = True
                    break
                if fuzz.token_set_ratio(token, kw) >= 90:
                    strong = True
                    break
            if not strong:
                logger.debug(f"Single-token '{token}' not strongly matching category '{best_cat}' -> ambiguous")
                return None

        return best_cat if best_score >= MIN_CONFIDENCE_SCORE else None
    except Exception as e:
        logger.error(f"Error dalam match_category: {str(e)}")
        return None

def get_suggestion():
    """Memberikan saran kategori yang tersedia"""
    try:
        categories = list(KEYWORDS.keys())
        if not categories:
            return "Maaf, tidak ada kategori yang tersedia."
        return f"Kategori yang tersedia: {', '.join(categories)}"
    except Exception as e:
        logger.error(f"Error dalam get_suggestion: {str(e)}")
        return "Maaf, terjadi kesalahan saat mengambil saran kategori."

def safe_get(d, *keys, default=None):
    """Safely get nested dictionary values"""
    if not isinstance(d, dict):
        return default
    
    current = d
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    
    return current

def generate_response(category, user_input):
    """
    Generate response berdasarkan kategori.
    Dengan error handling yang comprehensive.
    """
    try:
        is_valid, error_msg = validate_input(user_input)
        if not is_valid:
            return f"Error: {error_msg}"
        
        if not category:
            suggestions = get_suggestion()
            return f"Maaf, saya tidak paham pertanyaan Anda. {suggestions}"

        if not KB:
            logger.warning("Knowledge base kosong")
            return "Maaf, saya tidak memiliki informasi tentang pertanyaan Anda."

        if category == "jadwal":
            jadwal_data = safe_get(KB, "jadwal")
            if not jadwal_data:
                logger.warning("Data jadwal tidak ditemukan")
                return "Maaf, saya tidak memiliki informasi tentang pertanyaan Anda."
            
            try:
                hari_kerja = jadwal_data.get("hari_kerja", "tidak tersedia")
                jam_buka = jadwal_data.get("jam_buka", "tidak tersedia")
                jam_tutup = jadwal_data.get("jam_tutup", "tidak tersedia")
                istirahat = jadwal_data.get("istirahat", "tidak tersedia")
                return f"Lab buka {hari_kerja} pukul {jam_buka} - {jam_tutup} (istirahat {istirahat})."
            except Exception as e:
                logger.error(f"Error processing jadwal: {str(e)}")
                return "Maaf, saya tidak memiliki informasi tentang pertanyaan Anda."

        elif category == "aturan":
            aturan_data = safe_get(KB, "aturan")
            if not aturan_data:
                logger.warning("Data aturan tidak ditemukan")
                return "Maaf, saya tidak memiliki informasi tentang pertanyaan Anda."
            
            try:
                if "sanksi" in user_input.lower():
                    sanksi = aturan_data.get("sanksi", [])
                    if not sanksi or not isinstance(sanksi, list):
                        return "Maaf, saya tidak memiliki informasi tentang sanksi."
                    s = "\n".join(f"• {x}" for x in sanksi if x)
                    return f"Sanksi:\n{s}" if s else "Maaf, data sanksi tidak tersedia."
                else:
                    syarat = aturan_data.get("syarat", [])
                    if not syarat or not isinstance(syarat, list):
                        return "Maaf, saya tidak memiliki informasi tentang aturan."
                    s = "\n".join(f"• {x}" for x in syarat if x)
                    return f"Aturan lab:\n{s}" if s else "Maaf, data aturan tidak tersedia."
            except Exception as e:
                logger.error(f"Error processing aturan: {str(e)}")
                return "Maaf, saya tidak memiliki informasi tentang pertanyaan Anda."

        elif category == "spesifikasi":
            spesifikasi_data = safe_get(KB, "spesifikasi")
            if not spesifikasi_data:
                logger.warning("Data spesifikasi tidak ditemukan")
                return "Maaf, saya tidak memiliki informasi tentang pertanyaan Anda."
            
            try:
                pc_data = spesifikasi_data.get("pc", {})
                software_list = spesifikasi_data.get("software", [])
                
                if not pc_data or not software_list:
                    return "Maaf, data spesifikasi tidak lengkap."
                
                jumlah = pc_data.get("jumlah", "tidak tersedia")
                processor = pc_data.get("processor", "tidak tersedia")
                ram = pc_data.get("ram", "tidak tersedia")
                os = pc_data.get("os", "tidak tersedia")
                sw = ", ".join(software_list) if isinstance(software_list, list) else "tidak tersedia"
                
                return f"Spesifikasi: {jumlah} PC, {processor}, RAM {ram}, {os}. Software: {sw}"
            except Exception as e:
                logger.error(f"Error processing spesifikasi: {str(e)}")
                return "Maaf, saya tidak memiliki informasi tentang pertanyaan Anda."
        
        elif category == "greeting":
            # Simple friendly replies for greetings and small talk
            return "Halo! Saya asisten Lab ICLABS. Anda bisa menanyakan: 'jam buka', 'aturan lab', atau 'spesifikasi PC'. Ada yang ingin ditanyakan?"
        
        else:
            # Kategori tidak dikenali
            logger.warning(f"Kategori tidak dikenali: {category}")
            return "Maaf, saya tidak memiliki informasi tentang pertanyaan Anda."
    
    except Exception as e:
        logger.error(f"Unexpected error dalam generate_response: {str(e)}")
        return "Maaf, terjadi kesalahan. Silakan coba lagi."
