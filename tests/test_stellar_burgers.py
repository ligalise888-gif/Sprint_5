import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators import StellarBurgersLocators
from urls import Urls
from helpers import generate_valid_password, generate_random_email, login


class TestStellarBurgers:

    def test_registration_success(self, driver):
        """Успешная регистрация пользователя"""
        driver.get(Urls.REGISTER_URL)
        WebDriverWait(driver, 8).until(EC.visibility_of_element_located(StellarBurgersLocators.NAME_INPUT))

        random_email = generate_random_email()
        random_password = generate_valid_password()

        driver.find_element(*StellarBurgersLocators.NAME_INPUT).send_keys("Konstantin")
        driver.find_element(*StellarBurgersLocators.EMAIL_INPUT).send_keys(random_email)
        driver.find_element(*StellarBurgersLocators.PASSWORD_INPUT).send_keys(random_password)
        driver.find_element(*StellarBurgersLocators.REGISTER_BUTTON).click()

        WebDriverWait(driver, 8).until(EC.url_to_be(Urls.LOGIN_URL))
        assert driver.current_url == Urls.LOGIN_URL

    def test_registration_error_invalid_password(self, driver):
        """Ошибка при регистрации с коротким паролем"""
        driver.get(Urls.REGISTER_URL)
        WebDriverWait(driver, 8).until(EC.visibility_of_element_located(StellarBurgersLocators.NAME_INPUT))

        driver.find_element(*StellarBurgersLocators.NAME_INPUT).send_keys("Konstantin")
        driver.find_element(*StellarBurgersLocators.EMAIL_INPUT).send_keys(generate_random_email())
        driver.find_element(*StellarBurgersLocators.PASSWORD_INPUT).send_keys("123")
        driver.find_element(*StellarBurgersLocators.REGISTER_BUTTON).click()

        error_message = WebDriverWait(driver, 8).until(
            EC.visibility_of_element_located(StellarBurgersLocators.REGISTRATION_ERROR)
        )
        assert error_message.is_displayed()

    def test_login_from_main_page(self, driver, registered_user):
        """Вход через кнопку 'Войти в аккаунт' на главной"""
        driver.get(Urls.BASE_URL)
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable(StellarBurgersLocators.MAIN_LOGIN_BUTTON)
        ).click()
        login(driver, registered_user["email"], registered_user["password"])
        assert driver.find_element(*StellarBurgersLocators.ORDER_BUTTON).is_displayed()

    def test_login_from_personal_account(self, driver, registered_user):
        """Вход через кнопку 'Личный Кабинет'"""
        driver.get(Urls.BASE_URL)
        driver.find_element(*StellarBurgersLocators.PERSONAL_ACCOUNT_BUTTON).click()
        login(driver, registered_user["email"], registered_user["password"])
        assert driver.find_element(*StellarBurgersLocators.ORDER_BUTTON).is_displayed()

    def test_login_from_register_form(self, driver, registered_user):
        """Вход через ссылку 'Войти' на форме регистрации"""
        driver.get(Urls.REGISTER_URL)
        driver.find_element(*StellarBurgersLocators.LOGIN_LINK_FROM_FORM).click()
        login(driver, registered_user["email"], registered_user["password"])
        assert driver.find_element(*StellarBurgersLocators.ORDER_BUTTON).is_displayed()

    def test_login_from_forgot_password_form(self, driver, registered_user):
        """Вход через ссылку 'Войти' на форме восстановления пароля"""
        driver.get(Urls.FORGOT_PASSWORD_URL)
        driver.find_element(*StellarBurgersLocators.LOGIN_LINK_FROM_FORM).click()
        login(driver, registered_user["email"], registered_user["password"])
        assert driver.find_element(*StellarBurgersLocators.ORDER_BUTTON).is_displayed()

    def test_navigation_to_personal_account(self, driver, registered_user):
        """Переход в личный кабинет по клику на 'Личный кабинет'"""
        driver.get(Urls.LOGIN_URL)
        login(driver, registered_user["email"], registered_user["password"])
        driver.find_element(*StellarBurgersLocators.PERSONAL_ACCOUNT_BUTTON).click()
        WebDriverWait(driver, 8).until(EC.url_contains("/account/profile"))
        assert "/account/profile" in driver.current_url

    def test_navigation_from_account_to_constructor(self, driver, registered_user):
        """Переход из личного кабинета в конструктор по клику на логотип"""
        driver.get(Urls.LOGIN_URL)
        login(driver, registered_user["email"], registered_user["password"])
        driver.find_element(*StellarBurgersLocators.PERSONAL_ACCOUNT_BUTTON).click()
        WebDriverWait(driver, 8).until(EC.url_contains("/account/profile"))
        driver.find_element(*StellarBurgersLocators.LOGO_BUTTON).click()
        WebDriverWait(driver, 8).until(
            EC.visibility_of_element_located(StellarBurgersLocators.CONSTRUCTOR_HEADER)
        )
        assert driver.current_url == Urls.BASE_URL + "/"

    def test_logout(self, driver, registered_user):
        """Выход из аккаунта"""
        driver.get(Urls.LOGIN_URL)
        login(driver, registered_user["email"], registered_user["password"])
        driver.find_element(*StellarBurgersLocators.PERSONAL_ACCOUNT_BUTTON).click()
        WebDriverWait(driver, 8).until(EC.url_contains("/account/profile"))
        driver.find_element(*StellarBurgersLocators.LOGOUT_BUTTON).click()
        WebDriverWait(driver, 8).until(
            EC.visibility_of_element_located(StellarBurgersLocators.LOGIN_BUTTON)
        )
        assert driver.current_url == Urls.LOGIN_URL

    @pytest.mark.parametrize("tab_locator", StellarBurgersLocators.TABS)
    def test_constructor_tab_switch(self, driver, tab_locator):
        """Проверка переключения активного таба в Конструкторе"""
        driver.get(Urls.BASE_URL)
        tab = driver.find_element(*tab_locator)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab)
        WebDriverWait(driver, 8).until(EC.element_to_be_clickable(tab_locator))
        driver.execute_script("arguments[0].click();", tab)
        WebDriverWait(driver, 8).until(
            lambda d: "tab_tab_type_current" in tab.get_attribute("class")
        )
        assert "tab_tab_type_current" in tab.get_attribute("class")