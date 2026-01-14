from app import app
from flask import render_template, request, redirect, jsonify
import sqlite3, datetime, jwt
from app.database import init_db

init_db()

SECRET_KEY = "ITS_SECRET_2026"

@app.route('/')
def home():
    return redirect('/login')

# ===================== LOGIN =====================
@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    """
    Connexion admin
    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Token JWT
    """
    user = request.form['username']
    pwd = request.form['password']

    if user == "admin" and pwd == "admin":
        token = jwt.encode({
            "user": user,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm="HS256")

        return render_template("token.html", token=token)

    return "Accès refusé"


# ===================== AJOUT PATIENT =====================
@app.route('/new')
def new():
    return render_template("new.html")

@app.route('/new', methods=['POST'])
def add_patient():
    """
    Ajouter un patient
    ---
    parameters:
      - name: nom
        in: formData
        type: string
        required: true
      - name: adresse
        in: formData
        type: string
        required: true
      - name: pin
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Patient ajouté
    """
    nom = request.form['nom']
    adresse = request.form['adresse']
    pin = request.form['pin']

    conn = sqlite3.connect("sante.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO patients (nom, adresse, pin) VALUES (?,?,?)",
                (nom, adresse, pin))
    conn.commit()
    conn.close()
    return redirect('/new')


# ===================== LISTE PROTÉGÉE =====================
@app.route('/list')
def list_patients():
    """
    Liste des patients (JWT requis)
    ---
    parameters:
      - name: token
        in: query
        type: string
        required: true
    responses:
      200:
        description: Liste patients
    """
    token = request.args.get("token")
    if not token:
        return "Token requis"

    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return "Token invalide"

    conn = sqlite3.connect("sante.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()
    conn.close()

    return render_template("list.html", patients=data)
