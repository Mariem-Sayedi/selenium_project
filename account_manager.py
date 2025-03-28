from faker import Faker
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

fake = Faker()

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_user_data():
    """Génère des données utilisateur fictives."""
    return {
        "email": fake.email(),
        "password": fake.password(),
    }

def mon_compte_click(driver):
    """Clique sur l'icône 'Mon compte'."""
    try:
        # Attendre que l'élément soit cliquable
        mon_compte_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='icon header-compte']"))
        )
        # Cliquer sur l'élément
        mon_compte_btn.click()
        logging.info("Bouton 'Mon compte' cliqué avec succès !")

    except Exception as e:
        logging.error(f"Erreur lors du clic sur 'Mon compte' : {e}")

def authenticate_user(driver, json_path="users.json", user_index=4):
    """Remplit le formulaire de connexion avec les données d'un utilisateur."""
    try:
        # Charger les données utilisateur à partir du fichier JSON
        users = load_user_data(json_path)

        # Vérifier si l'index utilisateur est valide
        if not isinstance(users, list) or user_index >= len(users):
            logging.error("Index utilisateur invalide ou fichier JSON non valide.")
            return False

        # Récupérer les données utilisateur
        user_data = users[user_index]

        # Vérifier si les données utilisateur sont valides
        if not isinstance(user_data, dict) or "email" not in user_data or "password" not in user_data:
            logging.error(f"Données utilisateur invalides à l'index {user_index}.")
            return False

        # Remplir le formulaire de connexion
        input_email = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "j_username")))
        input_email.send_keys(user_data["email"])
        logging.info(f"Adresse e-mail '{user_data['email']}' remplie avec succès !")

        bouton_valider = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "next_button")))
        bouton_valider.click()
        logging.info("Bouton 'VALIDER' cliqué avec succès !")


        #selectionner le bouton radio je crée un compte
        try:
            # Attendre que l'élément soit cliquable
            radio_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "connexion_nocompte"))
            )
            if not radio_button.is_selected():
                radio_button.click()
                print("Le bouton radio 'Je crée mon compte' a été coché avec succès !")
            else:
                print("Le bouton radio est déjà sélectionné.")
        except Exception as e:
            print(f"Erreur lors de la sélection du bouton radio : {e}")

        bouton_valider.click()
        logging.info("Bouton 'VALIDER' cliqué avec succès !")


        # test.accepter_cookies(driver)

        input_password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_password")))
        input_password.clear()
        input_password.send_keys(user_data["password"])
        logging.info("Champ mot de passe rempli avec succès !")

        bouton_connexion = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submit_button")))
        bouton_connexion.click()
        logging.info("Bouton de connexion cliqué avec succès !")

        return True

    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Élément introuvable ou délai d'attente dépassé : {e}")
        return False

    except Exception as e:
        logging.error(f"Erreur lors du remplissage du formulaire : {e}")
        return False

def save_user_data(user_data, filename="users.json"):
    """Stocke les informations utilisateur dans un fichier JSON."""
    try:
        with open(filename, "a") as f:
            json.dump(user_data, f)
            f.write("\n")
        logging.info(f"Données utilisateur enregistrées dans {filename}")
    except Exception as e:
        logging.error(f"Erreur lors de l'enregistrement des données utilisateur : {e}")

def load_user_data(filename="users.json"):
    """Charge les informations utilisateur à partir d'un fichier JSON."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning(f"Fichier {filename} non trouvé. Retourne une liste vide.")
        return []
    except json.JSONDecodeError:
        logging.error(f"Erreur de décodage JSON dans {filename}. Assurez-vous que le fichier contient du JSON valide.")
        return []