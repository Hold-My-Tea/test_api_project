from dataclasses import asdict
import time


from http import HTTPStatus

import allure
import pytest
from assertpy import assert_that
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from accounts.account_api import create_account_request, get_account_by_id_request, delete_account_request, \
    get_accounts_list_request, patch_account_request
from accounts.account_helper import (create_100_length_alphanumeric_string, create_101_length_alphanumeric_string, \
 \
                                     create_alphanumeric_string, \
                                     create_50_length_alphanumeric_string,
                                     create_51_length_alphanumeric_string, create_lowercase_string,
                                     create_uppercase_string, create_simple_symbols_string,
                                     create_digits_string, create_mixed_case_string, create_complex_string,
                                     create_spaces_string, create_empty_string, create_russian_lowercase_string,
                                     create_russian_uppercase_string, create_russian_mix_case_string,
                                     create_special_symbols_string, create_extended_symbols_string,
                                     create_49_length_alphanumeric_string, create_99_length_alphanumeric_string)
from accounts.account_helper import get_fields_to_check_data, update_account_data, \
    update_account_data_one_field
from accounts.test_data import IPMIData, Snmpv2cData, Snmpv3Noauth, Name, FIXED_DATA_FIELDS
from accounts.tests.conftest import accounts_storage
from assertions import assert_status_code, assert_contains_key, assert_equal, assert_response_time


