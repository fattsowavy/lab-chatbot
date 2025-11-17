<<<<<<< HEAD
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
=======
# 📚 Documentation Index

Selamat datang! Berikut adalah panduan lengkap untuk memahami dan menggunakan Chatbot Lab ICLABS FIKOM UMI v2.0.

---

## 🚀 Getting Started (Start Here!)

**👉 Baca pertama:** [QUICKSTART.md](./QUICKSTART.md)

- Installation steps
- Running the application
- Basic testing
- Troubleshooting common issues
- API reference
- Deployment guide

---

## 📖 Documentation Files

### 1. **QUICKSTART.md** - Quick Start Guide

**Untuk siapa?** Pengguna baru yang ingin langsung running
**Isi:**

- Installation & setup
- Configuration
- Testing procedures
- API endpoints
- Troubleshooting

**Mulai dari sini jika Anda ingin:**

- Install dan run chatbot
- Test functionality
- Debug issues

---

### 2. **ROBUSTNESS.md** - Fitur Robustness Terperinci

**Untuk siapa?** Developers & tech leads yang ingin paham engineering
**Isi:**

- Input validation strategy
- Error handling approach
- Rate limiting mechanism
- Session management
- Logging system
- Security features
- Best practices

**Baca ini jika Anda ingin:**

- Understand system architecture
- Learn about security features
- Know how errors are handled
- Configure advanced settings

---

### 3. **MAINTENANCE.md** - Operations & Maintenance

**Untuk siapa?** DevOps & operations team
**Isi:**

- Daily maintenance tasks
- Performance tuning
- Security hardening
- Backup strategy
- Monitoring setup
- Database migration planning
- Version management

**Gunakan ini untuk:**

- Day-to-day operations
- Scaling decisions
- Security improvements
- Backup & disaster recovery
- Monitoring & alerting

---

### 4. **ARCHITECTURE.md** - System Design & Architecture

**Untuk siapa?** System architects & senior developers
**Isi:**

- System overview diagram
- Component details
- Data flow diagrams
- Error handling flow
- Database design (future)
- Deployment architecture
- Performance considerations
- Testing strategy

**Baca ini untuk:**

- Understand how system works
- Plan scaling & expansion
- Design future enhancements
- Setup production infrastructure

---

### 5. **UPGRADE_SUMMARY.md** - What's New in v2.0

**Untuk siapa?** Users upgrading from v1.0
**Isi:**

- Before & after comparison
- File changes summary
- Security improvements
- Performance improvements
- Key learnings
- Next steps

**Referensi ini untuk:**

- Understand what changed
- Learn from improvements
- Plan future upgrades
- Understand best practices

---

## 🛠️ Configuration Files

### `.env` - Environment Configuration

```bash
FLASK_DEBUG=True              # Development mode
SECRET_KEY=your-secret-key    # Change in production!
MIN_CONFIDENCE=50             # Category matching threshold
MAX_INPUT_LENGTH=500          # Max message length
MAX_HISTORY=100               # Max messages per session
LOG_LEVEL=INFO                # Logging detail level
RATE_LIMIT=True               # Enable rate limiting
MAX_REQUESTS=30               # Requests per minute per IP
```

### `config.py` - Python Configuration Module

Centralized configuration loaded from environment variables.

### `knowledge_base.json` - Chat Knowledge Database

Contains all information chatbot can answer about.

---

## 💻 Source Code Files

### `app.py` - Flask Application

- HTTP request handling
- Route definitions
- Session management
- Error handlers
- Rate limiting
- Logging integration

### `utils.py` - NLP Logic

- Input validation
- Category matching (fuzzy)
- Response generation
- Safe data access
- Knowledge base loading

### `logger_config.py` - Logging Setup

- File & console output
- Log rotation
- Timestamp formatting
- Level configuration

### `requirements.txt` - Python Dependencies

All packages needed to run the application.

---

## 📱 Frontend Files

### `templates/index.html`

- Web interface
- Input handling
- Chat display
- Typing indicators
- Timestamps

### `static/style.css` & `static/script.js`

