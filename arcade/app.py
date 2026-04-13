from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3, hashlib

app = Flask(__name__)
app.secret_key = "arcade_secret_2025"

def get_db():
    conn = sqlite3.connect("arcade.db")
    conn.row_factory = sqlite3.Row
    return conn

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form["username"].strip()
        p = request.form["password"]
        if not u or not p:
            return render_template("register.html", error="All fields required.")
        db = get_db()
        try:
            db.execute("INSERT INTO users(username,password) VALUES(?,?)", (u, hash_pw(p)))
            db.commit()
        except sqlite3.IntegrityError:
            db.close()
            return render_template("register.html", error="Username already taken.")
        db.close()
        session["user"] = u
        return redirect("/dashboard")
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    u = request.form["username"].strip()
    p = request.form["password"]
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE username=? AND password=?", (u, hash_pw(p))).fetchone()
    db.close()
    if row:
        session["user"] = u
        return redirect("/dashboard")
    return render_template("login.html", error="Invalid credentials.")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    db = get_db()
    scores = db.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 10").fetchall()
    me = db.execute("SELECT score FROM users WHERE username=?", (session["user"],)).fetchone()
    db.close()
    return render_template("dashboard.html", user=session["user"], scores=scores, my_score=me["score"] if me else 0)

@app.route("/game/<game_name>")
def game(game_name):
    if "user" not in session:
        return redirect("/")
    games = ["guess", "quiz", "tictactoe", "snake", "memory"]
    if game_name not in games:
        return redirect("/dashboard")
    return render_template(f"{game_name}.html", user=session["user"])

@app.route("/api/score", methods=["POST"])
def add_score():
    if "user" not in session:
        return jsonify({"error": "not logged in"}), 401
    data = request.get_json()
    pts = int(data.get("points", 0))
    if pts <= 0:
        return jsonify({"ok": False})
    db = get_db()
    db.execute("UPDATE users SET score = score + ? WHERE username=?", (pts, session["user"]))
    db.commit()
    new = db.execute("SELECT score FROM users WHERE username=?", (session["user"],)).fetchone()
    db.close()
    return jsonify({"ok": True, "total": new["score"]})

@app.route("/api/leaderboard")
def leaderboard():
    db = get_db()
    rows = db.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 10").fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    db = get_db()
    db.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        score INTEGER DEFAULT 0)""")
    db.commit()
    db.close()
    print("Arcade running at http://127.0.0.1:5000")
    app.run(debug=True)
