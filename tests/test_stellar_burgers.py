import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
import string

# ===================================================================================
# ЛОКАТОРЫ (С комментариями по требованию Пункта 3 задания)
# ===================================================================================
NAME_INPUT = (By.XPATH, ".//label[text()='Имя']/following-sibling::input")  # Поле ввода "Имя" на форме регистрации
EMAIL_INPUT = (By.XPATH, ".//label[text()='Email']/following-sibling::input")  # Поле ввода "Email" на форме регистрации и входа
PASSWORD_INPUT = (By.XPATH, ".//label[text()='Пароль']/following-sibling::input")  # Поле ввода "Пароль" на форме регистрации и входа
AUTH_BUTTON = (By.XPATH, ".//button[text()='Войти']")  # Кнопка "Войти" на форме авторизации
CABINET_BUTTON = (By.XPATH, ".//p[text()='Личный Кабинет']")  # Кнопка "Личный Кабинет" в шапке сайта
ORDER_BUTTON = (By.XPATH, ".//button[text()='Оформить заказ']")  # Кнопка "Оформить заказ" на главной странице
CONSTRUCTOR_HEADER = (By.XPATH, ".//h1[text()='Соберите бургер']")  # Заголовок страницы Конструктора

# ===================================================================================
# ФИКСТУРЫ И ГЕНЕРАТОРЫ
# ===================================================================================
@pytest.fixture(scope="function")
def driver():
    """Фикстура для запуска и закрытия браузера Chrome"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://stellarburgers.education-services.ru/")
    yield driver
    driver.quit()

def generate_email():
    """Генерация уникального email строго по формату ТЗ: имя_фамилия_номеркогорты_3цифры@домен"""
    cohort = "50"  # Твоя когорта 50
    random_digits = ''.join(random.choices(string.digits, k=3))
    return f"konstantinshreyder{cohort}_{random_digits}@gmail.com"

def generate_valid_password():
    """Генерация валидного пароля (от 6 символов)"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# ===================================================================================
# БЛОК 1: РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
# ===================================================================================
def test_registration_success(driver):
    """Успешная регистрация с динамическим логином и динамическим паролем"""
    driver.get("https://stellarburgers.education-services.ru/register")

    random_email = generate_email()
    random_password = generate_valid_password()

    driver.find_element(*NAME_INPUT).send_keys("Konstantin")
    driver.find_element(*EMAIL_INPUT).send_keys(random_email)
    driver.find_element(*PASSWORD_INPUT).send_keys(random_password)
    driver.find_element(By.XPATH, ".//button[text()='Зарегистрироваться']").click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(AUTH_BUTTON))
    assert driver.current_url == "https://stellarburgers.education-services.ru/login"


@pytest.mark.parametrize("invalid_password", ["a", "12345"])
def test_registration_short_password_error(driver, invalid_password):
    """Отображение ошибки при вводе некорректного (короткого) пароля"""
    driver.get("https://stellarburgers.education-services.ru/register")

    random_email = generate_email()

    driver.find_element(*NAME_INPUT).send_keys("Konstantin")
    driver.find_element(*EMAIL_INPUT).send_keys(random_email)
    driver.find_element(*PASSWORD_INPUT).send_keys(invalid_password)
    driver.find_element(By.XPATH, ".//button[text()='Зарегистрироваться']").click()

    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, ".//p[text()='Некорректный пароль']"))
    )
    assert error_msg.is_displayed()


