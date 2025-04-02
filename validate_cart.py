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
import navigation
# import test

CART_URL = "https://local.lafoirfouille.fr:3012/cart"