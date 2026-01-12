from app import app
from flask import render_template, request, jsonify

# =========================
# EXO 1 – simple API
# =========================
@app.route('/api/hello')
def api_hello():
    return jsonify({"message": "Hello MVC"})


# =========================
# EXO 2 – API with simple display
# =========================
@app.route('/hello')
def hello_page():
    return render_template("index.html", message="Hello depuis MVC")


# =========================
# EXO 3 – API with parameters display
# =========================
@app.route('/api/hello/<nom>')
def api_hello_nom(nom):
    return jsonify({
        "message": "Bonjour",
        "nom": nom
    })


# =========================
# EXO 4 – API with parameters retrieved from URL
# =========================
@app.route('/addition')
def addition():
    a = request.args.get('a')
    b = request.args.get('b')

    if a is None or b is None:
        return jsonify({"error": "Veuillez fournir a et b"}), 400

    return jsonify({
        "a": a,
        "b": b,
        "resultat": int(a) + int(b)
    })
