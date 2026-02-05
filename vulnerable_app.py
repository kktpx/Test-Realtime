import logging
from flask import Flask, request

# ตั้งค่าให้จด Log ลงไฟล์ 'access.log'
logging.basicConfig(filename='access.log', level=logging.INFO, 
                    format='%(message)s')

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Banking Login (Vulnerable)</h1>
    <form action="/login" method="get">
        User: <input type="text" name="user"><br>
        Pass: <input type="text" name="pass"><br>
        <input type="submit" value="Login">
    </form>
    """

@app.route('/login', methods=['GET'])
def login():
    user = request.args.get('user', '')
    password = request.args.get('pass', '')
    
    # 📝 จด Log รูปแบบเดียวกับที่เทรน AI มา
    # รูปแบบ: GET /login?user=...
    log_line = f"GET /login?user={user}&pass={password}"
    
    # บันทึกลงไฟล์ + ปริ้นหน้าจอ
    logging.info(log_line)
    print(f"📝 Logged: {log_line}")
    
    return f"<h3>Processing login for: {user}</h3>"

if __name__ == '__main__':
    # รันที่ Port 8080 (แยกกับ Dashboard)
    print("🎯 Vulnerable App running on port 8080...")
    app.run(host='0.0.0.0', port=8080)