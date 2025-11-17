# 🎯 Best Practices & Maintenance Guide

## Daily Maintenance

### Check Logs

```bash
# Monitor real-time logs
tail -f logs/chatbot.log

# Check for errors
grep ERROR logs/chatbot.log | tail -20

# Check disk usage
du -h logs/
```

### Clean Up Old Logs

```bash
# Automatic rotation happens at 5MB
# But you can manually cleanup old files
find logs/ -name "*.log.*" -type f -mtime +30 -delete
```

---

## Updating Knowledge Base

### Adding New Category

1. **Add to KEYWORDS in utils.py**

```python
KEYWORDS = {
    "jadwal": [...],
    "aturan": [...],
    "spesifikasi": [...],
    "kontak": [...],         # ← Add here
    "fasilitas": [...]
}
```

2. **Add to knowledge_base.json**

```json
{
  "kontak": {
    "email": "lab@umi.ac.id",
    "telepon": "(021) 123-4567",
    "lokasi": "Gedung A Lantai 3"
  }
}
```

3. **Add handler in generate_response()**

```python
elif category == "kontak":
    kontak_data = safe_get(KB, "kontak")
    if not kontak_data:
        return "Maaf, saya tidak memiliki informasi..."
    return format_response(kontak_data)
```

4. **Test**

```bash
# Test dengan pertanyaan yang cocok
# "Hubungi lab" atau "Email lab" dll
```

---

## Performance Optimization

### Current Limits

- **Max input**: 500 characters
- **Max history**: 100 messages per session
- **Rate limit**: 30 requests per minute per IP
- **Log file size**: 5MB before rotation

### Tuning for Different Scenarios

**Low Traffic Site**

```env
MAX_REQUESTS=60          # Allow more requests
MAX_HISTORY=200          # Keep more history
LOG_LEVEL=INFO           # Normal logging
```

**High Traffic Site**

```env
MAX_REQUESTS=10          # Stricter rate limiting
MAX_HISTORY=50           # Less history to save memory
LOG_LEVEL=WARNING        # Less logging overhead
```

**Low Memory Device**

```env
MAX_HISTORY=20           # Very limited history
FLASK_DEBUG=False        # No debug overhead
LOG_LEVEL=ERROR          # Only errors
```

---

## Security Hardening

### Before Production Deployment

1. **Update SECRET_KEY**

```bash
# Generate secure key
python -c "import secrets; print(secrets.token_hex(32))"

# Update .env
SECRET_KEY=<output dari command di atas>
```

2. **Disable Debug Mode**

```env
FLASK_DEBUG=False
```

3. **Set Secure Headers**

```python
# Add to app.py if needed:
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response
```

4. **Enable HTTPS**

```bash
# Use reverse proxy (nginx) atau load balancer
# Always use SSL/TLS in production
```

5. **Restrict CORS** (jika diperlukan)

```python
from flask_cors import CORS
CORS(app, origins=["yourdomain.com"])
```

---

## Monitoring & Alerting

### Health Check

```bash
# Check every 5 minutes
*/5 * * * * curl -s http://localhost:5000/health

# Alert if down
if [ $? -ne 0 ]; then
  # Send alert
  mail -s "Chatbot Down" admin@example.com
fi
```

### Log Monitoring

```bash
# Alert on errors
tail -f logs/chatbot.log | grep ERROR &

# Count errors per hour
grep ERROR logs/chatbot.log | \
  awk '{print $1, $2}' | \
  uniq -c
```

### Performance Metrics

```python
# Add to utils.py untuk track performance
import time

def time_operation(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper
```

---

## Backup Strategy

### Daily Backup

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/chatbot"
mkdir -p $BACKUP_DIR

# Backup knowledge base
cp knowledge_base.json $BACKUP_DIR/kb_$(date +%Y%m%d).json

# Backup logs
tar -czf $BACKUP_DIR/logs_$(date +%Y%m%d).tar.gz logs/

