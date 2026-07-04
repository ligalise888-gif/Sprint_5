import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия браузера Chrome"""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    # Если в Практикуме требуют запускать без отображения окна (headless), раскомментируй строку ниже:
    # options.add_argument("--headless")
    
    browser = webdriver.Chrome(service=service, options=options)
    yield browser
    browser.quit()