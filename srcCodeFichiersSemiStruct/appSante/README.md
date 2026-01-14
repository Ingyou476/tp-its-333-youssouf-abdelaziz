# Mini-Projet ITS-333 — API de Gestion des Patients

Nom : Youssouf Abdelaziz  
Classe : ITS2  
Matière : Bases de données & APIs  

## Objectif
Créer une API Flask de gestion de patients avec :
- Base SQLite
- SQLAlchemy
- JWT
- Swagger
- Docker

## Lancer l’application

Sans Docker :
pip install -r requirements.txt  
python run.py  

Avec Docker :
docker build -t app-sante .  
docker run -p 5000:5000 app-sante  

## Accès
Swagger : http://localhost:5000/apidocs  
Login : http://localhost:5000/login  

## Base de données
Base SQLite : sante.db

## Seed
python -m app.seed

Projet entièrement fonctionnel.
