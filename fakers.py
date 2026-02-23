import string
from random import choice, randint, random, shuffle
from string import ascii_letters, digits
from random import choice, randint
from string import ascii_lowercase, ascii_uppercase, digits

""""Numbers"""
def random_number(start: int = 100, end: int = 1000) -> int:
    return randint(start, end)

""""Strings"""

# Только строчные буквы латиница
def random_lowercase_string(start: int = 9, end: int = 25) -> str:
    return ''.join(choice(ascii_lowercase) for _ in range(randint(start, end)))

# Только заглавные буквы латиница
def random_uppercase_string(start: int = 9, end: int = 25) -> str:
    return ''.join(choice(ascii_uppercase) for _ in range(randint(start, end)))

# Только символы '.', '-', '_'
def random_symbols_string(start: int = 9, end: int = 25) -> str:
    symbols = '.-_'
    return ''.join(choice(symbols) for _ in range(randint(start, end)))

# Только цифры
def random_digits_string(start: int = 9, end: int = 25) -> str:
    return ''.join(choice(digits) for _ in range(randint(start, end)))

# Микс из заглавных и строчных букв
def random_mixed_case_string(start: int = 9, end: int = 25) -> str:
    return ''.join(choice(ascii_letters) for _ in range(randint(start, end)))

# Микс из заглавных, строчных букв и цифр
def random_alphanumeric_string(start: int = 9, end: int = 25) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(randint(start, end)))

# Микс из заглавных, строчных букв, цифр и символов '.', '-', '_'
def random_complex_string(start: int = 9, end: int = 25) -> str:
    characters = ascii_letters + digits + '.-_'
    return ''.join(choice(characters) for _ in range(randint(start, end)))

def random_alphanumeric_string_length_100(length: int = 100) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

def random_alphanumeric_string_length_99(length: int = 99) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

def random_alphanumeric_string_length_50(length: int = 50) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

def random_alphanumeric_string_length_49(length: int = 49) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

def random_alphanumeric_string_length_51(length: int = 51) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

def random_alphanumeric_string_length_101(length: int = 101) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

# Строка только из пробелов
def random_spaces_string(start: int = 9, end: int = 25) -> str:
    return ' ' * randint(start, end)

# Строка из русских строчных букв
def random_russian_lowercase_string(start: int = 9, end: int = 25) -> str:
    russian_lowercase = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    return ''.join(choice(russian_lowercase) for _ in range(randint(start, end)))

# Строка из русских заглавных букв
def random_russian_uppercase_string(start: int = 9, end: int = 25) -> str:
    russian_uppercase = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    return ''.join(choice(russian_uppercase) for _ in range(randint(start, end)))

# Строка микс из русских строчных и заглавных букв
def random_russian_mixed_case_string(start: int = 9, end: int = 25) -> str:
    russian_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    return ''.join(choice(russian_letters) for _ in range(randint(start, end)))

# Строка только с символами `.-!"@#$;%^:&?*()+=/<>\\`
def random_special_symbols_string(start: int = 9, end: int = 25) -> str:
    special_symbols = '.-!"@#$;%^:&?*()+=/<>\\'
    return ''.join(choice(special_symbols) for _ in range(randint(start, end)))

# Строка с доп символами `,|`~{}[]`
def random_extended_symbols_string(start: int = 9, end: int = 25) -> str:
    extended_symbols = '.,|`~{}[]'
    return ''.join(choice(extended_symbols) for _ in range(randint(start, end)))



def random_string_mix_symbols_letters_numbers(start: int = 10, end: int = 20) -> str:
    symbols = '.-!"@#$;%^:&?*()+=/<>\\'
    return ''.join(choice(ascii_letters + digits + symbols) for _ in range(randint(start, end)))








