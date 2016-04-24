import json

from objects.consignor_base import ConsignorBase


class RouteConsignor(object):
    @staticmethod
    def on_post(req, resp):
        _consignor = ConsignorBase()

        # Request body
        _payload = json.loads(str(req.stream.read(), encoding='utf-8'))
        # Authenticated execution
        _consignor.register_auth_token(req.auth)
        _result = _consignor.create_consignor(**_payload)
        # Response handlers
        resp.status = _result.get('status', {}).get('code')
        resp.body = json.dumps(_result)
