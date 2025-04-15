import driver_manager
import driver_manager
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import driver_manager
from selenium.webdriver.support.ui import Select
import random
import json
from selenium.webdriver.common.keys import Keys


driver = driver_manager.create_driver()


BASE_URL = driver_manager.get_base_url()
driver.maximize_window()


def search(driver, file="sous_sous_categories.json"): 
    driver.get(BASE_URL)
    try:
        with open(file, "r", encoding="utf-8") as f:
            sub_sub_categories = json.load(f)

        if not sub_sub_categories:
            print("Aucun produit trouvé dans le fichier !")
            return False

        query = random.choice(sub_sub_categories)


       
        try:
           input_search = WebDriverWait(driver, 30).until(
           EC.presence_of_element_located((By.ID, "search"))
        )
           print("Champ de recherche trouvé.")
        except TimeoutException:
          print("Champ de recherche introuvable ! Vérifie le sélecteur CSS.")
          return False
        input_search.clear()
        input_search.send_keys(query)
        input_search.submit()
        
        print(f"Recherche effectuée pour : {query}")
        return True

    except Exception as e:
        print(f"Erreur de recherche : {e}")
        return False


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
            input_element.send_keys("5000")
            input_element.send_keys(Keys.RETURN)
            print("Valeur de localisation entrée avec succès !")

            accepter_cookies(driver)

            choisir_magasin_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='btn']/a[contains(text(), 'Choisir')]"))
            )
            choisir_magasin_btn.click()
            print("Bouton 'Choisir ce magasin' cliqué avec succès !")

            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "popup_geoloc")))
            print("Popup de géolocalisation géré avec succès.")

        except NoSuchElementException:
            print("Popup de géolocalisation non trouvé, vérification du popup de cookies.")
            accepter_cookies(driver)

    except TimeoutException:
        print("Ni le popup de géolocalisation ni le popup de cookies n'ont été trouvés.")
    except Exception as e:
        print(f"Erreur lors de la gestion du popup de géolocalisation : {e}")




def main():
  driver.get(BASE_URL)
  time.sleep(2)
  if gerer_popup_geolocalisation(driver):
     time.sleep(30)
  search(driver)

if __name__ == "__main__":
  main()
