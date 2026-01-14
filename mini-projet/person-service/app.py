from flask import Flask, request, render_template, redirect, jsonify
import sqlite3, jwt, os

SECRET = "MICROSERVICE_SECRET"
app = Flask(__name__)

DB_PATH = "persons.db"

# --- Connexion DB sécurisée pour Docker ---
def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# --- Création table au démarrage ---
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS persons(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    db.commit()

# --- Vérification JWT ---
def valid(token):
    try:
        jwt.decode(token, SECRET, algorithms=["HS256"])
        return True
    except:
        return False

# --- Page Web ---
@app.route("/")
def home():
    token = request.args.get("token")
    if not valid(token):
        return "Unauthorized", 401

    with get_db() as db:
        persons = db.execute("SELECT * FROM persons").fetchall()

    return render_template("index.html", persons=persons, token=token)

# --- Ajouter personne ---
@app.route("/add", methods=["POST"])
def add():
    token = request.args.get("token")
    if not valid(token):
        return "Unauthorized", 401

    name = request.form.get("name")

    with get_db() as db:
        db.execute("INSERT INTO persons(name) VALUES(?)", (name,))
        db.commit()

    return redirect("/?token=" + token)

# --- API GET personne ---
@app.route("/persons/<int:id>")
def api_get(id):
    with get_db() as db:
        p = db.execute("SELECT * FROM persons WHERE id=?", (id,)).fetchone()

    return jsonify({"id": p[0], "name": p[1]}) if p else ("Not found", 404)

# --- API DELETE ---
@app.route("/persons/<int:id>", methods=["DELETE"])
def api_delete(id):
    with get_db() as db:
        cur = db.execute("DELETE FROM persons WHERE id=?", (id,))
        db.commit()

    return ("Deleted", 200) if cur.rowcount else ("Not found", 404)

app.run(host="0.0.0.0", port=5001)
