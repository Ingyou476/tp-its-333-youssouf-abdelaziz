from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route("/persons", methods=["POST"])
def create_person():
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "name required"}), 400

    p = Person(name=data["name"])
    db.session.add(p)
    db.session.commit()
    return jsonify({"id": p.id, "name": p.name}), 201


@app.route("/persons/<int:pid>", methods=["GET"])
def get_person(pid):
    p = Person.query.get(pid)
    if not p:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": p.id, "name": p.name})


@app.route("/persons/<int:pid>", methods=["DELETE"])
def delete_person(pid):
    p = Person.query.get(pid)
    if not p:
        return jsonify({"error": "not found"}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "deleted"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001)