# Keep only last 30 days
find $BACKUP_DIR -type f -mtime +30 -delete
```

### Schedule with cron

```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
```

---

## Troubleshooting Guide

### Problem: High Memory Usage

**Symptoms**: Memory keeps increasing

**Solutions**:

1. Reduce MAX_HISTORY
2. Check for memory leaks in custom code
3. Restart application daily
4. Use memory profiler:

```bash
pip install memory-profiler
python -m memory_profiler app.py
```

---

### Problem: Slow Response Time

**Symptoms**: Chatbot takes 2+ seconds to respond

**Solutions**:

1. Check logs for slow operations
2. Profile with:

```python
import cProfile
cProfile.run('match_category(user_input)')
```

3. Optimize fuzzy matching threshold
4. Cache KB if not changing frequently

---

### Problem: Rate Limiting Too Strict

**Symptoms**: Users getting 429 errors

**Solutions**:

1. Increase MAX_REQUESTS
2. Whitelist trusted IPs
3. Implement per-user rate limiting instead of per-IP

---

### Problem: Knowledge Base Corruption

**Symptoms**: JSON errors in logs

**Solutions**:

1. Validate JSON syntax:

```bash
python -m json.tool knowledge_base.json > /dev/null
```

2. Restore from backup
3. Check encoding (must be UTF-8)

---

## Database Migration (Future)

When moving to real database:

```python
# Current (in-memory):
conversation_history = {}

# Future (SQL):
# Store to database instead
# with automatic cleanup of old records

# Schema example:
# CREATE TABLE conversations (
#     id INT PRIMARY KEY,
#     session_id VARCHAR(36),
#     user_msg TEXT,
#     bot_response TEXT,
#     category VARCHAR(50),
#     timestamp DATETIME
# );
```

---

## Testing Checklist

### Unit Testing

- [ ] test_validate_input()
- [ ] test_match_category()
- [ ] test_safe_get()
- [ ] test_generate_response()

### Integration Testing

- [ ] test_chat_endpoint()
- [ ] test_history_endpoint()
- [ ] test_clear_endpoint()

### Stress Testing

- [ ] Send 1000 messages per minute
- [ ] Check memory usage
- [ ] Check response time
- [ ] Check for data corruption

### Security Testing

- [ ] SQL injection attempts (if DB added)
- [ ] XSS attempts
- [ ] Large payload attacks
- [ ] Rate limiting bypass

---

## Version Management

### Semantic Versioning

- **v1.0.0** - Initial release
- **v2.0.0** - Robustness improvements (current)
- **v2.1.0** - Bug fixes
- **v3.0.0** - Major features (database, ML, etc)

### Changelog

```markdown
## [2.0.0] - 2025-11-17

### Added

- Comprehensive error handling
- Rate limiting
- Logging system
- Configuration management
- Health check endpoint

### Changed

- Improved input validation
- Better error messages
- Session management

### Fixed

- Memory leaks
- Edge cases in matching
```

---

## Development Workflow

### Local Development

```bash
1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Copy .env and customize
5. Run app.py
6. Test with sample inputs
7. Check logs for errors
```

### Before Commit

```bash
1. Run tests
2. Check code quality
3. Update documentation
4. Verify no sensitive data in code
5. Clean up debug logs
```

### Deployment

```bash
1. Merge to main branch
2. Tag with version
3. Run tests in staging
4. Deploy to production
5. Monitor logs and metrics
6. Alert team on success
```

---

## Resources

### Documentation

- ROBUSTNESS.md - Detailed robustness features
- QUICKSTART.md - Quick start guide
- This file - Best practices

### Tools

- `python -m json.tool` - Validate JSON
- `grep` - Search logs
- `tail -f` - Monitor logs
- `curl` - Test endpoints

### External Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [FuzzyWuzzy Docs](https://github.com/seatgeek/fuzzywuzzy)
- [Python Logging](https://docs.python.org/3/library/logging.html)

---

## Contact & Support

For issues or improvements:

1. Check logs first
2. Review error messages
3. Consult ROBUSTNESS.md
4. Check knowledge_base.json format
5. Enable DEBUG logging for details

---

**Remember**: A robust system is one that fails gracefully and logs well! 📝✨
