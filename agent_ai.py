import time
import requests
import joblib
import os

LOG_FILE = 'access.log'
DASHBOARD_URL = "http://127.0.0.1:5000/api/predict"

# 🧠 โหลดสมอง AI ที่เราเทรนไว้
print("🧠 Loading AI Brain...")
if not os.path.exists('security_model.pkl'):
    print("❌ Error: ไม่เจอไฟล์ security_model.pkl (กรุณารัน train_ai.py ก่อน)")
    exit()

model = joblib.load('security_model.pkl')
print("✅ AI Ready!")

def ai_analyze(log_line):
    # ให้ AI ทำนาย (Predict)
    prediction = model.predict([log_line])[0]
    
    # ดูความมั่นใจ (Confidence) ของ AI (ลูกเล่นเสริม)
    probability = model.predict_proba([log_line]).max() * 100
    
    return prediction, probability

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

print(f"🕵️‍♀️ AI Agent Started... Monitoring: {LOG_FILE}")

# สร้างไฟล์ Log ดักไว้ก่อนถ้ายังไม่มี
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, 'w').close()

with open(LOG_FILE, 'r') as logfile:
    for line in follow(logfile):
        line = line.strip()
        if not line: continue
        
        # ส่งเข้า AI 
        result, confidence = ai_analyze(line)
        
        print(f"👁️ Scanned: {line[:50]}... -> 🤖 AI Says: {result} ({confidence:.1f}%)")
        
        # ถ้า AI บอกไม่ใช่ Normal ให้แจ้งเตือน Server
        if result != "Normal":
            payload = {
                "attack_type": result, # ส่งผลลัพธ์จาก AI ไปเลย
                "count": 999,
                # ค่าอื่นๆ ใส่หลอกไว้
                "protocol_type": "http",
                "service": "http_auth",
                "flag": "S0",
                "src_bytes": 0,
                "dst_bytes": 0,
                "same_srv_rate": 0.0
            }
            try:
                requests.post(DASHBOARD_URL, json=payload, timeout=1)
            except:
                pass