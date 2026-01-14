from flask import Flask, request, render_template_string, redirect
import jwt

app = Flask(__name__)
SECRET = "secret"

LOGIN_PAGE = """
<!doctype html>
<html>
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
</head>
<body class="bg-dark d-flex align-items-center justify-content-center vh-100">

<div class="card p-4 shadow-lg" style="width:350px">
<h3 class="text-center">Connexion</h3>
<form method="post">
<input class="form-control mb-2" name="user" placeholder="Login" required>
<input class="form-control mb-3" type="password" name="pass" placeholder="Mot de passe" required>
<button class="btn btn-primary w-100">Se connecter</button>
</form>
</div>
</body></html>
"""

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form["user"]=="admin" and request.form["pass"]=="1234":
            token = jwt.encode({"user":"admin"},SECRET,algorithm="HS256")
            return redirect(f"http://localhost:5001/?token={token}")
    return render_template_string(LOGIN_PAGE)

app.run(host="0.0.0.0",port=5000)
