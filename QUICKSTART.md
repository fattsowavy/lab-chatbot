# 🚀 Quick Start Guide - Lab Chatbot v2.0

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- Git (optional)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Knowledge Base

```bash
# Pastikan knowledge_base.json ada di root directory
ls knowledge_base.json
```

### 3. Run Application

```bash
# Development mode (dengan auto-reload)
python app.py

# Atau dengan environment variable
FLASK_DEBUG=True python app.py
```

### 4. Access Chatbot

Buka browser dan navigasi ke:

```
http://localhost:5000
```

---

## Configuration

Edit `.env` file untuk mengubah konfigurasi:

```bash
# Flask Settings
FLASK_DEBUG=True              # Development mode
SECRET_KEY=your-secret-key    # Change this in production!

# Chatbot Settings
MIN_CONFIDENCE=50             # Threshold untuk category matching
MAX_INPUT_LENGTH=500          # Maximum karakter per pesan
MAX_HISTORY=100               # Maximum messages per session

# Logging
LOG_LEVEL=INFO                # DEBUG, INFO, WARNING, ERROR
LOG_FILE=chatbot.log          # Log file name

# Rate Limiting
RATE_LIMIT=True               # Enable/disable rate limiting
MAX_REQUESTS=30               # Requests per minute per IP
```

---

## Troubleshooting

### Error: "Port 5000 already in use"

```bash
# Linux/Mac: Kill process on port 5000
lsof -i :5000
kill -9 <PID>

# Windows: PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force
```

### Error: "knowledge_base.json tidak ditemukan"

```bash
# Pastikan file ada di root directory (same folder as app.py)
# Atau update KB_FILE di .env
```

### Error: "Module not found"

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Application crashes on startup

```bash
# Check logs
tail -f logs/chatbot.log

# Run dengan verbose output
python -u app.py
```

---

## Testing

### Manual Testing

#### Test Category Matching

```bash
# Jadwal
"Berapa jam buka lab?"

# Aturan
"Apa saja aturan lab?"

# Spesifikasi
"Bagaimana spesifikasi PC lab?"

# Non-matching
"Cita-cita saya adalah..."
```

#### Test Error Handling

```bash
# Empty input - akan error

# Very long input (copy 500+ chars) - akan error

# Invalid JSON - POST dengan invalid JSON

# Rate limiting - send 30+ requests per minute
```

### Health Check

```bash
curl http://localhost:5000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-11-17T...",
  "active_sessions": 1
}
```

---

## Production Deployment

### Security Checklist

- [ ] Change `SECRET_KEY` di `.env`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Set `LOG_LEVEL=WARNING`
- [ ] Configure proper logging paths
- [ ] Set up HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up monitoring/alerting

### Environment Setup

```bash
# Create production config
export FLASK_ENV=production
export FLASK_DEBUG=False
export SECRET_KEY=<generate-secure-key>
```

### Running with Production Server

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Monitoring

```bash
# Watch logs in real-time
tail -f logs/chatbot.log

# Check disk space for logs
du -h logs/

# Rotate logs if needed
# (Automatic rotation at 5MB per file)
```

---

## File Structure

```
lab-chatbot/
├── app.py                    # Main Flask application
├── utils.py                  # NLP & response logic
├── config.py                 # Configuration management
├── logger_config.py          # Logging setup
├── knowledge_base.json       # Knowledge database
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── ROBUSTNESS.md            # Detailed robustness doc
├── QUICKSTART.md            # This file
├── templates/
│   └── index.html           # Web interface
├── static/
│   ├── style.css           # CSS (if needed)
│   └── script.js           # JS (if needed)
└── logs/                    # Log files (auto-created)
    └── chatbot.log
```

---

## API Reference

### POST /chat

Send a message to the chatbot.

**Request:**

```json
{
  "message": "Berapa jam buka lab?"
}
```

**Response (Success):**

```json
{
  "response": "Lab buka Senin - Sabtu pukul 07:00 - 18:00 (istirahat 12:00 - 13:00).",
  "category": "jadwal",
  "success": true
}
```

**Response (Error):**

```json
{
  "error": "Pesan tidak boleh kosong"
}
```

---

### GET /history

Retrieve conversation history.

**Response:**

```json
{
  "history": [
    {
      "user": "Berapa jam buka lab?",
      "bot": "Lab buka...",
      "category": "jadwal",
      "timestamp": "2025-11-17T10:30:00"
    }
  ]
}
```

---

### POST /clear

Clear conversation history.

**Response:**

```json
{
  "success": true
}
```

---

### GET /health

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2025-11-17T10:30:00",
  "active_sessions": 5
}
```

---

## Common Issues & Solutions

| Issue                                                  | Solution                                          |
| ------------------------------------------------------ | ------------------------------------------------- |
| "Kategori tidak ditemukan"                             | Pastikan KEYWORDS di utils.py sesuai dengan KB    |
| Bot selalu jawab "Maaf, saya tidak memiliki informasi" | Check knowledge_base.json format                  |
| Rate limiting blocks requests                          | Tunggu 1 menit atau increase MAX_REQUESTS di .env |
| Logs tidak tercatat                                    | Check permissions di logs/ folder                 |
| Memory usage tinggi                                    | Reduce MAX_HISTORY di .env                        |

---

## Support & Debugging

### Enable Debug Logging

```bash
# Update .env
LOG_LEVEL=DEBUG

# Restart application
python app.py
```

### View Detailed Logs

```bash
# Windows
type logs\chatbot.log

# Linux/Mac
cat logs/chatbot.log
```

### Test dengan cURL

```bash
# Send message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Berapa jam buka?"}'

# Get history
curl http://localhost:5000/history

# Health check
curl http://localhost:5000/health
```

---

## Next Steps

1. ✅ Customize knowledge base sesuai kebutuhan
2. ✅ Add more categories dan keywords
3. ✅ Setup production environment
4. ✅ Configure monitoring/alerting
5. ✅ Deploy ke server

---

**Happy Chatting! 🤖💬**

Untuk pertanyaan atau issues, check logs dan documentation di `ROBUSTNESS.md`.
