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
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import os
import logging


driver = driver_manager.create_driver()

BASE_URL = driver_manager.get_base_url()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

LOGIN_URL = "https://local.lafoirfouille.fr:3012/login"



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
            input_element.send_keys("halluin")
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







def cliquer_menu(driver):
    """Clique sur l'icône du menu."""
    try:
        menu_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'icon') and contains(@class, 'header-menu')]")))
        menu_element.click()
        print("Menu cliqué avec succès !")
    except Exception as e:
        print(f"Erreur lors du clic sur le menu : {e}")




def choisir_categorie_alea(driver):
    """Choisit une catégorie au hasard dans le menu."""
    try:
        main_menu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.menu")))
        category_links = main_menu.find_elements(By.CSS_SELECTOR, "ul.menu > li > a.category-node")
        random_category = random.choice(category_links)
        driver.execute_script("arguments[0].click();", random_category)
        print(f"Catégorie principale cliquée: {random_category.text}")
    except Exception as e:
        print(f"Erreur lors de la sélection de la catégorie : {e}")




def choisir_sous_categorie_alea(driver):
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

        anciens_noms = []
        if os.path.exists(fichier_json):
            with open(fichier_json, "r", encoding="utf-8") as f:
                try:
                    anciens_noms = json.load(f)
                except json.JSONDecodeError:
                    pass  

        tous_les_noms = list(set(anciens_noms + nouveaux_noms))

        with open(fichier_json, "w", encoding="utf-8") as f:
            json.dump(tous_les_noms, f, ensure_ascii=False, indent=4)

        random_sub_sub_category = random.choice(valid_sub_sub_category_links)
        random_sub_sub_category.click()

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Erreur lors de la sélection de la sous-sous-catégorie : {e}")




def choisir_produit_aleatoire(driver):
    """Choisit et clique sur un produit au hasard."""
    try:
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



def click_cart_icon(driver):
    """Clique sur l'icône du panier."""
    try:
        cart_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'icon content-slot-lp')]")))
        cart_element.click()
        print("Panier cliqué avec succès !")
        button_connexion = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Me connecter"))
     )
        button_connexion.click()

    except Exception as e:
        print(f"Erreur lors du clic sur le Panier : {e}")


def remplir_champ_avec_selection(name, valeur):
    champ = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, name)))
    champ.send_keys(valeur)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "dropdown-menu")))

    premiere_option = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dropdown-menu li:first-child")))
    premiere_option.click()


def verifier_presence_iframe(driver):
    """Vérifie la présence d'iframes sur une page web."""
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if len(iframes) > 0:
            print(f"Il y a {len(iframes)} iframe(s) sur cette page.")
            for iframe in iframes:
                print(f"ID: {iframe.get_attribute('id')}, Nom: {iframe.get_attribute('name')}, Source: {iframe.get_attribute('src')}")
            return True
        else:
            print("Aucun iframe trouvé sur cette page.")
            return False

    except Exception as e:
        print(f"Erreur lors de la vérification des iframes : {e}")
        return False



def load_user_data(filename="users600_cabries.json"):
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
    

def login(driver, user_index=12, json_path="users_thiais_cabries.json"):
    driver.get(LOGIN_URL)
     
    time.sleep(10)
    gerer_popup_geolocalisation(driver)
    time.sleep(10)

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

        gerer_popup_geolocalisation(driver)

        
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
   



def search(driver, file="sous_sous_categories.json"): 
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
        input_search.send_keys(Keys.RETURN)
        
        print(f"Recherche effectuée pour : {query}")
        return True

    except Exception as e:
        print(f"Erreur de recherche : {e}")
        return False



def main():
  
#   users = load_user_data("users600_GAP.json") 

  login(driver) 
  time.sleep(3)
       
  for j in range(15):
      search(driver)
      choisir_produit_aleatoire(driver)
      cliquer_menu(driver)
      choisir_categorie_alea(driver)
      choisir_sous_categorie_alea(driver)
      choisir_sous_sous_categorie(driver)
      choisir_produit_aleatoire(driver)
      ajouter_au_panier(driver)
        
  driver.quit()


#   click_cart_icon(driver)
#   account_manager.login(driver)
#   button_validation1 = WebDriverWait(driver, 10).until(
#   EC.element_to_be_clickable((By.LINK_TEXT, "VALIDER"))
#     )
#   button_validation1.click()

#   button_validation2 = WebDriverWait(driver, 10).until(
#   EC.element_to_be_clickable((By.LINK_TEXT, "Valider"))
#   )
#   button_validation2.click()
#   checkbox = driver.find_element(By.CLASS_NAME, "cdg-paiement sale-terms-checked")
#   print(checkbox)

  
#   checkbox = driver.find_element(By.ID, "test")

#   if not checkbox.is_selected():
#     checkbox.click()

#   actions = ActionChains(driver)
#   actions.move_to_element(checkbox).click().perform()


#   assert checkbox.is_selected(), "La case des CGV n'a pas été cochée !"
 



#         button_pay2 = WebDriverWait(driver, 30).until(
#             EC.visibility_of_element_located((By.CLASS_NAME, "cta-principal cta-desactive"))
#         )

#         # Utiliser JavaScript pour forcer le clic
#         driver.execute_script("arguments[0].click();", button_pay2)
#         print("Bouton de paiement cliqué avec succès !")

#   except TimeoutException:
#         print("Erreur : L'iframe, la case à cocher ou le bouton de paiement n'a pas été trouvé dans le temps imparti.")
#   except NoSuchElementException:
#         print("Erreur : L'élément n'a pas été trouvé.")
#   except Exception as e:
#         print(f"Erreur paiement : {e}")


#   button_pay2 = WebDriverWait(driver, 20).until(
#   EC.element_to_be_clickable((By.CLASS_NAME, "cta-principal cta-desactive"))
#   )
#   button_pay2.click()
# except Exception as e:
#        print(f"Erreur paiement : {e}")
    


if __name__ == "__main__":
  main()


#   try:
#      select_element = WebDriverWait(driver, 10).until(
#          EC.presence_of_element_located((By.XPATH, "//select[@title='Pays']"))
#      )

#      select = Select(select_element)
#      select.select_by_value("FR")
#      print("Pays sélectionné avec succès !")

 
#      remplir_champ_avec_selection("locality", "75001 Paris")
#      remplir_champ_avec_selection("streetName", "Rue de Rivoli")
#      remplir_champ_avec_selection("streetNumber", "10")


#      input_buildingName = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "building")))
#      input_buildingName.send_keys("A") 
#      input_buildingName.send_keys(Keys.RETURN)

#      input_line3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "line3")))
#      input_line3.send_keys("5B") 
#      input_line3.send_keys(Keys.RETURN)
     

#        button_pay1 = WebDriverWait(driver, 20).until(
#        EC.element_to_be_clickable((By.CLASS_NAME, "adress btn-submit red "))
#        )
#        button_pay1.click()
#   except Exception as e:
#         print(f"Erreur selection : {e}")
