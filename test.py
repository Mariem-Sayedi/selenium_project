from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.common.action_chains import ActionChains
import account_manager

# Configuration du WebDriver (ex: Chrome)
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

BASE_URL = "https://local.lafoirfouille.fr:3012/"
driver.maximize_window()

def accepter_cookies(driver):
    """Accepte les cookies sur la page."""
    try:
        wait = WebDriverWait(driver, 10)
        accept_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        accept_button.click()
        print("Bouton d'acceptation des cookies cliqué avec succès !")
    except Exception as e:
        print(f"Erreur lors du clic sur le bouton d'acceptation des cookies : {e}")

def gerer_popup_geolocalisation(driver):
    """Gère le popup de géolocalisation si présent."""
    try:
        popup = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "popup_geoloc")))
        print("Popup de géolocalisation détecté.")

        input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "locationForSearch")))
        input_element.clear()
        input_element.send_keys("13000")
        input_element.send_keys(Keys.RETURN)
        print("Valeur de localisation entrée avec succès !")

        choisir_magasin_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='btn']/a[contains(text(), 'Choisir')]")))
        choisir_magasin_btn.click()
        print("Bouton 'Choisir ce magasin' cliqué avec succès !")

        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "popup_geoloc")))
        print("Popup de géolocalisation géré avec succès.")
        return True
    except Exception as e:
        print(f"Erreur lors de la gestion du popup de géolocalisation : {e}")
        return False

def cliquer_menu(driver):
    """Clique sur l'icône du menu."""
    try:
        menu_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'header-menu content-slot-lp')]")))
        menu_element.click()
        print("Menu cliqué avec succès !")
    except Exception as e:
        print(f"Erreur lors du clic sur le menu : {e}")

def choisir_categorie(driver):
    """Choisit une catégorie au hasard dans le menu."""
    try:
        main_menu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.menu")))
        category_links = main_menu.find_elements(By.CSS_SELECTOR, "ul.menu > li > a.category-node")
        random_category = random.choice(category_links)
        driver.execute_script("arguments[0].click();", random_category)
        print(f"Catégorie principale cliquée: {random_category.text}")
    except Exception as e:
        print(f"Erreur lors de la sélection de la catégorie : {e}")

def choisir_sous_categorie(driver):
    """Choisit une sous-catégorie au hasard."""
    try:
        main_menu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.menu")))
        sub_category_links = main_menu.find_elements(By.CSS_SELECTOR, "ul.menu > li > ul.smenu > li > a.category-node")
        valid_sub_category_links = [link for link in sub_category_links if link.text.strip() != ""]
        random_sub_category = random.choice(valid_sub_category_links)
        driver.execute_script("arguments[0].click();", random_sub_category)
        print(f"Sous-catégorie cliquée: {random_sub_category.text}")
    except Exception as e:
        print(f"Erreur lors de la sélection de la sous catégorie : {e}")

def choisir_sous_sous_categorie(driver):
    """Choisit une sous-sous-catégorie au hasard."""
    try:
        main_menu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.menu")))
        sub_sub_category_links = main_menu.find_elements(By.CSS_SELECTOR, "ul.menu > li > ul.smenu > li > ul.ssmenu > li > a[href]")
        valid_sub_sub_category_links = [link for link in sub_sub_category_links if link.text.strip() != ""]
        random_sub_sub_category = random.choice(valid_sub_sub_category_links)
        driver.execute_script("arguments[0].click();", random_sub_sub_category)
        print(f"Sous-sous-catégorie cliquée: {random_sub_sub_category.text}")
    except Exception as e:
        print(f"Erreur lors de la sélection de la sous-sous catégorie : {e}")

def choisir_produit_aleatoire(driver):
    """Choisit et clique sur un produit au hasard."""
    try:
        while gerer_popup_geolocalisation(driver):
            time.sleep(2)
        produits = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "produit")))
        if produits:
            produit_aleatoire = random.choice(produits)
            print(f"Produit sélectionné : {produit_aleatoire.get_attribute('data')}")
            produit_aleatoire.click()
            print("Produit cliqué avec succès !")
        else:
            print("Aucun produit trouvé.")
    except Exception as e:
        print(f"Erreur lors de la sélection et du clic sur un produit : {e}")



def ajouter_au_panier(driver):
    """Clique sur le bouton 'Ajouter au panier'."""
    try:
        ajouter_panier_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Ajouter au panier')]"))
        )
        ajouter_panier_btn.click()
        print("Bouton 'Ajouter au panier' cliqué avec succès !")
    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'Ajouter au panier' : {e}")

# Étape 1: Ouvrir la page d'accueil
driver.get(BASE_URL)
time.sleep(2)

# Accepter les cookies
accepter_cookies(driver)

# Gérer le popup de géolocalisation
if gerer_popup_geolocalisation(driver):
    time.sleep(2)

# Naviguer dans le menu et choisir les catégories
cliquer_menu(driver)
choisir_categorie(driver)
choisir_sous_categorie(driver)
choisir_sous_sous_categorie(driver)

# Choisir un produit au hasard et cliquer dessus
choisir_produit_aleatoire(driver)


# Ajouter le produit au panier
ajouter_au_panier(driver)

# Garder le navigateur ouvert
time.sleep(5)




# ... (Configuration du WebDriver) ...

user_data = account_manager.generate_user_data()
account_manager.register_user(driver, "URL_INSCRIPTION", user_data)
account_manager.save_user_data(user_data)

# ... (Autres actions Selenium) ...

users = account_manager.load_user_data()
account_manager.authenticate_user(driver, "URL_CONNEXION", users[0])

# ... (Suite des tests) ...