@allure.feature('Accounts API')
class TestAccounts:

    @allure.story('Method Post')
    class TestPostMethod:


        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create all type accounts with valid data')
        def test_create_all_type_accounts(self, all_type_account_data):
            account_type, data = all_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }

            response = create_account_request(body)
            assert_status_code(response, HTTPStatus.CREATED)
            json_response = response.json()
            assert_contains_key(json_response, "id")
            if "id" in json_response:
                accounts_storage.append(json_response['id'])
            for key in ["name", "type", "data"]:
                assert_equal(json_response[key], body[key])

            # #Проверка даты создания (created_at)
            # created_at = json_response.get("created_at")
            #
            # # Проверяем, что created_at находится в пределах 2 минут от текущего времени
            # assert_created_at(created_at)

        @pytest.mark.skip(reason="Test fails. Bug is reported - duplicated accounts shouldn't be created")
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create duplicated accounts')
        def test_create_duplicated_accounts(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            assert_status_code(response, HTTPStatus.CREATED)
            json_response = response.json()
            accounts_storage.append(json_response['id'])  # Add id for fixture cleanup_accounts
            response_second_try = create_account_request(body)  #Create account with the same type and name
            json_response = response_second_try.json()
            if "id" in json_response:
                accounts_storage.append(json_response['id'])  # Add id for fixture cleanup_accounts
            assert_status_code(response_second_try, HTTPStatus.CONFLICT)



        @pytest.mark.parametrize("field, expected_error", [
            ("name", None),  # Clear name
            ("type", None),  # Clear type
            ("data", None),  # Clear data
        ])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account with missing necessary fields')
        def test_create_account_without_necessary_fields(self, field, expected_error, main_type_account_data):
            account_type, data = main_type_account_data

            body = dict(name=Name().name, type=account_type, data=asdict(data))

            body[field] = expected_error  # Clear field
            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответа

        @allure.title('Create account and verify performance')
        def test_create_account_and_verify_performance(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            start_time = time.time()
            response = create_account_request(body)
            end_time = time.time()
            assert_status_code(response, HTTPStatus.CREATED)
            assert_response_time(end_time - start_time, max_time=16.0)

            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])

        @allure.title('Create account without authorization')
        def test_create_account_without_authorization(self, main_type_account_data):
            # Подготавливаем данные для создания аккаунта
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }

            # Пытаемся создать аккаунт без авторизации
            response = create_account_request(body, auth=False)

            # Проверяем, что запрос завершился с ошибкой 401 Unauthorized
            assert_status_code(response, HTTPStatus.UNAUTHORIZED)


        """Name validation"""
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account name with max length')
        def test_create_account_name_max_length(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name(name=create_100_length_alphanumeric_string()).name,
                'type': account_type,
                'data': asdict(data)
            }

            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.CREATED)
            json_response = response.json()
            assert_contains_key(json_response, "id")  # Check if id is present
            assert_equal(json_response['name'], body['name'])  # Compare data

        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account name over max length')
        def test_create_account_name_over_max_length(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name(name=create_101_length_alphanumeric_string()).name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.BAD_REQUEST)




        @pytest.mark.parametrize("name_creator", [create_lowercase_string(), create_uppercase_string(),
                                          create_simple_symbols_string(), create_digits_string(),
                                          create_mixed_case_string(), create_alphanumeric_string(),
                                          create_complex_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account name with valid symbols')
        def test_create_account_name_valid_symbols(self, main_type_account_data, name_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name(name=name_creator).name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.CREATED)
            json_response = response.json()
            assert_contains_key(json_response, "id")  # Check if id is present
            assert_equal(json_response['name'], body['name'])  # Compare data


        @pytest.mark.skip(reason="Test fails. Bug is reported - spaces are not allowed in name field")
        @pytest.mark.parametrize("name_creator", [create_spaces_string(), create_empty_string(),
                                                  create_russian_lowercase_string(), create_russian_uppercase_string(
            ), create_russian_mix_case_string(), create_special_symbols_string(), create_extended_symbols_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account name with invalid symbols')
        def test_create_account_name_invalid_symbols(self, main_type_account_data, name_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name(name=name_creator).name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.BAD_REQUEST)

        """Type validation"""

        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create valid account type')
        def test_create_account_type_valid(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.CREATED)
            json_response = response.json()
            assert_contains_key(json_response, "id")  # Check if id is present
            assert_equal(json_response['type'], body['type'])  # Compare data

        @pytest.mark.parametrize("type_creator", [create_spaces_string(), create_empty_string(),
                                                  create_russian_lowercase_string(), create_russian_uppercase_string(
            ), create_special_symbols_string(), create_extended_symbols_string(), create_lowercase_string(),
            create_uppercase_string(), create_digits_string(), create_complex_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create invalid account type')
        def test_create_account_type_invalid(self, main_type_account_data, type_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': type_creator,
                'data': asdict(data)
            }
            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.BAD_REQUEST)



        """Data validation"""
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account with missing necessary data fields')
        def test_create_account_without_necessary_data_fields(self, main_type_account_data, required_data_fields):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }

            fields_to_check = get_fields_to_check_data(account_type, required_data_fields, body)

            for field in fields_to_check:
                with allure.step(f"Testing without required field in data: {field}"):
                    removed_value = body['data'].pop(field, None)
                    response = create_account_request(body)
                    if "id" in (json_response := response.json()):
                        accounts_storage.append(json_response['id'])
                    assert_status_code(response, HTTPStatus.BAD_REQUEST)

                    body['data'][field] = removed_value

        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account without unnecessary data fields')
        def test_create_account_without_unnecessary_data_fields(self, main_type_account_data, unnecessary_data_fields):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }

            fields_to_check = get_fields_to_check_data(account_type, unnecessary_data_fields, body)
            time.sleep(3)
            for field in fields_to_check:
                with allure.step(f"Testing without unnecessary fields: {field}"):
                    removed_value = body['data'].pop(field, None)
            response = create_account_request(body)

            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.CREATED)



        @pytest.mark.parametrize("data_creator", [create_lowercase_string(), create_uppercase_string(),
                                          create_simple_symbols_string(), create_digits_string(),
                                          create_mixed_case_string(), create_alphanumeric_string(),
                                          create_complex_string(), create_special_symbols_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account data with valid symbols')
        def test_create_account_data_valid_symbols(self, main_type_account_data, data_creator):
            account_type, data = main_type_account_data
            updated_data = update_account_data(data, data_creator, FIXED_DATA_FIELDS)

            body = {
                'name': Name().name,
                'type': account_type,
                'data': updated_data
            }
            print(body)
            time.sleep(3)
            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.CREATED)
            json_response = response.json()
            assert_contains_key(json_response, "id")  # Check if id is present
            assert_equal(json_response['data'], body['data'])  # Compare data

        @pytest.mark.skip(reason="Test fails. Bug is reported - spaces, russian letters and symbols except "
                                 "._-!@#$%;^&:?*()+=/<>\ are not allowed in data")
        @pytest.mark.parametrize("data_creator", [create_spaces_string(), create_empty_string(),
                                                  create_russian_lowercase_string(), create_russian_uppercase_string(
            ), create_russian_mix_case_string(), create_extended_symbols_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account data with invalid symbols all fields')
        def test_create_account_data_invalid_symbols_all_fields(self, main_type_account_data, data_creator):
            account_type, data = main_type_account_data
            updated_data = update_account_data(data, data_creator, FIXED_DATA_FIELDS)

            body = {
                'name': Name().name,
                'type': account_type,
                'data': updated_data
            }
            print(body)
            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.BAD_REQUEST)


        @pytest.mark.skip(reason="Test fails. Bug is reported - spaces, russian letters and symbols except "
                                 "._-!@#$%;^&:?*()+=/<>\ are not allowed in data")
        @pytest.mark.parametrize("field_to_update", [
            'username', 'auth_password', 'community', 'security_level', 'auth_encryption', 'privacy_password',
            'privacy_encryption', 'context_name'
        ])
        @pytest.mark.parametrize("data_creator", [
            create_spaces_string(), create_empty_string(),
            create_russian_lowercase_string(), create_russian_uppercase_string(
            ), create_russian_mix_case_string(), create_extended_symbols_string()
        ])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account data with invalid symbols each field')
        def test_create_account_data_invalid_symbols_each_field(self, main_type_account_data, data_creator, field_to_update):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }

            if field_to_update not in body['data'] or field_to_update == '' or field_to_update in FIXED_DATA_FIELDS:
                pass
            else:
                update_account_data_one_field(body, data_creator, field_to_update)
                with allure.step(
                        f"Testing with updated field: {field_to_update}, value: {body['data'][field_to_update]}"):
                    response = create_account_request(body)
                    if "id" in (json_response := response.json()):
                        accounts_storage.append(json_response['id'])
                    assert_status_code(response, HTTPStatus.BAD_REQUEST)

        @pytest.mark.parametrize("data_creator", [create_50_length_alphanumeric_string(), create_49_length_alphanumeric_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account data with max length')
        def test_create_account_data_max_length(self, main_type_account_data, data_creator):
            account_type, data = main_type_account_data
            updated_data = update_account_data(data, data_creator, FIXED_DATA_FIELDS)

            body = {
                'name': Name().name,
                'type': account_type,
                'data': updated_data
            }
            print(body)
            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.CREATED)
            json_response = response.json()
            assert_contains_key(json_response, "id")  # Check if id is present
            assert_equal(json_response['data'], body['data'])  # Compare data

        @pytest.mark.parametrize("data_creator", [create_51_length_alphanumeric_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account data with over max length')
        def test_create_account_data_over_max_length(self, main_type_account_data, data_creator):
            account_type, data = main_type_account_data
            updated_data = update_account_data(data, data_creator, FIXED_DATA_FIELDS)

            body = {
                'name': Name().name,
                'type': account_type,
                'data': updated_data
            }
            print(body)
            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.BAD_REQUEST)

        @pytest.mark.skip(reason="Test fails. Bug is reported - fields that should not be written in data are being "
                                 "passed")
        @pytest.mark.parametrize("field_to_update", [
            'security_level', 'auth_encryption', 'privacy_encryption'
        ])
        @pytest.mark.parametrize("data_creator", [create_alphanumeric_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Create account data with invalid fixed fields')
        def test_create_account_data_with_invalid_fixed_fields(self, all_type_account_data, field_to_update,
                                                               data_creator):
            account_type, data = all_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }

            if field_to_update not in body['data'] or field_to_update == '':
                pass
            else:
                update_account_data_one_field(body, data_creator, field_to_update)
                with allure.step(f"Testing with updated field: {field_to_update}, value: {body['data'][field_to_update]}"):
                    response = create_account_request(body)
                    if "id" in (json_response := response.json()):
                        accounts_storage.append(json_response['id'])
                    assert_status_code(response, HTTPStatus.BAD_REQUEST)



    @allure.story('Method Get by ID')
    class TestGetByIdMethod:
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Get by id all type accounts')
        def test_get_by_id_all_type_accounts(self, all_type_account_data):
            account_type, data = all_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.CREATED)
            response_post = response.json()

            response = get_account_by_id_request(response_post['id'])
            assert_status_code(response, HTTPStatus.OK)
            get_response = response.json()

            assert_equal(get_response["id"], response_post['id'])  # Проверяем совпадение идентификатора
            # Сравниваем остальные ключи
            assert_equal(get_response, response_post)


        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Get account by id after delete')
        def test_get_account_after_delete(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert_status_code(response, HTTPStatus.CREATED)
            response_post = response.json()


            response = delete_account_request(response_post['id'])
            assert_status_code(response, HTTPStatus.OK)

            response = get_account_by_id_request(response_post['id'])
            assert_status_code(response, HTTPStatus.NOT_FOUND)

        @pytest.mark.parametrize("id_creator", [create_alphanumeric_string(),
            create_empty_string(), create_digits_string(), create_complex_string(), create_uppercase_string(),
            create_lowercase_string(), create_russian_mix_case_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Get non-existent account by id')
        def test_get_non_existent_account_by_id(self, id_creator):
            response = get_account_by_id_request(id_creator)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND]

        @allure.title('Get account by id and verify caching')
        @pytest.mark.usefixtures("cleanup_accounts")
        def test_get_account_by_id_and_verify_caching(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)

            # Первый запрос
            response1 = get_account_by_id_request(account_id)
            assert_status_code(response1, HTTPStatus.OK)
            get_response1 = response1.json()

            # Второй запрос
            response2 = get_account_by_id_request(account_id)
            assert_status_code(response2, HTTPStatus.OK)
            get_response2 = response2.json()

            # Проверяем, что данные не изменились
            assert_equal(get_response1, get_response2)

        @allure.title('Get account by id and verify performance')
        @pytest.mark.usefixtures("cleanup_accounts")
        def test_get_account_by_id_and_verify_performance(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)

            start_time = time.time()
            response = get_account_by_id_request(account_id)
            end_time = time.time()

            assert_status_code(response, HTTPStatus.OK)
            assert_response_time(end_time - start_time, max_time=16.0)

        @allure.title('Get account by id without authorization')
        @pytest.mark.usefixtures("cleanup_accounts")
        def test_get_account_by_id_without_authorization(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)

            # Делаем запрос без авторизации
            response = get_account_by_id_request(account_id, auth=False)
            assert_status_code(response, HTTPStatus.UNAUTHORIZED)



    @allure.story('Method Delete by ID')
    class TestDeleteByIdMethod:
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Delete account by id')
        def test_delete_account_by_id(self, main_type_account_data):
            # Создаем аккаунт для теста
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

            response = delete_account_request(account_id)
            assert_status_code(response, HTTPStatus.OK)

            # Проверяем, что аккаунт действительно удален
            response = get_account_by_id_request(account_id)
            assert_status_code(response, HTTPStatus.NOT_FOUND)

        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Delete account by id without authorization')
        def test_delete_account_by_id_without_authorization(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

            # Пытаемся удалить аккаунт без авторизации
            response = delete_account_request(account_id, auth=False)
            assert_status_code(response, HTTPStatus.UNAUTHORIZED)

        @pytest.mark.parametrize("id_creator", [create_alphanumeric_string(),
                                                create_empty_string(), create_digits_string(), create_complex_string(),
                                                create_uppercase_string(),
                                                create_lowercase_string(), create_special_symbols_string(),
                                                create_russian_mix_case_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Delete non-existent account by id')
        def test_delete_non_existent_account(self, id_creator):
            response = delete_account_request(id_creator)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND]

        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Delete already deleted account')
        def test_delete_already_deleted_account(self, main_type_account_data):
            # Создаем аккаунт для теста
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

            # Удаляем аккаунт
            response = delete_account_request(account_id)
            assert_status_code(response, HTTPStatus.OK)
            # Пытаемся удалить аккаунт повторно
            response = delete_account_request(account_id)
            assert_status_code(response, HTTPStatus.NOT_FOUND)

        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Delete account and verify performance')
        def test_delete_account_and_verify_performance(self, main_type_account_data):
            # Создаем аккаунт для теста
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

            # Замеряем время выполнения запроса
            start_time = time.time()
            response = delete_account_request(account_id)
            end_time = time.time()
            assert_status_code(response, HTTPStatus.OK)
            assert_response_time(end_time - start_time, max_time=16.0)

    @allure.story('Method Get info page')
    class TestGetInfoPageMethod:
        @allure.title('Get accounts list without parameters')
        def test_get_accounts_list_without_parameters(self):

            response = get_accounts_list_request()
            # Выполняем запрос без параметров

            print(f"Response status code: {response.status_code}")
            print(f"Response body: {response.text}")

            # Проверяем статус ответа
            assert_status_code(response, HTTPStatus.OK)

            # Проверяем структуру ответа
            response_data = response.json()
            assert_that(response_data).contains_key("paging", "accounts")

            # Проверяем, что возвращается хотя бы один аккаунт
            assert_that(response_data["accounts"]).is_not_empty()

        @allure.title('Get accounts list with pagination')
        def test_get_accounts_list_with_pagination(self):
            page = 1
            limit = 5
            response = get_accounts_list_request(page=page, limit=limit)

            assert_status_code(response, HTTPStatus.OK)
            response_data = response.json()
            assert_that(response_data).contains_key("paging", "accounts")

            # Проверяем пагинацию
            paging = response_data["paging"]
            assert_that(paging["current_page"]).is_equal_to(page)
            assert_that(paging["next_page"]).is_equal_to(page+1)
            assert_that(paging["previous_page"]).is_equal_to(page - 1)
            assert_that(paging["per_page"]).is_equal_to(limit)
            assert_that(len(response_data["accounts"])).is_less_than_or_equal_to(limit)

        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Get accounts list with search query - name')
        def test_get_accounts_list_with_search_query_name(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            print(body)

            response = create_account_request(body)
            if "id" in (json_response := response.json()):
                accounts_storage.append(json_response['id'])
            search_query = body['name']
            response = get_accounts_list_request(q=search_query)

            assert_status_code(response, HTTPStatus.OK)
            response_data = response.json()
            assert_that(response_data).contains_key("paging", "accounts")

            for account in response_data["accounts"]:
                assert_that(
                    search_query in account.get("name", "") or
                    search_query in account.get("type", "") or
                    search_query in account.get("data", {}).get("username", "") or
                    search_query in account.get("data", {}).get("context_name", "") or
                    search_query in account.get("data", {}).get("auth_password", "") or
                    search_query in account.get("data", {}).get("privacy_password", "")
                ).is_true().described_as(
                    f"Search query '{search_query}' not found in account: {account}"
                )



        @allure.title('Get accounts list with empty search result')
        def test_get_accounts_list_with_empty_search_result(self):
            # Параметры запроса
            search_query = create_alphanumeric_string()

            # Выполняем запрос
            response = get_accounts_list_request(q=search_query)

            # Проверяем статус ответа
            assert_status_code(response, HTTPStatus.OK)

            # Проверяем, что результат пустой
            response_data = response.json()
            assert_that(response_data["accounts"]).is_empty()
            assert_that(response_data["paging"]["current_page"]).is_equal_to(1)
            assert_that(response_data["paging"]["next_page"]).is_equal_to(0)
            assert_that(response_data["paging"]["previous_page"]).is_equal_to(0)
            assert_that(response_data["paging"]["per_page"]).is_equal_to(10)
            assert_that(response_data["paging"]["total_page"]).is_equal_to(0)
            assert_that(response_data["paging"]["total_page"]).is_equal_to(0)

        @allure.title('Get accounts list without authorization')
        def test_get_accounts_list_without_authorization(self):
            response = get_accounts_list_request(auth=False)
            assert_status_code(response, HTTPStatus.UNAUTHORIZED)


    @allure.story('Method Patch account')
    class TestPatchAccountMethod:

        @pytest.mark.parametrize("name_creator", [create_lowercase_string(), create_uppercase_string(),
                                                  create_simple_symbols_string(), create_digits_string(),
                                                  create_complex_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account name with valid symbols (single field)')
        def test_update_account_name_valid(self, main_type_account_data, name_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

            # Обновляем поле "name"
            update_data = {
                'name': name_creator
            }
            response = patch_account_request(account_id, update_data)
            assert_status_code(response, HTTPStatus.OK)

            updated_account = get_account_by_id_request(account_id).json()
            assert_that(updated_account['name']).is_equal_to(name_creator)

        # @pytest.mark.parametrize("name_creator", [create_lowercase_string(), create_uppercase_string(),
        #                                           create_simple_symbols_string(), create_digits_string(),
        #                                           create_mixed_case_string(), create_alphanumeric_string(),
        #                                           create_complex_string()])
        # @pytest.mark.usefixtures("cleanup_accounts")
        # @allure.title('Update account name with valid symbols (full body request)')
        # def test_update_account_name_valid_full_body(self, main_type_account_data, name_creator):
        #     account_type, data = main_type_account_data
        #     body = {
        #         'name': Name().name,
        #         'type': account_type,
        #         'data': asdict(data)
        #     }
        #     response = create_account_request(body)
        #     account_id = response.json()['id']
        #     accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки
        #
        #     # Обновляем поле "name"
        #     update_data = {
        #         'name': name_creator,
        #         'type': account_type,
        #         'data': asdict(data)
        #     }
        #     response = patch_account_request(account_id, update_data)
        #     assert_status_code(response, HTTPStatus.OK)
        #
        #     updated_account = get_account_by_id_request(account_id).json()
        #     assert_that(updated_account['name']).is_equal_to(name_creator)
        #
        # @pytest.mark.skip(reason="Test fails. Bug is reported - spaces are not allowed in name field")
        # @pytest.mark.parametrize("name_creator", [create_spaces_string(), create_empty_string(),
        #                                           create_russian_lowercase_string(), create_russian_uppercase_string(
        #     ), create_russian_mix_case_string(), create_special_symbols_string(), create_extended_symbols_string(),
        #                                           create_empty_string(), create_spaces_string()])
        # @pytest.mark.usefixtures("cleanup_accounts")
        # @allure.title('Update account name with invalid symbols (full body)')
        # def test_update_account_name_invalid_full_body(self, main_type_account_data, name_creator):
        #     account_type, data = main_type_account_data
        #     body = {
        #         'name': Name().name,
        #         'type': account_type,
        #         'data': asdict(data)
        #     }
        #     response = create_account_request(body)
        #     account_id = response.json()['id']
        #     accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки
        #
        #     # Обновляем поле "name"
        #     update_data = {
        #
        #         'name': name_creator,
        #         'type': account_type,
        #         'data': asdict(data)
        #     }
        #     response = patch_account_request(account_id, update_data)
        #     assert_status_code(response, HTTPStatus.BAD_REQUEST)
        #
        #     updated_account = get_account_by_id_request(account_id).json()
        #     assert_that(updated_account['name']).is_equal_to(body['name'])

        @pytest.mark.skip(reason="Test fails. Bug is reported - spaces are not allowed in name field")
        @pytest.mark.parametrize("name_creator", [create_spaces_string(), create_empty_string(),
                                                  create_russian_lowercase_string(), create_russian_uppercase_string(
            ), create_special_symbols_string(), create_extended_symbols_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account name with invalid symbols (single field)')
        def test_update_account_name_invalid(self, main_type_account_data, name_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

            # Обновляем поле "name"
            update_data = {
                'name': name_creator
            }
            response = patch_account_request(account_id, update_data)
            assert_status_code(response, HTTPStatus.BAD_REQUEST)

            updated_account = get_account_by_id_request(account_id).json()
            assert_that(updated_account['name']).is_equal_to(body['name'])

        @pytest.mark.parametrize("name_creator", [create_100_length_alphanumeric_string(), create_99_length_alphanumeric_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account name max length (single field)')
        def test_update_account_name_max_length(self, main_type_account_data, name_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

            # Обновляем поле "name"
            update_data = {
                'name': name_creator
            }
            response = patch_account_request(account_id, update_data)
            assert_status_code(response, HTTPStatus.OK)

            updated_account = get_account_by_id_request(account_id).json()
            assert_that(updated_account['name']).is_equal_to(name_creator)


        @pytest.mark.parametrize("name_creator", [create_101_length_alphanumeric_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account name over max length (single field)')
        def test_update_account_name_over_max_length(self, main_type_account_data, name_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

            # Обновляем поле "name"
            update_data = {
                'name': name_creator
            }
            response = patch_account_request(account_id, update_data)
            assert_status_code(response, HTTPStatus.BAD_REQUEST)

            updated_account = get_account_by_id_request(account_id).json()
            assert_that(updated_account['name']).is_equal_to(body['name'])


        @pytest.mark.skip(reason="Test fails. Bug is reported - wrong response and status code if type is invalid")
        @pytest.mark.parametrize("type_creator", ['ipmi', 'snmpv2c', 'snmpv3', create_empty_string(),
                                                  create_spaces_string(),
                                                  create_simple_symbols_string(),
                                                  create_mixed_case_string(), create_alphanumeric_string(),
                                                  create_complex_string(), create_special_symbols_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account type (single field)')
        def test_update_account_type(self, main_type_account_data, type_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            if body['type'] == type_creator:
                pytest.skip(f"Skipping test: {type_creator}.")
            else:
                response = create_account_request(body)
                account_id = response.json()['id']
                accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

                # Обновляем поле "type"
                update_data = {
                    'type': type_creator
                }
                response = patch_account_request(account_id, update_data)
                assert_status_code(response, HTTPStatus.BAD_REQUEST)

                updated_account = get_account_by_id_request(account_id).json()
                assert_that(updated_account['type']).is_equal_to(body['type'])

        @pytest.mark.skip(reason="Test fails. Bug is reported - 500 status-code if type is invalid")
        @pytest.mark.parametrize("type_creator",
                                 ['ipmi', 'snmpv2c', 'snmpv3', create_lowercase_string(),
                                                  create_uppercase_string(), create_empty_string(),
                                                  create_spaces_string(),
                                                  create_simple_symbols_string(), create_digits_string(),
                                                  create_complex_string(), create_special_symbols_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account valid type with old data (full body)')
        def test_update_account_type_full_body_valid_type_old_data(self, main_type_account_data, type_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            if body['type'] == type_creator:
                pytest.skip(f"Skipping test: {type_creator}.")
            else:
                response = create_account_request(body)
                account_id = response.json()['id']
                accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

                # Обновляем поле "name"
                update_data = {
                    'name': body['name'],
                    'type': type_creator,
                    'data': asdict(data)
                }
                print(update_data)
                response = patch_account_request(account_id, update_data)
                assert_status_code(response, HTTPStatus.BAD_REQUEST)

                updated_account = get_account_by_id_request(account_id).json()
                assert_that(updated_account['type']).is_equal_to(body['type'])

        @pytest.mark.parametrize("type_creator, data_creator", [
            ('ipmi', IPMIData()),
            ('snmpv2c', Snmpv2cData()),
            ('snmpv3', Snmpv3Noauth())
        ])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account type with new valid body (full body)')
        def test_update_account_type_new_valid_body(self, main_type_account_data, type_creator, data_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

            # Обновляем поле "name"
            update_data = {
                'name': body['name'],
                'type': type_creator,
                'data': asdict(data_creator)
            }
            print(update_data)
            response = patch_account_request(account_id, update_data)
            assert_status_code(response, HTTPStatus.OK)

            updated_account = get_account_by_id_request(account_id).json()
            assert_that(update_data['type']).is_equal_to(updated_account['type'])
            assert_that(update_data['data']).is_equal_to(updated_account['data'])

        @pytest.mark.parametrize("type_creator, data_creator", [
            ('ipmi', Snmpv2cData()),
            ('snmpv2c', Snmpv3Noauth()),
            ('snmpv3', IPMIData())
        ])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account type with new invalid body (full body)')
        def test_update_account_type_new_invalid_body(self, main_type_account_data, type_creator, data_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

            # Обновляем поле "name"
            update_data = {
                'name': body['name'],
                'type': type_creator,
                'data': asdict(data_creator)
            }
            print(update_data)
            response = patch_account_request(account_id, update_data)
            assert_status_code(response, HTTPStatus.BAD_REQUEST)

            updated_account = get_account_by_id_request(account_id).json()
            assert_that(body['type']).is_equal_to(updated_account['type'])
            assert_that(body['data']).is_equal_to(updated_account['data'])

        @pytest.mark.skip(reason="Test fails. Bug is reported - duplicated accounts shouldn't be created")
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update and make duplicated account')
        def test_update_and_make_duplicated_account(self, main_type_account_data):
            account_type, data = main_type_account_data
            body_first = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response_first = create_account_request(body_first)
            account_id_first = response_first.json()['id']
            accounts_storage.append(account_id_first)  # Сохраняем ID для последующей очистки

            body_second = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response_second = create_account_request(body_second)
            account_id_second = response_second.json()['id']
            accounts_storage.append(account_id_first)  # Сохраняем ID для последующей очистки

            # Обновляем поле "name" второго аккаунта
            update_data = {
                'name': body_first['name'],
                'type': account_type,
                'data': asdict(data)
            }
            response_updated = patch_account_request(account_id_second, update_data)
            assert_status_code(response_updated, HTTPStatus.CONFLICT)

            updated_account = get_account_by_id_request(account_id_second).json()
            assert_that(body_first['name']).is_equal_to(updated_account['name'])



        @pytest.mark.parametrize("data_creator", [create_lowercase_string(), create_uppercase_string(),
                                                      create_simple_symbols_string(), create_digits_string(),
                                                      create_complex_string(), create_special_symbols_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account data with valid symbols (all fields)')
        def test_update_account_data_valid(self, main_type_account_data, data_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки
            updated_data = update_account_data(data, data_creator, FIXED_DATA_FIELDS)
            body_updated = {
                'name': Name().name,
                'type': account_type,
                'data': updated_data
            }
            print(body_updated['data'])
            response = patch_account_request(account_id, body_updated)
            assert_status_code(response, HTTPStatus.OK)

            updated_account = get_account_by_id_request(account_id).json()
            assert_that(updated_account['data']).is_equal_to(body_updated['data'])


        @pytest.mark.parametrize("data_creator", [create_50_length_alphanumeric_string(), create_49_length_alphanumeric_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account data with max length (all fields)')
        def test_update_account_data_max_length(self, main_type_account_data, data_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки
            updated_data = update_account_data(data, data_creator, FIXED_DATA_FIELDS)
            body_updated = {
                'name': Name().name,
                'type': account_type,
                'data': updated_data
            }
            response = patch_account_request(account_id, body_updated)
            assert_status_code(response, HTTPStatus.OK)

            updated_account = get_account_by_id_request(account_id).json()
            assert_that(updated_account['data']).is_equal_to(body_updated['data'])

        @pytest.mark.parametrize("data_creator", [create_51_length_alphanumeric_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account data over max length (all fields)')
        def test_update_account_data_over_max_length(self, main_type_account_data, data_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            print(body)
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки
            updated_data = update_account_data(data, data_creator, FIXED_DATA_FIELDS)
            body_updated = {
                'name': Name().name,
                'type': account_type,
                'data': updated_data
            }
            response = patch_account_request(account_id, body_updated)
            assert_status_code(response, HTTPStatus.BAD_REQUEST)

            updated_account = get_account_by_id_request(account_id).json()
            assert_that(updated_account['data']).is_equal_to(body['data'])

        @pytest.mark.skip(reason="Test fails. Bug is reported - spaces, russian letters and symbols except "
                                 "._-!@#$%;^&:?*()+=/<>\ are not allowed in data")
        @pytest.mark.parametrize("field_to_update", [
            'username', 'auth_password', 'community', 'security_level', 'auth_encryption', 'privacy_password',
            'privacy_encryption', 'context_name'
        ])
        @pytest.mark.parametrize("data_creator", [
            create_spaces_string(), create_empty_string(),
            create_russian_mix_case_string(), create_extended_symbols_string()
        ])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account data with invalid symbols each field')
        def test_update_account_data_invalid_symbols_each_field(self, main_type_account_data, data_creator,
                                                                field_to_update):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            print(body)
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки
            if field_to_update not in body['data'] or field_to_update == '' or field_to_update in FIXED_DATA_FIELDS:
                pytest.skip(f"Skipping test: {field_to_update} is not a valid field for update.")
            else:
                update_account_data_one_field(body, data_creator, field_to_update)
                with allure.step(
                        f"Testing with updated field: {field_to_update}, value: {body['data'][field_to_update]}"):
                    print(body)
                    response = patch_account_request(account_id, body)
                    assert_status_code(response, HTTPStatus.BAD_REQUEST)



        @pytest.mark.parametrize("field_to_update", [
            'username', 'auth_password', 'community', 'security_level', 'auth_encryption', 'privacy_password',
            'privacy_encryption', 'context_name'
        ])
        @pytest.mark.parametrize("data_creator", [
            create_simple_symbols_string(), create_digits_string(),
            create_mixed_case_string(), create_alphanumeric_string(),
            create_complex_string(), create_special_symbols_string()
        ])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account data with valid symbols each field')
        def test_update_account_data_valid_symbols_each_field(self, main_type_account_data, data_creator,
                                                                field_to_update):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки
            if field_to_update not in body['data'] or field_to_update == '' or field_to_update in FIXED_DATA_FIELDS:
                pytest.skip(f"Skipping test: {field_to_update} is not a valid field for update.")
            else:
                update_account_data_one_field(body, data_creator, field_to_update)
                with allure.step(
                        f"Testing with updated field: {field_to_update}, value: {body['data'][field_to_update]}"):
                    response = patch_account_request(account_id, body)
                    assert_status_code(response, HTTPStatus.OK)

        @pytest.mark.skip(reason="Test fails. Bug is reported - wrong response and status code if data is not full")
        @pytest.mark.parametrize("field_to_update", [
            'username', 'auth_password', 'community', 'security_level', 'auth_encryption', 'privacy_password',
            'privacy_encryption', 'context_name'
        ])
        @pytest.mark.parametrize("data_creator", [
            create_simple_symbols_string(), create_digits_string(),
            create_mixed_case_string(), create_alphanumeric_string(),
            create_complex_string(), create_special_symbols_string()
        ])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account data with valid symbols one field')
        def test_update_account_data_valid_symbols_one_field(self, main_type_account_data, data_creator,
                                                              field_to_update):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            if field_to_update not in body['data'] or field_to_update == '' or field_to_update in FIXED_DATA_FIELDS:
                pytest.skip(f"Skipping test: {field_to_update} is not a valid field for update.")
            else:
                response = create_account_request(body)
                account_id = response.json()['id']
                accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки
                update_data = {
                    'data': {field_to_update:data_creator}
                }
                print(update_data)
                with allure.step(
                        f"Testing with updated field: {field_to_update}, value: {update_data['data'][field_to_update]}"):
                    response_2 = patch_account_request(account_id, update_data)
                    assert_status_code(response_2, HTTPStatus.OK)
                    print(response_2.json())
                    assert_that(response_2.json()['data'][field_to_update]).is_equal_to(data_creator)

        @pytest.mark.skip(reason="Test fails. Bug is reported - wrong response and status code if data is from "
                                 "another type")
        @pytest.mark.parametrize("field_to_update", [
            'username', 'auth_password', 'community', 'security_level', 'auth_encryption', 'privacy_password',
            'privacy_encryption', 'context_name'
        ])
        @pytest.mark.parametrize("data_creator", [
            create_spaces_string(), create_empty_string(),
            create_russian_lowercase_string(), create_russian_uppercase_string(
            ), create_extended_symbols_string()
        ])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account data with invalid symbols one field')
        def test_update_account_data_invalid_symbols_one_field(self, main_type_account_data, data_creator,
                                                             field_to_update):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            if field_to_update not in body['data'] or field_to_update == '' or field_to_update in FIXED_DATA_FIELDS:
                pytest.skip(f"Skipping test: {field_to_update} is not a valid field for update.")
            else:
                response_post = create_account_request(body)
                account_id = response_post.json()['id']
                accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки
                update_data = {
                    'data': {field_to_update: data_creator}
                }
                print(update_data)
                with allure.step(
                        f"Testing with updated field: {field_to_update}, value: {update_data['data'][field_to_update]}"):
                    response = patch_account_request(account_id, update_data)
                    assert_status_code(response, HTTPStatus.BAD_REQUEST)
                    print(response.json())
                    assert_that(response.json()['data']).is_equal_to(response_post.json()['data'])

        @pytest.mark.skip(reason="Test fails. Bug is reported - wrong response and status code if data is from "
                                 "another type")
        @pytest.mark.parametrize("type_creator, data_creator", [
            ('ipmi', IPMIData()),
            ('snmpv2c', Snmpv2cData()),
            ('snmpv3', Snmpv3Noauth())
        ])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update account data with body from another type')
        def test_update_account_data_another_type_body(self, main_type_account_data, type_creator, data_creator):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки
            if account_type == type_creator:
                pytest.skip(f"Skipping test.")
            else:
                update_data = {
                    'data': asdict(data_creator)
                }
                print(update_data)
                response = patch_account_request(account_id, update_data)
                assert_status_code(response, HTTPStatus.BAD_REQUEST)

                updated_account = get_account_by_id_request(account_id).json()
                assert_that(body['data']).is_equal_to(updated_account['data'])


        @pytest.mark.parametrize("id_creator", [create_complex_string()])
        @pytest.mark.usefixtures("cleanup_accounts")
        @allure.title('Update non-existent account')
        def test_update_non_existent_account(self, main_type_account_data, id_creator):
            # Обновляем поле "name"
            update_data = {
                'name': create_alphanumeric_string()
            }
            response = patch_account_request(id_creator, update_data)
            assert_status_code(response, HTTPStatus.BAD_REQUEST)

        @allure.title('Update account without authorization')
        def test_update_without_authorization(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки
            update_data = {
                'name': create_alphanumeric_string()
            }
            response = patch_account_request(account_id, update_data, auth=False)
            assert_status_code(response, HTTPStatus.UNAUTHORIZED)

        @allure.title('Update account and verify performance')
        def test_update_performance(self, main_type_account_data):
            account_type, data = main_type_account_data
            body = {
                'name': Name().name,
                'type': account_type,
                'data': asdict(data)
            }
            response = create_account_request(body)
            account_id = response.json()['id']
            accounts_storage.append(account_id)  # Сохраняем ID для последующей очистки

            update_data = {
                'name': create_alphanumeric_string()
            }
            start_time = time.time()
            response = patch_account_request(account_id, update_data)
            end_time = time.time()

            # Проверяем статус ответа
            assert_status_code(response, HTTPStatus.OK)

            # Проверяем, что время выполнения запроса меньше допустимого значения (например, 1 секунда)
            assert (end_time - start_time) < 16.0, f"Request took too long: {end_time - start_time} seconds"































