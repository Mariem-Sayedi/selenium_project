from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
# import account_manager
import driver_manager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import popups
import navigation
import search

# Configuration du WebDriver (Chrome)
driver = driver_manager.create_driver()

BASE_URL = driver_manager.get_base_url()
driver.maximize_window()



def main():

  driver.get(BASE_URL)
  time.sleep(2)

  
navigation.choisir_sous_sous_categorie(driver)
search.search(driver)






# # Choisir un produit au hasard et cliquer dessus
# choisir_produit_aleatoire(driver)

# # Ajouter le produit au panier
# ajouter_au_panier(driver)

# Inscrire un nouvel utilisateur
# account_manager.mon_compte_click(driver)
# account_manager.authenticate_user(driver)



# driver_manager.quit_driver(driver)

if __name__ == "__main__":
  main()