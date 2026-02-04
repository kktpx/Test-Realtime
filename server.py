import time  # <--- 1. อย่าลืม import time
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ตัวแปรเก็บเวลาล่าสุดที่เจอโจมตี
last_attack_time = 0
attack_cooldown = 3.0  # ให้โชว์ค้างไว้อย่างน้อย 3 วินาที

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/predict', methods=['POST'])
def receive_data():
    global last_attack_time
    data = request.json
    
    # ถ้าเจอ Count สูงๆ (ที่เราจำลองไว้ใน Agent ตอนเจอ Ping)
    if data.get('count', 0) > 100:
        last_attack_time = time.time() # จดเวลาที่เจอโจมตีไว้
        current_status = "⚠️ Neptune (DoS Attack) Detected!"
    else:
        current_status = "✅ Normal Traffic"
        
    # ไม่ต้อง return status กลับไปที่ Agent ก็ได้ เพื่อความรวดเร็ว
    return jsonify({'result': 'received'})

@app.route('/api/status', methods=['GET'])
def get_status():
    global last_attack_time
    
    # คำนวณเวลา: ถ้าเพิ่งเจอโจมตีไปไม่ถึง 3 วินาที ให้บังคับโชว์ว่า Attack
    if (time.time() - last_attack_time) < attack_cooldown:
        return jsonify({'result': "⚠️ Neptune (DoS Attack) Detected!"})
    else:
        return jsonify({'result': "✅ Normal Traffic"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)