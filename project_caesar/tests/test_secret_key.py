# Local imports
from project_caesar.code import secret_key
from project_caesar.code.models import hex_string


secret_key_value_1 = '4d97755ababdaf0b29d880a22aebfaa903b60be619831a86f98f1fe00adbe026'


def test_validate_value_is_hex_string():
    sk = hex_string.HexString(value=secret_key_value_1)


def test_validate_value_is_hex_string_with_length_n():
    n = 32
    sk = hex_string.HexString(value=secret_key_value_1, length=n)

