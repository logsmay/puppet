import json

from falcon.util import uri

from objects.account_base import AccountBase

account = AccountBase()


class RouteAccount(object):
    @staticmethod
    def on_post(req, resp):
        _payload = uri.parse_query_string(req.query_string)

        _result = account.create_account(**_payload)
        resp.status = _result.get('status', {}).get('code')
        resp.body = json.dumps(_result)

    @staticmethod
    def on_put(req, resp):
        _payload = uri.parse_query_string(req.query_string)

        _result = account.update_account(**_payload)
        resp.status = _result.get('status', {}).get('code')
        resp.body = json.dumps(_result)
