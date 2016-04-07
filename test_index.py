import json

from objects.session_base import SessionBase

session = SessionBase()


def print_status(result):
    print(result.get('status', {}).get('code'))


def print_body(result):
    print(json.dumps(result))


def test(payload):
    _result = session.delete_session(**payload)

    print_status(_result)
    print_body(_result)


test({
    'auth_token': 'abcd'
})
