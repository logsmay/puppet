import json

from objects.session_base import SessionBase
from utils.functions import from_bytes

session = SessionBase()


class RouteSession(object):
    @staticmethod
    def on_post(req, resp):
        _payload = json.loads(from_bytes(req.stream.read()))

        _result = session.create_session(**_payload)

        resp.status = _result.get('status', {}).get('code')
        resp.body = json.dumps(_result)

    @staticmethod
    def on_delete(req, resp):
        _auth_token = req.get_header('Authorization',
                                     required=True)  # Do not use req.auth() as it doesn't offer required= option.

        _result = SessionBase().delete_session(auth_token=_auth_token)

        resp.status = _result.get('status', {}).get('code')
        resp.body = json.dumps(_result)
