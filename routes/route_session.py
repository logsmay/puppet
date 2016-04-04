import json

from falcon.util import uri

from objects.session_base import SessionBase

session = SessionBase()


class RoutePostSession(object):
    def on_get(self, req, resp):
        _payload = uri.parse_query_string(req.query_string)

        _result = session.create_session(**_payload)
        resp.status = _result.get('status', {}).get('code')
        resp.body = json.dumps(_result)
