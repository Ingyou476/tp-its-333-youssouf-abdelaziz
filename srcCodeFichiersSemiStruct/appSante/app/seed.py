from app import app, db
from app.models.group import Group
from app.models.etudiant import Etudiant

with app.app_context():
    g = Group(nom="ITS2")
    db.session.add(g)
    db.session.commit()

    e1 = Etudiant(nom="Alice", group=g)
    e2 = Etudiant(nom="Bob", group=g)
    e3 = Etudiant(nom="Charlie", group=g)

    db.session.add_all([e1, e2, e3])
    db.session.commit()

    print("Groupe ITS2 + 3 étudiants créés")
