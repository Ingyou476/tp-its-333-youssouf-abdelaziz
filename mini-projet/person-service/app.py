from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import jwt, requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "secret"
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route("/")
def home():
    persons = Person.query.all()
    return """
    <style>
    body{font-family:Arial;background:#f4f6f9;padding:40px}
    table{border-collapse:collapse;width:50%;background:white}
    th,td{padding:12px;border-bottom:1px solid #ddd}
    th{background:#007bff;color:white}
    a{color:red;text-decoration:none}
    </style>

    <h2>Gestion des personnes</h2>
    <form action="/add" method="post">
      <input name="name" placeholder="Nom" required>
      <button>Ajouter</button>
    </form><br>

    <table>
    <tr><th>ID</th><th>Nom</th><th>Action</th></tr>
    """ + "".join([
        f"<tr><td>{p.id}</td><td>{p.name}</td><td><a href='/delete/{p.id}'>❌</a></td></tr>"
        for p in persons
    ]) + "</table>"

@app.route("/add", methods=["POST"])
def add():
    db.session.add(Person(name=request.form['name']))
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    Person.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect("/")

@app.route("/persons", methods=["POST"])
def api_add():
    p = Person(name=request.json["name"])
    db.session.add(p)
    db.session.commit()
    return jsonify({"id":p.id,"name":p.name})

@app.route("/persons/<int:id>")
def check(id):
    p = Person.query.get(id)
    if not p: return jsonify({"error":"Not found"}),404
    return jsonify({"id":p.id})

if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0",port=5001)
