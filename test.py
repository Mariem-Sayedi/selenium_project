from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.common.action_chains import ActionChains

# Configuration du WebDriver (ex: Chrome)
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

BASE_URL = "https://www.lafoirfouille.fr"
driver.maximize_window()

# Étape 1: Ouvrir la page d'accueil
driver.get(BASE_URL)
time.sleep(2)

try:
    # Attendre que le bouton soit présent et cliquable
    wait = WebDriverWait(driver, 10)
    accept_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))

    # Cliquer sur le bouton
    accept_button.click()
    print("Bouton d'acceptation des cookies cliqué avec succès !")

except Exception as e:
    print(f"Erreur lors du clic sur le bouton d'acceptation des cookies : {e}")

def handle_geoloc_popup(driver):
    """Gère le popup de géolocalisation si présent."""
    try:
        # Attendre que le popup soit visible
        popup = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "popup_geoloc"))
        )
        print("Popup de géolocalisation détecté.")

        # Saisir la localisation et cliquer sur "Choisir ce magasin"
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "locationForSearch"))
        )
        input_element.clear()
        input_element.send_keys("13000")
        input_element.send_keys(Keys.RETURN)
        print("Valeur de localisation entrée avec succès !")

        choisir_magasin_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='btn']/a[contains(text(), 'Choisir')]"))
        )
        choisir_magasin_btn.click()
        print("Bouton 'Choisir ce magasin' cliqué avec succès !")

        # Attendre que le popup disparaisse
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "popup_geoloc"))
        )

        print("Popup de géolocalisation géré avec succès.")

        return True  # Indique que le popup a été géré

    except Exception as e:
        print(f"Erreur lors de la gestion du popup de géolocalisation : {e}")
        return False  # Indique que le popup n'a pas été géré ou une erreur est survenue

# Gestion du popup de géolocalisation (si présent)
if handle_geoloc_popup(driver):
    time.sleep(2)  # Attendre après la gestion du popup

# Attendre et cliquer sur l'icône du menu
try:
    menu_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'header-menu content-slot-lp')]"))
    )
    menu_element.click()
    print("Menu cliqué avec succès !")

except Exception as e:
    print(f"Erreur lors du clic sur le menu : {e}")

# Choix de la catégorie
try:
    main_menu = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.menu"))
    )
    print("Menu principal visible")

    category_links = main_menu.find_elements(By.CSS_SELECTOR, "ul.menu > li > a.category-node")

    print(f"Nombre de catégories principales trouvées : {len(category_links)}")
    for i, link in enumerate(category_links):
        print(f"{i+1}. {link.text}")

    if len(category_links) != 11:
        print(f"Nombre inattendu de catégories : {len(category_links)}")

    if category_links:
        random_category = random.choice(category_links)
        print(f"Catégorie principale sélectionnée : {random_category.text}")

        # Survoler l'élément parent (menu principal)
        actions = ActionChains(driver)
        actions.move_to_element(random_category).perform()

        # Faire défiler l'élément dans la vue
        driver.execute_script("arguments[0].scrollIntoView();", random_category)

        # Attendre que l'élément soit cliquable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(random_category))

        # Cliquer sur l'élément de la catégorie
        driver.execute_script("arguments[0].click();", random_category)
        print("Catégorie principale cliquée avec succès !")

except Exception as e:
    print(f"Erreur lors de la sélection de la catégorie : {e}")

# Garder le navigateur ouvert
time.sleep(1)

