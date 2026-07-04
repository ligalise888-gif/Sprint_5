import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators import StellarBurgersLocators
from urls import Urls
from helpers import generate_valid_password, generate_random_email

class TestStellarBurgers:

    def test_registration_success(self, driver):
        """Успешная регистрация пользователя"""
        driver.get(Urls.REGISTER_URL)
        
        # Ждем появления поля имени
        WebDriverWait(driver, 8).until(EC.visibility_of_element_located(StellarBurgersLocators.NAME_INPUT))
        
        random_email = generate_random_email()
        random_password = generate_valid_password()
        
        driver.find_element(*StellarBurgersLocators.NAME_INPUT).send_keys("Konstantin")
        driver.find_element(*StellarBurgersLocators.EMAIL_INPUT).send_keys(random_email)
        # Исправленный локатор пароля (ищем по лейблу)
        driver.find_element(By.XPATH, ".//label[text()='Пароль']/following-sibling::input").send_keys(random_password)
        driver.find_element(*StellarBurgersLocators.REGISTER_BUTTON).click()
        
        # Ожидаем переход на страницу логина
        WebDriverWait(driver, 8).until(EC.url_to_be(Urls.LOGIN_URL))
        assert driver.current_url == Urls.LOGIN_URL

    def test_registration_error_invalid_password(self, driver):
        """Ошибка при регистрации с коротким паролем"""
        driver.get(Urls.REGISTER_URL)
        
        WebDriverWait(driver, 8).until(EC.visibility_of_element_located(StellarBurgersLocators.NAME_INPUT))
        
        driver.find_element(*StellarBurgersLocators.NAME_INPUT).send_keys("Konstantin")
        driver.find_element(*StellarBurgersLocators.EMAIL_INPUT).send_keys(generate_random_email())
        # Исправленный локатор пароля (ищем по лейблу)
        driver.find_element(By.XPATH, ".//label[text()='Пароль']/following-sibling::input").send_keys("123")
        driver.find_element(*StellarBurgersLocators.REGISTER_BUTTON).click()
        
        # Ждем появления ошибки
        error_message = WebDriverWait(driver, 8).until(
            EC.visibility_of_element_located(StellarBurgersLocators.REGISTRATION_ERROR)
        )
        assert error_message.is_displayed()

    def test_login_from_main_page(self, driver):
        """Вход через кнопку 'Войти в аккаунт' на главной"""
        driver.get(Urls.BASE_URL)

    def test_login_from_personal_account(self, driver):
        """Вход через кнопку 'Личный Кабинет'"""
        driver.get(Urls.BASE_URL)

    def test_navigation_to_personal_account(self, driver):
        """Переход в личный кабинет по клику на 'Личный кабинет'"""
        driver.get(Urls.BASE_URL)

    def test_navigation_from_account_to_constructor(self, driver):
        """Переход из личного кабинета в конструктор"""
        driver.get(Urls.LOGIN_URL)

    def test_logout(self, driver):
        """Выход из аккаунта"""
        driver.get(Urls.LOGIN_URL)

    def test_constructor_sauce_tab(self, driver):
        """Проверка перехода на вкладку 'Соусы'"""
        driver.get(Urls.BASE_URL)
        sauce_tab = driver.find_element(*StellarBurgersLocators.SAUCE_TAB)
        sauce_tab.click()
        WebDriverWait(driver, 8).until(lambda d: "tab_tab_type_current" in sauce_tab.get_attribute("class"))
        assert "tab_tab_type_current" in sauce_tab.get_attribute("class")

    def test_constructor_filling_tab(self, driver):
        """Проверка перехода на вкладку 'Начинки'"""
        driver.get(Urls.BASE_URL)
        filling_tab = driver.find_element(*StellarBurgersLocators.FILLING_TAB)
        filling_tab.click()
        WebDriverWait(driver, 8).until(lambda d: "tab_tab_type_current" in filling_tab.get_attribute("class"))
        assert "tab_tab_type_current" in filling_tab.get_attribute("class")

    def test_constructor_bun_tab(self, driver):
        """Проверка перехода на вкладку 'Булки'"""
        driver.get(Urls.BASE_URL)
        driver.find_element(*StellarBurgersLocators.SAUCE_TAB).click()
        bun_tab = driver.find_element(*StellarBurgersLocators.BUN_TAB)
        bun_tab.click()
        WebDriverWait(driver, 8).until(lambda d: "tab_tab_type_current" in bun_tab.get_attribute("class"))
        assert "tab_tab_type_current" in bun_tab.get_attribute("class")