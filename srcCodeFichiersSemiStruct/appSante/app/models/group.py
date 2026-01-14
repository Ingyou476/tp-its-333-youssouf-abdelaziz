from app import db

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)

    etudiants = db.relationship('Etudiant', backref='group', lazy=True)
