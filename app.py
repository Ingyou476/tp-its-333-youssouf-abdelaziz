from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # IMPORTANT POUR UTF-8

@app.route('/api/salutation', methods=['GET'])
def salutation():
    return jsonify({"message": "Hello World"})

@app.route('/api/utilisateurs', methods=['POST'])
def creer_utilisateur():
    data = request.get_json()
    nom = data.get("nom")

    response = {
        "message": "Utilisateur reçu",
        "nom": nom
    }

    return Response(
        json.dumps(response, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )

if __name__ == '__main__':
    app.run(debug=True)
