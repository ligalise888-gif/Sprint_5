import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urls import Urls
from helpers import generate_valid_password, generate_random_email


@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия браузера Chrome"""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(service=service, options=options)
    yield browser
    browser.quit()


@pytest.fixture
def registered_user():
    """Регистрирует уникального пользователя через API перед тестом"""
    email = generate_random_email()
    password = generate_valid_password()
    requests.post(
        f"{Urls.BASE_URL}/api/auth/register",
        json={"email": email, "password": password, "name": "Konstantin"}
    )
    return {"email": email, "password": password}