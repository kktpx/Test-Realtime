import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline

# 1. สร้าง Dataset จำลอง (Data สำหรับสอน AI)
# เราสอนมันว่าหน้าตาแบบไหนคือ Normal, SQLi, หรือ XSS
data = [
    # --- Normal Traffic (คนดี) ---
    ("GET /login?user=admin&pass=1234", "Normal"),
    ("GET /home", "Normal"),
    ("GET /contact", "Normal"),
    ("POST /api/data", "Normal"),
    ("GET /images/logo.png", "Normal"),
    ("GET /style.css", "Normal"),
    ("LOGIN_ATTEMPT | User: somchai | Pass: 123456", "Normal"),
    
    # --- SQL Injection (โจรเจาะฐานข้อมูล) ---
    ("GET /login?user=' OR '1'='1", "SQL Injection"),
    ("GET /login?user=admin' --", "SQL Injection"),
    ("UNION SELECT table_name FROM information_schema.tables", "SQL Injection"),
    ("SELECT * FROM users WHERE name = '' OR '1'='1'", "SQL Injection"),
    ("LOGIN_ATTEMPT | User: ' OR 1=1 -- | Pass: ", "SQL Injection"),
    
    # --- XSS Attack (โจรฝังโค้ด) ---
    ("<script>alert('Hacked')</script>", "XSS Attack"),
    ("GET /search?q=<script>document.cookie</script>", "XSS Attack"),
    ("<img src=x onerror=alert(1)>", "XSS Attack"),
    ("javascript:alert('XSS')", "XSS Attack"),
    ("LOGIN_ATTEMPT | User: <script> | Pass: 1234", "XSS Attack")
]

# แปลงเป็น DataFrame
df = pd.DataFrame(data, columns=['text', 'label'])

print("🧠 Training AI Model...")

# 2. สร้าง Pipeline (ท่อส่งข้อมูล)
# - TfidfVectorizer: แปลงตัวหนังสือเป็นตัวเลข (AI อ่านหนังสือไม่ออก ต้องแปลงเป็น Vector)
# - RandomForestClassifier: สมอง AI ที่ใช้จำแนกประเภท
model = make_pipeline(TfidfVectorizer(), RandomForestClassifier())

# 3. เริ่มสอน (Fit)
model.fit(df['text'], df['label'])

# 4. บันทึกสมองเก็บไว้ใช้งาน (Save Model)
joblib.dump(model, 'security_model.pkl')

print("✅ Model Trained & Saved as 'security_model.pkl'")
print("Test Prediction ('<script>'):", model.predict(["<script>alert(1)</script>"])[0])