#choix de la sous-catégorie
try:
    # Trouver tous les liens de sous-catégories
    sub_category_links = main_menu.find_elements(By.CSS_SELECTOR, "ul.menu > li > ul.smenu > li > a.category-node")

    # Filtrer les sous-catégories non vides
    valid_sub_category_links = [link for link in sub_category_links if link.text.strip() != ""]

    # Afficher le nombre de sous-catégories valides
    print(f"Nombre de sous-catégories trouvées : {len(valid_sub_category_links)}")

    # Afficher les sous-catégories valides
    for i, link in enumerate(valid_sub_category_links):
        print(f"{i+1}. {link.text}")

    if valid_sub_category_links:
        # Choisir une sous-catégorie au hasard parmi les sous-catégories valides
        random_sub_category = random.choice(valid_sub_category_links)
        print(f"Catégorie secondaire sélectionnée : {random_sub_category.text}")

        # Survoler l'élément parent (menu principal)
        actions = ActionChains(driver)
        actions.move_to_element(random_sub_category).perform()

        # Faire défiler l'élément dans la vue
        driver.execute_script("arguments[0].scrollIntoView();", random_sub_category)

        # Attendre que l'élément soit cliquable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(random_sub_category))

        # Cliquer sur l'élément de la catégorie
        driver.execute_script("arguments[0].click();", random_sub_category)
        print("Catégorie secondaire cliquée avec succès !")

except Exception as e:
    print(f"Erreur lors de la sélection de la sous catégorie : {e}")

# Garder le navigateur ouvert
time.sleep(0)

#choix de la sous-sous-catégorie
try:
    # Trouver tous les liens de sous-catégories
    sub_sub_category_links = main_menu.find_elements(By.CSS_SELECTOR, "ul.menu > li > ul.smenu > li > ul.ssmenu > li > a[href]")

    # Filtrer les sous-catégories non vides
    valid_sub_sub_category_links = [link for link in sub_sub_category_links if link.text.strip() != ""]

    # Afficher le nombre de sous-catégories valides
    print(f"Nombre de sous-catégories trouvées : {len(valid_sub_sub_category_links)}")

    # Afficher les sous-catégories valides
    for i, link in enumerate(valid_sub_sub_category_links):
        print(f"{i+1}. {link.text}")

    if valid_sub_sub_category_links:
        # Choisir une sous-catégorie au hasard parmi les sous-catégories valides
        random_sub_sub_category = random.choice(valid_sub_sub_category_links)
        print(f"Catégorie secondaire sélectionnée : {random_sub_sub_category.text}")

        # Survoler l'élément parent (menu principal)
        actions = ActionChains(driver)
        actions.move_to_element(random_sub_sub_category).perform()

        # Faire défiler l'élément dans la vue
        driver.execute_script("arguments[0].scrollIntoView();", random_sub_sub_category)

        # Attendre que l'élément soit cliquable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(random_sub_sub_category))

        # Cliquer sur l'élément de la catégorie
        driver.execute_script("arguments[0].click();", random_sub_sub_category)
        print("Catégorie secondaire cliquée avec succès !")

except Exception as e:
    print(f"Erreur lors de la sélection de la sous-sous catégorie : {e}")

# Garder le navigateur ouvert
time.sleep(1)


# Gestion du popup de géolocalisation (si présent)
if handle_geoloc_popup(driver):
    time.sleep(2)  # Attendre après la gestion du popup




#choix d'un produit
# Sélection et clic aléatoire sur un produit avec gestion continue du popup
try:
    while True: # Boucle infinie pour gérer les apparitions répétées du popup
        if handle_geoloc_popup(driver):
            time.sleep(2)  # Attendre après la gestion du popup
        else:
            break  # Sortir de la boucle si le popup n'est pas trouvé

    produits = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "produit"))
    )

    if produits:
        produit_aleatoire = random.choice(produits)
        print(f"Produit sélectionné : {produit_aleatoire.get_attribute('data')}")
        produit_aleatoire.click()
        print("Produit cliqué avec succès !")
    else:
        print("Aucun produit trouvé.")

except Exception as e:
    print(f"Erreur lors de la sélection et du clic sur un produit : {e}")

# Garder le navigateur ouvert
time.sleep(5)


# Gestion du popup de géolocalisation (si présent)
if handle_geoloc_popup(driver):
    time.sleep(0)  # Attendre après la gestion du popup