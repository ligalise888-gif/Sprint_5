import random
import string

def generate_valid_password():
    """Генерация валидного пароля (от 6 символов)"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def generate_random_email():
    """Генерация уникального email"""
    return f"konstantin_{random.randint(100, 999)}@yandex.ru"