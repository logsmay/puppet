import json

from objects.account_base import AccountBase
from objects.session_base import SessionBase

account = AccountBase()
session = SessionBase()


def print_status(result):
    print(result.get('status', {}).get('code'))


def print_body(result):
    print(json.dumps(result))


def test(payload):
    _result = account.update_account(**payload)

    print_status(_result)
    print_body(_result)


test({
    'account_id': 5,
    'first_name': 'Nirmal',
    'password': '0987654321'
})
