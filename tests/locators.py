from selenium.webdriver.common.by import By


class StellarBurgersLocators:
    # Страница регистрации
    NAME_INPUT = (By.XPATH, ".//label[text()='Имя']/following-sibling::input")
    EMAIL_INPUT = (By.XPATH, ".//label[text()='Email']/following-sibling::input")
    PASSWORD_INPUT = (By.XPATH, ".//label[text()='Пароль']/following-sibling::input")
    REGISTER_BUTTON = (By.XPATH, ".//button[text()='Зарегистрироваться']")
    REGISTRATION_ERROR = (By.XPATH, ".//p[text()='Некорректный пароль']")
    LOGIN_LINK_FROM_FORM = (By.XPATH, ".//a[text()='Войти']")  # ссылка "Войти" на страницах регистрации/восстановления пароля

    # Страница логина / Главная
    LOGIN_BUTTON = (By.XPATH, ".//button[text()='Войти']")
    MAIN_LOGIN_BUTTON = (By.XPATH, ".//button[text()='Войти в аккаунт']")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, ".//p[text()='Личный Кабинет']")
    CONSTRUCTOR_BUTTON = (By.XPATH, ".//p[text()='Конструктор']")
    LOGO_BUTTON = (By.XPATH, ".//div[contains(@class, 'logo')]/a")
    LOGOUT_BUTTON = (By.XPATH, ".//button[text()='Выход']")
    ORDER_BUTTON = (By.XPATH, ".//button[text()='Оформить заказ']")  # признак успешного входа
    CONSTRUCTOR_HEADER = (By.XPATH, ".//h1[text()='Соберите бургер']")

    # Табы в Конструкторе
    SAUCE_TAB = (By.XPATH, ".//span[text()='Соусы']/..")
    FILLING_TAB = (By.XPATH, ".//span[text()='Начинки']/..")
    BUN_TAB = (By.XPATH, ".//span[text()='Булки']/..")

    # Список табов для параметризованного теста
    TABS = [SAUCE_TAB, FILLING_TAB, BUN_TAB]