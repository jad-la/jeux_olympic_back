# Projet application web pour la réservation de e_tickets des Jeux Olympiques 2024 

## Technologies utilisées
- **Backend** : Django, Python (encours de développement)
- **Frontend** : React (non développer pour l'instant)
- **Base de données** : PostgreSQL
- **Déploiement** :
  - Backend déployé sur Render.
  - Base de données PostgreSQL hébergée sur Render.
  - Frontend prévu pour être déployé sur Netlify.


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
   git clone https://github.com/jad-la/jeux_olympic_back.gitprojet_jeux_olympiques.git

2. Créez et activez un environnement virtuel 
python -m venv env
source env/bin/activate  # pour Linux/Mac
env\Scripts\activate      # pour Windows

3. installez les dépendances
pip install -r requirements.txt

### Documentation des API (Backend)
--> GET /api/sports/
- **Description** : Récupère la liste des sports disponibles.
- **Réponse**(en JSON) :
  [
      {
          "id": 1,
          "name": "Athlétisme",
          "description": "Découvrez les épreuves d'athlétisme des Jeux Olympiques"
      }
  ]

--> Get /api/sports/<id>/events/
**Description** : Récupère les détails d'un sport spécifique et les événements associés
- **Réponse**(en JSON) :
    [
        {
            "id": 2,
            "name": "100 m hommes",
            "description": "Découvrez l'épreuve incontournable du 100 mètres hommes lors des Jeux Olympiques. Ne manquez pas cet événement, achetez dès maintenant vos places.",
            "date": "2024-11-04",
            "time": "10:00:00",
            "location": "93200 Saint-Denis",
            "photo_url": "https://www.shutterstock.com/image-photo/ostrava-czechia-june-27-2023-260nw-2345997007.jpg"
        }
    ]

--> POST /api/users/register/
**Description** : Permet de créer un compte utilisateur.
- **Paramètres requis**:
    {
        "email": "marie@example.com",
        "first_name": "marie",
        "last_name": "liam",
        "password": "Test2-password123",
        "password2": "Test2-password123"
    }

--> POST /api/users/login/
**Description** : Connexion de l'utilisateur.
- **Paramètres requis**:
    {   
        "email": "user1@example.com",
        "password": "Test-password123"
    }

--> POST /api/cart/items/
**Description** : Permet à l'utilisateur connecté d'ajouter un événement à son panier.
- **Paramètres requis**:
    {   
        "event": 2, 
        "offer": "duo",
        "quantity": 1
    }

--> Get /api/cart/
**Description** : Récupère les arctiles dans le panier.
- **Réponse(JSON)**:
    {
        "id": 1,
        "user": 2,
        "created_at": "2024-09-11T21:18:59.426043Z",
        "items": [
            {
                "event": "100 m hommes",
                "offer": "duo",
                "quantity": 1,
                "total_price": 85.00
            }
        ]
    }

--> Post /api/bookings/
**Description** : Permet à l'utilisateur connecté de réserver les articles dans son panier.
- **Réponse(JSON)**:
    {
        "id": 3,
        "user": 2,
        "total_price": "200.00",
        "booking_date": "2024-09-11T22:23:49.762797Z"
    }

--> GET /api/tickets/
**Description** : Récupère la liste des tickets de l'utilisateur, avec le QR code généré.
- **Réponse(JSON)**:
    [
        {
            "id": 5,
            "booking": 3,
            "event": "100 m hommes",
            "offer": "duo",
            "qr_code": "http://127.0.0.1:8000/media/qrcodes/qrcode_3.png",
            "issued_at": "2024-09-11T22:23:50.262443Z"
        }
    ]
### Modèles de données
-->Modèle Sport (app events)
    - name : Nom du sport.
    - description : Description du sport.

-->Modèle event (app events)
    - sport : Référence à un Sport.
    - name : Nom de l'événement.
    - description : Description de l'événement.
    - date : Date de l'événement.
    - location : Lieu où se déroule l'événement.
    - photo_url : URL de l'image associée à l'événement.
    - price_solo, price_duo, price_family : Prix des offres en fonction du type de billet.


-->Modèle CustomUser (app users)
    - email : Adresse email de l'utilisateur.
    - first_name : Prénom de l'utilisateur.
    - last_name : Nom de l'utilisateur.
    - security_key : Clé de sécurité générée lors de la création du compte.
    - created_at : Date de création du compte.

-->Modèle Booking (app tickets)
    - user : Référence à un utilisateur.
    - total_price : Prix total de la réservation.
    - booking_date : Date de la réservation (générée automatiquement lors de la création).

-->Modèle Tickets (app tickets)
    - booking : Référence à une réservation.
    - event : Référence à un événement.
    - offer : Offre sélectionnée (solo, duo, famille).
    - security_key : Clé de sécurité associée au ticket.
    - qr_code : QR code unique associé au ticket.
    - issued_at : Date et heure de l'émission du ticket (générée automatiquement).

-->Modèle Cart (app tickets)
    - user : Référence à un utilisateur.
    - created_at : Date de création du panier (générée automatiquement).

-->Modèle CartItem (app tickets)
    - cart : Référence à un panier (Cart).
    - event : Référence à un événement.
    - offer : Offre sélectionnée (solo, duo, famille).
    - quantity : Quantité d'articles dans le panier.
    - total_price : Prix total pour cet article dans le panier.


### Déploiement
-->Backend (Django)
Le backend est déployé sur Render. Voici les étapes pour effectuer le déploiement :

- Connectez-vous à votre compte Render.
- Assurez-vous que votre dépôt GitHub est connecté à Render.
- Déployez l'application en cliquant sur "New Web Service".

-->Frontend (React)
Le frontend sera déployé sur Netlify après finalisation.