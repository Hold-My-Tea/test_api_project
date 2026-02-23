from http import HTTPStatus

import httpx
import pytest


from accounts.account_api import delete_account_request, create_account_request
from accounts.test_data import IPMIData, Snmpv2cData, Snmpv3Noauth, Snmpv3Nopriv, Snmpv3Priv
from assertions import assert_status_code



accounts_storage = []
@pytest.fixture(scope='class', autouse=True)
def cleanup_accounts():
    global accounts_storage
    yield  # Это позволяет тестам выполняться
    print(accounts_storage)
    for account_id in accounts_storage:
        response = delete_account_request(account_id)
        assert response.status_code in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]
    print(accounts_storage)


@pytest.fixture(params=[
    pytest.param(('ipmi', IPMIData()), id='IPMI account'),
    pytest.param(('snmpv2c', Snmpv2cData()), id='SNMPv2c account'),
    pytest.param(('snmpv3', Snmpv3Noauth()), id='SNMPv3 NoAuth'),
    pytest.param(('snmpv3', Snmpv3Nopriv(auth_encryption='md5')), id='SNMPv3 NoPriv (MD5)'),
    pytest.param(('snmpv3', Snmpv3Nopriv(auth_encryption='sha1')), id='SNMPv3 NoPriv (SHA1)'),
    pytest.param(('snmpv3', Snmpv3Nopriv(auth_encryption='sha256')), id='SNMPv3 NoPriv (SHA256)'),
    pytest.param(('snmpv3', Snmpv3Nopriv(auth_encryption='sha384')), id='SNMPv3 NoPriv (SHA384)'),
    pytest.param(('snmpv3', Snmpv3Nopriv(auth_encryption='sha512')), id='SNMPv3 NoPriv (SHA512)'),

    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='md5', privacy_encryption='aes')), id='SNMPv3 Priv (MD5 + AES)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='md5', privacy_encryption='aes192')), id='SNMPv3 Priv (MD5 + AES192)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='md5', privacy_encryption='aes256')), id='SNMPv3 Priv (MD5 + AES256)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='md5', privacy_encryption='des')), id='SNMPv3 Priv (MD5 + DES)'),

    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha1', privacy_encryption='aes')), id='SNMPv3 Priv (SHA1 + '
                                                                                              'AES)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha1', privacy_encryption='aes192')), id='SNMPv3 Priv (SHA1 + AES192)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha1', privacy_encryption='aes256')), id='SNMPv3 Priv (SHA1 + AES256)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha1', privacy_encryption='des')), id='SNMPv3 Priv (SHA1 + DES)'),

    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha256', privacy_encryption='aes')), id='SNMPv3 Priv (SHA256 + '
                                                                                              'AES)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha256', privacy_encryption='aes192')), id='SNMPv3 Priv (SHA256 + AES192)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha256', privacy_encryption='aes256')), id='SNMPv3 Priv (SHA256 + AES256)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha256', privacy_encryption='des')), id='SNMPv3 Priv (SHA256 + DES)'),

    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha384', privacy_encryption='aes')), id='SNMPv3 Priv (SHA384 + '
                                                                                              'AES)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha384', privacy_encryption='aes192')), id='SNMPv3 Priv (SHA384 + AES192)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha384', privacy_encryption='aes256')), id='SNMPv3 Priv (SHA384 + AES256)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha384', privacy_encryption='des')), id='SNMPv3 Priv (SHA384 + DES)'),

    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha512', privacy_encryption='aes')), id='SNMPv3 Priv (SHA512 + '
                                                                                                'AES)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha512', privacy_encryption='aes192')),
                 id='SNMPv3 Priv (SHA512 + AES192)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha512', privacy_encryption='aes256')),
                 id='SNMPv3 Priv (SHA512 + AES256)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha512', privacy_encryption='des')),
                 id='SNMPv3 Priv (SHA512 + DES)')
])
def all_type_account_data(request):
    return request.param



@pytest.fixture(params=[
    pytest.param(('ipmi', IPMIData()), id='IPMI account'),
    pytest.param(('snmpv2c', Snmpv2cData()), id='SNMPv2c account'),
    pytest.param(('snmpv3', Snmpv3Noauth()), id='SNMPv3 NoAuth'),
    pytest.param(('snmpv3', Snmpv3Nopriv(auth_encryption='md5')), id='SNMPv3 NoPriv (MD5)'),
    pytest.param(('snmpv3', Snmpv3Priv(auth_encryption='sha1', privacy_encryption='aes')), id='SNMPv3 Priv (SHA1 + '
                                                                                              'AES)')
])
def main_type_account_data(request):
    return request.param


@pytest.fixture
def required_data_fields():
    return {
        'snmpv3': {
            'nopriv': ['username', 'security_level', 'auth_encryption', 'auth_password'],
            'priv': ['username', 'security_level', 'auth_encryption', 'auth_password', 'privacy_encryption', 'privacy_password'],
            'noauth': ['username', 'security_level']
        },
        'snmpv2c': ['community'],
        'ipmi': ['username', 'auth_password']
    }


@pytest.fixture
def unnecessary_data_fields():
    return {
        'snmpv3': {
            'nopriv': ['privacy_encryption', 'privacy_password', 'context_name'],
            'priv': ['context_name'],
            'noauth': ['auth_encryption', 'auth_password', 'privacy_encryption', 'privacy_password', 'context_name']
        },
        'snmpv2c': [],
        'ipmi': []
    }


