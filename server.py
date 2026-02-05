from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import logging

# ปิด Log จุกจิกของ Flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    
    # --- 🤖 ส่วนที่เพิ่มมา: รองรับผลลัพธ์จาก AI Agent ---
    if 'attack_type' in data and data['attack_type'] != "Normal":
        attack_name = data['attack_type']
        print(f"🔥 Dashboard Alert: {attack_name}")
        
        # ส่งไปหน้าเว็บให้เด้งสีแดงพร้อมชื่อท่า
        socketio.emit('update_status', {
            'status': 'Danger',
            'message': f"{attack_name} Detected!",
            'color': '#dc3545'  # สีแดง
        })
        return jsonify({'result': 'AI Alert Received'})
    # ------------------------------------------------

    # (Logic เดิมสำหรับ Neptune/DoS ปล่อยไว้เหมือนเดิมก็ได้ หรือจะลบออกถ้าไม่ใช้แล้ว)
    return jsonify({'result': 'Normal'})

if __name__ == '__main__':
    # รันที่ Port 5000 (ศูนย์บัญชาการ)
    print("🏢 Dashboard Server running on port 5000...")
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)