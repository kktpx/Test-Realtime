import time
import joblib
import requests
import os
import urllib.parse  # ใช้สำหรับถอดรหัส URL

LOG_FILE = 'access.log'
DASHBOARD_URL = 'http://127.0.0.1:5000/api/predict'

print("🧠 Loading AI Brain...")
# โหลดโมเดล
model = joblib.load('security_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')
print("✅ AI Ready!")

def monitor_log():
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()

    f = open(LOG_FILE, 'r')
    f.seek(0, 2) # ไปที่ท้ายไฟล์

    print("🕵️ AI Agent Monitoring started...")
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
            
        line = line.strip()
        if not line: continue

        # --- 🧹 1. ขั้นตอนทำความสะอาด (Cleaning) ---
        
        # ตัดส่วน IP Address ข้างหน้าทิ้ง (เอาตั้งแต่ GET หรือ POST)
        if "GET" in line:
            line = line[line.find("GET"):]
        elif "POST" in line:
            line = line[line.find("POST"):]
            
        # ... (โค้ดส่วนตัด HTTP และ IP เหมือนเดิม) ...
        
        # ตัด HTTP/1.1 ทิ้ง
        if " HTTP/" in line:
            line = line.split(" HTTP/")[0]
            
        # 🔥 เพิ่มบรรทัดนี้: ถ้าเจอ & (Parameter ตัวต่อไป) ให้ตัดทิ้งเลย
        # เพื่อให้ AI โฟกัสแค่ Payload โหดๆ ข้างหน้า (เช่น user=SELECT...)
        # โดยไม่โดน pass=1234 มาเบี่ยงเบนความสนใจ
        if "&" in line:
            line = line.split("&")[0]

        # ถอดรหัส (เหมือนเดิม)
        decoded_line = urllib.parse.unquote_plus(line)
        
        # ... (ส่งเข้า AI เหมือนเดิม)
        # ลบเครื่องหมาย " ที่อาจติดมา
        line = line.replace('"', '').strip()
        # ----------------------------------------

        # --- 🔓 2. ถอดรหัส (Decoding) ---
        # ใช้ unquote_plus เพื่อแปลง '+' เป็น 'เว้นวรรค' (UNION+SELECT -> UNION SELECT)
        decoded_line = urllib.parse.unquote_plus(line)
        # ----------------------------------------

        # ส่งเข้า AI
        X_new = vectorizer.transform([decoded_line])
        prediction = model.predict(X_new)[0]
        prob = max(model.predict_proba(X_new)[0]) * 100

        # แสดงผล
        display_text = decoded_line if len(decoded_line) < 60 else decoded_line[:60] + "..."
        
        # ใส่สีให้ดูง่าย (ถ้าบน Terminal รองรับ)
        if prediction == "Normal":
            print(f"👁️ Scanned: {display_text} \n   └──> 🟢 {prediction} ({prob:.1f}%)")
        else:
            print(f"👁️ Scanned: {display_text} \n   └──> 🔴 {prediction} ({prob:.1f}%)")

        try:
            requests.post(DASHBOARD_URL, json={'attack_type': prediction})
        except:
            pass

if __name__ == '__main__':
    monitor_log()