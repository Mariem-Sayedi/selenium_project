from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import driver_manager
import json


driver = driver_manager.create_driver()

BASE_URL = driver_manager.get_base_url()
driver.maximize_window()




def accepter_cookies(driver):
    """Accepte les cookies sur la page."""
    try:
        wait = WebDriverWait(driver, 20)
        accept_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        accept_button.click()
        print("Bouton d'acceptation des cookies cliqué avec succès !")
        return True
    except Exception as e:
        print(f"Erreur lors du clic sur le bouton d'acceptation des cookies : {e}")
        return False

def gerer_popup_geolocalisation(driver):
    """Gère le popup de géolocalisation et les cookies si présents."""
    try:
        WebDriverWait(driver, 10).until(
            EC.any_of(
                EC.visibility_of_element_located((By.ID, "popup_geoloc")),
                EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))
            )
        )

        accepter_cookies(driver)

        try:
            popup = driver.find_element(By.ID, "popup_geoloc")
            print("Popup de géolocalisation détecté.")

            input_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "locationForSearch"))
            )
            input_element.clear()
            input_element.send_keys("13000")
            input_element.send_keys(Keys.RETURN)
            print("Valeur de localisation entrée avec succès !")

            # Accepter les cookies à nouveau au cas où il apparaît maintenant
            accepter_cookies(driver)

            # Cliquer sur "Choisir ce magasin"
            choisir_magasin_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='btn']/a[contains(text(), 'Choisir')]"))
            )
            choisir_magasin_btn.click()
            print("Bouton 'Choisir ce magasin' cliqué avec succès !")

            # Attendre la fermeture du popup
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "popup_geoloc")))
            print("Popup de géolocalisation géré avec succès.")

        except NoSuchElementException:
            print("Popup de géolocalisation non trouvé, vérification du popup de cookies.")
            accepter_cookies(driver)

    except TimeoutException:
        print("Ni le popup de géolocalisation ni le popup de cookies n'ont été trouvés.")
    except Exception as e:
        print(f"Erreur lors de la gestion du popup de géolocalisation : {e}")






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






import json
import os

def choisir_sous_sous_categorie(driver):
    """Ajoute les sous-sous-catégories au fichier JSON sans écrasement."""
    try:
        main_menu = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.menu"))
        )

        sub_sub_category_links = main_menu.find_elements(
            By.CSS_SELECTOR, "ul.menu > li > ul.smenu > li > ul.ssmenu > li > a[href]"
        )

        valid_sub_sub_category_links = [
            link for link in sub_sub_category_links if link.text.strip() != ""
        ]

        if not valid_sub_sub_category_links:
            print("Aucune sous-sous-catégorie disponible.")
            return

        nouveaux_noms = [link.text.strip() for link in valid_sub_sub_category_links]

        fichier_json = "sous_sous_categories.json"

        # Charger l'ancien contenu du fichier (s'il existe)
        anciens_noms = []
        if os.path.exists(fichier_json):
            with open(fichier_json, "r", encoding="utf-8") as f:
                try:
                    anciens_noms = json.load(f)
                except json.JSONDecodeError:
                    pass  # Si le fichier est vide ou corrompu, on ignore

        # Ajouter sans doublons
        tous_les_noms = list(set(anciens_noms + nouveaux_noms))

        # Sauvegarder
        with open(fichier_json, "w", encoding="utf-8") as f:
            json.dump(tous_les_noms, f, ensure_ascii=False, indent=4)

        # Choisir une sous-sous-catégorie au hasard et cliquer dessus
        random_sub_sub_category = random.choice(valid_sub_sub_category_links)
        # driver.execute_script("arguments[0].click();", random_sub_sub_category)
        random_sub_sub_category.click()
        # print(f"Sous-sous-catégorie cliquée : {random_sub_sub_category.text}")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Erreur lors de la sélection de la sous-sous-catégorie : {e}")




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



def main():
  
  driver.get(BASE_URL)
  time.sleep(2)
  if gerer_popup_geolocalisation(driver):
        time.sleep(30)
    # Naviguer dans le menu et choisir les catégories
  cliquer_menu(driver)

  for i in range(5000):
    choisir_categorie(driver)
    choisir_sous_categorie(driver)
    choisir_sous_sous_categorie(driver)


if __name__ == "__main__":
  main()
