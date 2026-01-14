from app import db

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
