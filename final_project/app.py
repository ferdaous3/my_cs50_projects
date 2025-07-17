from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# إعداد التطبيق
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# إنشاء قاعدة البيانات
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # جدول المستخدمين
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL
        )
    """)

    # جدول المهام
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

init_db()

# تسجيل حساب جديد
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "يجب ملء جميع الحقول"

        hash_pw = generate_password_hash(password)

        try:
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return "اسم المستخدم موجود بالفعل"

    return render_template("register.html")

# تسجيل الدخول
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            return redirect("/")
        else:
            return "اسم المستخدم أو كلمة المرور خاطئة"

    return render_template("login.html")

# تسجيل الخروج
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# الصفحة الرئيسية: قائمة المهام
@app.route("/", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == "POST":
        task = request.form.get("task")
        if task:
            cur.execute("INSERT INTO tasks (user_id, task) VALUES (?, ?)", (session["user_id"], task))
            conn.commit()

    cur.execute("SELECT task FROM tasks WHERE user_id = ?", (session["user_id"],))
    tasks = cur.fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

# تشغيل التطبيق
if name == "__main__":
    app.run(debug=True)