# ===================================================================================
# БЛОК 2: АВТОРИЗАЦИЯ (ВХОД) С РАЗНЫХ ТОЧЕК ИНТЕРФЕЙСА
# ===================================================================================
@pytest.mark.parametrize("start_url, click_locator", [
    ("https://stellarburgers.education-services.ru/", (By.XPATH, ".//button[text()='Войти в аккаунт']")),
    ("https://stellarburgers.education-services.ru/", CABINET_BUTTON),
    ("https://stellarburgers.education-services.ru/register", (By.XPATH, ".//a[text()='Войти']")),
    ("https://stellarburgers.education-services.ru/forgot-password", (By.XPATH, ".//a[text()='Войти']"))
])
def test_login_from_different_points(driver, start_url, click_locator):
    """Вход в систему с четырех разных точек UI под созданным аккаунтом"""
    driver.get(start_url)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(click_locator)).click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(EMAIL_INPUT))
    driver.find_element(*EMAIL_INPUT).send_keys("konstantinshreyder50_727@gmail.com")
    driver.find_element(*PASSWORD_INPUT).send_keys("kursavel7")
    driver.find_element(*AUTH_BUTTON).click()

    order_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(ORDER_BUTTON))
    assert order_btn.is_displayed()


# ===================================================================================
# БЛОК 3: ЛИЧНЫЙ КАБИНЕТ И НАВИГАЦИЯ
# ===================================================================================
def test_navigation_and_logout(driver):
    """Переход в ЛК, возврат по клику на Конструктор/Логотип и выход из аккаунта"""
    driver.get("https://stellarburgers.education-services.ru/login")
    driver.find_element(*EMAIL_INPUT).send_keys("konstantinshreyder50_727@gmail.com")
    driver.find_element(*PASSWORD_INPUT).send_keys("kursavel7")
    driver.find_element(*AUTH_BUTTON).click()
    
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(ORDER_BUTTON))

    # 1. Переход в Личный Кабинет
    driver.find_element(*CABINET_BUTTON).click()
    WebDriverWait(driver, 10).until(EC.url_contains("/account/profile"))
    assert "/account/profile" in driver.current_url

    # 2. Клик на кнопку "Конструктор"
    driver.find_element(By.XPATH, ".//p[text()='Конструктор']").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(CONSTRUCTOR_HEADER))
    assert driver.current_url == "https://stellarburgers.education-services.ru/"

    # Возвращаемся в ЛК для следующей проверки
    driver.find_element(*CABINET_BUTTON).click()
    WebDriverWait(driver, 10).until(EC.url_contains("/account/profile"))

    # 3. Клик на Логотип Stellar Burgers
    driver.find_element(By.XPATH, ".//div[contains(@class, 'logo')]/a").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(CONSTRUCTOR_HEADER))
    assert driver.current_url == "https://stellarburgers.education-services.ru/"

    # 4. Выход из аккаунта
    driver.find_element(*CABINET_BUTTON).click()
    logout_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, ".//button[text()='Выход']"))
    )
    logout_btn.click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(AUTH_BUTTON))
    assert driver.current_url == "https://stellarburgers.education-services.ru/login"


# ===================================================================================
# БЛОК 4: КОНСТРУКТОР БУРГЕРОВ
# ===================================================================================
def test_constructor_tabs(driver):
    """Проверка переключения активных табов в Конструкторе"""
    driver.get("https://stellarburgers.education-services.ru/")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(CONSTRUCTOR_HEADER))

    # Клик на Соусы
    sauce_tab = driver.find_element(By.XPATH, ".//span[text()='Соусы']/..")
    sauce_tab.click()
    WebDriverWait(driver, 5).until(lambda d: "tab_tab_type_current" in sauce_tab.get_attribute("class"))
    assert "tab_tab_type_current" in sauce_tab.get_attribute("class")

    # Клик на Начинки
    filling_tab = driver.find_element(By.XPATH, ".//span[text()='Начинки']/..")
    filling_tab.click()
    WebDriverWait(driver, 5).until(lambda d: "tab_tab_type_current" in filling_tab.get_attribute("class"))
    assert "tab_tab_type_current" in filling_tab.get_attribute("class")

    # Клик обратно на Булки
    bun_tab = driver.find_element(By.XPATH, ".//span[text()='Булки']/..")
    bun_tab.click()
    
    # Стабильное ожидание возвращения активного класса на вкладку Булки
    WebDriverWait(driver, 5).until(lambda d: "tab_tab_type_current" in bun_tab.get_attribute("class"))
    assert "tab_tab_type_current" in bun_tab.get_attribute("class")