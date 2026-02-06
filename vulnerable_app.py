import logging
from flask import Flask, request, render_template_string, redirect, url_for

# ตั้งค่า Log
logging.basicConfig(filename='access.log', level=logging.INFO, format='%(message)s')

app = Flask(__name__)

# เก็บ IP ที่โดนแบน (Memory)
BLOCKED_IPS = set()

# HTML Templates (ใส่ไว้ในไฟล์เดียวเลย ง่ายดี)
LOGIN_PAGE = """
<h2>🏦 Vulnerable Bank Login</h2>
<form action="/login" method="GET">
    User: <input type="text" name="user"><br>
    Pass: <input type="password" name="pass"><br>
    <button type="submit">Login</button>
</form>
<p style="color:gray">Try SQLi: admin' OR '1'='1</p>
"""

DASHBOARD_PAGE = """
<h1 style="color:green">✅ Welcome, Admin!</h1>
<p>This is the secret dashboard. You have bypassed the login!</p>
<hr>
<h3>💰 Balance: $1,000,000</h3>
<ul>
    <li><a href="/search?q=secret">Search Secret Data</a></li>
    <li><a href="/comment">Post Announcement</a></li>
    <li><a href="/logout">Logout</a></li>
</ul>
"""

ERROR_PAGE = """
<h2 style="color:red">❌ Login Failed</h2>
<a href="/">Try Again</a>
"""

# --- Routes ---

@app.route('/')
def home():
    return LOGIN_PAGE

@app.route('/login')
def login():
    # จำลองการตรวจสอบ Login
    user = request.args.get('user', '')
    password = request.args.get('pass', '')
    
    # บันทึก Log ตามปกติ
    log_request(request)

    # 🛑 จำลองช่องโหว่ SQL Injection แบบโง่ๆ
    # ถ้า user มีคำว่า OR '1'='1 ให้ถือว่าผ่านเลย (Bypass)
    if "OR '1'='1" in user or "OR 1=1" in user or user == "admin":
        return DASHBOARD_PAGE
    
    return ERROR_PAGE

@app.route('/dashboard')
def dashboard():
    return DASHBOARD_PAGE

@app.route('/search')
def search():
    log_request(request)
    q = request.args.get('q', '')
    # Reflected XSS: เอาสิ่งที่ user พิมพ์ มาแสดงผลตรงๆ โดยไม่กรอง
    return f"<h2>Search Results for: {q}</h2><p>No data found.</p>"

@app.route('/comment')
def comment():
    log_request(request)
    msg = request.args.get('msg', '')
    if msg:
        return f"<h2>Comment Posted:</h2><div style='border:1px solid #ccc; padding:10px'>{msg}</div>"
    return "<h2>Post Comment</h2><form><input name='msg'><button>Post</button></form>"

@app.route('/block_ip', methods=['POST'])
def block_ip():
    data = request.json
    ip = data.get('ip')
    if ip:
        BLOCKED_IPS.add(ip)
        return {"status": "blocked", "ip": ip}
    return {"status": "error"}

def log_request(req):
    # เช็ก IP Block
    if req.remote_addr in BLOCKED_IPS:
        return "BLOCKED"

    # เขียน Log
    full_query = req.query_string.decode("utf-8")
    if full_query:
        log_line = f"GET {req.path}?{full_query}"
    else:
        log_line = f"GET {req.path}"
    
    logging.info(log_line)
    for handler in logging.getLogger().handlers:
        handler.flush()
    print(f"📝 Request: {log_line}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)