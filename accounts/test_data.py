import json
from dataclasses import dataclass, field
from typing import Callable
from dataclasses import dataclass, field, asdict
from accounts.account_helper import create_alphanumeric_string, create_empty_string




@dataclass
class Name:
    name: str = field(default_factory=create_alphanumeric_string)

@dataclass
class Type:
    type: str = field(default_factory=create_alphanumeric_string)

@dataclass
class IPMIData:
    username: str = field(default_factory=create_alphanumeric_string)
    auth_password: str = field(default_factory=create_alphanumeric_string)

@dataclass
class Snmpv2cData:
    community: str = field(default_factory=create_alphanumeric_string)

@dataclass
class Snmpv3Noauth:
    username: str = field(default_factory=create_alphanumeric_string)
    security_level: str = 'noauth'
    auth_password: str = field(default_factory=create_empty_string)
    auth_encryption: str = field(default_factory=create_empty_string)
    privacy_password: str = field(default_factory=create_empty_string)
    privacy_encryption: str = field(default_factory=create_empty_string)
    context_name: str = field(default_factory=create_empty_string)



@dataclass
class Snmpv3Nopriv:
    username: str = field(default_factory=create_alphanumeric_string)
    security_level: str = 'nopriv'
    auth_password: str = field(default_factory=create_alphanumeric_string)
    auth_encryption: str = field(default_factory=create_alphanumeric_string)
    context_name: str = field(default_factory=create_alphanumeric_string)
    privacy_password: str = field(default_factory=create_empty_string)
    privacy_encryption: str = field(default_factory=create_empty_string)


@dataclass
class Snmpv3Priv:
    username: str = field(default_factory=create_alphanumeric_string)
    security_level: str = 'priv'
    auth_password: str = field(default_factory=create_alphanumeric_string)
    auth_encryption: str = field(default_factory=create_alphanumeric_string)
    privacy_password: str = field(default_factory=create_alphanumeric_string)
    privacy_encryption: str = field(default_factory=create_alphanumeric_string)
    context_name: str = field(default_factory=create_alphanumeric_string)


FIXED_DATA_FIELDS = {'security_level', 'auth_encryption', 'privacy_encryption'}


ACCOUNT_TYPE_FIELDS = {
    "ipmi": ["username", "auth_password"],
    "snmpv2c": ["community"],
    "snmpv3": [
        "username", "context_name", "auth_password", "security_level",
        "auth_encryption", "privacy_password", "privacy_encryption"
    ],

}

