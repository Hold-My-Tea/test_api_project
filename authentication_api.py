import os


def get_token(client):
    username = os.getenv('USER_NAME')
    password = 'admin'
    url = os.getenv('TOKEN_URL')


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'KEYCLOAK_LOCALE=ru'  # Добавляем куки
    }

    # Данные для отправки
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'scope': 'email profile openid',
        'client_id': 'admin-ui',
        'client_secret': ''  # Если есть секрет, добавьте его сюда
    }

    response = client.post(url, headers=headers, data=data)
    json_response = response.json()
    return json_response['access_token']