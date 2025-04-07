from faker import Faker
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time
import driver_manager
from selenium.webdriver.support.ui import Select
import random
import string
from popups import gerer_popup_geolocalisation


REGISTER_URL = "https://local.lafoirfouille.fr:3012/register"
LOGIN_URL = "https://local.lafoirfouille.fr:3012/login"

driver = driver_manager.create_driver()
driver.maximize_window()






logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




def generate_secure_password():
    faker = Faker()
    
    while True:
        password = faker.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        
        # Vérifier les critères
        if (len(password) >= 8 and
            any(c.isdigit() for c in password) and
            any(c.isalpha() for c in password) and
            sum(1 for c in password if c in string.punctuation) >= 8):
            return password






def generate_user_data():
    """Génère des données utilisateur fictives."""
    fake = Faker("fr_FR")   
    return {
        "email": fake.email(),
        "password": generate_secure_password(),
        "gender": fake.random_element(elements=("Male", "Female")), 
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "birthday": fake.date_of_birth().strftime('%Y-%m-%d'),
        "phone_number": fake.phone_number(),

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


def register(driver, user_index, json_path="users.json"):
    driver.get(REGISTER_URL)
    """Remplit le formulaire de connexion avec les données d'un utilisateur."""

    
    time.sleep(100)
    gerer_popup_geolocalisation(driver)
    time.sleep(70)

    try:
        users = load_user_data(json_path)

        if not isinstance(users, list) or user_index >= len(users):
            logging.error("Index utilisateur invalide ou fichier JSON non valide.")
            return False

        user_data = users[user_index]

        if not isinstance(user_data, dict) or "email" not in user_data or "password" not in user_data:
            logging.error(f"Données utilisateur invalides à l'index {user_index}.")
            return False


        input_email = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "registerForm.email")))
        input_email.send_keys(user_data["email"])
        logging.info(f"Adresse e-mail '{user_data['email']}' remplie avec succès !")

        input_password = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "password")))
        input_password.send_keys(user_data["password"])
        logging.info(f"password '{user_data['password']}' remplie avec succès !")

        input_check_mdp = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "check_mdp")))
        input_check_mdp.send_keys(user_data["password"])
        logging.info(f"check_mdp '{user_data['password']}' remplie avec succès !")
        
        input_first_name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "creation_prenom")))
        input_first_name.send_keys(user_data["first_name"])
        logging.info(f"first_name '{user_data['first_name']}' remplie avec succès !")

        input_last_name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "creation_nom")))
        input_last_name.send_keys(user_data["last_name"])
        logging.info(f"last_name '{user_data['last_name']}' remplie avec succès !")

        day_select = Select(driver.find_element(By.ID, "select_day").find_element(By.TAG_NAME, "select"))
        random_day = random.choice([str(i) for i in range(1, 32)])
        day_select.select_by_value(random_day)

        month_select = Select(driver.find_element(By.ID, "select_month").find_element(By.TAG_NAME, "select"))
        random_month = random.choice([str(i) for i in range(1, 13)])
        month_select.select_by_value(random_month)

        year_select = Select(driver.find_element(By.ID, "select_year").find_element(By.TAG_NAME, "select"))
        random_year = random.choice([str(i) for i in range(1920, 2020)])
        year_select.select_by_value(random_year)
        
        input_phone_number = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "creation_portable")))
        input_phone_number.send_keys(user_data["phone_number"])
        logging.info(f"phone_number '{user_data['phone_number']}' remplie avec succès !")
        time.sleep(20)

        checkbox = driver.find_element(By.ID, "creation_fid")
        if not checkbox.is_selected():
            checkbox.click()

        validate_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "bouton")))
        validate_button.click()    
        logging.info("Bouton 'VALIDER'  cliqué avec succès !")
    except Exception as e:
        logging.error(f"Erreur lors du remplissage du formulaire : {e}")
        return False




def login(driver, user_index=0, json_path="users.json"):
    driver.get(LOGIN_URL)
     
    time.sleep(10)
    gerer_popup_geolocalisation(driver)
    time.sleep(40)

    """Remplit le formulaire de connexion avec les données d'un utilisateur."""
    try:
        users = load_user_data(json_path)

        if not isinstance(users, list) or user_index >= len(users):
            logging.error("Index utilisateur invalide ou fichier JSON non valide.")
            return False

        user_data = users[user_index]

        if not isinstance(user_data, dict) or "email" not in user_data or "password" not in user_data:
            logging.error(f"Données utilisateur invalides à l'index {user_index}.")
            return False

        input_email = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "j_username")))
        input_email.send_keys(user_data["email"])
        logging.info(f"Adresse e-mail '{user_data['email']}' remplie avec succès !")
        
        bouton_valider1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "next_button")))
        bouton_valider1.click()
        logging.info("Bouton 'VALIDER' 1 cliqué avec succès !")

        input_password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_password")))
        input_password.clear()
        input_password.send_keys(user_data["password"])
        logging.info("Champ mot de passe rempli avec succès !")

        bouton_connexion = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "valid_button")))
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
    


def click_cart_icon(driver):
    """Clique sur l'icône du panier."""
    try:
        cart_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'icon content-slot-lp')]")))
        cart_element.click()
        print("Panier cliqué avec succès !")
        bouton_panier = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voir mon panier"))
     )
        bouton_panier.click()
    except Exception as e:
        print(f"Erreur lors du clic sur le Panier : {e}")






def main():
    users = load_user_data("users.json") 

    for i, user in enumerate(users):
        logging.info(f"Création du compte {i + 1}/{len(users)} : {user['email']}")
        register(driver, i) 
        time.sleep(10)


    # login(driver)

if __name__ == "__main__":
    main()