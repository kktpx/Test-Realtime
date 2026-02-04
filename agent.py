import time
import requests
from scapy.all import sniff, IP, TCP, UDP, ICMP

# ตั้งค่าให้ส่งไปที่เครื่องตัวเอง (Server AI)
SERVER_URL = "http://127.0.0.1:5000/api/predict"

def get_protocol_name(proto_num):
    # แปลงเลข Protocol เป็นชื่อ
    if proto_num == 6: return "tcp"
    if proto_num == 17: return "udp"
    if proto_num == 1: return "icmp"
    return "other"

def process_packet(packet):
    if IP in packet:
        try:
            # 1. ดึงข้อมูลพื้นฐาน
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            proto_name = get_protocol_name(packet[IP].proto)
            packet_len = len(packet)

            # ---------------------------------------------------------
            # 🛠️ ส่วนที่แก้ไขใหม่: ดึงเลข Port ปลายทางออกมาเช็ค
            # ---------------------------------------------------------
            target_port = 0
            if TCP in packet:
                target_port = packet[TCP].dport
            elif UDP in packet:
                target_port = packet[UDP].dport
            
            # ---------------------------------------------------------
            # 🧠 Logic ใหม่: แจ้งเตือนเมื่อไหร่?
            # 1. เมื่อเจอ ICMP (Ping)
            # 2. หรือเมื่อเจอการยิงไปที่ Port 80 (HTTP Standard)
            # (Traffic อื่นๆ เช่น Port 443, Background Windows จะถือว่าปกติ)
            # ---------------------------------------------------------
            is_attack_simulation = (proto_name == "icmp") or \
                                   (target_port == 80)

            # จัดเตรียมข้อมูลใส่กล่อง (JSON)
            payload = {
                "duration": 0,
                "protocol_type": proto_name,
                "service": "http",
                "flag": "S0" if is_attack_simulation else "SF", 
                "src_bytes": 0 if is_attack_simulation else packet_len,
                "dst_bytes": 0,
                "count": 250 if is_attack_simulation else 1,    # ถ้าโจมตี ให้เลขพุ่งเป็น 250
                "same_srv_rate": 0.1,
            }

            # แสดงผล Debug ในจอดำ (ให้ดูง่ายขึ้น)
            status_icon = "🔴" if is_attack_simulation else "🟢"
            print(f"{status_icon} Sent: {proto_name.upper()} (Port: {target_port}) -> Count: {payload['count']}")
            
            # 3. ส่งไปหา Server
            requests.post(SERVER_URL, json=payload, timeout=0.5)
            
        except Exception as e:
            # error เล็กน้อยช่างมัน ไม่ต้องรกหน้าจอ
            pass

# เริ่มทำงาน
print("🚀 Agent Started... Waiting for Attack...")
print("🎯 Condition: Ping (ICMP) OR Port 80 Only")
# ดักจับทุกอย่าง ยกเว้นพอร์ต 5000 (ที่เป็นช่องทางส่งข้อมูลของเราเอง)
sniff(filter="ip and not port 5000", prn=process_packet, store=0)