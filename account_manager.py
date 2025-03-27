from selenium import webdriver
from faker import Faker
import json

fake = Faker()

def generate_user_data():
    """Génère des données utilisateur fictives."""
    return {
        "email": fake.email(),
        "password": fake.password(),
    }

def register_user(driver, registration_url, user_data):
    """Inscrit un nouvel utilisateur."""
    # ... (Code Selenium pour remplir et soumettre le formulaire d'inscription) ...

def authenticate_user(driver, login_url, user_data):
    """Authentifie un utilisateur existant."""
    # ... (Code Selenium pour remplir et soumettre le formulaire de connexion) ...

def save_user_data(user_data, filename="users.json"):
    """Stocke les informations utilisateur dans un fichier JSON."""
    with open(filename, "a") as f:
        json.dump(user_data, f)
        f.write("\n")

def load_user_data(filename="users.json"):
    """Charge les informations utilisateur à partir d'un fichier JSON."""
    users = []
    try:
        with open(filename, "r") as f:
            for line in f:
                users.append(json.loads(line))
    except FileNotFoundError:
        pass
    return users