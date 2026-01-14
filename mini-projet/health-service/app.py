from flask import Flask,request,redirect,render_template_string
import json,requests,jwt

SECRET="secret"
DATA="health.json"
app=Flask(__name__)

def load(): 
    try:return json.load(open(DATA))
    except:return {}
def save(d): json.dump(d,open(DATA,"w"))

PAGE="""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
<div class="container mt-5">
<h2>Santé</h2>
<form method="post" action="/add?token={{token}}" class="row g-2">
<input class="form-control col" name=id placeholder="ID">
<input class="form-control col" name=poids placeholder="Poids">
<input class="form-control col" name=taille placeholder="Taille">
<input class="form-control col" name=tension placeholder="Tension">
<button class="btn btn-success">OK</button>
</form><br>

<table class="table table-bordered shadow">
<tr><th>ID</th><th>Poids</th><th>Taille</th><th>Tension</th></tr>
{% for k,v in data.items() %}
<tr><td>{{k}}</td><td>{{v['poids']}}</td><td>{{v['taille']}}</td><td>{{v['tension']}}</td></tr>
{% endfor %}
</table>
<a class="btn btn-secondary" href="http://localhost:5001/?token={{token}}">⬅ Retour</a>
</div>
"""

def valid(token):
    try: jwt.decode(token,SECRET,algorithms=["HS256"]); return True
    except: return False

@app.route("/")
def home():
    token=request.args.get("token")
    if not valid(token): return "Unauthorized"
    return render_template_string(PAGE,data=load(),token=token)

@app.route("/add",methods=["POST"])
def add():
    token=request.args.get("token")
    if not valid(token): return "Unauthorized"
    pid=request.form["id"]
    if requests.get(f"http://person-service:5001/persons/{pid}").status_code!=200:
        return "Personne inexistante"
    d=load()
    d[pid]={"poids":request.form["poids"],"taille":request.form["taille"],"tension":request.form["tension"]}
    save(d)
    return redirect("/?token="+token)

app.run(host="0.0.0.0",port=5002)
