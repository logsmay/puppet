import json

from objects.account_base import AccountBase
from utils.functions import from_bytes


class RouteAccount(object):
    @staticmethod
    def on_post(req, resp):
        _payload = json.loads(from_bytes(req.stream.read()))

        _result = AccountBase().create_account(**_payload)

        resp.status = _result.get('status', {}).get('code')
        resp.body = json.dumps(_result)

    @staticmethod
    def on_put(req, resp):
        _account_id = req.get_header('auth-account-id', required=True)
        _payload = json.loads(from_bytes(req.stream.read()))

        _result = AccountBase(_account_id).update_account(**_payload)

        resp.status = _result.get('status', {}).get('code')
        resp.body = json.dumps(_result)
