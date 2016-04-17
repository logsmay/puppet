import json

from objects.account_base import AccountBase
from objects.session_base import SessionBase


class RouteAccount(object):
    @staticmethod
    def on_post(req, resp):
        # Request body
        _payload = json.loads(str(req.stream.read()))
        # Execution
        _result = AccountBase().create_account(**_payload)
        # Response handlers
        resp.status = _result.get('status', {}).get('code')
        resp.body = json.dumps(_result)

    @staticmethod
    def on_put(req, resp):
        # Authorization header
        _auth_token = req.auth()
        # Request body
        _payload = json.loads(str(req.stream.read()))
        # Execution
        _result = SessionBase(auth_token=_auth_token).update_account(**_payload)
        # Response handlers
        resp.status = _result.get('status', {}).get('code')
        resp.body = json.dumps(_result)
