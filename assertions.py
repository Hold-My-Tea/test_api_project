from datetime import datetime, timedelta

from assertpy import assert_that
from dateutil import parser

def assert_status_code(response: object, expected_status: object) -> object:
    assert_that(response.status_code).described_as(
        f"Expected status code {expected_status}, but got {response.status_code}. Response body: {response.text}"
    ).is_equal_to(expected_status)

def assert_contains_key(json_response, key):

    assert_that(json_response).described_as(
        f"Expected key '{key}' not found in JSON response. Available keys: {list(json_response.keys())}"
    ).contains_key(key)

def assert_equal(actual, expected):

    assert_that(actual).described_as(
        f"Expected value '{expected}', but got '{actual}'"
    ).is_equal_to(expected)

def assert_not_equal(actual, expected):

    assert_that(actual).described_as(
        f"Expected value '{actual}' to be different from '{expected}', but they are equal"
    ).is_not_equal_to(expected)


def assert_response_time(response_time, max_time):
    """
    Проверяет, что время выполнения запроса не превышает допустимого значения.
    :param response_time: Фактическое время выполнения запроса.
    :param max_time: Максимально допустимое время выполнения запроса.
    """
    assert_that(response_time).described_as(
        f"Request took too long: {response_time} seconds (max allowed: {max_time} seconds)"
    ).is_less_than(max_time)

def assert_created_at(response_created_at):
    """
    Проверяет, что дата создания (created_at) находится в пределах 2 минут от текущего времени.
    :param response_created_at: Дата создания из ответа API в формате строки.
    """
    # Парсим строку с датой из ответа
    created_at = parser.isoparse(response_created_at)

    # Получаем текущее время
    current_time = datetime.now(created_at.tzinfo)  # Учитываем временную зону из ответа

    # Вычисляем разницу между текущим временем и временем создания
    time_difference = abs(current_time - created_at)

    # Проверяем, что разница не превышает 2 минут
    assert_that(time_difference).described_as(
        f"Created_at is not within the expected range. "
        f"Expected difference: <= 2 minutes, actual difference: {time_difference}"
    ).is_less_than_or_equal_to(timedelta(minutes=2))