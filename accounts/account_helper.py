from dataclasses import asdict

from fakers import \
    random_string_mix_symbols_letters_numbers, random_alphanumeric_string_length_100, \
    random_alphanumeric_string_length_50, random_alphanumeric_string_length_51, random_alphanumeric_string_length_101, \
    random_lowercase_string, random_uppercase_string, random_symbols_string, random_digits_string, \
    random_mixed_case_string, random_alphanumeric_string, random_complex_string, random_spaces_string, \
    random_russian_lowercase_string, random_russian_uppercase_string, random_russian_mixed_case_string, \
    random_special_symbols_string, random_extended_symbols_string, random_alphanumeric_string_length_99, \
    random_alphanumeric_string_length_49


def create_lowercase_string():
    return random_lowercase_string()

def create_uppercase_string():
    return random_uppercase_string()

def create_simple_symbols_string():
    return random_symbols_string()

def create_digits_string():
    return random_digits_string()

def create_mixed_case_string():
    return random_mixed_case_string()

def create_alphanumeric_string():
    return random_alphanumeric_string()

def create_complex_string():
    return random_complex_string()

def create_100_length_alphanumeric_string():
    return random_alphanumeric_string_length_100()

def create_99_length_alphanumeric_string():
    return random_alphanumeric_string_length_99()

def create_50_length_alphanumeric_string():
    return random_alphanumeric_string_length_50()

def create_49_length_alphanumeric_string():
    return random_alphanumeric_string_length_49()

def create_51_length_alphanumeric_string():
    return random_alphanumeric_string_length_51()

def create_101_length_alphanumeric_string():
    return random_alphanumeric_string_length_101()

def create_spaces_string():
    return random_spaces_string()

def create_russian_lowercase_string():
    return random_russian_lowercase_string()

def create_russian_uppercase_string():
    return random_russian_uppercase_string()

def create_russian_mix_case_string():
    return random_russian_mixed_case_string()

def create_special_symbols_string():
    return random_special_symbols_string()

def create_extended_symbols_string():
    return random_extended_symbols_string()

def create_mix_symbols_letters_numbers_string():
    return random_string_mix_symbols_letters_numbers()

def create_empty_string():
    return ""




def get_fields_to_check_data(account_type, data_fields, body):
    if account_type == 'snmpv3':
        security_level = body['data'].get('security_level', 'noauth')
        return data_fields['snmpv3'].get(security_level, [])
    return data_fields.get(account_type, [])

def get_account_by_type(account_type, account_responses):
    """Helper method to find an account by its type."""
    for account in account_responses:
        if account["type"] == account_type:
            return account
    return None




def update_account_data(data, data_creator, excluded_fields):
    """
    Обновляет данные аккаунта, исключая указанные поля.
    """
    updated_data = {}
    for field, value in asdict(data).items():
        if isinstance(value, str) and value and field not in excluded_fields:
            updated_data[field] = data_creator  # Генерируем новое значение
        else:
            updated_data[field] = value  # Оставляем без изменений
    return updated_data


def update_account_data_fixed_fields_only(data, data_creator, excluded_fields):
    """
    Обновляет данные аккаунта, обновляя только поля, указанные в excluded_fields.
    """
    updated_data = {}
    for field, value in asdict(data).items():
        if field in excluded_fields:  # Проверяем, что поле входит в excluded_fields
            updated_data[field] = data_creator  # Генерируем новое значение
        else:
            updated_data[field] = value  # Оставляем без изменений
    return updated_data

def update_account_data_one_field(body, data_creator, field_to_update):
    """
    Обновляет поле 'data' в body, заменяя только одно указанное поле.
    """
    for field, value in body['data'].items():
        if field == field_to_update:  # Обновляем только указанное поле
            body['data'][field] = data_creator
        else:
            pass