Optional CSS and JavaScript for styling/additional features.

---

## 🗂️ Directory Structure

```
lab-chatbot/
├── 📄 Source Code
│   ├── app.py                    ← Flask application
│   ├── utils.py                  ← NLP logic
│   ├── config.py                 ← Configuration
│   └── logger_config.py           ← Logging setup
│
├── 📋 Data Files
│   ├── knowledge_base.json        ← Chat knowledge
│   ├── requirements.txt           ← Dependencies
│   └── .env                       ← Environment variables
│
├── 🎨 Frontend
│   ├── templates/
│   │   └── index.html            ← Web interface
│   └── static/
│       ├── style.css             ← Styling
│       └── script.js             ← Additional JS
│
├── 📚 Documentation
│   ├── QUICKSTART.md             ← Quick start guide (START HERE!)
│   ├── ROBUSTNESS.md             ← Feature details
│   ├── MAINTENANCE.md            ← Operations guide
│   ├── ARCHITECTURE.md           ← System design
│   ├── UPGRADE_SUMMARY.md        ← What's new
│   └── README.md                 ← This file
│
└── 📁 Runtime
    ├── logs/
    │   └── chatbot.log           ← Application logs (auto-created)
    └── __pycache__/              ← Python cache (auto-created)
```

---

## 🎯 Quick Navigation

### I want to...

**...install and run the chatbot**
→ Read [QUICKSTART.md](./QUICKSTART.md) → Installation section

**...understand security features**
→ Read [ROBUSTNESS.md](./ROBUSTNESS.md) → Security section

**...set up production environment**
→ Read [QUICKSTART.md](./QUICKSTART.md) → Production Deployment section
→ Then read [MAINTENANCE.md](./MAINTENANCE.md) → Security Hardening

**...monitor and maintain the system**
→ Read [MAINTENANCE.md](./MAINTENANCE.md)

**...understand how the system works**
→ Read [ARCHITECTURE.md](./ARCHITECTURE.md)

**...know what's new in v2.0**
→ Read [UPGRADE_SUMMARY.md](./UPGRADE_SUMMARY.md)

**...debug issues**
→ Check logs: `tail -f logs/chatbot.log`
→ Read [QUICKSTART.md](./QUICKSTART.md) → Troubleshooting

**...add new features**
→ Read [ARCHITECTURE.md](./ARCHITECTURE.md) → Design section
→ Then read [MAINTENANCE.md](./MAINTENANCE.md) → Adding New Category

---

## 📚 Reading Order by Role

### For Developers

1. QUICKSTART.md - Get it running
2. ARCHITECTURE.md - Understand design
3. ROBUSTNESS.md - Learn features
4. Source code (app.py, utils.py)

### For DevOps/Operations

1. QUICKSTART.md - Installation & basic setup
2. MAINTENANCE.md - Daily operations
3. ARCHITECTURE.md - Deployment architecture
4. ROBUSTNESS.md - Monitoring section

### For Managers/Tech Leads

1. UPGRADE_SUMMARY.md - Quick overview
2. ROBUSTNESS.md - Feature summary
3. ARCHITECTURE.md - System overview
4. MAINTENANCE.md - Roadmap section

### For System Architects

1. ARCHITECTURE.md - Start here
2. ROBUSTNESS.md - Deep dive into features
3. MAINTENANCE.md - Scaling and optimization
4. Source code - Implementation details

---

## ✨ Key Features

### Input Validation

- Max 500 characters per message
- Empty input detection
- Whitespace validation
- See: ROBUSTNESS.md → Input Validation

### Error Handling

- Comprehensive exception catching
- Graceful degradation
- Meaningful error messages
- See: ROBUSTNESS.md → Error Handling

### Rate Limiting

- 30 requests per minute per IP
- Automatic cleanup
- Configurable
- See: ROBUSTNESS.md → Security Features

### Session Management

- UUID-based session IDs
- Automatic timeout (1 hour)
- Conversation history (max 100 messages)
- See: ROBUSTNESS.md → Session Management

### Logging

