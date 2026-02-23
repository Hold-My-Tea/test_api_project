from http import HTTPStatus

import httpx

from assertions import assert_status_code, assert_contains_key, assert_equal
from config import BASE_URL
from authentication_api import get_token

from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

@retry(
            stop=stop_after_attempt(7),
            wait=wait_fixed(3),
            retry=retry_if_exception_type((httpx.ConnectError, httpx.ConnectTimeout)),  # Повторять только при ошибке
                                          # подключения
        )
def create_account_request(body, auth=True):
    """Создание запроса для создания аккаунта."""
    with httpx.Client(verify=False) as client:
        headers = {
            "Content-Type": "application/json",
        }
        if auth:  # Добавляем заголовок авторизации только если auth=True
            token = get_token(client)
            headers["Authorization"] = f'Bearer {token}'

        response = client.post(
            f'{BASE_URL}',  # URL для создания аккаунта
            json=body,  # Тело запроса
            headers=headers,
        )
    return response


@retry(
            stop=stop_after_attempt(7),
            wait=wait_fixed(3),
            retry=retry_if_exception_type((httpx.ConnectError, httpx.ConnectTimeout)),  # Повторять только при ошибке
                                          # подключения
        )
def patch_account_request(account_id, body, auth=True):
    """Создание запроса для изменения аккаунта."""
    with httpx.Client(verify=False) as client:
        headers = {
            "Content-Type": "application/json",
        }
        if auth:  # Добавляем заголовок авторизации только если auth=True
            token = get_token(client)
            headers["Authorization"] = f'Bearer {token}'

        response = client.patch(
            f'{BASE_URL}/{account_id}',
            json=body,
            headers=headers,
        )
    return response


@retry(
            stop=stop_after_attempt(7),
            wait=wait_fixed(3),
            retry=retry_if_exception_type((httpx.ConnectError, httpx.ConnectTimeout)),  # Повторять только при ошибке
                                          # подключения
        )
def get_account_by_id_request(account_id, auth=True):
    """Создание запроса для получения аккаунта по ID."""
    with httpx.Client(verify=False) as client:
        headers = {
            "Content-Type": "application/json",
        }
        if auth:  # Добавляем заголовок авторизации только если auth=True
            token = get_token(client)
            headers["Authorization"] = f'Bearer {token}'

        response = client.get(
            f'{BASE_URL}/{account_id}',
            headers=headers,
        )
    return response

@retry(
            stop=stop_after_attempt(7),
            wait=wait_fixed(3),
            retry=retry_if_exception_type((httpx.ConnectError, httpx.ConnectTimeout)),  # Повторять только при ошибке
                                          # подключения
        )
def delete_account_request(account_id, auth=True):
    """Создание запроса для удаления аккаунта по ID."""
    with httpx.Client(verify=False) as client:
        headers = {
            "Content-Type": "application/json",
        }
        if auth:  # Добавляем заголовок авторизации только если auth=True
            token = get_token(client)
            headers["Authorization"] = f'Bearer {token}'

        response = client.delete(
            f'{BASE_URL}/{account_id}',
            headers=headers,
        )
    return response


@retry(
            stop=stop_after_attempt(7),
            wait=wait_fixed(3),
            retry=retry_if_exception_type((httpx.ConnectError, httpx.ConnectTimeout)),  # Повторять только при ошибке
                                          # подключения
        )
def get_accounts_list_request(page=None, limit=None, q=None, auth=True):
    params = {}
    if page is not None:
        params["page"] = page
    if limit is not None:
        params["limit"] = limit
    if q is not None:
        params["q"] = q

    headers = {"Content-Type": "application/json"}
    if auth:
        with httpx.Client(verify=False) as client:
            token = get_token(client)
            headers["Authorization"] = f'Bearer {token}'

    with httpx.Client(verify=False) as client:
        return client.get(f'{BASE_URL}', headers=headers, params=params)