import random
import string
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import StellarBurgersLocators


def generate_valid_password():
    """Генерация валидного пароля (от 6 символов)"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


def generate_random_email():
    """Генерация уникального email"""
    return f"konstantin_{random.randint(100, 999)}@yandex.ru"


def login(driver, email, password):
    """Заполняет форму логина и подтверждает вход"""
    WebDriverWait(driver, 8).until(
        EC.visibility_of_element_located(StellarBurgersLocators.EMAIL_INPUT)
    )
    driver.find_element(*StellarBurgersLocators.EMAIL_INPUT).send_keys(email)
    driver.find_element(*StellarBurgersLocators.PASSWORD_INPUT).send_keys(password)
    driver.find_element(*StellarBurgersLocators.LOGIN_BUTTON).click()
    WebDriverWait(driver, 8).until(
        EC.visibility_of_element_located(StellarBurgersLocators.ORDER_BUTTON)
    )