- File + console output
- Automatic rotation (5MB per file)
- Structured format with timestamps
- See: ROBUSTNESS.md → Logging & Monitoring

---

## 🔧 Configuration Quick Reference

| Setting          | Default | Type   | File |
| ---------------- | ------- | ------ | ---- |
| DEBUG            | True    | bool   | .env |
| SECRET_KEY       | dev-key | string | .env |
| MIN_CONFIDENCE   | 50      | int    | .env |
| MAX_INPUT_LENGTH | 500     | int    | .env |
| MAX_HISTORY      | 100     | int    | .env |
| LOG_LEVEL        | INFO    | string | .env |
| RATE_LIMIT       | True    | bool   | .env |
| MAX_REQUESTS     | 30      | int    | .env |

Change in `.env` file and restart application.

---

## 📊 Useful Commands

### Installation

```bash
pip install -r requirements.txt
```

### Running

```bash
python app.py              # Development mode
FLASK_DEBUG=False python app.py  # Production
```

### Testing

```bash
# Health check
curl http://localhost:5000/health

# Chat test
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Berapa jam buka?"}'

# View logs
tail -f logs/chatbot.log
```

### Configuration

```bash
# Edit settings
nano .env

# Restart to apply
python app.py
```

---

## 🚨 Troubleshooting Quick Links

| Issue                 | Reference                                 |
| --------------------- | ----------------------------------------- |
| Installation failed   | QUICKSTART.md → Troubleshooting           |
| Port 5000 in use      | QUICKSTART.md → Troubleshooting           |
| Knowledge base errors | QUICKSTART.md → Troubleshooting           |
| Rate limiting issues  | MAINTENANCE.md → Tuning                   |
| Performance problems  | MAINTENANCE.md → Performance Optimization |
| Security concerns     | ROBUSTNESS.md → Security Features         |
| Memory usage high     | MAINTENANCE.md → Troubleshooting          |

---

## 📞 Support Resources

1. **Check logs first**

   ```bash
   tail -f logs/chatbot.log
   ```

2. **Review documentation**

   - Find your role above in "Reading Order"
   - Look for relevant section

3. **Test with cURL**

   - Use API testing commands in QUICKSTART.md
   - Check response and error messages

4. **Enable debug logging**
   ```bash
   # In .env
   LOG_LEVEL=DEBUG
   # Restart and check logs for more details
   ```

---

## 📈 Version Info

- **Current Version**: 2.0.0
- **Release Date**: November 17, 2025
- **Status**: Production Ready ✅
- **Previous**: 1.0.0 (Basic version)

### What's Different from v1.0?

See [UPGRADE_SUMMARY.md](./UPGRADE_SUMMARY.md)

---

## 🎓 Learning Path

```
START
  ↓
├─→ QUICKSTART.md (5 mins)
│   ├─→ Install & run (10 mins)
│   └─→ Test API (5 mins)
│
├─→ ROBUSTNESS.md (15 mins)
│   └─→ Understand features
│
├─→ ARCHITECTURE.md (20 mins)
│   └─→ System design deep dive
│
└─→ Source Code Review
    └─→ app.py, utils.py (30 mins)

TOTAL: ~85 minutes to full understanding
```

---

## ✅ Checklist for Getting Started

- [ ] Read QUICKSTART.md
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run application: `python app.py`
- [ ] Open browser: `http://localhost:5000`
- [ ] Test with sample questions
- [ ] Check logs: `tail -f logs/chatbot.log`
- [ ] Test API endpoints with cURL
- [ ] Review ROBUSTNESS.md for features
- [ ] Update .env for your environment
- [ ] Deploy to production when ready

---

## 🎉 You're Ready!

Chatbot Anda siap untuk digunakan. Mulai dari [QUICKSTART.md](./QUICKSTART.md) dan nikmati!

Untuk pertanyaan atau issues:

1. Check logs
2. Review relevant documentation
3. Run diagnostic commands
4. Enable debug logging if needed

**Happy chatting! 🤖💬**
>>>>>>> 5d4ae0c (fix: error handling)
