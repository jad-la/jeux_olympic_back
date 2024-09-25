# Projet application web pour la réservation de e_tickets des Jeux Olympiques 2024 

## Description
L'application permet aux utilisateur de parcourir différents événement liés à des sports spécifique, de se connect ou s'inscrire pour réserver leur tickets et de recevoir les tickets avec un QR code.

## Technologies utilisées
- **Backend** : Django, Python, Django REST Framework 
- **Frontend** : React 
- **Base de données** : PostgreSQL
- **Déploiement** :
  - Backend déployé sur Render.
  - Base de données PostgreSQL hébergée sur Render.
  - Frontend déployé sur Netlify.


## Structure du projet
Le projet coté backend est organisé en plusieurs applications Django :

- **events** : Gère les sports et les événements.
- **users** : Gère les utilisateurs (l'authentification, création de compte, utilisateur et admin).
- **tickets** : Gère la réservation des tickets, les paniers et la génération de QR codes pour les tickets.


## Configuration du projet
### Pré-requis
- Python 3.8+
- PostgreSQL

### Installation
1. Clonez le projet :
   git clone https://github.com/jad-la/jeux_olympic_back.git

2. Créez et activez un environnement virtuel 
python -m venv env
source env/bin/activate  # pour Linux/Mac
env\Scripts\activate      # pour Windows

3. installez les dépendances
pip install -r requirements.txt

### Configurer la base de données
- Créez et configurer une base de données

### Configurer les variables d'environnement
- Créez un fichier .env et ajoutez vos propres informations de configuration (base de données, clé...)

### Appliquer les migrations
- python manage.py migrate

### Lancer le serveur
- python manage.py runserver

### Déploiement
-->Backend (Django)
Le backend est déployé sur Render. Voici les étapes pour effectuer le déploiement :

- Connectez-vous à votre compte Render ou créez un compte.
- Assurez-vous que votre dépôt GitHub est connecté à Render.
- Déployez l'application en cliquant sur "New Web Service".

