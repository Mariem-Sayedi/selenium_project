from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://local.lafoirfouille.fr:3012/"

def create_driver():
    """Crée et renvoie une instance de WebDriver."""
    options = Options()
    options.add_experimental_option("detach", True) 
    driver = webdriver.Chrome(options=options)
    return driver

def quit_driver(driver):
    """Ferme le WebDriver."""
    driver.quit()

def get_base_url():
    """Renvoie l'URL de base."""
    return BASE_URL