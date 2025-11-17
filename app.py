from flask import Flask, render_template, request, jsonify, session
from utils import match_category, generate_response
from logger_config import logger
from config import SECRET_KEY, SESSION_LIFETIME, MAX_CONVERSATION_HISTORY, DEBUG, TESTING
from datetime import datetime, timedelta
import uuid
from functools import wraps
import json

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = SESSION_LIFETIME

# Store conversation history in memory (untuk development)
conversation_history = {}
request_count = {}  # untuk rate limiting

def rate_limit(max_requests=30, time_window=60):
    """Decorator untuk rate limiting"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                client_ip = request.remote_addr
                now = datetime.now()
                
                if client_ip not in request_count:
                    request_count[client_ip] = []
                
                # Clean old requests
                request_count[client_ip] = [
                    req_time for req_time in request_count[client_ip]
                    if (now - req_time).seconds < time_window
                ]
                
                if len(request_count[client_ip]) >= max_requests:
                    logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                    return jsonify({"error": "Terlalu banyak permintaan. Coba lagi nanti."}), 429
                
                request_count[client_ip].append(now)
                return f(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error dalam rate_limit: {str(e)}")
                return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def cleanup_old_sessions():
    """Bersihkan session yang sudah expired"""
    try:
        now = datetime.now()
        expired_sessions = []
        
        for session_id in list(conversation_history.keys()):
            if len(conversation_history[session_id]) > MAX_CONVERSATION_HISTORY:
                # Jaga hanya history terbaru
                conversation_history[session_id] = conversation_history[session_id][-MAX_CONVERSATION_HISTORY:]
        
        logger.debug(f"Cleanup sessions completed. Active sessions: {len(conversation_history)}")
    except Exception as e:
        logger.error(f"Error dalam cleanup_old_sessions: {str(e)}")

@app.before_request
def before_request():
    """Jalankan sebelum setiap request"""
    try:
        session.permanent = True
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
            conversation_history[session['session_id']] = []
            logger.info(f"New session created: {session['session_id']}")
    except Exception as e:
        logger.error(f"Error dalam before_request: {str(e)}")

@app.route("/", methods=["GET"])
def index():
    """Render halaman utama"""
    try:
        logger.info(f"Index page accessed from {request.remote_addr}")
        return render_template("index.html")
    except Exception as e:
        logger.error(f"Error rendering index: {str(e)}")
        return jsonify({"error": "Terjadi kesalahan saat memuat halaman."}), 500

@app.route("/chat", methods=["POST"])
@rate_limit(max_requests=30, time_window=60)
def chat():
    """Endpoint untuk chat dengan bot"""
    try:
        # Validasi request
        if not request.is_json:
            logger.warning("Invalid content type in chat request")
            return jsonify({"error": "Content-Type harus application/json"}), 400
        
        user_msg = request.json.get("message", "").strip()
        session_id = session.get('session_id', str(uuid.uuid4()))
        
        # Validasi input
        if not user_msg:
            logger.warning(f"[{session_id}] Empty message received")
            return jsonify({"error": "Pesan tidak boleh kosong"}), 400
        
        if len(user_msg) > 500:
            logger.warning(f"[{session_id}] Message too long: {len(user_msg)}")
            return jsonify({"error": "Pesan terlalu panjang (maksimal 500 karakter)"}), 400
        
        logger.info(f"[{session_id}] User message: {user_msg}")
        
        # Initialize history jika belum ada
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        # Match category dan generate response
        category = match_category(user_msg)
        bot_response = generate_response(category, user_msg)
        
        logger.info(f"[{session_id}] Bot response category: {category}")
        
        # Store dalam history
        conversation_record = {
            "user": user_msg,
            "bot": bot_response,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
        
        conversation_history[session_id].append(conversation_record)
        
        # Cleanup history jika terlalu panjang
        if len(conversation_history[session_id]) > MAX_CONVERSATION_HISTORY:
            conversation_history[session_id] = conversation_history[session_id][-MAX_CONVERSATION_HISTORY:]
        
        return jsonify({
            "response": bot_response,
            "category": category,
            "success": True
        }), 200
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request")
        return jsonify({"error": "Format JSON tidak valid"}), 400
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "Maaf, terjadi kesalahan server."}), 500

@app.route("/history", methods=["GET"])
@rate_limit(max_requests=30, time_window=60)
def get_history():
    """Endpoint untuk mendapatkan history percakapan"""
    try:
        session_id = session.get('session_id')
        
        if not session_id or session_id not in conversation_history:
            logger.warning(f"History requested for invalid session: {session_id}")
            return jsonify({"history": []}), 200
        
        logger.debug(f"[{session_id}] History retrieved: {len(conversation_history[session_id])} items")
        return jsonify({"history": conversation_history[session_id]}), 200
    
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        return jsonify({"error": "Gagal mengambil history"}), 500

@app.route("/clear", methods=["POST"])
@rate_limit(max_requests=30, time_window=60)
def clear_history():
    """Endpoint untuk clear history percakapan"""
    try:
        session_id = session.get('session_id')
        
        if session_id in conversation_history:
            conversation_history[session_id] = []
            logger.info(f"[{session_id}] Conversation history cleared")
        
        return jsonify({"success": True}), 200
    
    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}")
        return jsonify({"error": "Gagal menghapus history"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "active_sessions": len(conversation_history)
        }), 200
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return jsonify({"status": "unhealthy"}), 500

@app.errorhandler(400)
def bad_request(e):
    logger.warning(f"400 Bad Request: {str(e)}")
    return jsonify({"error": "Bad Request"}), 400

@app.errorhandler(404)
def not_found(e):
    logger.warning(f"404 Not Found: {request.path}")
    return jsonify({"error": "Endpoint tidak ditemukan"}), 404

@app.errorhandler(429)
def rate_limit_exceeded(e):
    logger.warning(f"429 Rate Limit Exceeded: {request.remote_addr}")
    return jsonify({"error": "Terlalu banyak permintaan"}), 429

@app.errorhandler(500)
def server_error(e):
    logger.error(f"500 Internal Server Error: {str(e)}")
    return jsonify({"error": "Terjadi kesalahan server"}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({"error": "Terjadi kesalahan yang tidak terduga"}), 500

if __name__ == "__main__":
    try:
        logger.info("Starting Flask application...")
        app.run(
            debug=DEBUG,
            host='0.0.0.0',
            port=5000,
            use_reloader=DEBUG
        )
    except Exception as e:
        logger.critical(f"Failed to start application: {str(e)}", exc_info=True)
        exit(1)
