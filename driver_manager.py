from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait



BASE_URL = "https://local.lafoirfouille.fr:3012/"

def create_driver():
    """Crée et renvoie une instance de WebDriver."""
    options = Options()
    options.add_experimental_option("detach", True) 
    driver = webdriver.Chrome(options=options)
    # WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    return driver

def quit_driver(driver):
    """Ferme le WebDriver."""
    driver.quit()

def get_base_url():
    """Renvoie l'URL de base."""
    return BASE_URL