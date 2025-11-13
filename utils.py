import json
import re
from fuzzywuzzy import fuzz

with open('knowledge_base.json', 'r', encoding='utf-8') as f:
    KB = json.load(f)
    
KEYWORDS = {
    "jadwal": ["jadwal", "buka", "tutup", "istirahat", "hari kerja"],
    "aturan": ["aturan", "sanksi", "syarat", "peraturan", "dilarang"],
    "spesifikasi": ["spesifikasi", "pc", "komputer", "software", "hardware", "mysql"]
}
def extract_keywords(text):
    return re.findall(r'\b\w+\b', text.lower())

def match_category(user_input):
    best_score = 0
    best_cat = None
    for cat, words in KEYWORDS.items():
        score = sum(fuzz.partial_ratio(word, user_input.lower()) for word in words)
        if score > best_score:
            best_score = score
            best_cat = cat
    return best_cat if best_score >= 50 else None

def generate_response(category, user_input):
    if not category:
        return "Maaf, saya tidak paham. Coba tanya: jam buka, aturan, atau spesifikasi PC."

    if category == "jadwal":
        j = KB["jadwal"]
        return f"Lab buka {j['hari_kerja']} pukul {j['jam_buka']} - {j['jam_tutup']} (istirahat {j['istirahat']})."

    if category == "aturan":
        if "sanksi" in user_input.lower():
            s = "\n".join(f"• {x}" for x in KB["aturan"]["sanksi"])
            return f"Sanksi:\n{s}"
        else:
            s = "\n".join(f"• {x}" for x in KB["aturan"]["syarat"])
            return f"Aturan lab:\n{s}"

    if category == "spesifikasi":
        p = KB["spesifikasi"]["pc"]
        sw = ", ".join(KB["spesifikasi"]["software"])
        return f"Spesifikasi: {p['jumlah']} PC, {p['processor']}, RAM {p['ram']}, {p['os']}. Software: {sw}"