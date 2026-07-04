from selenium.webdriver.common.by import By

class StellarBurgersLocators:
    # Страница регистрации (Используем универсальный поиск по тексту внутри лейбла/инпута)
    NAME_INPUT = (By.XPATH, ".//label[text()='Имя']/following-sibling::input") 
    EMAIL_INPUT = (By.XPATH, ".//label[text()='Email']/following-sibling::input")
    PASSWORD_INPUT = (By.XPATH, ".//input[@name='password']")
    REGISTER_BUTTON = (By.XPATH, ".//button[text()='Зарегистрироваться']")
    REGISTRATION_ERROR = (By.XPATH, ".//p[text()='Некорректный пароль']")

    # Страница логина / Главная
    LOGIN_BUTTON = (By.XPATH, ".//button[text()='Войти']")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, ".//p[text()='Личный Кабинет']")
    CONSTRUCTOR_BUTTON = (By.XPATH, ".//p[text()='Конструктор']")
    LOGO_BUTTON = (By.XPATH, ".//div[contains(@class, 'logo')]")
    LOGOUT_BUTTON = (By.XPATH, ".//button[text()='Выход']")

    # Табы в Конструкторе
    SAUCE_TAB = (By.XPATH, ".//span[text()='Соусы']/..")
    FILLING_TAB = (By.XPATH, ".//span[text()='Начинки']/..")
    BUN_TAB = (By.XPATH, ".//span[text()='Булки']/..")